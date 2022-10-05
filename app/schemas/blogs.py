from pydantic import BaseModel, conint
from datetime import datetime
from typing import Optional

from app.schemas.users import Owner


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
    user_id: int
    owner: Owner

    class Config:
        orm_mode = True


class BlogVote(BaseModel):
    bid: int
    dir: conint(ge=0, le=1)
