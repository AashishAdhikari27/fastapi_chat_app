from fastapi import APIRouter, WebSocket, Query
from sqlmodel import Session, select
from .database import engine
from .models import Message, User
from .auth import decode_token
import json

router = APIRouter()

active_connections = {}

@router.websocket("/ws/{room_id}")
async def websocket_endpoint(
    websocket: WebSocket,
    room_id: int,
    token: str = Query(...)
):
    # Verify JWT
    payload = decode_token(token)
    if not payload:
        await websocket.close(code=1008)
        return
    
    username = payload.get("sub")
    if not username:
        await websocket.close(code=1008)
        return
    
    # Get user from database
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == username)).first()
        if not user:
            await websocket.close(code=1008)
            return
        user_id = user.id
    
    # Accept connection
    await websocket.accept()
    
    # Add to active connections
    if room_id not in active_connections:
        active_connections[room_id] = []
    active_connections[room_id].append(websocket)
    
    try:
        # Send last 20 messages
        with Session(engine) as session:
            messages = session.exec(
                select(Message)
                .where(Message.room_id == room_id)
                .order_by(Message.timestamp.desc())
                .limit(20)
            ).all()
            
            # Fetch usernames for messages
            formatted_messages = []
            for msg in reversed(messages):
                user = session.get(User, msg.user_id)
                if user:
                    formatted_messages.append({
                        "id": msg.id,
                        "text": msg.text,
                        "timestamp": msg.timestamp.isoformat(),
                        "username": user.username
                    })
            
            for msg in formatted_messages:
                await websocket.send_json(msg)
        
        # Handle incoming messages
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Save to database
            with Session(engine) as session:
                new_message = Message(
                    text=message_data["text"],
                    user_id=user_id,
                    room_id=room_id
                )
                session.add(new_message)
                session.commit()
                session.refresh(new_message)
                
                # Get username for new message
                user = session.get(User, user_id)
                username = user.username if user else "Unknown"
                
                # Broadcast to all in room
                message_payload = {
                    "id": new_message.id,
                    "text": new_message.text,
                    "timestamp": new_message.timestamp.isoformat(),
                    "username": username
                }
                
                for connection in active_connections[room_id]:
                    await connection.send_json(message_payload)
                    
    except Exception as e:
        print(f"WebSocket error: {e}")
    finally:
        # Remove connection
        if room_id in active_connections:
            if websocket in active_connections[room_id]:
                active_connections[room_id].remove(websocket)
            if not active_connections[room_id]:
                del active_connections[room_id]