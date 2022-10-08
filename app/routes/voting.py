from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from typing import Any

from app.models.blogs import FastapiBlogPost
from app.models.voting import FastapiVoting
from app.schemas.blogs import BlogVote
from app.database import get_db
from app.utils.oauth2 import get_current_user


router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(data: BlogVote,
         db: Session = Depends(get_db),
         current_user: Any = Depends(get_current_user)):

    try:
        if not db.query(FastapiBlogPost).filter(FastapiBlogPost.bid == data.bid).first():
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Data Found")

        query = db.query(FastapiVoting).filter(FastapiVoting.blog_id == data.bid,
                                               FastapiVoting.user_id == current_user.uid)
        result = query.first()

        if data.dir == 1:
            if result:
                raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                                    detail=f"User Has Already Voted")

            new_vote = FastapiVoting(blog_id=data.bid, user_id=current_user.uid)
            db.add(new_vote)
        else:
            if not result:
                raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No Data Found")

            query.delete(synchronize_session=False)
    except Exception as e:
        db.rollback()
        raise e
    else:
        db.commit()
        return {"message": "successful"}
