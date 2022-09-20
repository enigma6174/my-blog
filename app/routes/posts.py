from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List

from app.models.blogs import FastapiBlogPost
from app.schemas.blogs import PostRequest, PostResponse
from app.utils.operations import insert, find, delete, update
from app.database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[PostResponse])
async def get_posts(db: Session = Depends(get_db)):
    try:
        posts = db.query(FastapiBlogPost).all()
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return posts


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
async def create_post(payload: PostRequest, db: Session = Depends(get_db)):
    try:
        modified_payload = FastapiBlogPost(**payload.dict())
        new_post = insert(db, modified_payload)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return new_post


@router.get("/{pid}", response_model=PostResponse)
async def get_post(pid: int, db: Session = Depends(get_db)):
    try:
        found_post = find(db, pid, FastapiBlogPost)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return found_post


@router.put("/{pid}", response_model=PostResponse)
def update_post(pid: int, payload: PostRequest, db: Session = Depends(get_db)):
    try:
        updated_post = update(db, pid, FastapiBlogPost, payload.dict())
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return updated_post


@router.delete("/{pid}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(pid: int, db: Session = Depends(get_db)):
    try:
        delete(db, pid, FastapiBlogPost)
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
