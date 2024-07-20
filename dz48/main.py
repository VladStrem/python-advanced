from fastapi import FastAPI, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from fastapi.templating import Jinja2Templates
from models import Article, Base
from schemas import Article as ArticleSchema
from schemas import ArticleCreate, ArticleUpdate
from crud import (get_article, get_articles, 
                  create_article, update_article, delete_article)
from database import SessionLocal, engine

Base.metadata.create_all(bind=engine)

app = FastAPI()

templates = Jinja2Templates(directory="templates")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
        
@app.get("/")
def read_root(request: Request, db: Session = Depends(get_db)):
    articles = get_articles(db=db)
    return templates.TemplateResponse("article.html", {"request": request, "articles": articles})


@app.post("/articles/", response_model=ArticleSchema)
def create_article_endpoint(article: ArticleCreate, db: Session = Depends(get_db)):
    return create_article(db, article)


@app.get("/articles/{article_id}", response_model=ArticleSchema)
def read_article(article_id: int, db: Session = Depends(get_db)):
    db_article = get_article(db=db, article_id=article_id)
    if db_article is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Article not found")
    return db_article


@app.put("/articles/{article_id}", response_model=ArticleSchema)
def update_article_endpoint(article_id: int, article: ArticleUpdate, db: Session = Depends(get_db)):
    return update_article(db=db, article_id=article_id, payload=article)


@app.delete("/articles/{article_id}", response_model=ArticleSchema)
def delete_article_endpoint(article_id: int, db: Session = Depends(get_db)):
    return delete_article(db, article_id)
