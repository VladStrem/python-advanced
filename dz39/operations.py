from sqlalchemy.orm import Session
from sqlalchemy import select
from models import Student
from faker import Faker
from datetime import date

fake = Faker()

class StudentDB:

    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, first_name: str, last_name: str, email: str, birth_date: date, is_budget: bool = None):
        student = Student(
            first_name=first_name,
            last_name=last_name,
            email=email,
            birth_date=birth_date,
            is_budget=is_budget
        )
        self.db.add(student)
        self.db.commit()
        self.db.refresh(student)
        return student

    def get_all(self):
        stmt = select(Student).order_by(Student.last_name)
        return self.db.execute(stmt).scalars().all()
        #return self.db.query(Student).order_by(Student.last_name).all()

    def update(self, student_id: int, **kwargs):
        stmt = select(Student).filter_by(id=student_id)
        student = self.db.execute(stmt).scalar_one_or_none()
        #student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None
        for key, value in kwargs.items():
            setattr(student, key, value)
        self.db.commit()
        self.db.refresh(student)
        return student

    def delete(self, student_id: int):
        student = self.db.execute(select(Student).filter_by(id=student_id)).scalar_one_or_none()
        #student = self.db.query(Student).filter(Student.id == student_id).first()
        if not student:
            return None
        self.db.delete(student)
        self.db.commit()
        return student

    def fill_with_fake_data(self, count: int = 10):
        for _ in range(count):
            self.add(
                first_name=fake.first_name(),
                last_name=fake.last_name(),
                email=fake.email(),
                birth_date=fake.date_of_birth(),
                is_budget=fake.boolean()
            )

    def get_budget_students_born_after(self, date_after: date):
        return self.db.execute(
            select(Student).filter(Student.is_budget == True, Student.birth_date > date_after)
        ).scalars().all()
        #return self.db.query(Student).filter(Student.is_budget == True, Student.birth_date > date_after).all()

    def get_total_students(self):
        return self.db.query(Student).count()
