from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, Field


# Shared properties between user models
class UserBase(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True
    is_superuser: bool = False


# Properties to receive on user creation
class UserCreate(UserBase):
    username: str = Field(
        ...,
        min_length=3,
        max_length=64,
        pattern=r"^[A-Za-z0-9-_.]+$",
    )
    email: EmailStr
    password: str


# Properties to receive on user update
class UserUpdate(UserBase):
    password: Optional[str] = None


class UserInDBBase(UserBase):
    created_at: datetime
    api_key: str

    class Config:
        from_attributes = True


# Properties to return via API
class User(UserInDBBase):
    pass


# Properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str
