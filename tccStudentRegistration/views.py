from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Disciplina, Aluno


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
                return HttpResponse("Your account was inactive.")
        else:
            # TODO: retirar esses prints e ajustar a resposta
            print("Someone tried to login and failed.")
            print("They used username: {} and password: {}".
                  format(username, password))
            return HttpResponse("Invalid login details given")
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
    return render(request, 'tcc/turmas.html', {})


@login_required
def disciplinas(request):
    disciplinas = Disciplina.objects.all()
    return render(request,
                  'tcc/disciplinas.html',
                  {'disciplinas': disciplinas})


@login_required
def disciplina_detail(request, pk):
    disciplina = get_object_or_404(Disciplina, pk=pk)
    return render(request,
                  'tcc/disciplina_detail.html',
                  {'disciplina': disciplina})


@login_required
def alunos(request):
    alunos = Aluno.objects.all()
    return render(request, 'tcc/alunos.html', {'alunos': alunos})


@login_required
def aluno_detail(request, pk):
    aluno = get_object_or_404(Aluno, pk=pk)
    return render(request,
                  'tcc/aluno_detail.html',
                  {'aluno': aluno})
