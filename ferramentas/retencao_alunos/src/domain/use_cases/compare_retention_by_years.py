from abc import ABC, abstractmethod
from typing import Dict

class CompareRetentionByYearInterface(ABC):

    @abstractmethod
    def compare_retention_by_years(self, discipline: str) -> Dict: pass
