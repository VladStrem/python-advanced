from sqlalchemy import insert, select, update, delete, func
from tables import students, grades


def add_student(conn, first_name, last_name, birth_date):
    stmt = insert(students).values(first_name=first_name, last_name=last_name, birth_date=birth_date)
    conn.execute(stmt)
    conn.commit()


def add_grade(conn, subject, score, student_id):
    stmt = insert(grades).values(subject=subject, score=score, student_id=student_id)
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


def get_students_with_grades(conn):
    stmt = select(students.c.id, students.c.first_name, students.c.last_name, students.c.birth_date,
                  grades.c.subject, grades.c.score).select_from(
        students.join(grades, students.c.id == grades.c.student_id)
    ).order_by(students.c.last_name, students.c.first_name)
    result = conn.execute(stmt)
    return result.fetchall()


def get_student_by_last_name(conn, last_name):
    stmt = select(students.c.first_name, students.c.last_name, grades.c.subject, grades.c.score).select_from(
        students.join(grades, students.c.id == grades.c.student_id)
    ).where(students.c.last_name == last_name)
    result = conn.execute(stmt)
    return result.fetchall()


def get_average_score(conn):
    stmt = select(grades.c.subject, func.round(func.avg(grades.c.score), 2).label('average_score')).group_by(grades.c.subject)
    result = conn.execute(stmt)
    return result.fetchall()

