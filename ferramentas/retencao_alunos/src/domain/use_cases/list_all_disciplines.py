from abc import ABC, abstractmethod
from typing import Dict

class ListAllDisciplinesInterface(ABC):

    @abstractmethod
    def list_all_disciplines(self) -> Dict: pass
