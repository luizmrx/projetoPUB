from abc import ABC, abstractmethod

class DeleteExistingDemandsInterface(ABC):

    @abstractmethod
    def delete_all_by_year_semester(self, year: int, semester: int) -> None: pass
