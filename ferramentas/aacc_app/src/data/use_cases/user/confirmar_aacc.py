from .....src.data.interfaces.aacc_repository import AaccRepositoryInterface
from .....src.data.interfaces.aacc_avaliacao_repository import AaccParaAvaliacaoRepositoryInterface
from .....src.domain.use_cases.user.confirmar_aacc import ConfirmarAaccInterface

class ConfirmarAacc(ConfirmarAaccInterface):

    def __init__(self, aacc_repository: AaccRepositoryInterface, aacc_avaliacao_repo: AaccParaAvaliacaoRepositoryInterface) -> None:
        
        self.__aacc_repository = aacc_repository
        self.__aacc_avaliacao_repo = aacc_avaliacao_repo

    def confirmar_aacc(self, aacc: str):
        
        self.__aacc_repository.update_status_aacc(
            id_aacc=aacc, status=3)
        

        aac = self.__aacc_repository.select_aacc_by_id(id_aacc=aacc)
        aac_avaliacao = self.__aacc_avaliacao_repo.select_aacc_para_avaliacao(id_aacc=aacc)

        return aac, aac_avaliacao
    