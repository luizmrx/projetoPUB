from typing import List
from .....src.domain.use_cases.user.listar_users import ListarUsersInterface
from .....src.domain.models.user import User
from .....src.data.interfaces.user_repository import UserRepositoryInterface

class ListarUsers(ListarUsersInterface):

    def __init__(self, user_repository = UserRepositoryInterface):

        self.__user_repository = user_repository

    def listar_users(self) -> List[User]:
        
        response = self.__user_repository.select_all_usernames()

        return response
    