from typing import Dict
from ....src.domain.use_cases.list_retention_indexes import ListRetentionIndexesInterface
from ....src.data.interfaces.discipline_repository import DisciplineRepositoryInterface
from ....src.data.interfaces.discipline_demand_repository import DisciplineDemandRepositoryInterface

class ListRetentionIndexes(ListRetentionIndexesInterface):

    def __init__(self, discipline_repo: DisciplineRepositoryInterface,
                  discipline_demand_repo: DisciplineDemandRepositoryInterface) -> None:
        self.__discipline_repo = discipline_repo
        self.__discipline_demand_repo = discipline_demand_repo

    def list_retention_indexes_even(self, year: int, semester: int) -> Dict:
        
        response = {}
        disciplines = self.__discipline_repo.list_disciplines_by_semester(0)

        for discipline in disciplines:
            demand_info = self.__discipline_demand_repo.read_discipline_demand(
                discipline = discipline.code,
                year = year,
                semester= semester)
            
            response[f"{discipline.code} {discipline.name}"] = demand_info["students to study - late"]

        return response
    
    def list_retention_indexes_odd(self, year: int, semester: int) -> Dict:
        
        response = {}
        disciplines = self.__discipline_repo.list_disciplines_by_semester(1)

        for discipline in disciplines:
            demand_info = self.__discipline_demand_repo.read_discipline_demand(
                discipline = discipline.code,
                year = year,
                semester= semester)
            
            response[f"{discipline.code} {discipline.name}"] = demand_info["students to study - late"]

        return response