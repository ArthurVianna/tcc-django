from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('turmas/', views.turmas, name='turmas'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('alunos/', views.alunos, name='alunos'),
    path('disciplinas/<int:pk>/', views.disciplina_detail,
         name='disciplina_detail'),
    path('alunos/<int:pk>/', views.aluno_detail,
         name='aluno_detail'),
    path('turmas/<int:pk>/', views.turma_detail,
         name='turma_detail'),
]
