from sqlalchemy.orm import Mapped, mapped_column, DeclarativeBase
from sqlalchemy import String, Integer


class Base(DeclarativeBase):
    pass


class Article(Base):
    __tablename__ = "articles"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    author: Mapped[str] = mapped_column(String, index=True)
    year: Mapped[int] = mapped_column(Integer)