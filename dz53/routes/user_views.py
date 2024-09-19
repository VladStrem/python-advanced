# routes/user_views.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from models.user import User
from schemas.user import UserCreate, UserUpdate, UserOut, UserAuth
from services.crud_user import get_user_by_email, create_user, update_user, authenticate_user, get_all_users, \
    delete_user_by_id
from database import get_db

router = APIRouter(prefix="/users", tags=["User"])


@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    return create_user(db, user)


@router.get("/", response_model=list[UserOut])
def list_users(db: Session = Depends(get_db)):
    return get_all_users(db)


@router.delete("/{user_id}", response_model=dict)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    deleted = delete_user_by_id(db, user_id)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return {"detail": "User deleted successfully"}


@router.put("/make-superuser/{user_id}", response_model=UserOut)
def make_superuser(user_id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user

# # routes/user_views.py
# from typing import List
#
# from fastapi import APIRouter, Depends, HTTPException, status
# from sqlalchemy.orm import Session
#
# from models.user import User
# from schemas.user import UserCreate, UserUpdate, UserOut, UserAuth
# from services.crud_user import get_user_by_email, create_user, update_user, authenticate_user
# from database import get_db
#
# router = APIRouter(prefix="/users", tags=["User"])
#
#
# @router.post("/register", response_model=UserOut)
# def register_user(user: UserCreate, db: Session = Depends(get_db)):
#     db_user = get_user_by_email(db, user.email)
#     if db_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
#     return create_user(db, user)
#
#
# @router.get("/users", response_model=List[UserOut])
# def get_users(db: Session = Depends(get_db)):
#     return db.query(User).all()
#
#
# @router.post("/auth", response_model=UserOut)
# def authenticate(user: UserAuth, db: Session = Depends(get_db)):
#     authenticated_user = authenticate_user(db, user.email, user.password)
#     if not authenticated_user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
#     return authenticated_user
#
#
# @router.put("/update", response_model=UserOut)
# def update_user_data(user_update: UserUpdate, auth_user: UserAuth, db: Session = Depends(get_db)):
#     user = authenticate_user(db, auth_user.email, auth_user.password)
#     if not user:
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid credentials")
#     updated_user = update_user(db, user, user_update)
#     return updated_user
#
#
# @router.delete("/users/{user_id}", response_model=dict)
# def delete_user(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#
#     db.delete(user)
#     db.commit()
#
#     return {"message": "User deleted successfully"}
#
#
# @router.put("/make-superuser/{user_id}", response_model=UserOut)
# def make_superuser(user_id: int, db: Session = Depends(get_db)):
#     user = db.query(User).filter(User.id == user_id).first()
#     if not user:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
#     user.is_superuser = True
#     db.commit()
#     db.refresh(user)
#     return user
