from ..interface.json_serializible import JsonSerializableInterface

class Student(JsonSerializableInterface):

    def __init__(self, num_usp: str, name: str, start_year: int) -> None:

        self.num_usp = num_usp
        self.name = name
        self.start_year = start_year
        self.pk = None

    def to_json(self) -> dict:
        return {
            "nro_usp": self.num_usp,
            "nome": self.name,
            "ano_ingresso": self.start_year
        }
    
    def identifier(self) -> str:
        return self.num_usp
    