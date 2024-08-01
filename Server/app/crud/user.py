from sqlalchemy.orm import Session
from app.models.user import User
from sqlalchemy.orm import Session
from app import models, schemas
from app.utils import get_password_hash



def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()

def create_user(db: Session, user_data: dict):  # Accepting a plain dictionary
    # Extracting fields from user_data
    name = user_data.get("name")
    email = user_data.get("email")
    password = user_data.get("password")
    
    # Hash the password
    hashed_password = get_password_hash(password)
    
    # Create a new user instance
    db_user = models.user.User(
        name=name,
        email=email,
        hashed_password=hashed_password,
        is_active=True,
        email_verified=False,
    )
    
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
