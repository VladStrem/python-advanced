from sqlalchemy.orm import DeclarativeBase, relationship, Mapped, mapped_column
from sqlalchemy import String, ForeignKey, Column, Table, Integer
from typing import List, Optional
from database import engine


class Base(DeclarativeBase):
    pass


StudentCourse = Table(
    "StudentCourse",
    Base.metadata,
    Column("student_id", ForeignKey("students.id"), primary_key=True),
    Column("course_id", ForeignKey("courses.id"), primary_key=True)
)


class Student(Base):
    __tablename__ = "students"

    id: Mapped[int] = mapped_column(primary_key=True)
    first_name: Mapped[str] = mapped_column(String(30), nullable=False)
    last_name: Mapped[str] = mapped_column(String(30), nullable=False)

    profile: Mapped["StudentProfile"] = relationship("StudentProfile", back_populates="student", uselist=False)
    courses: Mapped[List["Course"]] = relationship(secondary=StudentCourse, back_populates="students")

    def __repr__(self):
        return f"Student(id={self.id}, first_name={self.first_name}, last_name={self.last_name})"


class Course(Base):
    __tablename__ = "courses"

    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30), nullable=False)
    description: Mapped[str] = mapped_column(String(255))
    hours: Mapped[int] = mapped_column(Integer)

    students: Mapped[List["Student"]] = relationship(secondary=StudentCourse, back_populates="courses")

    def __repr__(self):
        return f"Course(id={self.id}, name={self.name}, description={self.description}, hours={self.hours})"


class StudentProfile(Base):
    __tablename__ = "student_profiles"

    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    student_id: Mapped[int] = mapped_column(ForeignKey("students.id"), unique=True)
    address: Mapped[Optional[str]] = mapped_column(String(100))
    phone_number: Mapped[Optional[str]] = mapped_column(String(20))

    student: Mapped["Student"] = relationship("Student", back_populates="profile")