from pydantic import BaseModel, EmailStr
from datetime import datetime
from typing import Optional


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserSend(BaseModel):
    uid: int
    email: EmailStr
    inserted_dt: datetime

    class Config:
        orm_mode = True


class Owner(BaseModel):
    email: EmailStr
    inserted_dt: datetime

    class Config:
        orm_mode = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token = EmailStr
    password: str


class TokenData(BaseModel):
    uid: Optional[str] = None
