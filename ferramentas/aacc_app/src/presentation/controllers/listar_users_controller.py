from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.user.listar_users import ListarUsersInterface

class ListarUsersController(ControllerInterface):

    def __init__(self, use_case: ListarUsersInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        response = self.__use_case.listar_users()

        return HttpResponse (
            status_code= 200,
            body= {
                "data": response
            }
        )
    