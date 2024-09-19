# services/crud_user.py
from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from typing import Optional
from bcrypt import hashpw, gensalt, checkpw
########


from sqlalchemy.orm import Session
from sqlalchemy import select
from models.user import User
from schemas.user import UserCreate, UserUpdate
from typing import Optional
from bcrypt import hashpw, gensalt, checkpw


# Інші функції ...

def get_all_users(db: Session):
    return db.query(User).all()


def delete_user_by_id(db: Session, user_id: int) -> bool:
    user = db.get(User, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False


# def get_users(db: Session):
#     return db.query(User).all()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    stmt = select(User).offset(skip).limit(limit)
    users = db.scalars(stmt).all()
    return users


def get_user_by_email(db: Session, email: str) -> Optional[User]:
    stmt = select(User).where(User.email == email)
    return db.scalars(stmt).first()


def create_user(db: Session, user_create: UserCreate) -> User:
    hashed_password = hashpw(user_create.password.encode('utf-8'), gensalt())
    db_user = User(username=user_create.username, email=user_create.email, password=hashed_password)
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
        setattr(user, field, value)
    db.commit()
    db.refresh(user)
    return user


def authenticate_user(db: Session, email: str, password: str) -> Optional[User]:
    user = get_user_by_email(db, email)
    if user and checkpw(password.encode('utf-8'), user.password):
        return user
    return None
