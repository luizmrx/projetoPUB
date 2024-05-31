from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.data.use_cases.list_students_subjects import ListStudentsSubjects
from ...src.presentation.controllers.list_students_subjects_controller import ListStudentsSubjectsController

def list_students_subjects_composer():

    demand_repo = DisciplineDemandRepository()

    use_case = ListStudentsSubjects(discipline_demand_repo= demand_repo)
    
    controller = ListStudentsSubjectsController(use_case= use_case)

    return controller
