from pydantic import BaseModel, EmailStr
from datetime import datetime


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserSend(BaseModel):
    uid: int
    email: EmailStr
    inserted_dt: datetime

    class Config:
        orm_mode = True
