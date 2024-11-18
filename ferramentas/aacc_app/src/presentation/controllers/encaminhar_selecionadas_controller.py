from ....src.presentation.http_types.http_request import HttpRequest
from ....src.presentation.http_types.http_response import HttpResponse
from ....src.presentation.interfaces.controller_interface import ControllerInterface
from ....src.domain.use_cases.user.encaminhar_aacc import EncaminharAaccInterface


class EncaminharSelecionadasAaccController(ControllerInterface):

    def __init__(self, use_case: EncaminharAaccInterface) -> None:
        self.__use_case = use_case

    def handle(self, http_request: HttpRequest) -> HttpResponse:
        
        try: 
            aaccs = http_request.query_params["id_aaccs"]
            avaliador : str = http_request.query_params["id_avaliador"]

            if aaccs:
                    print(aaccs)
                    # Handle multiple AACC ID
                    responses = []
                    for aacc in aaccs.split(","):
                        print(aacc)
                        response = self.__use_case.encaminhar_aacc(
                            aacc=aacc,
                            avaliador=avaliador
                        )
                        responses.append(response)

                    return HttpResponse(
                        status_code=200,
                        body={
                             "data": responses
                        }
                    )
        except Exception as e:
            return HttpResponse(
                status_code=500,
                body={"data": str(e)}
            )