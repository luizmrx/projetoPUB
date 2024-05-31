from ....src.domain.use_cases.get_subject_demand import GetSubjectDemandInterface
from ....src.data.interfaces.discipline_demand_repository import DisciplineDemandRepositoryInterface
from ....src.data.interfaces.discipline_repository import DisciplineRepositoryInterface
from typing import Dict

class GetSubjectDemand(GetSubjectDemandInterface):

    def __init__(self, demand_repo: DisciplineDemandRepositoryInterface) -> None:

        self.__demand_repo = demand_repo

    def get_subject_demand_info(self, code: str, year: int, semester: int) -> Dict:

        return self.__demand_repo.read_discipline_demand(discipline= code, year= year, semester= semester)
