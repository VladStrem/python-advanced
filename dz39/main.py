from database import engine, SessionLocal
from models import Base
from operations import StudentDB
from datetime import date

def re_create_table():
    Base.metadata.drop_all(engine)
    Base.metadata.create_all(engine)

re_create_table()

# Ініціалізація бази даних
Base.metadata.create_all(bind=engine)

# Створення сесії
db = SessionLocal()

# Приклад використання
student_db = StudentDB(db)

# Додавання фейкових студентів
student_db.fill_with_fake_data(5)

# Отримання всіх студентів
students = student_db.get_all()
for student in students:
    print(student.id, student.first_name, student.last_name)

# Оновлення даних студента
updated_student = student_db.update(1, first_name="UpdatedName")
print(updated_student.first_name)

# Видалення студента
student_db.delete(2)

# Отримання студентів на бюджеті, що народилися після певної дати
budget_students = student_db.get_budget_students_born_after(date(2000, 1, 1))
for student in budget_students:
    print(student.id, student.first_name, student.last_name)

# Загальна кількість студентів
total_students = student_db.get_total_students()
print(f"Total students: {total_students}")
