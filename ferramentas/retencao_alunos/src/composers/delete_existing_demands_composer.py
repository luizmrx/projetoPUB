from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.data.use_cases.delete_existing_demands import DeleteExistingDemands

def delete_existing_demands_composer(year: int, semester: int):

    demand_repo = DisciplineDemandRepository()  

    use_case = DeleteExistingDemands(demands_repo= demand_repo)

    use_case.delete_all_by_year_semester(year= year, semester= semester)
