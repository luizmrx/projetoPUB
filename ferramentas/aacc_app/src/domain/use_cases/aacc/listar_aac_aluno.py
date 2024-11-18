from abc import ABC, abstractmethod
from typing import List
from .....src.domain.models.aacc import Aacc

class ListarAacAlunoInterface(ABC):

    @abstractmethod
    def listar_aacs_aluno(self, aluno: str) -> List[Aacc]: pass
