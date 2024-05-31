from typing import Dict
from ....src.domain.use_cases.list_all_disciplines import ListAllDisciplinesInterface
from ....src.data.interfaces.discipline_repository import DisciplineRepositoryInterface
from ....src.domain.models.discipline import Discipline

class ListAllDisciplines(ListAllDisciplinesInterface):

    def __init__(self, discipline_repo: DisciplineRepositoryInterface) -> None:

        self.__discipline_repo = discipline_repo

    def list_all_disciplines(self) -> Dict:
        
        disciplines = self.__discipline_repo.list_all_disciplines()
        response = {}

        for discipline in disciplines:
            response[f"{discipline.code} {discipline.name}"] = discipline.name

        return response
    