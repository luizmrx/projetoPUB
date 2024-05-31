from abc import ABC, abstractmethod
from typing import List
from .....src.domain.models.user import User

class ListarUsersInterface(ABC):

    @abstractmethod
    def listar_users(self) -> List[User]: pass
    