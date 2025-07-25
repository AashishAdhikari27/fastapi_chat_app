from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session, select
from .database import engine, create_db_and_tables
from .models import User, Room, Message
from .schemas import UserCreate, UserRead, Token, MessageCreate
from .auth import get_password_hash, verify_password, create_access_token
from .dependencies import get_current_user, role_required
from .config import settings
from .websocket import router as ws_router

# OAuth2 scheme for Swagger UI
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

app = FastAPI(
    title="Chat API",
    description="FastAPI Chat Application with JWT Authentication",
    version="0.1.0",
    openapi_tags=[
        {
            "name": "Authentication",
            "description": "User registration and login"
        },
        {
            "name": "User",
            "description": "User related operations"
        },
        {
            "name": "Admin",
            "description": "Admin only operations"
        },
        {
            "name": "WebSocket",
            "description": "Real-time chat operations"
        }
    ]
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

def create_initial_data():
    with Session(engine) as session:
        # Create default rooms
        rooms_to_create = [
            Room(id=1, name="General Chat", description="Main chat room"),
            Room(id=2, name="Random", description="Off-topic discussions"),
            Room(id=3, name="Help", description="Get support here")
        ]
        
        for room in rooms_to_create:
            existing = session.get(Room, room.id)
            if not existing:
                session.add(room)
        
        # Create admin user if not exists
        admin = session.exec(select(User).where(User.username == "admin")).first()
        if not admin:
            hashed_password = get_password_hash("adminpassword")
            admin_user = User(username="admin", password=hashed_password, role="admin")
            session.add(admin_user)
        
        # Create test user if not exists
        test_user = session.exec(select(User).where(User.username == "testuser")).first()
        if not test_user:
            hashed_password = get_password_hash("testpassword")
            test_user = User(username="testuser", password=hashed_password)
            session.add(test_user)
        
        session.commit()

@app.on_event("startup")
def on_startup():
    # Validate environment variables
    if not settings.DATABASE_URL:
        raise ValueError("DATABASE_URL not set in .env")
    if not settings.JWT_SECRET_KEY:
        raise ValueError("JWT_SECRET_KEY not set in .env")
    
    create_db_and_tables()
    create_initial_data()
    print("✅ Database initialized")

# Auth endpoints
@app.post("/signup", response_model=UserRead, tags=["Authentication"])
def signup(user: UserCreate):
    with Session(engine) as session:
        # Check if username exists
        existing_user = session.exec(select(User).where(User.username == user.username)).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Username already exists")
        
        hashed_password = get_password_hash(user.password)
        new_user = User(username=user.username, password=hashed_password)
        session.add(new_user)
        session.commit()
        session.refresh(new_user)
        return new_user

# Updated login endpoint to use OAuth2 form
@app.post("/login", response_model=Token, tags=["Authentication"])
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    with Session(engine) as session:
        user = session.exec(select(User).where(User.username == form_data.username)).first()
        if not user or not verify_password(form_data.password, user.password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        access_token = create_access_token(
            data={"sub": user.username, "role": user.role}
        )
        return {"access_token": access_token, "token_type": "bearer"}

# Protected endpoints
@app.get("/me", response_model=UserRead, tags=["User"])
def get_current_user_endpoint(user: User = Depends(get_current_user)):
    return user

# Admin-only endpoint with security declaration
@app.get("/admin/dashboard", tags=["Admin"])
def admin_dashboard(user: User = Depends(role_required("admin"))):
    return {"message": f"Welcome admin {user.username}!"}

# Include WebSocket router
app.include_router(ws_router, tags=["WebSocket"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)