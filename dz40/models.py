from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy import String, Integer, Boolean, Date, DateTime, func, ForeignKey


class Base(DeclarativeBase):
    pass


class Grade(Base):
    __tablename__ = 'grades'

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    subject: Mapped[str] = mapped_column(String(50), nullable=False)
    score: Mapped[int] = mapped_column(Integer, nullable=False)
    student_id: Mapped[int] = mapped_column(Integer, ForeignKey('students.id'), nullable=False)

    # Відношення "один-до-багатьох" з таблицею Student
    student = relationship("Student", back_populates="grades")


class Student(Base):
    __tablename__ = 'students'
    
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)
    email: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    birth_date: Mapped[Date] = mapped_column(Date, nullable=False)
    is_budget: Mapped[bool] = mapped_column(Boolean, default=None)
    created_at: Mapped[DateTime] = mapped_column(DateTime, server_default=func.now())
    
    grades = relationship("Grade", back_populates="student", cascade="all, delete-orphan")
    