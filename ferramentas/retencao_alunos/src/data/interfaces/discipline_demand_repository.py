from abc import ABC, abstractmethod
from typing import Dict, List
from ....src.domain.models.discipline_demand import DisciplineDemand
from ....src.domain.models.discipline import Discipline

class DisciplineDemandRepositoryInterface(ABC):

    @abstractmethod
    def register_demand(self, demand: DisciplineDemand) -> None: pass

    @abstractmethod
    def create_demand_instance(self, demand: DisciplineDemand): pass

    @abstractmethod
    def delete_all_demands(self) -> None: pass

    @abstractmethod
    def list_late_students(self, year: int, semester: int) -> Dict: pass

    @abstractmethod
    def read_discipline_demand(self, discipline: Discipline, year: int, semester: int) -> Dict: pass

    @abstractmethod
    def register_batch_demands(self, demands: List[Discipline]) -> None: pass

    @abstractmethod
    def existing_demand(self, discipline: str, student: str, year: int) -> bool: pass

    @abstractmethod
    def delete_by_year_semester(self, year: int, semester: int) -> None: pass
