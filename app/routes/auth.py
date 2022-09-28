from fastapi import APIRouter, Depends, HTTPException, Response, status
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.users import UserLogin
from app.models.users import FastapiUsers
from app.utils.password import verify_password
from app.utils.oauth2 import create_access_token

router = APIRouter(tags=['Authentication'])


@router.post("/login")
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    try:
        user = db.query(FastapiUsers).filter(user_credentials.username == FastapiUsers.email).first()

        if not user:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

        if not verify_password(user_credentials.password, user.password):
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid Credentials")

    except Exception as e:
        raise e

    else:
        access_token = create_access_token(data={"user_id": user.uid})
        return {"access_token": access_token, "token_type": "bearer"}
