from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from uuid import UUID

from database import SessionLocal
from schemas.user import *
from services import crud

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=List[PostInDB])
def read_posts(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts(db, skip=skip, limit=limit)
    return posts


@router.get("/{post_id}", response_model=PostInDB)
def read_post(post_id: UUID, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return db_post


@router.post("/users/{author_id}/posts/", response_model=PostInDB)
def create_post_for_user(author_id: int, post: PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db=db, post=post, author_id=author_id)


@router.get("/users/{author_id}/posts/", response_model=List[PostInDB])
def read_posts_by_author(author_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    posts = crud.get_posts_by_author(db, author_id=author_id, skip=skip, limit=limit)
    return posts


@router.put("/{post_id}", response_model=PostInDB)
def update_post(post_id: UUID, post_update: PostUpdate, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.update_post(db=db, db_post=db_post, post_update=post_update)


@router.delete("/{post_id}", response_model=PostInDB)
def delete_post(post_id: UUID, db: Session = Depends(get_db)):
    db_post = crud.get_post(db, post_id=post_id)
    if db_post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return crud.delete_post(db=db, post_id=post_id)
