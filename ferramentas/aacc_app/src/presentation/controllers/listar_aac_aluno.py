from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.aacc.listar_aac_aluno import ListarAacAlunoInterface

class ListarAacAlunoController(ControllerInterface):

    def __init__(self, use_case: ListarAacAlunoInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        aluno : str = http_request.query_params["aluno"]
        response = self.__use_case.listar_aacs_aluno(aluno = aluno)

        return HttpResponse (
            status_code= 200,
            body= {
                "data": response
            }
        )
    