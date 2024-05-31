from abc import ABC, abstractmethod
from typing import List
from ....src.domain.models.discipline import Discipline

class DisciplineRepositoryInterface(ABC):

    @abstractmethod
    def register_discipline(self, discipline: Discipline) -> None: pass

    @abstractmethod
    def list_disciplines_by_semester(self, semester: int) -> List[Discipline]: pass

    @abstractmethod
    def list_all_disciplines(self) -> List[Discipline]: pass
