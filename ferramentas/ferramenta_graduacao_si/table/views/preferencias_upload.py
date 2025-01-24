from datetime import datetime
from ..models import *
import re
import unidecode

def pref_disc_excel_impar(sem, row, prof_db, header):
    values = (
        [row for row in row[2:17]] if sem == "impar" else [row for row in row[17:31]]
    )

    ano = AnoAberto.objects.get(id=1).Ano
    ini = 18 if sem == "par" else 2
    mensagens = []

    # adaptação
    if sem == "opt":
        ini = 42
        values = [row for row in row[42:78]]

    for i, value in enumerate(values, start=ini):
        if value is None or value == "Não Selecionado":
            continue

        if sem == "opt":
            value = 1

        col_value = header[i]
        cod_mtr = re.search(r"ACH\d{4}", col_value) if col_value is not None else "" # cod_mtr será nulo em casos de testes quando deletar manualmente a matéria
        semestre = 2 if sem == "par" else 1
        try:
            disc_bd = Disciplina.objects.get(CoDisc=cod_mtr.group())
            preferencia = Preferencias(
                NumProf=prof_db,
                CoDisc=disc_bd,
                AnoProf=ano,
                nivel=int(value),
                Semestre=semestre,
            )
            preferencia.save()
        except Exception as e:
            print(f"ERRO no registro da preferência, todos os códigos de seleção do forms precisam estar no BD. {e}")
            if cod_mtr:
                mensagem = (f"Erro no registro da preferência, código da disciplina: {cod_mtr.group()}")
                mensagens.append(mensagem)
    
    instancia, created = RelatoriosPlanilhas.objects.get_or_create(id=1)
    msg_anterior = instancia.upload_preferencias
    if msg_anterior: mensagens.append(msg_anterior)
    mensagens_texto = "\n".join(mensagens) if mensagens else ""
    instancia.upload_preferencias = mensagens_texto
    instancia.save()


def pref_horarios(row, prof_db, semestre_par):
    if semestre_par:
        MtvRestricao.objects.filter(restricao__semestre="2", restricao__nro_usp=prof_db).delete()
        Restricao.objects.filter(semestre="2", nro_usp=prof_db).delete()
        values = [row for row in row[3:7]]
        dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]

        mtv_prof = None
        if row[8] is not None:
            mtv_prof = MtvRestricao(mtv=row[8])
            mtv_prof.save()

        for dia, value in zip(dias_semana, values):
            if value is not None:
                per = unidecode.unidecode(value.lower())
                restHro = Restricao(periodo=per, dia=dia, nro_usp=prof_db, semestre="2")
                if mtv_prof:
                    restHro.motivos = mtv_prof
                restHro.save()

        if row[2] is not None:
            dia = unidecode.unidecode(row[2].lower())
            Restricao.criar_restricoes(
                periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="2"
            )

        if row[36] is not None:
            dia = unidecode.unidecode(row[36].lower())
            # print(f"dia {dia} professor: {prof_db.NomeProf}")
            Restricao.criar_restricoes(
                periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="1"
            )

    if semestre_par:
        return

    dict_imped = {
        "manha": unidecode.unidecode(row[37].lower()) if row[37] else None,
        "tarde": unidecode.unidecode(row[38].lower()) if row[38] else None,
        "noite": unidecode.unidecode(row[39].lower()) if row[39] else None
    }

    for per, dia in dict_imped.items():
        if dia is None:
            continue

        Restricao.criar_restricoes(
                periodo=per, dia=dia, nro_usp=prof_db, semestre="1", impedimento=True
        )

        mtv_xl = row[40] if row[40] else "Sem especificação no forms"
        mtv_prof = MtvRestricao(mtv=mtv_xl)
        mtv_prof.save()

        rest = prof_db.restricao_set.filter(
            dia=dia, periodo=per, semestre="1"
        ).first()

        mtv_prof = False

        if row[40] is not None:
            mtv_prof = MtvRestricao(mtv=row[40])
            mtv_prof.save()

        if not rest:
            rest = Restricao(periodo=per, dia=dia, nro_usp=prof_db, semestre="1")

        if rest and mtv_prof:
            rest.motivos = mtv_prof

        rest.save()

        break

    if row[41] is not None:
        dia = unidecode.unidecode(row[41].lower())
        # print(f"dia {dia} professor: {prof_db.NomeProf}")
        Restricao.criar_restricoes(
            periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="1"
        )




#Versão antiga
# def pref_disc_excel_impar(sem, row, prof_db, header):
#     values = (
#         [row for row in row[2:18]] if sem == "impar" else [row for row in row[18:32]]
#     )
#     ano = AnoAberto.objects.get(id=1).Ano
#     ini = 18 if sem == "par" else 2
#     for i, value in enumerate(values, start=ini):
#         if value is None or value == "Não Selecionado":
#             continue
#         col_value = header[i]
#         cod_mtr = re.search(r"ACH\d{4}", col_value)
#         semestre = 2 if sem == "par" else 1
#         try:
#             disc_bd = Disciplina.objects.get(CoDisc=cod_mtr.group())
#             preferencia = Preferencias(
#                 NumProf=prof_db,
#                 CoDisc=disc_bd,
#                 AnoProf=ano,
#                 nivel=int(value),
#                 Semestre=semestre,
#             )
#             preferencia.save()
#         except Exception as e:
#             # print(f"funçao: pref_disc: {e}")
#             pass
#
#
# def pref_horarios(row, prof_db, semestre_par):
#     if semestre_par:
#         MtvRestricao.objects.filter(restricao__semestre="2", restricao__nro_usp=prof_db).delete()
#         Restricao.objects.filter(semestre="2", nro_usp=prof_db).delete()
#         values = [row for row in row[3:7]]
#         dias_semana = ["segunda", "terca", "quarta", "quinta", "sexta"]
#
#         mtv_prof = None
#         if row[8] is not None:
#             mtv_prof = MtvRestricao(mtv=row[8])
#             mtv_prof.save()
#
#         for dia, value in zip(dias_semana, values):
#             if value is not None:
#                 per = unidecode.unidecode(value.lower())
#                 restHro = Restricao(periodo=per, dia=dia, nro_usp=prof_db, semestre="2")
#                 if mtv_prof:
#                     restHro.motivos = mtv_prof
#                 restHro.save()
#
#     if semestre_par and row[2] is not None:
#         dia = unidecode.unidecode(row[2].lower())
#         Restricao.criar_restricoes(
#             periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="2"
#         )
#     if semestre_par and row[36] is not None:
#         dia = unidecode.unidecode(row[36].lower())
#         # print(f"dia {dia} professor: {prof_db.NomeProf}")
#         Restricao.criar_restricoes(
#             periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="1"
#         )
#
#     if not semestre_par and row[34] is not None:
#         dia, per = row[34].split()
#         dia = unidecode.unidecode(dia.lower())
#         per = unidecode.unidecode(per.lower())
#         Restricao.criar_restricoes(
#                 periodo=per, dia=dia, nro_usp=prof_db, semestre="1", impedimento=True
#             )
#         # print(f"dia: {dia} periodo: {per} professor: {prof_db.NomeProf}")
#         rest = prof_db.restricao_set.filter(
#             dia=dia, periodo=per, semestre="1"
#         ).first()
#
#         mtv_prof = False
#
#         if row[35] is not None:
#             mtv_prof = MtvRestricao(mtv=row[35])
#             mtv_prof.save()
#
#         if not rest:
#             rest = Restricao(periodo=per, dia=dia, nro_usp=prof_db, semestre="1")
#
#         if rest and mtv_prof:
#             rest.motivos = mtv_prof
#
#         rest.save()
#
#     if row[36] is not None:
#         dia = unidecode.unidecode(row[36].lower())
#         # print(f"dia {dia} professor: {prof_db.NomeProf}")
#         Restricao.criar_restricoes(
#             periodo="todos_periodos", dia=dia, nro_usp=prof_db, semestre="1"
#         )