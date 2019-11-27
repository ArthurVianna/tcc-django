# flake8: noqa
from tccStudentRegistration.models import *
from django.db.models import Min
import time

def getMatriculasCompletas():
    matriculas = Matricula.objects.exclude(
        situacao_matricula=SituacaoMatricula.objects.get(
            descricao_situacao_matricula='Matrícula')
    )
    return matriculas
    pass


def getAlunoEvadiram():
    matriculas = Aluno.objects.exclude(
        forma_evasao=FormaEvasao.objects.get(
            descricao_evasao='Sem evasão')
    )
    return matriculas
    pass


def getCursoAluno(grraluno):
    aluno = Aluno.objects.get(grr_aluno=grraluno)
    matriculaAluno = Matricula.objects.filter(aluno=aluno,periodo_matricula=aluno.periodo_ingresso)
    if(matriculaAluno.count() == 0):
        matriculaAluno = Matricula.objects.filter(aluno=aluno,periodo_matricula=Min('periodo_matricula'))
    matriculaPrimeiroAno = matriculaAluno[0]
    return matriculaPrimeiroAno.curso


def getMatriculasAluno(grraluno):
    aluno = Aluno.objects.get(grr_aluno=grraluno)
    matriculas = Matricula.objects.filter(aluno=aluno)
    return matriculas

def countMatriculasAluno(grraluno):
    return getMatriculasAluno(grraluno).count()

def getLatestIngresso():
    return Aluno.objects.latest('periodo_ingresso').periodo_ingresso

def countRetencoesAluno(grrAluno):
    matriculas = getMatriculasAluno(grrAluno)
    situacaoMatriculas = SituacaoMatricula.objects.filter(descricao_situacao_matricula__in=situacaoMatriculasReprovados())
    return matriculas.filter(situacao_matricula__in=situacaoMatriculas).count()


def calculoIra(grrAluno):
    # Somatória (NOTAS x CH Cumprida) / CH TOTAL x 100
    matriculas = getMatriculasAluno(grrAluno)
    chTotal = 0
    somatoria = 0
    for matricula in matriculas:
        chCumprida = int(matricula.disciplina.carga_horaria) - matricula.faltas_matricula
        somatoria += matricula.media_final_matricula * chCumprida
        chTotal += int(matricula.disciplina.carga_horaria)

    return somatoria / (chTotal*100)

def deleteAlunosEvadiram():
    matriculas = Aluno.objects.exclude(
        forma_evasao=FormaEvasao.objects.get(
            descricao_evasao='Sem evasão')
    )
    matriculas.delete()

def getQtdSemestres(grrAluno):
    aluno = Aluno.objects.get(grr_aluno=grrAluno)
    ingresso = aluno.periodo_ingresso
    evasao = aluno.periodo_evasao
    months= (evasao.year - ingresso.year) * 12 + (evasao.month - ingresso.month)
    #if((months/6) +1 < 6):
    #    print("GRR : " + grrAluno + " semestres = " + str(months/6 +1) + "  meses : " + str(months))
    return (months/6) +1


def situacaoMatriculasReprovados():
    reprovado = ['Reprovado por nota',
                 'Reprovado por Frequência',
                 'Cancelado',
                 'Incompleto',
                 'Reprovado sem nota',
                 'Matrícula',
                 'Trancamento Total',
                 'Disciplina sem Oferta',
                 'Trancamento Administrativo',
                 'PROVAR',
                 'Trancamento CEPE',
                 'Trancamento Outra IES',
                 'Suficiente',
                 'Reprov Conhecimento',
                 'Reprov Adiantamento',
                 'Trancamento por amparo Legal',
                 'Isento por Transferência',
                 'Desistência de Vaga',
                 'Processo Administrativo',
                 'Horas']
    return reprovado
