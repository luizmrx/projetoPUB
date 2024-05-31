from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.data.use_cases.get_subject_demand import GetSubjectDemand
from ...src.presentation.controllers.get_subject_demand_controller import GetSubjectDemandController

def get_subject_demand_composer():

    demand_repo = DisciplineDemandRepository()

    use_case = GetSubjectDemand(demand_repo = demand_repo)
    
    controller = GetSubjectDemandController(use_case= use_case)

    return controller
