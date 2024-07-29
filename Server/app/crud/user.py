from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import get_password_hash
from app.schemas.user import UserCreate



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, User: UserCreate):
    hashed_password = get_password_hash(User.password)
    db_user = models.user.User(
        name=User.name,
        email=User.email,
        hashed_password=hashed_password,
        is_active=True,
        email_verified=False,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
