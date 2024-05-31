from abc import ABC, abstractmethod
from typing import Dict

class GetSubjectDemandInterface(ABC):

    @abstractmethod
    def get_subject_demand_info(self, code: str, year: int, semester: int) -> Dict: pass
