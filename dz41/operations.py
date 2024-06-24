from database import Session as SessionMaker
from models import Base, Student, Course
from database import engine
from sqlalchemy import select
from faker import Faker
import random


def re_create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data():
    fake = Faker()
    with SessionMaker() as session:
        students = [Student(first_name=fake.first_name(), last_name=fake.last_name()) for _ in range(10)]
        session.add_all(students)

        courses = [
            Course(name="Mathematics", description=fake.text(), hours=40),
            Course(name="Physics", description=fake.text(), hours=35),
            Course(name="Chemistry", description=fake.text(), hours=30),
            Course(name="Biology", description=fake.text(), hours=25),
            Course(name="Python Basic", description=fake.text(), hours=45)
        ]
        session.add_all(courses)
        session.commit()

        for student in students:
            student.courses = random.sample(courses, k=random.randint(1, len(courses)))
        session.commit()


def get_student_courses(student_id):
    with SessionMaker() as session:
        stmt = select(Student).where(Student.id == student_id)
        student = session.scalars(stmt).one_or_none()
        if student:
            print([(course.id, course.name) for course in student.courses])


def get_course_students(course_name):
    with SessionMaker() as session:
        stmt = select(Course).where(Course.name == course_name)
        course = session.scalars(stmt).one_or_none()
        if course:
            print([(student.id, student.first_name, student.last_name) for student in course.students])