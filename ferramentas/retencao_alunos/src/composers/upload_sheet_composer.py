from ...src.infra.db.repositories.discipline_demand_repository import DisciplineDemandRepository
from ...src.infra.db.repositories.discipline_repository import DisciplineRepository
from ...src.infra.db.repositories.student_repository import StudentRepository
from ...src.data.use_cases.upload_retention_sheet import UploadRetentionSheet
from ...src.presentation.controllers.upload_retention_sheet_controller import UploadRetentionSheetController

def upload_sheet_composer():

    discipline_repo = DisciplineRepository()
    demand_repo = DisciplineDemandRepository()
    student_repo = StudentRepository()

    use_case = UploadRetentionSheet(discipline_repo= discipline_repo,
                                    discipline_demand_repo= demand_repo,
                                    student_repo= student_repo)
    
    controller = UploadRetentionSheetController(use_case= use_case)

    return controller
