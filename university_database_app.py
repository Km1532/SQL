import sqlite3
def connect_to_db():
    conn = sqlite3.connect('university.db')
    conn.row_factory = sqlite3.Row
    return conn, conn.cursor()
def add_student(name, age, major, cursor, conn):
    cursor.execute("INSERT INTO students (name, age, major) VALUES (?, ?, ?)", (name, age, major))
    conn.commit()
def add_course(course_name, instructor, cursor, conn):
    cursor.execute("INSERT INTO courses (course_name, instructor) VALUES (?, ?)", (course_name, instructor))
    conn.commit()
def register_student_for_course(student_id, course_id, cursor, conn):
    cursor.execute("INSERT INTO student_courses (student_id, course_id) VALUES (?, ?)", (student_id, course_id))
    conn.commit()
def get_students_registered_for_course(course_id, cursor):
    cursor.execute("SELECT s.name FROM students s INNER JOIN student_courses sc ON s.id=sc.student_id WHERE sc.course_id=?", (course_id,))
    rows = cursor.fetchall()
    return [row["name"] for row in rows]
def view_students(cursor):
    cursor.execute("SELECT * FROM students")
    rows = cursor.fetchall()
    for row in rows:
        print(f"ID: {row['id']}, Ім'я: {row['name']}, Вік: {row['age']}, Факультет: {row['major']}")
def view_courses(cursor):
    cursor.execute("SELECT * FROM courses")
    rows = cursor.fetchall()
    for row in rows:
        print(row)
def main_menu():
    print("1. Додати нового студента")
    print("2. Додати новий курс")
    print("3. Реєстрація студента на курс")
    print("4. Переглянути студентів")
    print("5. Переглянути курси")
    print("6. Переглянути студентів на конкретному курсі")
    print("0. Вихід")
def main():
    conn, cursor = connect_to_db()
    while True:
        main_menu()
        choice = input("Виберіть опцію: ")
        if choice == "1":
            name = input("Введіть ім'я студента: ")
            age = input("Введіть вік студента: ")
            major = input("Введіть факультет студента: ")
            add_student(name, age, major, cursor, conn)
        elif choice == "2":
            course_name = input("Введіть назву курсу: ")
            instructor = input("Введіть викладача: ")
            add_course(course_name, instructor, cursor, conn)
        elif choice == "3":
            student_id = input("Введіть ID студента: ")
            course_id = input("Введіть ID курсу: ")
            register_student_for_course(student_id, course_id, cursor, conn)
        elif choice == "4":
            view_students(cursor)
        elif choice == "5":
            view_courses(cursor)
        elif choice == "6":
            course_id = input("Введіть ID курсу: ")
            students_registered = get_students_registered_for_course(course_id, cursor)
            print(f"Студенти, які ходять на цей курс: {students_registered}")
        elif choice == "0":
            break
        else:
            print("Некоректний вибір.")
    conn.close()
if __name__ == "__main__":
    main()
