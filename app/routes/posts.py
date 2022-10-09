from fastapi import APIRouter, HTTPException, Depends, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Any, Optional

from app.models.blogs import FastapiBlogPost
from app.models.voting import FastapiVoting
from app.schemas.blogs import PostRequest, PostResponse, PostData
from app.utils.oauth2 import get_current_user
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db),
                    limit: int = 10,
                    skip: int = 0,
                    search: Optional[str] = ""):
    try:
        query = db.query(FastapiBlogPost, func.count(FastapiVoting.blog_id).label("likes"))\
            .join(FastapiVoting, FastapiBlogPost.bid == FastapiVoting.blog_id, isouter=True)\
            .group_by(FastapiBlogPost.bid)

        result = query.filter(FastapiBlogPost.title.contains(search)).limit(limit).offset(skip).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostData)
async def create_post(payload: PostRequest,
                      db: Session = Depends(get_db),
                      current_user: Any = Depends(get_current_user)):
    try:
        new_post = FastapiBlogPost(user_id=current_user.uid, **payload.dict())
        db.add(new_post)
        db.commit()
        db.refresh(new_post)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return new_post


@router.get("/{pid}", response_model=PostResponse)
async def get_post(pid: int,
                   db: Session = Depends(get_db),
                   user_id: int = Depends(get_current_user)):
    try:
        query = db.query(FastapiBlogPost).filter(FastapiBlogPost.bid == pid)
        result = query.first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Data Found")

        query = db.query(
            FastapiBlogPost,
            func.count(FastapiVoting.blog_id).label("likes")).join(
            FastapiVoting,
            FastapiBlogPost.bid == FastapiVoting.blog_id, isouter=True).filter(FastapiBlogPost.bid == pid)

        result = query.first()
    except Exception as e:
        raise e
    else:
        return result


@router.put("/{pid}", response_model=PostData)
def update_post(pid: int,
                payload: PostRequest,
                db: Session = Depends(get_db),
                current_user: Any = Depends(get_current_user)):
    try:
        query = db.query(FastapiBlogPost).filter(FastapiBlogPost.bid == pid)
        result = query.first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Data Found")

        if result.user_id != int(current_user.uid):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Enough Privileges To Update")

        query.update(payload.dict(), synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
    else:
        return query.first()


@router.delete("/{pid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(pid: int,
                      db: Session = Depends(get_db),
                      current_user: Any = Depends(get_current_user)):
    try:
        query = db.query(FastapiBlogPost).filter(FastapiBlogPost.bid == pid)
        result = query.first()

        if not result:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"No Data Found")

        if result.user_id != int(current_user.uid):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Not Enough Privileges To Delete")

        query.delete(synchronize_session=False)
        db.commit()
    except Exception as e:
        db.rollback()
        raise e
