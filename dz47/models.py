from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Boolean


class Base(DeclarativeBase):
    pass


class TodoModel(Base):
    __tablename__ = "todos"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    title: Mapped[str] = mapped_column(String, index=True)
    complete: Mapped[bool] = mapped_column(Boolean, default=False)