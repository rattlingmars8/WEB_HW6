import sqlite3
from datetime import datetime, date, timedelta

from faker import Faker
from uuid import uuid4
import random

fake = Faker("uk-UA")


class DatabaseManager:
    def __init__(self, db_name):
        self.db_name = db_name
        self.connection = None
        self.cursor = None

    def __enter__(self):
        self.connection = sqlite3.connect(self.db_name)
        self.cursor = self.connection.cursor()
        return self.cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.commit()
            self.connection.close()


class Student:
    def __init__(self, id, fullname, group_id):
        self.id = id
        self.fullname = fullname
        self.group_id = group_id

    def generate_insert_query(self):
        return """
        INSERT INTO students (id, fullname, group_id) VALUES (?, ?, ?)
        """, (
            self.id,
            self.fullname,
            self.group_id,
        )


class Group:
    def __init__(self, id, name):
        self.id = id
        self.name = name

    def generate_insert_query(self):
        return """
        INSERT INTO groups (id, name) VALUES (?, ?)
        """, (
            self.id,
            self.name,
        )


class Teacher:
    def __init__(self, id, fullname):
        self.id = id
        self.fullname = fullname

    def generate_insert_query(self):
        return """
        INSERT INTO teachers (id, fullname) VALUES (?, ?)
        """, (
            self.id,
            self.fullname,
        )


class Subject:
    def __init__(self, sub_name, teacher_id):
        # self.id = id
        self.sub_name = sub_name
        self.teacher_id = teacher_id

    def generate_insert_query(self):
        return """
        INSERT INTO subjects (sub_name, teacher_id) VALUES (?, ?)
        """, (
            self.sub_name,
            self.teacher_id,
        )


class Grade:
    def __init__(self, subject_id, student_id, grade, date_of):
        self.subject_id = subject_id
        self.student_id = student_id
        self.grade = grade
        self.time_of = date_of

    def generate_insert_query(self):
        return """
        INSERT INTO grades (subject_id, student_id, grade, date_of) VALUES (?,?,?,?)
        """, (
            self.subject_id,
            self.student_id,
            self.grade,
            self.time_of,
        )


# Встановлення зв'язку з базою даних
with DatabaseManager("database.db") as cursor:
    # Створення таблиці студентів
    cursor.execute(
        """
        DROP TABLE IF EXISTS students
        """
    )
    cursor.execute(
        """
        CREATE TABLE students (
        id VARCHAR(20) PRIMARY KEY, 
        fullname VARCHAR(100), 
        group_id INT REFERENCES [groups] (id)
        )
        """
    )

    # Створення таблиці груп
    cursor.execute(
        """
        DROP TABLE IF EXISTS groups
        """
    )
    cursor.execute(
        """
        CREATE TABLE groups (
        id INT PRIMARY KEY, 
        name VARCHAR(100)
        )
        """
    )

    # Створення таблиці вчителів
    cursor.execute(
        """
        DROP TABLE IF EXISTS teachers
        """
    )
    cursor.execute(
        """
        CREATE TABLE teachers (
        id VARCHAR(20) PRIMARY KEY,
        fullname VARCHAR(100)
        )
        """
    )

    # Створення таблиці предметів
    cursor.execute(
        """
        DROP TABLE IF EXISTS subjects
        """
    )
    cursor.execute(
        """
        CREATE TABLE subjects (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        sub_name STRING, 
        teacher_id REFERENCES teachers (id)
        )
        """
    )

    # Створення таблиці оцінок
    cursor.execute(
        """
        DROP TABLE IF EXISTS grades
        """
    )
    cursor.execute(
        """
        CREATE TABLE grades (
        id INTEGER PRIMARY KEY AUTOINCREMENT, 
        subject_id REFERENCES subjects (id),
        student_id REFERENCES students (id),
        grade INTEGER,
        date_of DATE
        )
        """
    )

    # Генерація випадкових даних і заповнення таблиць
    students = []
    for _ in range(50):
        # Генерація унікального ідентифікатора студента
        student_id = uuid4().hex

        student_name = fake.name()
        group_id = fake.random_int(min=1, max=3)
        student = Student(student_id, student_name, group_id)
        students.append(student)

    for student in students:
        query, params = student.generate_insert_query()
        cursor.execute(query, params)

    groups = [(1, "Group 1"), (2, "Group 2"), (3, "Group 3")]
    for group_id, group_name in groups:
        group = Group(group_id, group_name)
        query, params = group.generate_insert_query()
        cursor.execute(query, params)

    teachers = []
    for _ in range(5):
        # Генерація унікального ідентифікатора вчителя
        teacher_id = uuid4().hex

        teacher_name = fake.name()
        teacher = Teacher(teacher_id, teacher_name)
        teachers.append(teacher)

    for teacher in teachers:
        query, params = teacher.generate_insert_query()
        cursor.execute(query, params)

    SUBJECTS = [
        "Математика",
        "Українська мова і література",
        "Історія України",
        "Фізика",
        "Хімія",
        "Біологія",
        "Економіка",
        "Комп'ютерні науки",
    ]
    for subject_name in SUBJECTS:
        # Вибір випадкового ідентифікатора вчителя зі списку вчителів
        teacher_id = random.choice([teacher.id for teacher in teachers])
        subject = Subject(subject_name, teacher_id)
        query, params = subject.generate_insert_query()
        cursor.execute(query, params)

    def seed_grades():
        start_date = datetime.strptime("2023-01-16", "%Y-%m-%d")
        end_date = datetime.strptime("2023-11-25", "%Y-%m-%d")

        def get_list_dates(start: date, end: date):
            result = []
            current_date = start
            while current_date <= end:
                # Додавання дати до списку результатів, якщо це не субота або неділя
                if current_date.isoweekday() < 6:
                    result.append(current_date)
                current_date += timedelta(days=1)
            return result

        list_dates = get_list_dates(start_date, end_date)

        list_of_Grades = []
        for day in list_dates:
            # Вибір випадкового ідентифікатора предмета зі списку предметів
            rand_subject_id = random.randint(1, len(SUBJECTS))
            # Вибір випадкових ідентифікаторів студентів зі списку студентів
            rand_students = random.sample(
                [student.id for student in students], random.randint(1, 6)
            )
            for st in rand_students:
                grade = Grade(rand_subject_id, st, random.randint(1, 12), day.date())
                list_of_Grades.append(grade)

        return list_of_Grades

    # Генерація оцінок і заповнення таблиці оцінок
    grades = seed_grades()
    for gr in grades:
        query, params = gr.generate_insert_query()
        cursor.execute(query, params)
