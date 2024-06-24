from database import Session as SessionMaker
from models import Base, Student, Course, StudentProfile
from database import engine
from sqlalchemy import select
from faker import Faker
import random


def re_create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)


def insert_data():
    with SessionMaker() as session:
        faker = Faker()
        students = []
        for _ in range(10):
            student = Student(
                first_name=faker.first_name(),
                last_name=faker.last_name()
            )
            students.append(student)
            session.add(student)

        courses = []
        for _ in range(5):
            course = Course(
                name=faker.word(),
                description=faker.sentence(),
                hours=random.randint(10, 100)
            )
            courses.append(course)
            session.add(course)

        session.commit()

        for student in students:
            student.courses = random.sample(courses, k=random.randint(1, len(courses)))

        for student in students:
            profile = StudentProfile(
                student_id=student.id,
                address=faker.address(),
                phone_number=faker.phone_number()
            )
            session.add(profile)

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


def get_student_profile(student_id):
    with SessionMaker() as session:
        stmt = select(StudentProfile).where(StudentProfile.student_id == student_id)
        profile = session.scalars(stmt).one_or_none()
        if profile:
            print(f"Address: {profile.address}, Phone Number: {profile.phone_number}")