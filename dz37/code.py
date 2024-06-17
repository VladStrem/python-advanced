from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from sqlalchemy import insert, select, update, delete
from datetime import date

engine = create_engine('sqlite:///students.db', echo=True)

metadata = MetaData()

students = Table('students', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('first_name', String, nullable=False),
                 Column('last_name', String, nullable=False),
                 Column('birth_date', Date, nullable=False)
                 )

metadata.create_all(engine)


def add_student(conn, first_name, last_name, birth_date):
    stmt = insert(students).values(first_name=first_name, last_name=last_name, birth_date=birth_date)
    conn.execute(stmt)
    conn.commit()


def get_all_students(conn):
    stmt = select(students).order_by(students.c.last_name, students.c.first_name)
    result = conn.execute(stmt)
    return result.fetchall()


def update_student(conn, student_id, first_name=None, last_name=None, birth_date=None):
    stmt = update(students).where(students.c.id == student_id)
    values = {}
    if first_name:
        values['first_name'] = first_name
    if last_name:
        values['last_name'] = last_name
    if birth_date:
        values['birth_date'] = birth_date
    stmt = stmt.values(**values)
    conn.execute(stmt)
    conn.commit()


def delete_student(conn, student_id):
    stmt = delete(students).where(students.c.id == student_id)
    conn.execute(stmt)
    conn.commit()


with engine.connect() as connection:
    add_student(connection, 'John', 'Doe', date(2000, 1, 15))
    add_student(connection, 'Jane', 'Smith', date(2001, 2, 20))
    add_student(connection, 'Ivan', 'Petrov', date(2000, 6, 22))
    add_student(connection, 'Abril', 'Shaw', date(2001, 5, 10))

    students_list = get_all_students(connection)
    for student in students_list:
        print(student)

    update_student(connection, 1, first_name='Johnny')

    delete_student(connection, 5)

    students_list = get_all_students(connection)
    for student in students_list:
        print(student)
