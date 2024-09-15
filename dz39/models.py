from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import String, Integer, Boolean, Date, DateTime, func


class Base(DeclarativeBase):
    pass


class Student(Base):
    __tablename__ = 'students'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_budget: Mapped[bool] = mapped_column(Boolean, default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())