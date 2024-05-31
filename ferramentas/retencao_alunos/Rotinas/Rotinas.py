from ..models import Demanda_por_disciplina, Disciplina, Aluno
from ..utilitarios.calcula_semestre import semestre


class Rotinas():

    def __init__(self) -> None:
        pass

    @classmethod
    def informações_disciplina(cls, disciplina):
        #método que devolve informações da disciplina passada por parâmetro
        disc = disciplina
        resp = {}
        demanda = Demanda_por_disciplina.objects.filter(
            disciplina = Disciplina.objects.get(codigo = disc)
        )

        semestre_ideal = Disciplina.objects.get(codigo = disc).semestre_ideal
        resp["periodo ideal"] = semestre_ideal
        resp["total de alunos"] = len(demanda)
        resp["alunos cursando"] = 0
        resp["alunos a cursar"] = 0
        resp["alunos a cursar - período ideal"] = 0
        resp["alunos a cursar - atrasados"] = 0

        descricao_atrasados = {}
        
        
        for caso in demanda:
            if caso.cursando:
                resp["alunos cursando"] += 1
            else:
                resp["alunos a cursar"] += 1
                if caso.atrasado:
                    resp["alunos a cursar - atrasados"] += 1
                    aluno = Aluno.objects.get(nro_usp = caso.aluno)
                    semestre_aluno = semestre(aluno.ano_ingresso)
                    if f"{semestre_aluno} semestre" in descricao_atrasados:
                        descricao_atrasados[f"{semestre_aluno} semestre"] += 1
                    else:
                        descricao_atrasados[f"{semestre_aluno} semestre"] = 1
                else:
                    resp["alunos a cursar - período ideal"] += 1
        resp["descrição dos atrasados"] = descricao_atrasados

        return resp
    
    @classmethod
    def listar_disciplinas_atrasados_semestre_par(cls):
        #método que devolve em ordem decrescente as disciplinas com maior número de alunos atrasados
        resp = {}
        disciplinas = Disciplina.objects.all()
        for disciplina in disciplinas:
            if disciplina.semestre_ideal % 2 == 0: #semestre par
                retorno = cls.informações_disciplina(disciplina.codigo)
                resp[f"{disciplina.codigo} {disciplina.nome}"] = retorno["alunos a cursar - atrasados"]

        return dict(sorted(resp.items(), key=lambda item: item[1], reverse=True))
    
    @classmethod
    def listar_disciplinas_atrasados_semestre_impar(cls):
        #método que devolve em ordem decrescente as disciplinas com maior número de alunos atrasados
        resp = {}
        disciplinas = Disciplina.objects.all()
        for disciplina in disciplinas:
            if disciplina.semestre_ideal % 2 != 0: #semestre impar
                retorno = cls.informações_disciplina(disciplina.codigo)
                resp[f"{disciplina.codigo} {disciplina.nome}"] = retorno["alunos a cursar - atrasados"]

        return dict(sorted(resp.items(), key=lambda item: item[1], reverse=True))
    
    
    @classmethod
    def listar_alunos_atrasados(cls):
        #método que devolve uma lista em ordem decrescente dos alunos com matérias atrasadas
        resp = {}
        alunos = Aluno.objects.all()
        for aluno in alunos:
            
            qnt = Demanda_por_disciplina.objects.filter(
                aluno = Aluno.objects.get(nro_usp = aluno.nro_usp),
                atrasado = True
            )
            if(len(qnt) != 0) : resp[f"{aluno.nro_usp} {aluno.nome} - ingresso em: {aluno.ano_ingresso}"] = len(qnt)

        return dict(sorted(resp.items(), key=lambda item: item[1], reverse=True))
    
    