from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas import ArticleCreate, ArticleUpdate
from models import Article


def get_article(db: Session, article_id: int):
    stmt = select(Article).filter(Article.id == article_id)
    result = db.execute(stmt).scalar_one_or_none()
    return result


def get_articles(db: Session, skip: int = 0, limit: int = 10):
    stmt = select(Article).offset(skip).limit(limit)
    result = db.execute(stmt).scalars().all()
    return result


def create_article(db: Session, article: ArticleCreate):
    db_article = Article(**article.dict())
    db.add(db_article)
    db.commit()
    db.refresh(db_article)
    return db_article


def update_article(db: Session, article_id: int, payload: ArticleUpdate):
    stmt = select(Article).where(Article.id == article_id)
    db_article = db.execute(stmt).scalar_one_or_none()
    if not db_article:
        return db_article
    update_data = payload.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_article, key, value)
    db.commit()
    db.refresh(db_article)
    return db_article


def delete_article(db: Session, article_id: int):
    stmt = select(Article).where(Article.id == article_id)
    db_article = db.execute(stmt).scalar_one_or_none()
    if db_article:
        db.delete(db_article)
        db.commit()
    return db_article
