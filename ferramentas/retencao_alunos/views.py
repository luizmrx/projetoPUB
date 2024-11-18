from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
# from .utilitarios.Planilha import Planilha
# from .utilitarios.Upload_DB import Upload
# from .utilitarios.calcula_semestre import semestre
import os
from django.core.files.storage import FileSystemStorage
# from .models import Aluno, Disciplina, Demanda_por_disciplina
# from .Rotinas.Rotinas import Rotinas
# from tqdm import tqdm
# import json
from .utilitarios.Gera_pdf import Gera_pdf
# from channels.layers import get_channel_layer
# from asgiref.sync import async_to_sync

from .src.composers.upload_sheet_composer import upload_sheet_composer
from .src.composers.list_retention_even_composer import list_retention_even_composer
from .src.composers.list_retention_odd_composer import list_retention_odd_composer
from .src.composers.list_students_subjects_composer import list_students_subjects_composer
from .src.composers.delete_existing_demands_composer import delete_existing_demands_composer
from .src.composers.get_subject_demand_composer import get_subject_demand_composer
from .src.composers.list_all_disciplines_composer import list_all_disciplines_composer

from .src.presentation.adapters.request_adapter import request_adapter

def home(request):

    http_request = request_adapter(request, list_all_disciplines_composer())

    disciplines = http_request.body["data"]
    
    context = {
        "disciplines": disciplines
    }

    return render(request, 'home.html', context)

def firststeps(request):
    #upload_planilha(request)
    return render(request, 'firststeps.html')

def carregar_planilha(request): 
    return render(request, 'carregarplanilha.html') 

def retorna_info_materia(request):
    
    http_request = request_adapter(request, get_subject_demand_composer())

    return JsonResponse(http_request.body["data"])
    
    
def lista_materias_atrasados_impar(request):

    http_request = request_adapter(request, list_retention_odd_composer())

    return JsonResponse(http_request.body["data"])



def lista_materias_atrasados_par(request):
    
    http_request = request_adapter(request, list_retention_even_composer())


    return JsonResponse(http_request.body["data"])

def upload_planilha(request):

    if request.method == 'POST' and request.FILES.get('file'):

        year = request.POST['year']
        semester = request.POST['semester']


        uploaded_file = request.FILES['file']
        
        # Specify the directory where you want to save the file
        upload_dir = '~/ferramentas/retencao_alunos/excel_data'
        
        # Initialize FileSystemStorage with the desired directory
        fs = FileSystemStorage(location=upload_dir)

        # Check if the file already exists
        if fs.exists(f"database_{year}_{semester}semester.xls"):
            # If the file exists, delete it
            os.remove(os.path.join(upload_dir, f"database_{year}_{semester}semester.xls"))

            delete_existing_demands_composer(year= int(year), semester= int(semester))

        
        # Save the uploaded file directly to the specified directory
        fs.save(f"database_{year}_{semester}semester.xls", uploaded_file)
    
        request_adapter(request, upload_sheet_composer())

        return JsonResponse({"data": "Ok"})
    
       



def generate_pdf(request):
    
    semestre = request.GET.get("semester_name")
    year = request.GET.get("year")

    if semestre == "1":
        data = request_adapter(request, list_retention_odd_composer()).body["data"]
        semestre_name = "Ímpar"

    else:
        data = request_adapter(request, list_retention_even_composer()).body["data"]
        semestre_name = "Par"
    
    data = dict(sorted(data.items(), key=lambda item: item[1], reverse=True))
   
    gerador_pdf = Gera_pdf(data, f"Alunos atrasados por disciplina - Semestre {semestre_name} de {year}")
    gerador_pdf.gera_pdf()
    
    with open("relatorio.pdf", "rb") as pdf_file:
        response = HttpResponse(pdf_file.read(), content_type="application/pdf")

    # Define o nome do arquivo para download
    response['Content-Disposition'] = 'attachment; filename=relatorio.pdf'

    return response

def listar_alunos_atrasados(request):

    http_request = request_adapter(request, list_students_subjects_composer())

    return JsonResponse(http_request.body["data"])
