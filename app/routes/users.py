from fastapi import APIRouter, status, HTTPException, Depends
from sqlalchemy.orm import Session

from app.models.users import FastapiUsers
from app.schemas.users import UserCreate, UserSend
from app.utils.password import hash_password
from app.database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=UserSend)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    try:
        hashed_password = hash_password(user.password)
        user.password = hashed_password

        new_user = FastapiUsers(**user.dict())

        db.add(new_user)
        db.commit()
        db.refresh(new_user)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return new_user


@router.get("/{uid}", response_model=UserSend)
async def get_user(uid: int, db: Session = Depends(get_db)):
    try:
        user = db.query(FastapiUsers).filter(FastapiUsers.uid == uid).first()
        if not user:
            raise Exception(f"No user data found for id {uid}")
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"{e}")
    else:
        return user
