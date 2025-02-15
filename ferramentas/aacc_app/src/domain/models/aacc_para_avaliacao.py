from ....src.domain.interfaces.json_serializible import JsonSerializableInterface

class AaccParaAvaliacao(JsonSerializableInterface):

    def __init__(self, id_avaliador: str, id_aacc: str, status: int, comentarios: str, carga_aprovada: str) -> None:

        # STATUS_CHOICES = [
        #     (0, 'Aguardando'),
        #     (1, 'Deferida'),
        #     (2, 'Indeferida')
        # ]

        self.id_avaliador = id_avaliador
        self.id_aacc = id_aacc
        self.status = status
        self.comentarios = comentarios
        self.carga_aprovada = carga_aprovada

    def to_json(self):
        return {
            "id_avaliador": self.id_avaliador,
            "id_aacc": self.id_aacc,
            "comentarios": self.comentarios,
            "status": self.status,
            "carga_aprovada": self.carga_aprovada
        }
    
    def identificador(self) -> str:
        return str(self.id_aacc)
    