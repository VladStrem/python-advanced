from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from schemas.user import UserCreate, UserUpdate, UserOut, UserAuth
from services.crud_user import get_user_by_email, create_user, update_user, authenticate_user, get_user_by_id, delete_user
from database import get_db

router = APIRouter(prefix="/users", tags=["User"])

@router.post("/register", response_model=UserOut)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return create_user(db, user)

@router.post("/auth", response_model=UserOut)
def authenticate(user: UserAuth, db: Session = Depends(get_db)):
    authenticated_user = authenticate_user(db, user.email, user.password)
    if not authenticated_user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    return authenticated_user

@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@router.put("/update", response_model=UserOut)
def update_user_data(user_update: UserUpdate, auth_user: UserAuth, db: Session = Depends(get_db)):
    user = authenticate_user(db, auth_user.email, auth_user.password)
    if not user:
        raise HTTPException(status_code=400, detail="Invalid credentials")
    updated_user = update_user(db, user, user_update)
    return updated_user


@router.put("/{user_id}/make_superuser", response_model=UserOut)
def make_superuser(user_id: int, auth_user: UserAuth, db: Session = Depends(get_db)):
    admin_user = authenticate_user(db, auth_user.email, auth_user.password)
    if not admin_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized")
    
    user = get_user_by_id(db, user_id)
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    
    user.is_superuser = True
    db.commit()
    db.refresh(user)
    return user


@router.delete("/{user_id}", response_model=dict)
def delete_user_data(user_id: int, auth_user: UserAuth, db: Session = Depends(get_db)):
    user = authenticate_user(db, auth_user.email, auth_user.password)
    if not user or not user.is_superuser:
        raise HTTPException(status_code=400, detail="Invalid credentials or not authorized")
    delete_user(db, user_id)
    return {"detail": "User deleted"}
