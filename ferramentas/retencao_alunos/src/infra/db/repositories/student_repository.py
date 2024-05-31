from .....models import Student as Student_db
from typing import List
from django.db import transaction
from ....data.interfaces.student_repository import StudentRepositoryInterface
from .....src.domain.models.student import Student

class Student_Registering_Exception(Exception):
    def __init__(self, message="Student could not be registered!"):
        self.message = message
        super().__init__(self.message)

class StudentRepository(StudentRepositoryInterface):

    @classmethod
    def register_student(cls, student: Student) -> None:

        #check if the student is already registered
        exists = Student_db.objects.filter(num_usp=student.nro_usp)
        if not exists:
            new_student = Student_db.objects.create(
                num_usp= student.num_usp,
                name=student.name,
                start_year=student.start_year
            )
            try:
                new_student.save()
            except Student_Registering_Exception as e:
                print(f"Exception: {e}")

    @classmethod
    def create_student_instance(cls, student: Student):
        
        new_student = Student_db.objects.create(
            num_usp= student.num_usp,
            name=student.name,
            start_year=student.start_year
        )
        return new_student
        


    @classmethod
    def existing_student(cls, student_id: str) -> bool:

        exists = Student_db.objects.filter(num_usp=student_id)
        if exists: return True
        return False


    @classmethod
    @transaction.atomic
    def register_batch_students(cls, list_students: List[Student]) -> None: 

        Student_db.objects.bulk_create(list_students, ignore_conflicts=True)
    
    @classmethod
    def list_students(cls) -> List[Student]:

        students = Student_db.objects.all()
        resp = []

        for student in students: 
            register = Student(
                num_usp= student.num_usp,
                name=student.name,
                start_year=student.start_year
            )
            resp.append(register)
        
        return resp