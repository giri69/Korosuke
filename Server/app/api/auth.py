from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from app.crud.user import get_user_by_email 
from app.crud.user import create_user
from app.schemas.user import User 
from app.schemas.user import UserCreate
from app.db.base import get_db
from app.utils import verify_password, create_access_token
from datetime import timedelta
from app.config import settings  

router = APIRouter()

@router.post("/signup", response_model=User)
def signup(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db=db, User=user)

@router.post("/login")
def login(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, email=user.email)
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid credentials")
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": db_user.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
