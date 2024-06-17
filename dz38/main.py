from datetime import date
from database import engine
from operations import (add_student, add_grade, get_all_students,
                        update_student, delete_student, get_students_with_grades,
                        get_student_by_last_name, get_average_score)


with engine.connect() as connection:
    add_student(connection, 'John', 'Doe', date(2000, 1, 15))
    add_student(connection, 'Jane', 'Smith', date(2001, 2,20))
    add_student(connection, 'Alice', 'Johnson', date(2002, 3, 25))

    add_grade(connection, 'Math', 11, 1)
    add_grade(connection, 'Science', 12, 1)
    add_grade(connection, 'Math', 10, 2)
    add_grade(connection, 'Science', 9, 2)
    add_grade(connection, 'Math', 10, 3)
    add_grade(connection, 'Science', 8, 3)

    students_with_grades = get_students_with_grades(connection)
    for grade in students_with_grades:
        print(grade)

    student_grades = get_student_by_last_name(connection, 'Smith')
    for row in student_grades:
        print(row)

    avg_scores = get_average_score(connection)
    for row in avg_scores:
        print(row)
