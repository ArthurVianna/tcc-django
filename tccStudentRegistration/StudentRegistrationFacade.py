from datetime import date
from django.utils import timezone
from django.contrib.auth.models import User
from .models import Disciplina, Aluno, Matricula, PredicaoEvasao, Comentario, FormaEvasao
from django.shortcuts import render, get_object_or_404
from django.db.models import Count


class StudentRegistrationFacade(object):
    """docstring for StudentRegistrationFacade"""
    def __init__(self, arg):
        super(StudentRegistrationFacade, self).__init__()
        self.arg = arg
    
    @staticmethod
    def getListaUsuarios():
        users = User.objects.all()
        return users

    @staticmethod
    def getAluno(pk):
        aluno = get_object_or_404(Aluno, pk=pk)
        return aluno

    @staticmethod
    def getComments(aluno):
        comentarios = Comentario.objects.filter(aluno=aluno)
        if comentarios:
            comentarios = comentarios.order_by('data_comentario')
        return comentarios

    @staticmethod
    def getPredicao(aluno):
        predicao = PredicaoEvasao.objects.filter(aluno=aluno)
        if predicao:
            predicao = predicao.latest('periodo_predicao')
        return predicao

    @staticmethod
    def getMatriculas(aluno):
        return Matricula.objects.filter(aluno=aluno).order_by(
            'periodo_matricula')

    @staticmethod
    def getListaAlunos():
        return Aluno.objects.all().order_by('periodo_ingresso')

    @staticmethod
    def getDictPredicoes():
        predicao = PredicaoEvasao.objects.all()
        predicoes = {}
        if predicao:
            predicao = PredicaoEvasao.objects.filter(periodo_predicao=predicao.latest('periodo_predicao').periodo_predicao)
            for predict in predicao:
                predicoes[predict.aluno.grr_aluno] = predict

        return predicoes

    @staticmethod
    def createComment(user,aluno,texto):
        data = timezone.now()
        comentario = Comentario()
        comentario.user = user
        comentario.aluno = aluno
        comentario.data_comentario = data
        comentario.texto_comentario = texto
        comentario.save()

    @staticmethod
    def getListDisciplinas():
        return Disciplina.objects.all()

    @staticmethod
    def getListTurma():
        return Aluno.objects.values('periodo_ingresso').annotate(
            num_alunos=Count('periodo_ingresso')).order_by('periodo_ingresso')

    @staticmethod
    def getTurma(periodo_ingresso):
        return Aluno.objects.filter(periodo_ingresso=periodo_ingresso)

    @staticmethod
    def getDisciplina(pk):
        return get_object_or_404(Disciplina, pk=pk)

    @staticmethod
    def getLatestMatriculas(disciplina):
        max_year = Matricula.objects.latest('periodo_matricula')
        if(max_year.periodo_matricula.month > 7):
            dateRange = [str(max_year.periodo_matricula.year) + "-07-01",
                         str(max_year.periodo_matricula.year) + "-12-31"]
        else:
            dateRange = [str(max_year.periodo_matricula.year) + "-01-01",
                         str(max_year.periodo_matricula.year) + "-06-30"]
        alunos = Matricula.objects.filter(disciplina=disciplina,
                                          periodo_matricula__range=dateRange)
        return alunos
        


