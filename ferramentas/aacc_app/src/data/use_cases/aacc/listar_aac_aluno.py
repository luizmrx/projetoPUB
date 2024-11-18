from typing import List
from .....src.domain.models.aacc import Aacc
from .....src.domain.use_cases.aacc.listar_aac_aluno import ListarAacAlunoInterface
from .....src.data.interfaces.aacc_repository import AaccRepositoryInterface

class ListarAacAluno(ListarAacAlunoInterface):

    def __init__(self, aac_repository: AaccRepositoryInterface) -> None:

        self.__aac_repository = aac_repository

    def listar_aacs_aluno(self, aluno: str) -> List[Aacc]: 

        response = self.__aac_repository.select_aac_aluno(aluno= aluno)

        return response
    