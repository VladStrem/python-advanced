from operations import re_create_table, insert_data, get_course_students, get_student_courses, get_student_profile


if __name__ == '__main__':
    re_create_table()
    insert_data()
    get_student_courses("1")
    get_course_students("Mathematics")
    get_student_profile(1)