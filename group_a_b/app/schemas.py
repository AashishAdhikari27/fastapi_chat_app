from pydantic import BaseModel
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    password: str

class UserRead(BaseModel):
    id: int
    username: str
    role: str

class Token(BaseModel):
    access_token: str
    token_type: str

class MessageCreate(BaseModel):
    text: str
    room_id: int

class MessageRead(BaseModel):
    id: int
    text: str
    timestamp: datetime
    username: str