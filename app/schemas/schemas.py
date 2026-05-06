from pydantic import BaseModel, EmailStr
from typing import Optional


# --- User Schemas ---
class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    role: str = "student"


class UserLogin(BaseModel):
    username: str
    password: str


class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    role: str

    class Config:
        from_attributes = True


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None