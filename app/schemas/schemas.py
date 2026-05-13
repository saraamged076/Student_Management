from pydantic import BaseModel, EmailStr, ConfigDict
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

    model_config = ConfigDict(from_attributes=True)


# --- Token Schemas ---
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPair(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    role: str


class RefreshRequest(BaseModel):
    refresh_token: str


class TokenData(BaseModel):
    username: Optional[str] = None
    role: Optional[str] = None
    
# --- Student Schemas ---

class StudentCreate(BaseModel):
    name: str
    department: str
    gpa: float


class StudentUpdate(BaseModel):
    name: str
    department: str
    gpa: float


class StudentResponse(BaseModel):
    id: int
    name: str
    department: str
    gpa: float
    owner_id: int

    model_config = ConfigDict(from_attributes=True)