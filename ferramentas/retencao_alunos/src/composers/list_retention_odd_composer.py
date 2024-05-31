from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.infra.db.repositories.discipline_repository import DisciplineRepository
from ...src.data.use_cases.list_retention_indexes import ListRetentionIndexes
from ...src.presentation.controllers.list_retention_odd_controller import ListRetentionOddController

def list_retention_odd_composer():

    discipline_repo = DisciplineRepository()
    demand_repo = DisciplineDemandRepository()

    use_case = ListRetentionIndexes(discipline_repo= discipline_repo,
                                    discipline_demand_repo= demand_repo)
    
    controller = ListRetentionOddController(use_case= use_case)

    return controller
