from typing import Optional
from pydantic import BaseModel


class MessageRequest(BaseModel):
    """Schema for the request payload."""
    message: str
    model: Optional[str] = "gpt-3.5-turbo"  # Default model

class MessageResponse(BaseModel):
    """Schema for the response payload."""
    message: str

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"
