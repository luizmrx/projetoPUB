from ...src.infra.db.repositories.discipline_repository import DisciplineRepository
from ...src.data.use_cases.list_all_disciplines import ListAllDisciplines
from ...src.presentation.controllers.list_all_disciplines_controller import ListAllDisciplinesController

def list_all_disciplines_composer():

    discipline_repo = DisciplineRepository()

    use_case = ListAllDisciplines(discipline_repo= discipline_repo)
    
    controller = ListAllDisciplinesController(use_case= use_case)

    return controller
