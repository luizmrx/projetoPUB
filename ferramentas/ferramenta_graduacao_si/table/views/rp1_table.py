import json

import openpyxl
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseBadRequest, JsonResponse
from django.shortcuts import render
from ..models import *
from django.shortcuts import redirect

import unicodedata

from .planilha_distribuicao import *
from .planilha_docentes import *
from .salvar_modificacoes import *
from .preferencias_upload import *


@login_required
def load_rp1(request):
    if request.method != "POST":
        return render(request, "table/rp1Table.html")

    excel_file = request.FILES.get("excel_file", None)

    if not excel_file:
        return redirect("ferramenta_graduacao_si:page_rp1")

    if not excel_file.name.endswith(".xlsx"):
        return redirect("ferramenta_graduacao_si:page_rp1")

    workbook = openpyxl.load_workbook(excel_file)
    worksheet = workbook.active

    RP1Turma.objects.filter(ano=AnoAberto.objects.get(id=1).Ano).delete()
    turmas_erro = ""

    dias_validos = ("seg", "ter", "qua", "qui", "sex")
    hrs_validos = ("08h - 12h", "14h - 18h", "19h - 22h45")

    for row in worksheet.iter_rows(min_row=3, max_col=5, values_only=True):

        dia_semana = row[2][0:3].strip()
        horario = row[2][4:].strip().lower()

        if dia_semana.lower() in dias_validos and horario in hrs_validos:
            try:
                new_rp1 = RP1Turma.objects.create(
                    codigo=row[1],
                    profs_adicionais=row[4],
                    cursos=row[3],
                    ano=AnoAberto.objects.get(id=1).Ano
                )
                DiaAulaRP1(turma_rp1=new_rp1, dia_semana=dia_semana, horario=horario).save()

            except Exception as e:
                print(e)
                return redirect("ferramenta_graduacao_si:page_rp1")
        else:
            turmas_erro += f"{row[1]}, "

    return redirect("ferramenta_graduacao_si:page_rp1", [turmas_erro])


@login_required
def page_rp1(request, text=""):

    rp1_turmas = RP1Turma.objects.filter(ano=AnoAberto.objects.get(id=1).Ano)
    profs_objs = RP1TurmaPreview.objects.filter(codigo=99).first().professor_si.all()
    rest_turno = {"manha": 0, "tarde": 22, "noite": 48}
    dia_sem = {"segunda": 0, "terca": 2, "quarta": 4, "quinta": 6, "sexta": 8}
    auto_profs = {}
    restricoes_profs = {}
    impedimentos_totais = {}
    detalhes_profs = {}
    for prof_obj in profs_objs:
        auto_profs[prof_obj.NomeProf] = prof_obj.Apelido
        restricoes = prof_obj.restricao_set.filter(semestre="1")

        nome = remover_acentos(prof_obj.NomeProf.lower())
        detalhes_profs[nome] = [prof_obj.NomeProf, prof_obj.Apelido, prof_obj.pos_doc, prof_obj.pref_optativas,
                                prof_obj.consideracao1, prof_obj.consideracao2]

        restricoes_profs[str(prof_obj.Apelido)] = []
        impedimentos_totais[str(prof_obj.Apelido)] = []

        for rest_prof in restricoes:
            list_rest_indice = []
            indice = dia_sem[rest_prof.dia] + rest_turno[rest_prof.periodo]
            if rest_prof.periodo == "tarde" and rest_prof.dia == "segunda":
                list_rest_indice = [indice, 23, 33, 34, 35, 36]
            elif rest_prof.periodo == "tarde":
                list_rest_indice = [indice, indice + 1, indice + 13, indice + 14]
            elif rest_prof.periodo == "noite":
                indice = indice - 2
                list_rest_indice = [
                    indice,
                    indice + 1,
                    indice + 11,
                    indice + 12,
                    indice + 22,
                    indice + 23,
                    indice + 33,
                    indice + 34,
                ]
            else:
                list_rest_indice = [indice, indice + 1, indice + 11, indice + 12]

            if str(prof_obj.Apelido) in restricoes_profs:
                restricoes_profs[str(prof_obj.Apelido)] += list_rest_indice
            else:
                restricoes_profs[str(prof_obj.Apelido)] = list_rest_indice

            # impedimento total
            if rest_prof.impedimento:
                impedimentos_totais[str(prof_obj.Apelido)] = list_rest_indice

    text = text.replace("[", "").replace("]", "").replace("'", "")
    
    profs_verificados = []
    for prof in profs_objs:
        profs_verificados.append(prof)
    
    for turma in rp1_turmas:
        professores = turma.professor_si.all()
        for professor in professores:
            if professor not in profs_verificados:
                turma.professor_si.remove(professor)

    print(restricoes_profs)
    ano_aberto = AnoAberto.objects.get(id=1).Ano
    context = {
        "rp1": rp1_turmas,
        "auto_profs": gera_sugestoes_rp1(ano_aberto),
        "total_profs": profs_rp1(ano_aberto),
        "text_erro": text,
        "anoAberto": ano_aberto,
        "impedimentos_totais": impedimentos_totais,
        "rest_horarios": restricoes_profs,
        "detalhes_profs": detalhes_profs,
    }
    return render(request, "table/rp1Table.html", context)
 
def remover_acentos(texto):
    # Normaliza o texto para decompor caracteres acentuados
    nfkd = unicodedata.normalize('NFD', texto)
    # Remove os caracteres diacríticos (acentos)
    return ''.join([c for c in nfkd if unicodedata.category(c) != 'Mn'])

def prof_na_restricao(tur, restricoes):
    impedimento = False
    nao_gostaria = False

    dia_aula_rp1 = DiaAulaRP1.objects.get(turma_rp1=tur)

    # dicionário de correspondencia dos dias da semana
    corresp_dias_semana_restricao = {
        "Seg": "segunda",
        "Ter": "terca",
        "Qua": "quarta",
        "Qui": "quinta",
        "Sex": "sexta"
    }
    # dicionário de correspondencia de horário para período
    corresp_horarios_restricao = {
        "08h - 12h": "manha",
        "14h - 18h": "tarde",
        "19h - 22h45": "noite"
    }

    for restricao in restricoes:
        if (restricao.dia == corresp_dias_semana_restricao[dia_aula_rp1.dia_semana] and restricao.periodo == corresp_horarios_restricao[dia_aula_rp1.horario]):

            if restricao.impedimento:
                impedimento = True

            nao_gostaria = True


    return {
        'impedimento': impedimento,
        'prof_nao_gosta_hr': nao_gostaria
    }

@login_required
def salvar_profs_rp1(request):
    is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
    if not is_ajax:
        return HttpResponseBadRequest('Invalid request')
    if request.method != 'POST':
        return JsonResponse({'status': 'Invalid request'}, status=400)

    data = json.load(request)
    erros = {}
    alertas = {}
    ano = AnoAberto.objects.get(id=1).Ano
    tur = RP1Turma.objects.get(id=data["id"])
    tur.professor_si.clear()

    print("Verificando lista")
    print(data["lProfs"])

    if data["lProfs"] == ['', '', '']:
        return JsonResponse({'status': 'String vazia', 'sugestoes': gera_sugestoes_rp1(ano)})

    for prof in data["lProfs"]:
        erro_caso = {}
        alerta_caso = {}
        if not prof:
            continue

        # devemos adaptaros horarios e dias para serem compatíveis com as restrições
        # dicionário de correspondencia dos dias da semana
        corresp_dias_semana = {
            "Seg": 0,
            "Ter": 2,
            "Qua": 4,
            "Qui": 6,
            "Sex": 8
        }

        # dicionário de correspondencia de horário
        corresp_horarios = {
            "08h - 12h": [0,1],
            "14h - 18h": [2,4],
            "19h - 22h45": [5,7]
        }

        dia_aula_rp1 = DiaAulaRP1.objects.get(turma_rp1 = tur)
        prof_bd = Professor.objects.get(NomeProf=prof)

        print(corresp_horarios[dia_aula_rp1.horario])

        for horario in corresp_horarios[dia_aula_rp1.horario]:
            print(horario)
            data = {
                "info": {
                    'cod_disc': 'ACH0041',
                    'professor': prof_bd.Apelido,
                    'horario': horario,
                    'dia': corresp_dias_semana[dia_aula_rp1.dia_semana],
                    'extra': False,
                    "cod_turma": 0
                },
                "semestre": 1
            }
            aula_manha_noite(data, alertas, ano)
            aula_noite_outro_dia_manha(data, alertas, ano)
            
            # print(aula_msm_horario(data["info"], ano, data, erros))
            # print("do professor " + data["info"]["professor"])

            if horario in (0, 2, 5): conf_tbl = conflito_hr_na_tbl_rp1(dia_aula_rp1, prof_bd, ano, erros)
            confl_hr = aula_msm_horario(data["info"], ano, data, erros)
            print(confl_hr)
            if confl_hr: break
 

        if not conf_tbl and not confl_hr:
            try:
                #Devemos priorizar o caso em que ocorre algum true, ou seja, a função aula_msm_horario será executada duas vezes, se em algum momento ela retornar true, então não podemos salvar o professor. Se ela não retornar true em nenhuma das duas chamadas, podemos salvar o professor no banco de dados.
                tur.professor_si.add(prof_bd)
                print("Salvou prof")
                # break
            except Exception as e:
                print("erroooo")
        else:
            erros["nome_prof"] = prof_bd.NomeProf
            print(erros["nome_prof"])

        restricoes = prof_bd.restricao_set.all()

    print("Verificando professores")
    print(tur.professor_si.all())

    print(erros)
    print(alertas)
    resp = {'erros': erros,
            'alertas': alertas,
            # 'restricao_prof':prof_na_restricao(tur, restricoes),
            'sugestoes': gera_sugestoes_rp1(ano)
            }

    return JsonResponse(resp)

def conflito_hr_na_tbl_rp1(dia_gravar, prof, ano, erros):

    turmas = RP1Turma.objects.filter(professor_si=prof, ano=ano)

    for turma in turmas:

        dia_gravado_bd = DiaAulaRP1.objects.get(turma_rp1=turma)
        print(dia_gravado_bd.horario)

        if(dia_gravado_bd.dia_semana == dia_gravar.dia_semana and dia_gravado_bd.horario == dia_gravar.horario):

            msg=(
                f"Professor(a) {prof.NomeProf} já possui"
                f" uma turma de RP1 gravado nesse horário nessa tabela"
            )
            erros["prof_msm_hr"] = msg
            return True
        

def contar_professores(lista_professores):
    contagem = {}

    for professor in lista_professores:
        if professor in contagem:
            contagem[professor] += 1
        else:
            contagem[professor] = 1

    return contagem

def profs_rp1(ano):
    profs_objs = RP1TurmaPreview.objects.filter(codigo=99).first().professor_si.all()
    total_profs = {}

    for prof_obj in profs_objs:
        total_profs[prof_obj.NomeProf] = prof_obj.Apelido

    return total_profs


def gera_sugestoes_rp1(ano):
    #código adaptado da função remove_rp do planilhas_docentes.py
    rps = RP1Turma.objects.filter(ano=ano)
    rp_preview = RP1TurmaPreview.objects.all()
    profs_objs = RP1TurmaPreview.objects.filter(codigo=99).first().professor_si.all()
    auto_profs = {}


    for prof_obj in profs_objs:
        auto_profs[prof_obj.NomeProf] = prof_obj.Apelido

    lista_prof_preview = []

    for turma in rp_preview:
        profs = turma.professor_si.all()
        for prof in profs:
            lista_prof_preview.append(prof)

    dict_prof_preview = contar_professores(lista_prof_preview)


    for tur in rps:
        profs = tur.professor_si.all()
        for prof in profs:
            if prof in dict_prof_preview:
                dict_prof_preview[prof] -= 1

            # Comentar o próximo trecho para poder testar o mesmo professor na tabela de rp1 (somente para teste)
            if (prof in dict_prof_preview and dict_prof_preview[prof] == 0) or (not prof in dict_prof_preview):
                try:
                    del auto_profs[prof.NomeProf]
                except:
                    print("Erro ao deletar o professor do auto_profs")


    return auto_profs

