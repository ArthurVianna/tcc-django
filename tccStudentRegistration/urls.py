from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', auth_views.LoginView.as_view(
        template_name='registration/login.html'
    ), name='login'),
    path('logout/', views.user_logout, name='logout'),

    path('dashboard/', views.dashboard, name='dashboard'),
    path('turmas/', views.turmas, name='turmas'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('alunos/', views.alunos, name='alunos'),
    path('usuarios/', views.usuarios, name='usuarios'),
    path('disciplina/<int:pk>/', views.disciplina_detail,
         name='disciplina_detail'),
    path('aluno/<int:pk>/', views.aluno_detail,
         name='aluno_detail'),
    path('turma/<str:pk>/', views.turma_detail,
         name='turma_detail'),
    path('cadastrar_usuario', views.cadastrar_usuario,
         name="cadastrar_usuario"),
    path('editar_usuario/<int:pk>', views.editar_usuario,
         name="editar_usuario"),
]
