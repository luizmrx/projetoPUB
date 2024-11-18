import os
from tqdm import tqdm
from typing import Dict
from concurrent.futures import ThreadPoolExecutor, as_completed
from ....src.domain.use_cases.upload_retention_sheet import UploadRetentionSheetInterface
from ....src.data.interfaces.student_repository import StudentRepositoryInterface
from ....src.data.interfaces.discipline_demand_repository import DisciplineDemandRepositoryInterface
from ....src.data.interfaces.discipline_repository import DisciplineRepositoryInterface
from ....src.domain.models.student import Student
from ....src.domain.models.discipline_demand import DisciplineDemand
from ....utilitarios.Planilha import Planilha
from ....models import Student as Student_db
from ....models import Discipline as Discipline_db
from ....models import DisciplineDemand as DisciplineDemand_db
from ....utilitarios.calcula_semestre import semestre

class UploadRetentionSheet(UploadRetentionSheetInterface):

    def __init__(self, student_repo: StudentRepositoryInterface, 
                 discipline_demand_repo: DisciplineDemandRepositoryInterface,
                 discipline_repo: DisciplineRepositoryInterface) -> None:
        
        self.__student_repo = student_repo
        self.__discipline_demand_repo = discipline_demand_repo
        self.__discipline_repo = discipline_repo


    def upload_sheet(self, path: str, year: int, semester: int) -> Dict:
        # Finding the file
        file = os.path.abspath(f"~/ferramentas/retencao_alunos/excel_data/{path}")

        # Working with the xls file using pandas
        sheet = Planilha(file)
        disciplines = self.__discipline_repo.list_all_disciplines()

        student_objects = set()
        demand_objects = []

        for discipline in disciplines:
            try:
                data = sheet.get_arquivo_materia(discipline.code)
                print("Loading subject " + discipline.code)

                for index, line in tqdm(data.iloc[1:].iterrows(), total=len(data) - 1, unit='line'):
                    student = Student(
                        num_usp=line["Número USP"],
                        name=line["Nome do Aluno"],
                        start_year=line["Data de ingresso"],
                    )
                    # Check if the student with the same num_usp already exists
                    
                    stud = Student_db(
                        num_usp=student.num_usp,
                        name=student.name,
                        start_year=student.start_year,
                    )
                    student_objects.add(stud)

                    student_semester = semestre(stud.start_year, year)

                    late = False

                    if discipline.ideal_semester < student_semester:
                        late = True

                    demand = DisciplineDemand(
                        discipline=discipline.code,
                        student=line["Número USP"],
                        currently_studying=True if line["Cursando?"] == "Sim" else False,
                        year=year,
                        late= late,
                        semester= semester
                    )
                
                    demand_objects.append(DisciplineDemand_db(
                        discipline=Discipline_db.objects.get(code = demand.discipline),
                        student= stud,
                        currently_studying=demand.currently_studying,
                        year=demand.year,
                        late=demand.late,
                        semester = semester
                    ))
            except:
                pass

        # Batch insert students and demands
        self.__student_repo.register_batch_students(student_objects)
        self.__discipline_demand_repo.register_batch_demands(demand_objects)

        print("Data loading succeed!")
