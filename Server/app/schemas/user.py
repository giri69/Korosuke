from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional

class UserBase(BaseModel):
    email: EmailStr

class UserCreate(UserBase):
    name: str
    password: str

class User(UserBase):
    id: int
    name: str
    is_active: bool
    email_verified: bool
    account_created: datetime
    modified_date: Optional[datetime] = None

    class Config:
        orm_mode = True
