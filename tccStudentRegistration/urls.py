from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('mudar_senha/', views.mudar_senha, name='mudar_senha'),

    path('dashboard/', views.dashboard, name='dashboard'),

    path('turmas/', views.turmas, name='turmas'),
    path('turma/<str:periodo_ingresso>/', views.turma_detail,
         name='turma_detail'),

    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('disciplina/<int:pk>/', views.disciplina_detail,
         name='disciplina_detail'),

    path('alunos/', views.alunos, name='alunos'),
    path('alunos_perigo/', views.alunos_perigo, name='alunos_perigo'),
    path('aluno/<int:pk>/', views.aluno_detail,
         name='aluno_detail'),

    path('usuarios/', views.usuarios, name='usuarios'),
    path('cadastrar_usuario', views.cadastrar_usuario,
         name="cadastrar_usuario"),
    path('editar_usuario/<int:pk>', views.editar_usuario,
         name="editar_usuario"),

    path('importCSV/', views.importCSV, name="importCSV"),
]
