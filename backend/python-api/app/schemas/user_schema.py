from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from datetime import datetime

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50)
    name: str = Field(..., min_length=3, max_length=100)
    email: EmailStr
    address: Optional[str] = None
    phone: Optional[str] = None

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, max_length=100)

class UserRead(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: Optional[str] = None

