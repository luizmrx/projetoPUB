from typing import Dict
from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.list_retention_indexes import ListRetentionIndexesInterface


class ListRetentionOddController(ControllerInterface):

    def __init__(self, use_case: ListRetentionIndexesInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:

        year = int(http_request.query_params["year"])
        semester = int(http_request.query_params["semester"])
        
        response : Dict = self.__use_case.list_retention_indexes_odd(year= year,semester= semester)

        return HttpResponse (
            status_code= 200,
            body= {
                "data": response
            }
        )
    
    