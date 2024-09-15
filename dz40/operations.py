from sqlalchemy.orm import Session
from sqlalchemy import func, select
from models import Student, Grade
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
    
    
class GradeDB:
    def __init__(self, db_session: Session):
        self.db = db_session

    def add(self, subject: str, score: int, student_id: int):
        grade = Grade(subject=subject, score=score, student_id=student_id)
        self.db.add(grade)
        self.db.commit()
        self.db.refresh(grade)
        return grade

    def get_all(self):
        return self.db.execute(select(Grade).order_by(Grade.subject)).scalars().all()

    def update(self, grade_id: int, **kwargs):
        stmt = select(Grade).filter_by(id=grade_id)
        grade = self.db.execute(stmt).scalar_one_or_none()
        if not grade:
            return None
        for key, value in kwargs.items():
            setattr(grade, key, value)
        self.db.commit()
        self.db.refresh(grade)
        return grade

    def delete(self, grade_id: int):
        grade = self.db.execute(select(Grade).filter_by(id=grade_id)).scalar_one_or_none()
        if not grade:
            return None
        self.db.delete(grade)
        self.db.commit()
        return grade

    def get_grades_by_student_lastname(self, last_name: str):
        return self.db.execute(
            select(Grade).join(Student).filter(Student.last_name == last_name)
        ).scalars().all()

    def get_grades_by_subject(self, subject: str):
        return self.db.execute(
            select(Grade).filter(Grade.subject == subject).order_by(Student.last_name)
        ).scalars().all()

    def get_average_score_by_subject(self):
        result = self.db.execute(
            select(Grade.subject, func.avg(Grade.score)).group_by(Grade.subject)
        ).all()
        return result
