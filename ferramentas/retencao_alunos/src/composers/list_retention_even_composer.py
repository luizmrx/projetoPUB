from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.infra.db.repositories.discipline_repository import DisciplineRepository
from ...src.data.use_cases.list_retention_indexes import ListRetentionIndexes
from ...src.presentation.controllers.list_retention_even_controller import ListRetentionEvenController

def list_retention_even_composer():

    discipline_repo = DisciplineRepository()
    demand_repo = DisciplineDemandRepository()

    use_case = ListRetentionIndexes(discipline_repo= discipline_repo,
                                    discipline_demand_repo= demand_repo)
    
    controller = ListRetentionEvenController(use_case= use_case)

    return controller
