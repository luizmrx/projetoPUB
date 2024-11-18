from typing import List
from .....src.data.interfaces.aacc_repository import AaccRepositoryInterface
from .....src.domain.models.aacc import Aacc
from .....src.domain.models.aacc_para_confirmacao import AaccParaConfirmacao
from .....models import Aacc as AACC_db
from .....models import AaccParaAvaliacao as AaccParaAvaliacao_db

class AaccRepository(AaccRepositoryInterface):

    @classmethod
    def select_aacc_by_id(cls, id_aacc: str) -> Aacc: 
        try:
            query = AACC_db.objects.filter(id_aacc=id_aacc)[0]
            response = Aacc(
                    id_aacc = query.id_aacc,
                    aluno = query.aluno,
                    doc = query.doc,
                    data_envio = query.data_envio,
                    status = query.status,
                    atividade = query.atividade,
                    area = query.area,
                    ano_semestre = query.ano_semestre,
                    titulo = query.titulo,
                    inicio = query.inicio,
                    fim = query.fim,
                    carga_horaria = query.carga_horaria
                )
            return response
        except Exception:
            raise Exception(f"Não foi possível encontrar a aacc buscada {id_aacc}!")
        
    @classmethod
    def select_aacc_by_status(cls, status: int) -> List[Aacc]:
        try:
            query = AACC_db.objects.filter(status= status)
            response : List[Aacc] = []
            for dado in query:
                aacc_registrada = Aacc(
                    id_aacc = dado.id_aacc,
                    aluno = dado.aluno,
                    doc = dado.doc,
                    data_envio = dado.data_envio,
                    status = dado.status,
                    atividade = dado.atividade,
                    area = dado.area,
                    ano_semestre = dado.ano_semestre,
                    titulo = dado.titulo,
                    inicio = dado.inicio,
                    fim = dado.fim,
                    carga_horaria = dado.carga_horaria
                )
                response.append(aacc_registrada)
            return response
        except: 
            raise Exception(f"Erro ao buscar por AACC'S com status {status}!")
        
    @classmethod
    def select_aacc_avaliadas(cls) -> List[AaccParaConfirmacao]:
        try:
            query = AACC_db.objects.filter(status=2)
            response : List[Aacc] = []
            for dado in query:
                aacc_avaliada =  AaccParaAvaliacao_db.objects.get(id_aacc=dado)
                aacc_registrada = AaccParaConfirmacao(
                    id_aacc = dado.id_aacc,
                    aluno = dado.aluno,
                    doc = dado.doc,
                    data_envio = dado.data_envio,
                    status_avaliacao= aacc_avaliada.status,
                    atividade = dado.atividade,
                    area = dado.area,
                    ano_semestre = dado.ano_semestre,
                    titulo = dado.titulo,
                    inicio = dado.inicio,
                    fim = dado.fim,
                    carga_horaria = dado.carga_horaria,
                    id_avaliador= aacc_avaliada.id_avaliador,
                    comentarios= aacc_avaliada.comentarios
                )
                response.append(aacc_registrada)
            return response
        except: 
            raise Exception("Erro ao buscar por AACC'S para confirmação!")
        
    @classmethod
    def update_status_aacc(cls, id_aacc: str, status: int) -> None:
        try: 
            query = AACC_db.objects.get(id_aacc=id_aacc)
            query.status = status
            query.save()
        except:
            raise Exception(f"Erro ao atualizar status da AACC {id_aacc}!")

    @classmethod
    def create_aacc(cls, aacc: Aacc) -> None:
        try:
            #verifica se a AAC já foi cadastrada
            aac = AACC_db.objects.filter(
                aluno = aacc.aluno,
                titulo = aacc.titulo,
                inicio = aacc.inicio,
                fim = aacc.fim
            )
            if aac: return
            new_aacc = AACC_db.objects.create(
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

            new_aacc.save()
        except Exception as e: 
            print(e)
            raise Exception("Erro ao registrar Aacc!")

    @classmethod
    def select_aac_aluno(cls, aluno: str) -> List[Aacc]:
        try:
            query = AACC_db.objects.filter(aluno= aluno)
            response : List[Aacc] = []
            for dado in query:
                aacc_registrada = Aacc(
                    id_aacc = dado.id_aacc,
                    aluno = dado.aluno,
                    doc = dado.doc,
                    data_envio = dado.data_envio,
                    status = dado.status,
                    atividade = dado.atividade,
                    area = dado.area,
                    ano_semestre = dado.ano_semestre,
                    titulo = dado.titulo,
                    inicio = dado.inicio,
                    fim = dado.fim,
                    carga_horaria = dado.carga_horaria
                )
                response.append(aacc_registrada)
            return response
        except: 
            raise Exception(f"Erro ao buscar por AACC'S  do aluno {aluno}!")