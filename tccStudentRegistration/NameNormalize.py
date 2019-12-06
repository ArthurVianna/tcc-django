from tccStudentRegistration.surnames import *
from tccStudentRegistration.names import *
from tccStudentRegistration.disciplinas import *

print(names[0])
print(surnames[0])

nameLen = len(names) -1
surnameLen = len(surnames) -1

import random
from tccStudentRegistration.models import *

disciplinas = Disciplina.objects.all()
disciplinaDict = {}
count = 0
for disciplina in disciplinas:
    name = nameDisciplinas[count]
    disciplina.descricao_disciplina = name
    disciplinaDict[disciplina.codigo_disciplina] = name
    count+=1
    disciplina.save()
alunos = None
alunos = Aluno.objects.all()
alunoDict = {}
if(alunos):
    for aluno in alunos:
        name = names[random.randint(0,nameLen)] + " " + surnames[random.randint(0,surnameLen)]
        aluno.nome_aluno = name
        alunoDict[aluno.grr_aluno] = name
        aluno.save()

from datawarehouseManager.models import *
disciplinas = Disciplina.objects.filter(codigo_disciplina__in=disciplinaDict.keys())
alunos = Aluno.objects.filter(grr_aluno__in=alunoDict.keys())
for disciplina in disciplinas:
    disciplina.descricao_disciplina = disciplinaDict[disciplina.codigo_disciplina]
    disciplina.save()
if alunos :
    for aluno in alunos:
        aluno.nome_aluno = alunoDict[aluno.grr_aluno]
        aluno.save()

print()
print(str(random.randint(0,1)))

print("Ready")
