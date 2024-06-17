from sqlalchemy import ForeignKey,Table, Column, Integer, String, Date
from database import metadata, engine

students = Table(
    'students',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('first_name', String(50), nullable=False),
    Column('last_name', String(50), nullable=False),
    Column('birth_date', Date, nullable=False)
)

grades = Table(
    'grades',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('subject', String(100), nullable=False),
    Column('score', Integer, nullable=False),
    Column('student_id', Integer, ForeignKey('students.id'))
)
metadata.create_all(engine)