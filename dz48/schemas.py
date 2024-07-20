from pydantic import BaseModel
from typing import Optional


class ArticleBase(BaseModel):
    title: str
    author: str
    year: int
    
    
class ArticleCreate(ArticleBase):
    pass


class ArticleUpdate(BaseModel):
    title: str | None = None
    author: str | None = None
    year: int | None = None


class Article(ArticleBase):
    id: int
    
    class Config:
        from_attributes = True