from typing import List
from abc import ABC, abstractmethod
from ....src.domain.models.aacc import Aacc

class AaccRepositoryInterface(ABC):

    @abstractmethod
    def select_aacc_by_id(self, id_aacc: str) -> Aacc: pass

    @abstractmethod
    def select_aacc_by_status(self, status: int) -> List[Aacc]: pass

    @abstractmethod
    def select_aacc_avaliadas(self) -> List[Aacc]: pass

    @abstractmethod
    def update_status_aacc(self, id_aacc: str, status: int) -> None: pass

    @abstractmethod
    def create_aacc(self, aacc: Aacc) -> None: pass

    @abstractmethod
    def select_aac_aluno(self, aluno: str) -> None: pass
