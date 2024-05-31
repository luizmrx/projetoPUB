from django.urls import path
from . import views
app_name = 'retencao_alunos'
urlpatterns = [
    #urls para as páginas ---
    path('', views.firststeps, name="firststeps"),
    path('home.html', views.home, name="home"),
    path('carregarplanilha.html', views.carregar_planilha, name="carregar_planilha"),
    #-------
    path('upload_planilha', views.upload_planilha, name="upload_planilha"),
    path('retorna_info_materia/', views.retorna_info_materia, name="retorna_info_materia"),
    path('lista_materias_atrasados_par/', views.lista_materias_atrasados_par, name="lista_materias_atrasados_par"),
    path('lista_materias_atrasados_impar/', views.lista_materias_atrasados_impar, name="lista_materias_atrasados_impar"),
    path('generate_pdf/', views.generate_pdf, name="generate_pdf"),
    path('listar_alunos_atrasados', views.listar_alunos_atrasados, name="listar_alunos_atrasados"),
]