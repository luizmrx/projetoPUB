from typing import Dict
from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.get_subject_demand import GetSubjectDemandInterface


class GetSubjectDemandController(ControllerInterface):

    def __init__(self, use_case: GetSubjectDemandInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        # year = int(http_request.query_params["year"])
        code = http_request.query_params["code"]
        year = int(http_request.query_params["year"])
        semester = int(http_request.query_params["semester"])

        response : Dict = self.__use_case.get_subject_demand_info(code= code, semester= semester, year= year)

        return HttpResponse (
            status_code= 200,
            body= {
                "data": response
            }
        )
    