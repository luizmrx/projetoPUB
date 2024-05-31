from ..interface.json_serializible import JsonSerializableInterface

class Discipline(JsonSerializableInterface):

    def __init__(self, code: str, name: str, ideal_semester: int) -> None:

        self.code = code
        self.name = name
        self.ideal_semester = ideal_semester

    def to_json(self) -> dict:
        return {
            "codigo": self.code,
            "nome": self.name,
            "semestre_ideal": self.ideal_semester
        }
    
    def identifier(self) -> str:
        return self.code
    