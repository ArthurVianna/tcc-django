from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.db.models import Count
from .models import Disciplina, Aluno, Matricula


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            if user.is_active:
                login(request, user)
                return redirect('dashboard/')
                # return render(request, 'tcc/dashboard.html', {})
            else:
                # TODO: ajustar a resposta
                return render(request, 'registration/login.html', {'msg':"Your account was inactive."})
        else:
            # TODO: retirar esses prints e ajustar a resposta
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".
                  format(username, password))
            return render(request, 'registration/login.html', {'msg':"Invalid login details given"})
    else:
        return render(request, 'registration/login.html', {})


def user_logout(request):
    logout(request)
    return render(request, 'registration/login.html', {})


@login_required
def dashboard(request):
    return render(request, 'tcc/dashboard.html', {})


@login_required
def turmas(request):
    turmas = Aluno.objects.values('periodo_ingresso').annotate(
        num_alunos=Count('periodo_ingresso')).order_by('periodo_ingresso')
    return render(request, 'tcc/turmas.html', {'turmas': turmas})


@login_required
def turma_detail(request, pk):
    # turma = get_object_or_404(Aluno, pk=pk)
    alunos = Aluno.objects.filter(periodo_ingresso=pk)
    return render(request,
                  'tcc/turma_detail.html',
                  {'alunos': alunos})
    # 'turma': turma,


@login_required
def disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request,
                  'tcc/disciplinas.html',
                  {'disciplinas': disciplinas})


@login_required
def disciplina_detail(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    max_year = Matricula.objects.latest('periodo_matricula')
    if(max_year.periodo_matricula.month > 7):
        dateRange = [str(max_year.periodo_matricula.year) + "-07-01",
                     str(max_year.periodo_matricula.year) + "-12-31"]
    else:
        dateRange = [str(max_year.periodo_matricula.year) + "-01-01",
                     str(max_year.periodo_matricula.year) + "-06-30"]
    alunos = Matricula.objects.filter(disciplina__id=pk,
                                      periodo_matricula__range=dateRange)
    return render(request,
                  'tcc/disciplina_detail.html',
                  {'disciplina': disciplina, 'alunos': alunos})


@login_required
def alunos(request):
    alunos = Aluno.objects.all().order_by('periodo_ingresso')
    return render(request, 'tcc/alunos.html', {'alunos': alunos})


@login_required
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    matricula = Matricula.objects.filter(aluno__id=pk).order_by(
        'periodo_matricula')
    return render(request,
                  'tcc/aluno_detail.html',
                  {'aluno': aluno, 'matricula': matricula})
