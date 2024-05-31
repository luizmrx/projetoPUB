from abc import ABC, abstractmethod
from typing import Dict


class ListStudentsSubjectsInterface(ABC):

    @abstractmethod
    def list_students_most_subjects_to_do(self, year: int, semester: int) -> Dict: pass
