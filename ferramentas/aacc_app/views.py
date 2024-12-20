import os
import json
import threading
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from .decorators import *
#use_cases
from .src.data.use_cases.aacc.list_pendentes import AaccListaPendentes
from .src.data.use_cases.user.encaminhar_aacc import EncaminharAacc
from .src.data.use_cases.user.avaliar_aacc import AvaliarAacc
from .src.data.use_cases.user.confirmar_aacc import ConfirmarAacc
from .src.data.use_cases.user.cadastrar_user import CadastrarUser
from .src.data.use_cases.user.autenticar_user import AutenticarUser
from .src.data.use_cases.user.listar_users import ListarUsers
from .src.data.use_cases.aacc.listar_aac_aluno import ListarAacAluno
#repositórios
from .src.infra.db.repositories.aacc_avaliacao_repository import AaccParaAvaliacaoRepository
from .src.infra.db.repositories.aacc_repository import AaccRepository
from .src.infra.db.repositories.user_repository import UserRepository
#controllers
from .src.presentation.controllers.nao_encaminhadas_controller import NaoEncaminhadasController
from .src.presentation.controllers.nao_avaliadas_controller import NaoAvaliadasController
from .src.presentation.controllers.nao_confirmadas_controller import NaoConfirmadasController
from .src.presentation.controllers.encaminhar_aacc_controller import EncaminharAaccController
from .src.presentation.controllers.avaliar_aacc_controller import AvaliarAaccController
from .src.presentation.controllers.confirmar_aacc_controller import ConfirmarAaccController
from .src.presentation.controllers.cadastrar_user_controller import CadastrarUserController
from .src.presentation.controllers.autenticar_user_controller import AutenticarUserController
from .src.presentation.controllers.listar_users_controller import ListarUsersController
from .src.presentation.controllers.listar_aac_aluno import ListarAacAlunoController
from .src.presentation.controllers.encaminhar_selecionadas_controller import EncaminharSelecionadasAaccController
#adapters
from .src.presentation.adapters.request_adapter import request_adapter
#presenters
from .src.presentation.presenters.json_response import json_response
#scrapper
from .scrapper import scrapper
from .scrapper_retorno import scrapper_retorno
#email
from .email import send_activity_assignment_email

# Create your views here.
def index(request):
    return redirect("aacc_app:login")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def home_page(request):
    return render(request, 'home_aac.html')

@login_required(login_url="/login")
def avaliar_page(request):
    return render(request, "avaliacao.html")

@login_required(login_url="/login")
def historico_page(request):

    if request.method == "GET":

        aluno_context = request.GET["aluno"]

        context = {
            "aluno_context": aluno_context
        }

        return render(request, "historico.html", context)

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def encaminhamentos_page(request):
    return render(request, 'encaminhamentos.html')

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def confirmar_page(request):
    return render(request, "confirmar.html")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def scrapping(request):
    if request.method == 'GET':
        scrapper()
        return render(request, "encaminhamentos.html")
    else:
        return HttpResponse("error: Invalid request method")
    
@unauthenticated_user 
def login(request):

    if request.method == 'GET': return render(request, "login.html")
    
    if request.method == 'POST':

        user_repository = UserRepository()
        use_case = AutenticarUser(user_repository= user_repository)
        controller = AutenticarUserController(use_case= use_case)
        http_response = request_adapter(request=request, controller= controller)

        response = http_response.body["data"]

        if response:
            login_django(request, response)
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
                if group == "coordenador":
                    return redirect("aacc_app:home")
                
            return redirect("aacc_app:avaliar_page")
        
        return HttpResponse("Login inválido")
        
    
    return HttpResponse("error: Invalid request method")

def logout(request):
    logout_django(request)
    return redirect('aacc_app:login')

@unauthenticated_user
def cadastro(request):

    if request.method == 'GET': return render(request, "cadastro.html")
    
    if request.method == 'POST':

        user_repository = UserRepository()
        use_case = CadastrarUser(user_repository= user_repository)
        controller = CadastrarUserController(use_case= use_case)
        request_adapter(request=request, controller= controller)


        return HttpResponse("Usuário cadastrado com sucesso!")
    
    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def encaminhar(request):

    if request.method == 'POST':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = EncaminharAacc(aacc_repository= aacc_repository,
                                aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = EncaminharAaccController(use_case = use_case)

        http_response = request_adapter(request=request, controller= controller)

        response = http_response.body["data"]

        send_activity_assignment_email("lucastferracin@gmail.com", "primeiro teste")

        return HttpResponse(response)
    
    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def encaminhar_selecionadas(request):

    if request.method == 'POST':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = EncaminharAacc(aacc_repository= aacc_repository,
                                aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = EncaminharSelecionadasAaccController(use_case = use_case)

        http_response = request_adapter(request=request, controller= controller)

        response = http_response.body["data"]

        return HttpResponse(response)
    
    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
def avaliar(request):

    if request.method == 'POST':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = AvaliarAacc(aacc_repository= aacc_repository,
                                aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = AvaliarAaccController(use_case = use_case)

        http_response = request_adapter(request=request, controller= controller)

        response = http_response.body["data"]

        return HttpResponse(response)
    
    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def confirmar(request):

    if request.method == 'POST':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()

        use_case = ConfirmarAacc(aacc_repository= aacc_repository, 
                                 aacc_avaliacao_repo=aacc_avaliacao_repository)
        controller = ConfirmarAaccController(use_case = use_case)

        http_response = request_adapter(request=request, controller= controller)

        aac, acc_avaliacao = http_response.body["data"]

        #ordenar scraping de retorno ao jupiter
        if http_response.status_code == 200:

            scrapper_retorno(aac=aac, aac_avaliação=acc_avaliacao)

        return HttpResponse("success!")
    
    return HttpResponse("error: Invalid request method")

@allowed_users(["coordenador"])
def nao_encaminhadas(request):

    if request.method == 'GET':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = AaccListaPendentes(aacc_repository= aacc_repository,
                                    aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = NaoEncaminhadasController(use_case = use_case)

        http_response = request_adapter(request=request, controller= controller)

        response = json_response(http_response.body["data"])

        return JsonResponse(json.dumps(response, cls=DjangoJSONEncoder), safe=False)

    
    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
def nao_avaliadas(request):

    if request.method == 'GET':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = AaccListaPendentes(aacc_repository= aacc_repository,
                                    aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = NaoAvaliadasController(use_case= use_case)

        http_response = request_adapter(request= request, controller= controller)

        response = json_response(http_response.body["data"])

        return JsonResponse(json.dumps(response, cls=DjangoJSONEncoder), safe=False)

    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def nao_confirmadas(request):

    if request.method == 'GET':

        aacc_repository = AaccRepository()
        aacc_avaliacao_repository = AaccParaAvaliacaoRepository()
        use_case = AaccListaPendentes(aacc_repository= aacc_repository,
                                    aacc_avaliacao_repository= aacc_avaliacao_repository)
        controller = NaoConfirmadasController(use_case= use_case)

        http_response = request_adapter(request= request, controller= controller)

        response = json_response(http_response.body["data"])

        return JsonResponse(json.dumps(response, cls=DjangoJSONEncoder), safe=False)

    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
@allowed_users(["coordenador"])
def listar_users(request):

    if request.method == 'GET':

        user_repository = UserRepository()

        use_case = ListarUsers(user_repository= user_repository)
        controller = ListarUsersController(use_case= use_case)

        http_response = request_adapter(request= request, controller= controller)

        response = json_response(http_response.body["data"])

        return JsonResponse(json.dumps(response, cls=DjangoJSONEncoder), safe=False)

    return HttpResponse("error: Invalid request method")

@login_required(login_url="/login")
def listar_aac_aluno(request):

    if request.method == 'GET':

        aac_repository = AaccRepository()

        use_case = ListarAacAluno(aac_repository= aac_repository)
        controller = ListarAacAlunoController(use_case= use_case)

        http_response = request_adapter(request= request, controller= controller)

        response = json_response(http_response.body["data"])

        return JsonResponse(json.dumps(response, cls=DjangoJSONEncoder), safe=False)

    return HttpResponse("error: Invalid request method")




#utilitarios
@login_required(login_url="/login")
def visualizar_documento(request, nome_arquivo):
    caminho_documento = os.path.join(
        "/home/lucas/Desktop/projetos/IC/hub_ferramentas_si/hub_ferramentas_SI/ferramentas/aacc_app/comprovantes_aac/", nome_arquivo)
    with open(caminho_documento, 'rb') as documento:
        response = HttpResponse(documento.read(), content_type='application/pdf')
        response['Content-Disposition'] = f'inline; filename={nome_arquivo}'
        return response
    