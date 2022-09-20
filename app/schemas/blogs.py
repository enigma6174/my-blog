from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class PostRequest(BaseModel):
    title: str
    content: str
    is_published: Optional[bool] = False
    rating: Optional[int] = 0


class PostResponse(BaseModel):
    bid: int
    title: str
    content: str
    rating: int
    is_published: bool
    inserted_dt: datetime

    class Config:
        orm_mode = True
