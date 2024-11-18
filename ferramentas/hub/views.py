from django.shortcuts import render, redirect
from django.contrib.auth import login as login_django
from django.contrib.auth import logout as logout_django
from django.contrib.auth.decorators import login_required
from .decorators import *

from .src.data.use_cases.user.cadastrar_user import CadastrarUser
from .src.data.use_cases.user.autenticar_user import AutenticarUser

from .src.infra.db.repositories.user_repository import UserRepository

from .src.presentation.controllers.cadastrar_user_controller import CadastrarUserController
from .src.presentation.controllers.autenticar_user_controller import AutenticarUserController


#adapters
from .src.presentation.adapters.request_adapter import request_adapter


def index(request):
    return redirect("hub:login")


@login_required(login_url="/login")
def hub_page(request):
    return render(request, 'hub_page.html')

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
                    return redirect("hub:hub_page")
                
            return redirect("hub:hub_page")
        
        return HttpResponse("Login inválido")
    
def logout(request):
    logout_django(request)
    return redirect('hub:login')

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