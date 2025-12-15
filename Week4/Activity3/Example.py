from Repositories.Repository import * 
from  Entities.Entity import *
from DB.SQLiteEngine import SQLiteEngine
from DB.MySQLEngine import MySQLEngine
import os
from Config import *
from datetime import date,timedelta
import random 
if __name__ == "__main__":
    print(os.getcwd())
    db = SQLiteEngine("./data/school.db")
    # db=MySQLEngine("127.0.0.1","root","rootpassword","mydb")
    with open("init_sqlite.sql", "r") as f:
    # with open("init.sql", "r") as f:
        sql_contents = f.read()
        db.executescript(sql_contents)
        db.commit()    
    # ---------------- Repositories ----------------
    student_repo = StudentRepository(db)
    teacher_repo = TeacherRepository(db)
    course_repo = CourseRepository(db)
    enroll_repo = EnrollmentRepository(db)
    teach_repo = TeachingAssignmentRepository(db)

    # ---------------- Generate Students ----------------
    first_names = ["Alice","Bob","Charlie","Diana","Ethan","Fiona","George","Hannah","Ian","Julia"]
    last_names = ["Johnson","Smith","Brown","Prince","Hunt","White","Black","Green","Lee","Clark"]

    students = []
    for i in range(50):
        full_name = f"{random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name}@example.com"
        enroll_date = date.today() - timedelta(days=random.randint(0, 1000))
        student = Student(full_name=full_name, email=email, enroll_date=enroll_date)
        existing = student_repo.select({"email": email})
        if not existing:
            students.append(student)
            student.student_id = student_repo.insert(student) 
        else:
            students.append(existing[0])

    # ---------------- Generate Teachers ----------------
    teachers = []
    for i in range(10):
        full_name = f"Dr. {random.choice(first_names)} {random.choice(last_names)}"
        email = f"{full_name}@example.com"
        hire_date = date.today() - timedelta(days=random.randint(0, 3000))
        teacher = Teacher(full_name=full_name, email=email, hire_date=hire_date)
        existing = teacher_repo.select({"email": email})
        if not existing:
            teachers.append(teacher)
            teacher.teacher_id=teacher_repo.insert(teacher)
        else:
            teachers.append(existing[0])

    # ---------------- Generate Courses ----------------
    courses = []
    course_codes = ["MSE800","MSE801","MSE802","MSE803","MSE804"]
    for i, code in enumerate(course_codes):
        course = Course(course_code=code, course_name=f"Course {code}")
        existing = course_repo.select({"course_code": code})
        if not existing:
            course.course_id=course_repo.insert(course)
            courses.append(course)
        else:
            courses.append(existing[0])
    # ---------------- Generate Enrollments ----------------
    for student in students:
        # Each student enrolls in 1-3 random courses
        for course in random.sample(courses, random.randint(1, 5)):
            print(str(student))
            enrollment = Enrollment(student_id=student.student_id, course_id=course.course_id)
            enroll_repo.insert(enrollment)

    # ---------------- Generate Teaching Assignments ----------------
    for teacher in teachers:
        # Each teacher assigned to 1-2 random courses
        for course in random.sample(courses, random.randint(1, 5)):
            assignment = TeachingAssignment(teacher_id=teacher.teacher_id, course_id=course.course_id)
            teach_repo.insert(assignment)

    # ---------------- Commit and Close ----------------
    db.commit()

    # 1️⃣ Number of students in MSE800
    rows = db.fetch("""
        SELECT COUNT(e.enrollment_id) AS student_count
        FROM enrollments e
        JOIN courses c ON e.course_id = c.course_id
        WHERE c.course_code = 'MSE800' AND e.is_deleted = 0;
    """)
    print(rows[0][0])
    

    # 2️⃣ List all teachers teaching MSE801
    rows = db.fetch("""
        SELECT distinct t.full_name
        FROM teachers t
        JOIN teaching_assignments ta ON t.teacher_id= ta.teacher_id and ta.is_deleted=0
        JOIN courses c on c.course_id=ta.course_id and c.is_deleted=0
        WHERE c.course_code = 'MSE801' AND c.is_deleted = 0 ;
    """)
    teacher_names = [row["full_name"] for row in rows]  # preferred for readability
    print(teacher_names)

    # print([str(Appointment(**row)) for row in map(dict, db.fetch("select * from appointments"))])
    # print(list( map(dict,db.fetch("select * from appointments"))))
    db.close()