from pandas import pandas as pd
from datawarehouseManager.dbManager import *
from datetime import datetime


matriculas = getMatriculasCompletas()
alunos = getAlunoEvadiram()
print(alunos)



from datawarehouseManager.models import *
reprovado = ['Reprovado por nota'
, 'Reprovado por Frequência'
, 'Cancelado'
, 'Incompleto'
, 'Reprovado sem nota'
, 'Matrícula'
, 'Trancamento Total'
, 'Disciplina sem Oferta'
, 'Trancamento Administrativo'
, 'PROVAR'
, 'Trancamento CEPE'
, 'Trancamento Outra IES'
, 'Suficiente'
, 'Reprov Conhecimento'
, 'Reprov Adiantamento'
, 'Trancamento por amparo Legal'
, 'Isento por Transferência'
, 'Desistência de Vaga'
, 'Processo Administrativo'
, 'Horas']

evadidosSemConcluirSituacao = [ 'Transferência Externa'
, 'Reopção'
, 'Reintegração'
, 'Mudança de Habilitação Interna'
, 'Jubilamento'
, 'Cancelamento Convênio'
, 'Desistência'
, 'Abandono'
, 'Desligamento com Penalidades'
, 'Cancelamento Administrativo'
, 'Cancelamento Judicial'
, 'Cancelamento Pedido'
, 'Mobilidade Acadêmica'
, 'Desistência PROVAR'
, 'Desistência Vestibular'
, 'Falecimento'
, 'Mudança de Campus'
, 'Mudança de Turno'
, 'Novo Vestibular'
, 'Descumprimento Edital'
, 'Cancelamento a Pedido do Calouro'
, 'Não Confirmação de Vaga'
, 'Término de Registro Temporário'
, 'Decisão Administrativa']

aprovado = ['Aprovado'
, 'Dispensa de Disciplinas (com nota)'
, 'Dispensa de Disciplinas (sem nota)'
, 'Aprovado sem nota'
, 'Equivalência de Disciplina'
, 'Adiantamento'
, 'Aprov Conhecimento'
, 'Aproveitamento de estudos'
, 'Aprov Adiantamento'
, 'Aproveitamento de Créditos']
fatoMatriculaLista = []

for aluno in alunos:
    sem,created = Semestre.objects.get_or_create(inicioSemestre=aluno.periodo_evasao)
    situacaoEvasao,created = StituacaoEvasao.objects.get_or_create(descricao_evasao=aluno.forma_evasao.descricao_evasao)
    turma,created = Turma.objects.get_or_create(periodo_ingresso=aluno.periodo_ingresso)
    formaIngresso,created = FormaIngresso.objects.get_or_create(descricao_ingresso=aluno.forma_ingresso.descricao_ingresso)
    alu,created = Aluno.objects.get_or_create(grr_aluno=aluno.grr_aluno,turma=turma,forma_ingresso=formaIngresso)
    if(created):
        alu.nome_aluno = aluno.nome_aluno
        alu.save()
    cursoAlu = getCursoAluno(alu.grr_aluno)
    curso,created = Curso.objects.get_or_create(codigo_curso=cursoAlu.codigo_curso)
    if(created):
        curso.descricao_curso = cursoAlu.descricao_curso
        curso.save()
    fatoEvasao = FatoEvasao()
    fatoEvasao.alunoEvasao = alu
    fatoEvasao.situacaoEvasao = situacaoEvasao
    fatoEvasao.cursoEvasao = curso
    fatoEvasao.semestreEvasao = sem
    fatoEvasao.quantidadeRetencoes = countRetencoesAluno(alu.grr_aluno)
    fatoEvasao.ira = calculoIra(alu.grr_aluno)
    if situacaoEvasao.descricao_evasao in evadidosSemConcluirSituacao:
        fatoEvasao.coeficienteEvasao = '1.0'
    else:
        fatoEvasao.coeficienteEvasao = '0.0'
    fatoEvasao.save()

for matricula in matriculas:
    break
    sem,created = Semestre.objects.get_or_create(inicioSemestre=matricula.periodo_matricula)
    situacaoMatricula,created = SituacaoMatricula.objects.get_or_create(descricao_situacao_matricula=matricula.situacao_matricula.descricao_situacao_matricula)
    turma,created = Turma.objects.get_or_create(periodo_ingresso=matricula.aluno.periodo_ingresso)
    formaIngresso,created = FormaIngresso.objects.get_or_create(descricao_ingresso=matricula.aluno.forma_ingresso.descricao_ingresso)
    aluno,created = Aluno.objects.get_or_create(grr_aluno=matricula.aluno.grr_aluno,turma=turma,forma_ingresso=formaIngresso)
    if(created):
        aluno.nome_aluno = matricula.aluno.nome_aluno
        aluno.save()
    disciplina,created = Disciplina.objects.get_or_create(codigo_disciplina=matricula.disciplina.codigo_disciplina)
    if(created):
        disciplina.descricao_disciplina = matricula.disciplina.descricao_disciplina
        disciplina.carga_horaria = matricula.disciplina.carga_horaria
        disciplina.save()
    curso,created = Curso.objects.get_or_create(codigo_curso=matricula.curso.codigo_curso)
    if(created):
        curso.descricao_curso = matricula.curso.descricao_curso
        curso.save()
    if not (curso.disciplinas.filter(codigo_disciplina=disciplina.codigo_disciplina).exists()):
        curso.disciplinas.add(disciplina)
        curso.save()
    fatoMatricula = FatoMatricula()
    fatoMatricula.alunoMatricula = aluno
    fatoMatricula.situacaoMatricula = situacaoMatricula
    fatoMatricula.disciplinaMatricula = disciplina
    fatoMatricula.cursoMatricula = curso
    fatoMatricula.semestreMatricula = sem
    fatoMatricula.faltasMatricula = matricula.faltas_matricula
    fatoMatricula.mediaMatricula = matricula.media_final_matricula
    if situacaoMatricula.descricao_situacao_matricula not in aprovado:
        fatoMatricula.coeficienteRetencao = '1.0'
    else:
        fatoMatricula.coeficienteRetencao = '0.0'
    fatoMatriculaLista.add(fatoMatricula)
    fatoMatricula.save()






#for fato in fatoMatriculaLista
#    FatoMatricula.objects.get_or_create()
    

