# flake8: noqa
# runScript in shell
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc.settings")

import django
django.setup()

# your imports, e.g. Django models
from tccStudentRegistration.models import *
#from tccStudentRegistration.importCSV import *
#from datawarehouseManager.dataMining import *
from datawarehouseManager.models import *

from sklearn.preprocessing import StandardScaler
from pandas import pandas as pd
scaler = StandardScaler()
print("working")

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
, 'Reprov Conhecimento'
, 'Reprov Adiantamento'
, 'Trancamento por amparo Legal'
, 'Isento por Transferência'
, 'Desistência de Vaga'
, 'Processo Administrativo'
, 'Horas']



evadiu = []



#'Reprovado por nota'
#'Reprovado por Frequência'
#'Cancelado'
#'Trancamento Total'
#'Reprovado sem nota'
#'Incompleto'
#'Reprov Conhecimento'
#'Reprov Adiantamento'



fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False,semestreEvasao__isnull=False)
df = pd.DataFrame(list(fatoEvasaoLista.values()))


	#alunoMatricula__isnull=False,
    #situacaoMatricula__isnull=False,
    #disciplinaMatricula__isnull=False,
    #cursoMatricula__isnull=False,
    #semestreMatricula__isnull=False)
listaRetencoes = []
qtdMatriculas = []
retencoesDict = {}
maxCount = 0
for i , j in df.iterrows():
	#print(i,j)
	#print(j["alunoEvasao_id"])
	retencoes = FatoMatricula.objects.filter(alunoMatricula__id=j["alunoEvasao_id"],situacaoMatricula__descricao_situacao_matricula__in=reprovado
		,disciplinaMatricula__isnull=False
		,cursoMatricula__isnull=False
		,semestreMatricula__isnull=False)
	listaDisciplinasReprovadas = []
	qtdMatriculas += [FatoMatricula.objects.filter(alunoMatricula__id=j["alunoEvasao_id"],situacaoMatricula__isnull=False
		,disciplinaMatricula__isnull=False
		,cursoMatricula__isnull=False
		,semestreMatricula__isnull=False).count()]
	count = 0 
	for x in retencoes:
		#if(x.situacaoMatricula.descricao_situacao_matricula in ['Trancamento Total']):
		listaDisciplinasReprovadas += [x.disciplinaMatricula.pk]
		pkDisciplinaMatricula = str(x.disciplinaMatricula.pk)
		if(retencoesDict.get(pkDisciplinaMatricula,0) != 0):
			retencoesDict[pkDisciplinaMatricula] += 1
		else:
			retencoesDict[pkDisciplinaMatricula] = 1
		count+=1
		#print(x.disciplinaMatricula.codigo_disciplina)
	if(count > maxCount):
		maxCount = count
	#print(retencoes)
	
	listaRetencoes += [listaDisciplinasReprovadas]
	#print(listaRetencoes)
	#print(count)

print("qtdMatriculas:")
print(qtdMatriculas)

retencoesFloat = []
for i in listaRetencoes:
	somador = 0
	for j in i:
		somador += retencoesDict[str(j)]
	retencoesFloat += [somador]

mask = df.situacaoEvasao_id != 1
column_name = 'situacaoEvasao_id'
df.loc[mask, column_name] = 3
		
			


df = df.drop("coeficienteEvasao",axis=1)
df = df.drop("alunoEvasao_id",axis=1)
df = df.drop("cursoEvasao_id",axis=1)
df = df.drop("semestreEvasao_id",axis=1)
df = df.drop("quantidadeEvasao",axis=1)

df = df.drop("id",axis=1)
#df['Retencoes'] = retencoesFloat
df['qtdMatriculas'] = qtdMatriculas

mask = df.situacaoEvasao_id != 1
column_name = 'situacaoEvasao_id'
df.loc[mask, column_name] = 3
#df = df.astype({"Retencoes": float})
print(df)
#df.


#print(df)
variavelqqr = df.drop("situacaoEvasao_id",axis=1)
print("variavel qqr = " , variavelqqr)
print(variavelqqr.shape)
print("df shape = ", df.shape )#.astype({"Retencoes": float})
scaler.fit(variavelqqr)
scaled_features = scaler.transform(variavelqqr)#.astype({"Retencoes": float}))
print("Scaled features", scaled_features)
df_feat = pd.DataFrame(scaled_features,columns=['quantidadeRetencoes','ira','qtdMatriculas'])#,'Retencoes'
print(df_feat)

from sklearn.model_selection import train_test_split
x = df_feat
y = df['situacaoEvasao_id']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=42)
from sklearn.neighbors import KNeighborsClassifier

knn = KNeighborsClassifier(n_neighbors=1)
knn.fit(x_train,y_train)

pred = knn.predict(x_test)

print(pred)


from sklearn.metrics import classification_report,confusion_matrix

print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))



