from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Boolean


class Base(DeclarativeBase):
    pass


class Todo(Base):
    __tablename__ = "todos"
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    description: Mapped[str] = mapped_column(String, index=True)
    completed: Mapped[bool] = mapped_column(Boolean, default=False)
