from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.db.models import Count
from django.shortcuts import redirect
from .models import Disciplina, Aluno, Matricula


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def dashboard(request):
    print(request.user)  # chamar o user da session
    return render(request, 'tcc/dashboard.html', {})


@login_required
def turmas(request):
    turmas = Aluno.objects.values('periodo_ingresso').annotate(
        num_alunos=Count('periodo_ingresso')).order_by('periodo_ingresso')
    return render(request, 'tcc/turmas.html', {'turmas': turmas})


@login_required
def turma_detail(request, pk):
    alunos = Aluno.objects.filter(periodo_ingresso=pk)
    return render(request,
                  'tcc/turma_detail.html',
                  {'alunos': alunos})


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


@login_required
def usuarios(request):
    users = User.objects.all()
    return render(request, 'tcc/usuarios.html', {'users': users})


@login_required
def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            # users = User.objects.all()
            # return render(request, 'tcc/usuarios.html', {'users': users})
            return redirect('editar_usuario', pk=user.pk)
    else:
        form_usuario = UserCreationForm()
    return render(request, 'tcc/new_user.html', {'form_usuario': form_usuario})


@login_required
def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form_usuario = UserChangeForm(request.POST, instance=user)
        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            return redirect('usuarios')
    else:
        form_usuario = UserChangeForm(instance=user)
    return render(request, 'tcc/edit_user.html',
                  {'form_usuario': form_usuario})
