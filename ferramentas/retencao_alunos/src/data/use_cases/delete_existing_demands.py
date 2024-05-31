from ....src.domain.use_cases.delete_existing_demands import DeleteExistingDemandsInterface
from ....src.data.interfaces.discipline_demand_repository import DisciplineDemandRepositoryInterface

class DeleteExistingDemands(DeleteExistingDemandsInterface):

    def __init__(self, demands_repo: DisciplineDemandRepositoryInterface) -> None:
        
        self.__demands_repo = demands_repo

    def delete_all_by_year_semester(self, year: int, semester: int) -> None:
        
        self.__demands_repo.delete_by_year_semester(year= year, semester= semester)
        