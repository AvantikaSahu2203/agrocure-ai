from typing import Optional
from pydantic import BaseModel, EmailStr
from app.models.status_enums import UserRole

# Shared properties
class UserBase(BaseModel):
    email: Optional[str] = None
    role: Optional[UserRole] = UserRole.FARMER
    full_name: Optional[str] = None
    phone_number: Optional[str] = None
    is_active: Optional[bool] = True
    is_verified: Optional[bool] = False
    verification_code: Optional[str] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    email: str
    password: str

# Schema for JSON Login
class UserLogin(BaseModel):
    username: str
    password: str

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

class UserInDBBase(UserBase):
    id: Optional[str]  # We use UUIDs which are strings in JSON
    # uuid as str is easier for pydantic sometimes.

    class Config:
        orm_mode = True

from datetime import datetime

# Additional properties to return via API
class User(UserInDBBase):
    created_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None

class UserInDB(UserInDBBase):
    hashed_password: str
