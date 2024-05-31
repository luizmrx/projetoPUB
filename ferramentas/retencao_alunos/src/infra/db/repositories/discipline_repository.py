from .....src.data.interfaces.discipline_repository import DisciplineRepositoryInterface
from .....src.domain.models.discipline import Discipline
from typing import List
from .....models import Discipline as Discipline_db

class Discipline_Registering_Exception(Exception):
    def __init__(self, message="Discipline could not be registered!"):
        self.message = message
        super().__init__(self.message)

class DisciplineRepository(DisciplineRepositoryInterface):

    @classmethod
    def register_discipline(cls, discipline: Discipline) -> None:

        #check if the discipline is already registered
        exists = Discipline_db.objects.filter(nro_usp=discipline.nro_usp)
        if not exists:
            new_discipline = Discipline_db.objects.create(
                code= discipline.code,
                name= discipline.name,
                ideal_semester = discipline.ideal_semester
            )
            try:
                new_discipline.save()
            except Discipline_Registering_Exception as e:
                print(f"Exception: {e}")

    @classmethod
    def list_disciplines_by_semester(self, semester: int) -> List[Discipline]:

        #semester = 1 -> odd semesters
        #semester = 0 -> even semesters
        all_disciplines = Discipline_db.objects.all()
        resp = []
        for discipline in all_disciplines:
            if discipline.ideal_semester % 2 == semester:
                register = Discipline(
                    code = discipline.code,
                    name = discipline.name,
                    ideal_semester = discipline.ideal_semester
                )
                resp.append(register)
        
        return resp
    
    @classmethod
    def list_all_disciplines(cls) -> List[Discipline]:

        all_disciplines = Discipline_db.objects.all()
        resp = []
        for discipline in all_disciplines:
            register = Discipline(
                code = discipline.code,
                name = discipline.name,
                ideal_semester = discipline.ideal_semester
            )
            resp.append(register)
        
        return resp


    
            