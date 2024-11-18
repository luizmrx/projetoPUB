from typing import List
from django.contrib.auth.models import User
from .....src.data.interfaces.aacc_avaliacao_repository import AaccParaAvaliacaoRepositoryInterface
from .....src.domain.models.aacc import Aacc
from .....src.domain.models.aacc_para_avaliacao import AaccParaAvaliacao
from .....models import Aacc as AACC_db
from .....models import AaccParaAvaliacao as AaccParaAvaliacao_db

class AaccParaAvaliacaoRepository(AaccParaAvaliacaoRepositoryInterface):

    @classmethod
    def select_pendentes_avaliador(cls, id_avaliador: str) -> List[Aacc]:
        try:
            user = User.objects.get(username=id_avaliador)
            query = AaccParaAvaliacao_db.objects.filter(id_avaliador=user, status = 0)
            response : List[Aacc] = []
            for dado in query:
                aacc = AACC_db.objects.get(id_aacc= dado.id_aacc.id_aacc)
                aacc_registrada = Aacc(
                    id_aacc = aacc.id_aacc,
                    aluno = aacc.aluno,
                    doc = aacc.doc,
                    data_envio = aacc.data_envio,
                    status = aacc.status,
                    atividade = aacc.atividade,
                    area = aacc.area,
                    ano_semestre = aacc.ano_semestre,
                    titulo = aacc.titulo,
                    inicio = aacc.inicio,
                    fim = aacc.fim,
                    carga_horaria = aacc.carga_horaria
                )
                response.append(aacc_registrada)
            return response
        except:
            raise Exception(f"Erro ao procurar Aacc's para avaliação do avaliador {id_avaliador}!")

    @classmethod
    def select_aacc_para_avaliacao(cls, id_aacc: str) -> AaccParaAvaliacao:
        try:
            query = AaccParaAvaliacao_db.objects.filter(id_aacc=id_aacc)[0]
            response = AaccParaAvaliacao (
                id_aacc = id_aacc,
                id_avaliador = query.id_avaliador,
                comentarios = query.comentarios,
                status = query.status,
                carga_aprovada=query.carga_aprovada
            )
            return response
        except Exception:
            raise Exception(f"Não foi possível encontrar a aacc_para_avaliação buscada {id_aacc}!")
    
    @classmethod
    def register_aacc_para_avaliacao(cls, id_aacc: str, id_avaliador: str) -> None:
        try:
            novo_registro = AaccParaAvaliacao_db.objects.create(
                id_avaliador=User.objects.get(username=id_avaliador),
                id_aacc=AACC_db.objects.get(id_aacc= id_aacc)
            )
            novo_registro.save()
        except:
            raise Exception(f"Erro ao registrar Aacc {id_aacc} "
                            f"para avaliação do avaliador {id_avaliador}!")
        
    @classmethod
    def register_avaliacao(cls, id_aacc: str, comentarios: str, status: int, carga_aprovada: str) -> None:
        try:
            query = AACC_db.objects.get(id_aacc= id_aacc)
    
            aacc_para_avaliacao = AaccParaAvaliacao_db.objects.get(id_aacc=query)
            aacc_para_avaliacao.status = status
            aacc_para_avaliacao.comentarios = comentarios
            aacc_para_avaliacao.carga_aprovada = carga_aprovada
            aacc_para_avaliacao.save()
        except:
            raise Exception(f"Erro ao registra avaliação da AACC {id_aacc}!")
        