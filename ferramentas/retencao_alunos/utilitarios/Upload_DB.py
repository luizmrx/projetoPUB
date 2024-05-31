from ..models import Aluno, Disciplina, Demanda_por_disciplina
from .calcula_semestre import semestre

class Cadastro_Aluno_Exception(Exception):
    def __init__(self, mensagem="Ocorreu um erro ao cadastrar um aluno"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)

class Cadastro_Demanda_Exception(Exception):
    def __init__(self, mensagem="Ocorreu um erro ao cadastrar uma demanda de disciplina"):
        self.mensagem = mensagem
        super().__init__(self.mensagem)


class Upload():

    def upload_Alunos(nro_usp, nome, ingresso):

        #checar se o aluno já está cadastrado
        exists = Aluno.objects.filter(nro_usp=nro_usp)
        if not exists:
            new_aluno = Aluno.objects.create(
                nro_usp=nro_usp,
                nome=nome,
                ano_ingresso=ingresso
            )
            try:
                new_aluno.save()
            except Cadastro_Aluno_Exception as e:
                print(f"Exceção capturada: {e}")

    def upload_Demanda(cod_disc, nro_usp, cursando):

        disciplina = Disciplina.objects.get(
            codigo = cod_disc
        )

        aluno = Aluno.objects.get(
            nro_usp = nro_usp
        )

        semestre_aluno = semestre(aluno.ano_ingresso)

        atrasado = False

        if disciplina.semestre_ideal < semestre_aluno - 1:
            atrasado = True

        if cursando == "Sim":
            cursando = True
        else: cursando = False

        new_demanda = Demanda_por_disciplina.objects.create(
            disciplina = disciplina,
            aluno = aluno,
            cursando = cursando,
            atrasado = atrasado
        )

        try:
            new_demanda.save()

        except Cadastro_Demanda_Exception as e:
                print(f"Exceção capturada: {e}")