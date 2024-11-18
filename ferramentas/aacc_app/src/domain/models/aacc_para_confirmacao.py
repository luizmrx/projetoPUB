from ....src.domain.interfaces.json_serializible import JsonSerializableInterface

class AaccParaConfirmacao(JsonSerializableInterface):

    def __init__(self, id_aacc: str, aluno: str, doc, data_envio: str, 
                 id_avaliador: str,atividade: str, area:str,
                  ano_semestre: str, titulo: str,
                   inicio: str, fim: str, 
                    carga_horaria: str, status_avaliacao: int, comentarios: str) -> None:

        # STATUS_CHOICES = [
        #     (0, 'Aguardando'),
        #     (1, 'Deferida'),
        #     (2, 'Indeferida')
        # ]

        self.id_avaliador = id_avaliador
        self.id_aacc = id_aacc
        self.doc = doc
        self.aluno = aluno
        self.data_envio = data_envio
        self.status_avaliacao = status_avaliacao
        self.comentarios = comentarios
        self.atividade = atividade
        self.area = area
        self.ano_semestre = ano_semestre
        self.titulo = titulo
        self.inicio = inicio
        self.fim = fim
        self.carga_horaria = carga_horaria

    def to_json(self):
        return {
            "aluno": self.aluno,
            "data_envio": self.data_envio,
            "doc": str(self.doc),
            "avaliacao": self.status_avaliacao,
            "comentarios": self.comentarios,
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
    