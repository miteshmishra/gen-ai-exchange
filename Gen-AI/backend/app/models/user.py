from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

class UserBase(BaseModel):
    email: EmailStr
    full_name: Optional[str] = None

class UserCreate(UserBase):
    password: str

class UserInDB(UserBase):
    id: int
    hashed_password: str
    created_at: datetime

class UserSchema(UserBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
    id: int
    
    class Config:
        orm_mode = True
