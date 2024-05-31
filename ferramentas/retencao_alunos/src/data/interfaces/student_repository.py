from abc import ABC, abstractmethod
from typing import List
from ....src.domain.models.student import Student

class StudentRepositoryInterface(ABC):

    @abstractmethod
    def register_student(self, student: Student) -> None: pass

    @abstractmethod
    def create_student_instance(self, student: Student): pass
 
    @abstractmethod
    def list_students(self) -> List[Student]: pass

    @abstractmethod
    def existing_student(self, student_id: str) -> bool: pass

    @abstractmethod
    def register_batch_students(self, list_students: List[Student]) -> None: pass
    