from datetime import datetime
from Entities.BaseEntity import BaseEntity

# ---------------- Student Entity ----------------
class Student(BaseEntity["Student"]):
    __table__ = "students"
    __id_field__ = "student_id"
    __auto_increment__ = True

    def __init__(self, student_id=None, full_name=None, email=None, enroll_date=None, **kwargs):
        self.student_id = student_id
        self.full_name = full_name
        self.email = email
        self.enroll_date = enroll_date
        super().__init__(**kwargs)

# ---------------- Teacher Entity ----------------
class Teacher(BaseEntity["Teacher"]):
    __table__ = "teachers"
    __id_field__ = "teacher_id"
    __auto_increment__ = True

    def __init__(self, teacher_id=None, full_name=None, email=None, hire_date=None, **kwargs):
        self.teacher_id = teacher_id
        self.full_name = full_name
        self.email = email
        self.hire_date = hire_date
        super().__init__(**kwargs)

# ---------------- Course Entity ----------------
class Course(BaseEntity["Course"]):
    __table__ = "courses"
    __id_field__ = "course_id"
    __auto_increment__ = True

    def __init__(self, course_id=None, course_code=None, course_name=None, **kwargs):
        self.course_id = course_id
        self.course_code = course_code
        self.course_name = course_name
        super().__init__(**kwargs)

# ---------------- Enrollment Entity ----------------
class Enrollment(BaseEntity["Enrollment"]):
    __table__ = "enrollments"
    __id_field__ = "enrollment_id"
    __auto_increment__ = True

    def __init__(self, enrollment_id=None, student_id=None, course_id=None, **kwargs):
        self.enrollment_id = enrollment_id
        self.student_id = student_id
        self.course_id = course_id
        super().__init__(**kwargs)

# ---------------- Teaching Assignment Entity ----------------
class TeachingAssignment(BaseEntity["TeachingAssignment"]):
    __table__ = "teaching_assignments"
    __id_field__ = "assignment_id"
    __auto_increment__ = True

    def __init__(self, assignment_id=None, teacher_id=None, course_id=None, **kwargs):
        self.assignment_id = assignment_id
        self.teacher_id = teacher_id
        self.course_id = course_id
        super().__init__(**kwargs)