from abc import ABC, abstractmethod
from .....src.domain.models.aacc import Aacc

class AaccRegisterInterface(ABC):

    @abstractmethod
    def register_aacc(self, aacc: Aacc) -> None: pass
