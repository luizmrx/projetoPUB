from django.db import models
from django.db.models.signals import pre_save
from django.dispatch import receiver

class Meta:

    db_table = 'tool_manage'

class Professor(models.Model):
    NroUsp = models.DecimalField(
        primary_key=True, max_digits=7, decimal_places=0, default="0"
    )
    NomeProf = models.CharField(max_length=50, default="")
    Apelido = models.CharField(max_length=35, default="")
    Telefone = models.DecimalField(
        max_digits=8, decimal_places=0, null=True, blank=True
    )
    Celular = models.DecimalField(max_digits=9, decimal_places=0, null=True, blank=True)
    Sala = models.CharField(max_length=25, default="", null=True)
    Email = models.CharField(max_length=30, default="", null=True)
    PG_1_semestre = models.IntegerField(default=0)
    PG_2_semestre = models.IntegerField(default=0)
    consideracao1 = models.CharField(max_length=500, default=None, null=True, blank=True)
    consideracao2 = models.CharField(max_length=500, default=None, null=True, blank=True)
    pos_doc = models.CharField(max_length=500, default="", null=True, blank=True) #Descontinuado, olhe a tbl justificativamenos8horas
    pref_optativas = models.CharField(max_length=300, default="", null=True, blank=True) # Descontinuado
    em_atividade = models.BooleanField(default=True)

    def __str__(self):
        return str(self.NomeProf)

class justificativaMenos8Horas(models.Model):
    justificativas = [
        ("afastado", "Afastado"),
        ("compensacao_creditos", "Compensação de Créditos"),
        ("emprestimo", "Empréstimo"),
        ("licenca_maternidade", "Licença-Maternidade"),
        ("licenca_premio", "Licença-Prêmio"),
        ("sem_contrato", "Sem Contrato"),
        ("pos_doc", "Pós-Doutorado")
    ]
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE)
    justificativa = models.CharField(max_length=20, choices=justificativas, default="licenca_premio")
    ano = models.DecimalField(max_digits=4, default=2024, decimal_places=0)
    semestre_ano = models.CharField(default="P", max_length=1, choices=[("P", "par"), ("I", "impar")])
    texto_justificando = models.CharField(max_length=500, default=None, null=True, blank=True)
    class Meta:
        unique_together = (("professor", "ano", "semestre_ano"),)



class Disciplina(models.Model):
    CoDisc = models.CharField(primary_key=True, max_length=7)
    professores = models.ManyToManyField(Professor, through="Preferencias")
    Abreviacao = models.CharField(max_length=10, null=True)
    NomeDisc = models.CharField(max_length=200, null=True)
    SemestreIdeal = models.IntegerField(choices=list(zip(range(1, 9), range(1, 9))))
    creditos = [(0, 0), (2, 2), (4, 4)]
    CreditosAula = models.IntegerField(choices=creditos, default=4)
    tipo = [
        ("obrigatoria", "Obrigatória"),
        ("optativaCB", "Optativa - Ciclo Básico"),
        ("optativaSI", "Optativa - Sistemas de informação"),
    ]
    TipoDisc = models.CharField(max_length=12, choices=tipo, default="obrigatoria")
    ativa = models.BooleanField(default=True)
    def __str__(self):
        return str(self.CoDisc)


class Preferencias(models.Model):
    NumProf = models.ForeignKey(Professor, on_delete=models.CASCADE)
    CoDisc = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    AnoProf = models.DecimalField(max_digits=4, default=2024, decimal_places=0)
    Semestre = models.IntegerField(choices=[(1, "impar"), (2, "par")])
    PRIORIDADE = [
        (1, "1"),
        (2, "2"),
        (3, "3")
    ]
    nivel = models.IntegerField(choices=PRIORIDADE, default=1)

    class Meta:
        unique_together = (("NumProf", "CoDisc", "AnoProf"),)

    def __str__(self):
        return f"{str(self.NumProf.Apelido)} - {str(self.CoDisc.Abreviacao)}"


class Turma(models.Model):
    CoDisc = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    CodTurma = models.DecimalField(max_digits=2, decimal_places=0, default=0)
    Ano = models.DecimalField(max_digits=4, decimal_places=0, null=True, blank=True)
    NroUSP = models.ForeignKey(Professor, on_delete=models.CASCADE)
    NroAlunos = models.IntegerField(null=True, blank=True)
    Eextra = models.CharField(max_length=1, choices=[("S", "Sim"), ("N", "Não")])
    semestre_extra = models.DecimalField(max_digits=1, decimal_places=0, default=0)
    SemestreAno = models.CharField(default="P", max_length=1, choices=[("P", "par"), ("I", "impar")])

    class Meta:
        unique_together = (("Ano", "CodTurma", "CoDisc", "SemestreAno", "Eextra", "NroUSP"),)

    def __str__(self):
        return "0" + str(self.CodTurma) + "/" + str(self.CoDisc) 


class Dia(models.Model):
    dias = [(0, "Segunda"), (2, "Terça"), (4, "Quarta"), (6, "Quinta"), (8, "Sexta")]
    DiaSemana = models.DecimalField(
        max_digits=4, decimal_places=0, choices=dias, default=2
    )
    Turmas = models.ManyToManyField(Turma)

    horarios = [
        (0, "8:00 - 09:45h"),
        (1, "10:15 - 12:00h"),
        (2, "14:00 - 15:45h"),
        (4, "16:15-18:00h"),
        (5, "19:00 - 20:45h"),
        (7, "21:00 - 22:45h"),
    ]
    Horario = models.IntegerField(choices=horarios)
    turnos = [("mat", "Matutino"), ("vesp", "Vespertino"), ("Not", "Noturno")]
    Turno = models.CharField(max_length=15, choices=turnos, default="")

    class Meta:
        unique_together = (("Horario", "DiaSemana"),)

    def __str__(self):
        return f"{self.get_DiaSemana_display()}/{self.get_Horario_display()}"


class RP1Turma(models.Model):
    professor_si = models.ManyToManyField(Professor)
    codigo = models.IntegerField()
    profs_adicionais = models.CharField(max_length=300, default=None, null=True, blank=True)
    cursos = models.CharField(max_length=300, default=None, null=True, blank=True)
    ano = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        unique_together = (("codigo", "cursos", "profs_adicionais", "ano"),)


# Serve para preencher a planilha de atribuição
class RP1TurmaPreview(models.Model):
    professor_si = models.ManyToManyField(Professor)
    codigo = models.IntegerField()
    ano = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        unique_together = (("codigo", "ano"),)


class DiaAulaRP1(models.Model):
    turma_rp1 = models.ForeignKey(RP1Turma, on_delete=models.CASCADE)
    dias = [("Seg", "Seg"), ("Ter", "Ter"), ("Qua", "Qua"), ("Qui", "Qui"), ("Sex", "Sex")]
    dia_semana = models.CharField(max_length=3, choices=dias, default=None)
    horarios = [
        ("08h - 12h", "08h - 12h"),
        ("14h – 18h", "14h - 18h"),
        ("19h - 22h45", "19h - 22h45"),
    ]
    horario = models.CharField(default=None, max_length=20, choices=horarios)

    class Meta:
        unique_together = (("turma_rp1", "dia_semana", "horario"),)


class Turmas_RP(models.Model):

    turma = models.ForeignKey(Turma, on_delete=models.CASCADE)

    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, default="")

    class Meta:
        unique_together = (("turma", "professor"),)

    def __str__(self):
        return "0" + str(self.turma) + "/" + str(self.professor)


class MtvRestricao(models.Model):
    mtv = models.CharField(max_length=500, default="")


class AnoAberto(models.Model):
    Ano = models.DecimalField(max_digits=4, decimal_places=0, default=2022)


class Restricao(models.Model):
    PERIODO_CHOICES = (
        ("todos_periodos", "Todos períodos do dia"),
        ("manha", "Manhã"),
        ("tarde", "Tarde"),
        ("noite", "Noite"),
    )
    DIA_CHOICES = (
        ("todos_dias", "Todos os dias da semana"),
        ("segunda", "Segunda-feira"),
        ("terca", "Terça-feira"),
        ("quarta", "Quarta-feira"),
        ("quinta", "Quinta-feira"),
        ("sexta", "Sexta-feira"),
        ("sabado", "Sábado"),
        ("domingo", "Domingo"),
    )
    nro_usp = models.ForeignKey(Professor, on_delete=models.CASCADE)
    periodo = models.CharField(max_length=15, choices=PERIODO_CHOICES)
    dia = models.CharField(max_length=15, choices=DIA_CHOICES)
    motivos = models.ForeignKey(MtvRestricao, on_delete=models.CASCADE, null=True, default=None, blank=True)
    SEMESTRE_CHOICES = (
        ("1", "1 semestre"),
        ("2", "2 semestre")
    )
    semestre = models.CharField(max_length=15, choices=SEMESTRE_CHOICES, default=None)

    impedimento = models.BooleanField(default=False)

    class Meta:
        unique_together = (("nro_usp", "periodo", "dia", "semestre"),)

    def __str__(self):
        return f"{self.nro_usp.Apelido} ({str(self.periodo)} / {str(self.dia)})"

    @classmethod
    def criar_restricoes(cls, periodo, dia, nro_usp, semestre, impedimento=False, motivos=None):
        if periodo == "todos_periodos" and dia == "todos_dias":
            raise ValueError(
                "A restrição não pode ser em todos os dias e em todos os períodos ao mesmo tempo."
            )

        # Cria uma lista de objetos de restrição para cada dia se a restrição for para todos os dias
        if dia == "todos_dias":
            restricoes = [
                cls(periodo=periodo, dia=dia_opcao[0], nro_usp=nro_usp, motivos=motivos, semestre=semestre, impedimento=impedimento)
                for dia_opcao in cls.DIA_CHOICES[1:]
            ]
            cls.objects.bulk_create(restricoes, ignore_conflicts=True)

        # Cria uma restrição normal, ou seja, para um dia e perído específico, não é necesário(apagar)
        elif periodo != "todos_periodos":
            cls.objects.create(periodo=periodo, dia=dia, nro_usp=nro_usp, motivos=motivos, semestre=semestre, impedimento=impedimento)

        # Cria uma lista de objetos de restrição para todos os período em um mesmo dia
        else:
            restricoes = [
                cls(periodo=periodo_opcao[0], dia=dia, nro_usp=nro_usp, motivos=motivos, semestre=semestre, impedimento=impedimento)
                for periodo_opcao in cls.PERIODO_CHOICES[1:]
            ]
            cls.objects.bulk_create(restricoes, ignore_conflicts=True)


#Turma TADI
class TadiTurma(models.Model):
    professor_si = models.ManyToManyField(Professor)
    codigo = models.IntegerField()
    curso = models.CharField(max_length=300, default=None, null=True, blank=True)
    ano = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        unique_together = (("codigo", "curso", "ano"),)


class TadiTurmaPreview(models.Model):
    professor_si = models.ManyToManyField(Professor)
    codigo = models.IntegerField()
    ano = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        unique_together = (("codigo", "ano"),)


class DiaAulaTadi(models.Model):
    turma_tadi = models.ForeignKey(TadiTurma, on_delete=models.CASCADE)
    dias = [("Seg", "Seg"), ("Ter", "Ter"), ("Qua", "Qua"), ("Qui", "Qui"), ("Sex", "Sex")]
    dia_semana = models.CharField(max_length=3, choices=dias, default=None)
    horarios = [
        ("8:00 - 09:45h", "8:00 - 09:45h"),
        ("10:15 - 12:00h", "10:15 - 12:00h"),
        ("14:00 - 15:45h", "14:00 - 15:45h"),
        ("16:15 - 18:00h", "16:15 - 18:00h"),
        ("19:00 - 20:45h", "19:00 - 20:45h"),
        ("21:00 - 22:45h", "21:00 - 22:45h"),
    ]
    horario = models.CharField(default=None, max_length=20, choices=horarios)

    class Meta:
        unique_together = (("turma_tadi", "dia_semana", "horario"),)


class RP2TurmaPreview(models.Model):
    professor_si = models.ManyToManyField(Professor)
    codigo = models.IntegerField()
    ano = models.DecimalField(max_digits=4, decimal_places=0)

    class Meta:
        unique_together = (("codigo", "ano"),)

class RelatoriosPlanilhas(models.Model):
    upload_atribuicao = models.TextField(default="")
    gerar_atribuicao = models.TextField(default="")
    upload_preferencias = models.TextField(default="")
    upload_rp1 = models.TextField(default="")
    upload_tadi = models.TextField(default="")

@receiver(pre_save, sender= AnoAberto)
def zerarPG(sender, instance, **kwargs):
    if instance.pk is not None:
        ano_anterior = AnoAberto.objects.get(pk=instance.pk)
        if ano_anterior.Ano != instance.Ano:
            Professor.objects.update(PG_1_semestre=0, PG_2_semestre=0)
            RelatoriosPlanilhas.objects.update(upload_atribuicao="", gerar_atribuicao="", upload_preferencias="", upload_rp1="", upload_tadi="")