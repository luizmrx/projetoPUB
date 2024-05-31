from .....src.domain.models.aacc import Aacc
from .....src.data.interfaces.aacc_repository import AaccRepositoryInterface
from .....src.domain.use_cases.aacc.register_aacc import AaccRegisterInterface

class AaccRegister(AaccRegisterInterface):

    def __init__(self, aacc_repository: AaccRepositoryInterface):

        self.__aacc_repository = aacc_repository

    def register_aacc(self, aacc: Aacc) -> None:
        
        return self.__aacc_repository.create_aacc(aacc= aacc)
