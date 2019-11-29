from datawarehouseManager.datawarehouseFacade import *  # noqa
from datetime import date
from django.contrib import messages
from django.shortcuts import render, get_object_or_404
from django.contrib.auth import logout, update_session_auth_hash
from django.core.files.storage import FileSystemStorage
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.shortcuts import redirect
from .StudentRegistrationFacade import StudentRegistrationFacade
from .ImportDataFacade import ImportDataFacade
from .forms import EditarUsuarioForm
from .templateFilters import *  # noqa


def user_logout(request):
    logout(request)
    return redirect('login')


@login_required
def mudar_senha(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            messages.success(request, 'Sua senha foi alterada!')
            return render(request, 'tcc/mudar_senha.html', {'form': form})
        else:
            messages.error(request, 'Por favor corrija os erros abaixo.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'tcc/mudar_senha.html', {'form': form})


@login_required
def dashboard(request):
    # print(request.user)  # chamar o user da session
    chart = datawarehouseFacade.getFatoEvasaoPorcentagemRetidosSemestre()  # noqa
    return render(request, 'tcc/dashboard.html', {'chart': chart})


@login_required
def turmas(request):
    turmas = StudentRegistrationFacade.getListTurma()
    return render(request, 'tcc/turmas.html', {'turmas': turmas})


@login_required
def turma_detail(request, periodo_ingresso):
    alunos = StudentRegistrationFacade.getTurma(periodo_ingresso)
    return render(request,
                  'tcc/turma_detail.html',
                  {'alunos': alunos})


@login_required
def disciplinas(request):
    disciplinas = StudentRegistrationFacade.getListDisciplinas()
    return render(request,
                  'tcc/disciplinas.html',
                  {'disciplinas': disciplinas})


@login_required
def disciplina_detail(request, pk):
    dictResponse = {}
    disciplina = StudentRegistrationFacade.getDisciplina(pk)
    dictResponse['disciplina'] = disciplina
    if disciplina:
        dictResponse['alunos'] = StudentRegistrationFacade.getLatestMatriculas(
            disciplina)
        detalhes = datawarehouseFacade.getDisciplinaDetalhesMatricula(disciplina.codigo_disciplina)  # noqa
        # chart = getSemiCircleDonutChart(createDataWithPercentage(
        #     detalhes['porcentagemReprovacao'], "\% reprovacao",
        #     "\% aprovacao"), "Porcentagem Aprovacao")
    return render(request, 'tcc/disciplina_detail.html', dictResponse)


@login_required
def alunos(request):
    alunos = StudentRegistrationFacade.getListaAlunos()
    predicoes = StudentRegistrationFacade.getDictPredicoes()
    return render(request, 'tcc/alunos.html', {'alunos': alunos,
                  'predicoes': predicoes})


@login_required
def alunos_perigo(request):
    predicao = PredicaoEvasao.objects.filter(
        forma_evasao=FormaEvasao.objects.get(descricao_evasao="Abandono"),
        periodo_predicao=PredicaoEvasao.objects.latest(
            'periodo_predicao').periodo_predicao)
    return render(request, 'tcc/alunos_perigo.html', {'predicoes': predicao})


@login_required
def aluno_detail(request, pk):
    dictResponse = {}
    aluno = StudentRegistrationFacade.getAluno(pk)
    dictResponse['aluno'] = aluno
    if aluno:
        if request.method == "POST":
            request.user
            if aluno and request.POST['newComentario']:
                StudentRegistrationFacade.createComment(
                    request.user, aluno, request.POST['newComentario'])
        dictResponse['comentarios'] = StudentRegistrationFacade.getComments(aluno)  # noqa
        dictResponse['detalhes'] = datawarehouseFacade.getAlunoDetalhesMatricula(aluno.grr_aluno)  # noqa
        dictResponse['predicao'] = StudentRegistrationFacade.getPredicao(aluno)
        dictResponse['matricula'] = StudentRegistrationFacade.getMatriculas(aluno)  # noqa
    return render(request, 'tcc/aluno_detail.html', dictResponse)


@login_required
def usuarios(request):
    users = StudentRegistrationFacade.getListaUsuarios()
    return render(request, 'tcc/usuarios.html', {'users': users})


@login_required
def cadastrar_usuario(request):
    if request.method == "POST":
        form_usuario = UserCreationForm(request.POST)
        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            return redirect('editar_usuario', pk=user.pk)
    else:
        form_usuario = UserCreationForm()
    return render(request, 'tcc/new_user.html', {'form_usuario': form_usuario})


@login_required
def editar_usuario(request, pk):
    user = get_object_or_404(User, pk=pk)
    if request.method == "POST":
        form_usuario = EditarUsuarioForm(request.POST, instance=user)
        if form_usuario.is_valid():
            user = form_usuario.save(commit=False)
            user.date_joined = timezone.now()
            user.save()
            return redirect('usuarios')
    else:
        form_usuario = EditarUsuarioForm(instance=user)
    return render(request, 'tcc/edit_user.html',
                  {'form_usuario': form_usuario})


@login_required
def importCSV(request):
    msg = ""
    if request.method == 'POST':
        if not request.FILES['document'].name.endswith('.csv'):
            msg = "Arquivo não é um .csv"
        else:
            uploaded_file = request.FILES['document']
            fs = FileSystemStorage()
            today = date.today()
            fileName = "historico_" + str(today) + ".csv"
            fileName = fs.save(fileName, uploaded_file)
            path = fs.location + "/" + fileName
            if not ImportDataFacade.validateFile(path):
                msg = "Arquivo não possui os dados necessários para a importação"  # noqa
            else:
                ImportDataFacade.importNewDataThread(path=path)
                return dashboard(request)
    return render(request, 'tcc/importCSV_form.html', {'msg': msg})
