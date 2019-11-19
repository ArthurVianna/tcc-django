from django.urls import path
from . import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('turmas/', views.turmas, name='turmas'),
    path('disciplinas/', views.disciplinas, name='disciplinas'),
    path('alunos/', views.alunos, name='alunos'),
    path('disciplina/<int:pk>/', views.disciplina_detail,
         name='disciplina_detail'),
    path('aluno/<int:pk>/', views.aluno_detail,
         name='aluno_detail'),
    path('turma/<str:pk>/', views.turma_detail,
         name='turma_detail'),
]
