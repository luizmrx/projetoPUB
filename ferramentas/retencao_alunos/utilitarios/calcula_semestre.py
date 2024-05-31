import datetime

def semestre(ano_aluno, ano):

    ano_atual = ano
    ano_curso =  ano_atual - int(ano_aluno) + 1
    if datetime.datetime.now().month <= 6: semestre_aluno = ano_curso + (ano_atual - int(ano_aluno))
    else: semestre_aluno  = ano_curso + (ano_atual - int(ano_aluno)) + 1
    return semestre_aluno
