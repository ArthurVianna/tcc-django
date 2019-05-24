# flake8: noqa
from pandas import pandas as pd
from tccStudentRegistration.models import *
from datetime import datetime
# data = pd.read_csv("src/main/db/csv/historico.csv")

class importCSV(object):
	"""docstring for importCSV"""
	def __init__(self):
		super(importCSV, self).__init__()

	def getCSVData(self,path):
		return pd.read_csv(path)

importcsv = importCSV()
historico = importcsv.getCSVData("tccStudentRegistration"+"/" + "historico.csv")
evasao = importcsv.getCSVData("tccStudentRegistration/evasao.csv")
ingresso = importcsv.getCSVData("tccStudentRegistration/ingresso.csv")
situacaoDisciplina = importcsv.getCSVData("tccStudentRegistration/situacaoDisciplina.csv")
# print(historico)
# print(evasao)
# print(ingresso)
# print(situacaoDisciplina)
evasaoDic = {}
for index, row in evasao.iterrows():
	if(row[3] == 'S' and row[1] != 0):
		tempEvasao,created = FormaEvasao.objects.get_or_create(descricao_evasao=row[2])
		evasaoDic[row[1]] = tempEvasao

ingressoDic = {}
for index, row in ingresso.iterrows():
	if(row[3] == 'S' and row[1] != 0):
		tempIngresso,created = FormaIngresso.objects.get_or_create(descricao_ingresso=row[2])
		ingressoDic[row[1]] = tempIngresso
# print(evasaoDic)
listaDadosAlunos = ["MATR_ALUNO","ID_ALUNO","PERIODO_INGRE_ITEM","PERIODO_EVA_ITEM","ANO_INGRESSO","ANO_EVASAO","FORMA_EVASAO_ITEM","FORMA_INGRE_ITEM"]
dfAlunos = historico[listaDadosAlunos].groupby(["MATR_ALUNO"]).min()
alunoDic = {}
for index, row in dfAlunos.iterrows():
	aluno,created = Aluno.objects.get_or_create(grr_aluno=row.name,
		defaults={
			"periodo_ingresso":datetime(2019,1,1),
			"forma_ingresso":ingressoDic[2]
		})
	# if(created):
	aluno.nome_aluno = row["ID_ALUNO"]
	if(row["PERIODO_INGRE_ITEM"] == 201):
		mesIngresso = 1
	else:
		mesIngresso = 7
	if(row["PERIODO_EVA_ITEM"] == 202):
		mesEvasao = 7
	else:
		mesEvasao = 1
	aluno.periodo_ingresso = datetime(row["ANO_INGRESSO"],mesIngresso,1)
	aluno.forma_ingresso = ingressoDic[row["FORMA_INGRE_ITEM"]]
	if(row["ANO_EVASAO"] > 0):
		aluno.periodo_evasao = datetime(row["ANO_EVASAO"],mesEvasao,1)
	aluno.forma_evasao = evasaoDic[row["FORMA_EVASAO_ITEM"]]
	alunoDic[row.name] = aluno
	aluno.save()

listaDadosDisciplina = ["COD_ATIV_CURRIC","NOME_ATIV_CURRIC","CH_TOTAL"]
dfDisciplinas = historico[listaDadosDisciplina].groupby(["COD_ATIV_CURRIC"]).max()
disciplinaDic = {}
for index, row in dfDisciplinas.iterrows():
    disciplina,created = Disciplina.objects.get_or_create(codigo_disciplina=row.name)
    disciplina.descricao_disciplina = row["NOME_ATIV_CURRIC"]
    disciplina.carga_horaria = row["CH_TOTAL"]
    disciplinaDic[row.name] = disciplina
    disciplina.save()


listaDadosCursoDisciplina = listaDadosDisciplina + ["COD_CURSO"]
dfCursos = historico[["COD_CURSO"]].groupby(["COD_CURSO"]).min()
cursoDic = {}
for index, row in dfCursos.iterrows():
    curso,created = Curso.objects.get_or_create(codigo_curso=row.name)
    # if(created):
    dfCursosDisciplinas = historico[listaDadosCursoDisciplina].where(historico["COD_CURSO"]==row.name).groupby(["COD_CURSO","COD_ATIV_CURRIC"]).max()
    for index2, row2 in dfCursosDisciplinas.iterrows():
        curso.disciplinas.add(disciplinaDic[row2.name[1]])
    cursoDic[row.name] = curso
    curso.save()



situacaoDisciDic = {}
for index, row in situacaoDisciplina.iterrows():
    if(row[3] == 'S' and row[1] != 0):
        tempSituacao,created = SituacaoMatricula.objects.get_or_create(descricao_situacao_matricula=row[2])
        situacaoDisciDic[row[1]] = tempSituacao
# id, media_final_matricula, faltas_matricula, periodo_matricula, situacao_matricula_id, aluno_id, disciplina_id

for index, row in historico.iterrows():
    if(row["PERIODO_ITEM"] == 201):
        mesMatricula = 1
    else:
        mesMatricula = 7
    matricula = Matricula.objects.get_or_create(
        situacao_matricula=situacaoDisciDic[row["SITUACAO_ITEM"]],
        aluno=alunoDic[row["MATR_ALUNO"]],
        disciplina=disciplinaDic[row["COD_ATIV_CURRIC"]],
        periodo_matricula=datetime(row["ANO"],mesMatricula,1),
        curso=cursoDic[row["COD_CURSO"]],
        media_final_matricula=row["MEDIA_FINAL"],
        faltas_matricula=row["NUM_FALTAS"]
        )


# print(aluno)
# aluno.save()

# test = FormaEvasao()
# test.descricao_evasao = "Testing"
# print(test.descricao_evasao)
# test.save()
# print(historico)
# filtera = historico["FORMA_EVASAO_ITEM"]=="26"

# print(historico)
# df = historico.groupby(["FORMA_EVASAO_ITEM","MATR_ALUNO"]).count()
# for index, row in df.iterrows():
# 	print(row[0],row[3])
# print(df)

# sorting dataframe
# df.sort_values("FORMA_EVASAO_ITEM", inplace = True)

# print(df.keys())

# filtera = df.index["FORMA_EVASAO_ITEM"]=="26"

# filtering data
# df.where(filtera, inplace = True)

# display
# df

# print(df)
