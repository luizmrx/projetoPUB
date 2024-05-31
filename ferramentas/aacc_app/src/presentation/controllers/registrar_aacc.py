from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.aacc.register_aacc import AaccRegisterInterface
from ....src.domain.models.aacc import Aacc

class RegistrarAaccController(ControllerInterface):

    def __init__(self, use_case: AaccRegisterInterface):

        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        
        aacc = Aacc(
            id_aacc=0,
            aluno = http_request.query_params["aluno"],
            data_envio=http_request.query_params["data_envio"],
            status=http_request.query_params["status"],
            doc= http_request.query_params["doc"],
            atividade = http_request.query_params["atividade"],
            area= http_request.query_params["area"],
            ano_semestre= http_request.query_params["ano_semestre"],
            titulo= http_request.query_params["titulo"],
            inicio = http_request.query_params["inicio"],
            fim= http_request.query_params["fim"],
            carga_horaria= http_request.query_params["carga_horaria"]
        )

        response = self.__use_case.register_aacc(
            aacc= aacc
        )

        return HttpResponse (
            status_code= 200,
            body= {
                "data": response
            }
        )
    