from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


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
    return render(request, 'tcc/disciplinas.html', {})


@login_required
def alunos(request):
    return render(request, 'tcc/alunos.html', {})
