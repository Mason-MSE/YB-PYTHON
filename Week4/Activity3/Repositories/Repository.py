from Repositories.BaseRepository import Repository
from Entities.Entity import *

# ---------------- Student Repository ----------------
class StudentRepository(Repository[Student]):
    def __init__(self, db):
        super().__init__(db, Student.__table__, Student)

# ---------------- Teacher Repository ----------------
class TeacherRepository(Repository[Teacher]):
    def __init__(self, db):
        super().__init__(db, Teacher.__table__, Teacher)

# ---------------- Course Repository ----------------
class CourseRepository(Repository[Course]):
    def __init__(self, db):
        super().__init__(db, Course.__table__, Course)

# ---------------- Enrollment Repository ----------------
class EnrollmentRepository(Repository[Enrollment]):
    def __init__(self, db):
        super().__init__(db, Enrollment.__table__, Enrollment)

# ---------------- Teaching Assignment Repository ----------------
class TeachingAssignmentRepository(Repository[TeachingAssignment]):
    def __init__(self, db):
        super().__init__(db, TeachingAssignment.__table__, TeachingAssignment)