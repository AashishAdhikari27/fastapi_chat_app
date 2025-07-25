from pydantic import BaseModel
from typing import Optional


# schemas.py --- This file contains Pydantic models for data validation and serialization
# Pydantic models are used to define the structure of data that is sent and received in API requests and responses.


# Shared properties
class UserBase(BaseModel): # Base model for user data i.e. for creating and reading user data
    username: str

class UserCreate(UserBase):  # Model for creating new users
    password: str
    role: str  # "user" or "admin"

class UserLogin(BaseModel):  # Model for user login
    username: str
    password: str

class Token(BaseModel): # Model for authentication token
    access_token: str
    token_type: str

class TokenData(BaseModel): # Model for token data
    username: Optional[str] = None
    role: Optional[str] = None
