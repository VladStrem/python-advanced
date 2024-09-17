from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from typing import Optional
from bcrypt import hashpw, gensalt, checkpw

def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()

def get_user_by_id(db: Session, user_id: int) -> Optional[User]:
    return db.get(User, user_id)

def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = hashpw(user_create.password.encode('utf-8'), gensalt())
    db_user = User(
        username=user_create.username, 
        email=user_create.email, 
        password=hashed_password,
        is_superuser=user_create.is_superuser
        )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user(db: Session, user: User, user_update: UserUpdate) -> User:
    payload_dict = user_update.dict(exclude_unset=True)
    if not payload_dict:
        return user
    for field, value in payload_dict.items():
        if field == "password":
            value = hashpw(value.encode('utf-8'), gensalt())
        elif field == "is_superuser":
            value = bool(value)
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user

def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if user and checkpw(password.encode('utf-8'), user.password):
        return user
    return None

def delete_user(db: Session, user_id: int):
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
