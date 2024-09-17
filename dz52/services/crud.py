from sqlalchemy.orm import Session
from models.user import *
from schemas.user import *


def get_posts(db: Session, skip: int = 0, limit: int = 10):
    return db.query(Post).offset(skip).limit(limit).all()


def get_post(db: Session, post_id: UUID):
    return db.query(Post).filter(Post.id == post_id).first()


def get_posts_by_author(db: Session, author_id: int, skip: int = 0, limit: int = 10):
    return db.query(Post).filter(Post.author_id == author_id).offset(skip).limit(limit).all()


def create_post(db: Session, post: PostCreate, author_id: int):
    db_post = Post(**post.dict(), author_id=author_id)
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post


def update_post(db: Session, db_post: Post, post_update: PostUpdate):
    if post_update.title:
        db_post.title = post_update.title
    if post_update.content:
        db_post.content = post_update.content
    if post_update.published:
        db_post.published = post_update.published
    db.commit()
    db.refresh(db_post)
    return db_post


def delete_post(db: Session, post_id: UUID):
    db_post = db.query(Post).filter(Post.id == post_id).first()
    if db_post:
        db.delete(db_post)
        db.commit()
    return db_post
