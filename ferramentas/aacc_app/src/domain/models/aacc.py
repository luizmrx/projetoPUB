from ....src.domain.interfaces.json_serializible import JsonSerializableInterface

class Aacc(JsonSerializableInterface):

    def __init__(self, id_aacc: str, aluno: str, data_envio: str,
                  status: int, atividade: str, area: str, ano_semestre: str,
                  titulo: str, inicio: str, fim: str, carga_horaria: str, doc) -> None:

        # STATUS_CHOICES = [
        #     (0, 'Aguardando'),
        #     (1, 'Enviada'),
        #     (2, 'Avaliada'),
        #     (3, 'Confirmada'),
        # ]
        self.id_aacc = id_aacc
        self.aluno = aluno
        self.data_envio = data_envio
        self.status = status
        # estrutura de dado da aacc vinda do jupiter
        self.atividade = atividade
        self.area = area
        self.ano_semestre = ano_semestre
        self.titulo = titulo
        self.inicio = inicio
        self.fim = fim
        self.carga_horaria = carga_horaria
        self.doc = doc

    def to_json(self):
        return {
            "id_aacc": self.id_aacc,
            "aluno": self.aluno,
            "doc": str(self.doc),
            "data_envio": self.data_envio,
            "status": self.status,
            "atividade": self.atividade,
            "area": self.area,
            "ano_semestre": self.ano_semestre,
            "titulo": self.titulo,
            "inicio": self.inicio,
            "fim": self.fim,
            "carga_horaria": self.carga_horaria
        }
    
    def identificador(self) -> str:
        return str(self.id_aacc)
    