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

print("Start For")
retencoesFloat = []
porcentagemMatriculaAprovado = []
for index,i in enumerate(listaRetencoes):
	#print("Index : " + str(index))
	qtdR = df.quantidadeRetencoes[index]
	#print("QTDR : "+str(qtdR))
	qtdM = qtdMatriculas[index]
	#print("QTDM : "+str(qtdM))


	porcentagemMatriculaAprovado += [(qtdR / qtdM)]
	somador = 0
	for j in i:
		somador += retencoesDict[str(j)]
	retencoesFloat += [somador]

mask = df.situacaoEvasao_id != 1
column_name = 'situacaoEvasao_id'
df.loc[mask, column_name] = 3
print(porcentagemMatriculaAprovado)




df = df.drop("coeficienteEvasao",axis=1)
df = df.drop("alunoEvasao_id",axis=1)
df = df.drop("cursoEvasao_id",axis=1)
df = df.drop("semestreEvasao_id",axis=1)
df = df.drop("quantidadeEvasao",axis=1)

df = df.drop("id",axis=1)
df = df.drop("quantidadeRetencoes",axis=1)
#df['Retencoes'] = retencoesFloat
df['qtdMatriculas'] = porcentagemMatriculaAprovado

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
df_feat = pd.DataFrame(scaled_features,columns=['ira','qtdMatriculas'])#,'Retencoes'
print(df_feat)

from sklearn.model_selection import train_test_split
x = df_feat
y = df['situacaoEvasao_id']

x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=50)
from sklearn.neighbors import KNeighborsClassifier
#KNN
from sklearn import tree
#Decision tree
from sklearn.naive_bayes import GaussianNB
#Gaussian Processes - naive bayes
from sklearn.neural_network import MLPClassifier
#Multi-layer Perceptron NNM(Neural network models)

knn = KNeighborsClassifier(n_neighbors=3)
knn.fit(x_train,y_train)

gnb = GaussianNB()
gnbFit = gnb.fit(x_train, y_train)

clf = tree.DecisionTreeClassifier()
clf = clf.fit(x_train, y_train)


#clfMLPTest = MLPClassifier(activation='relu',alpha=0.01,hidden_layer_sizes=(50, 100, 50),learning_rate='adaptive',solver='adam',max_iter=100)#solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=0





parameters_using = {
	'activation': 'relu', 'alpha': 0.05, 'hidden_layer_sizes': (50, 100, 50), 'learning_rate': 'adaptive', 'solver': 'adam',
	'activation': 'relu', 'alpha': 0.0001, 'hidden_layer_sizes': (50, 50, 50), 'learning_rate': 'constant', 'solver': 'adam',
	'activation': 'logistic', 'alpha': 0.01, 'hidden_layer_sizes': (50, 50, 50), 'learning_rate': 'adaptive', 'solver': 'sgd', #0.52
	'activation': 'relu', 'alpha': 0.001, 'hidden_layer_sizes': (50, 100, 50), 'learning_rate': 'constant', 'solver': 'adam'
}

clfMLPTest = MLPClassifier(max_iter=100,activation='relu',alpha=0.001,hidden_layer_sizes=(50,100,50),learning_rate='constant',solver='adam')
clfMLPTest = clfMLPTest.fit(x_train, y_train)
parameter_space = {
    'hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
    'activation': ['tanh', 'relu','identity','logistic'],
    'solver': ['sgd', 'adam','lbfgs'],
    'alpha': [0.00001,0.0001,0.001,0.01,0.1],
    'learning_rate': ['constant','adaptive'],
    #'learning_rate_init' :[0.001,0.01,0.1,0.0001],
    'power_t' : [0.5,0.1,0.9],
    #'shuffle ' : [True,False]

}

#mlp = MLPClassifier(max_iter=100)
#from sklearn.model_selection import GridSearchCV

#clfMLP = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=3)
#clfMLP = clfMLP.fit(x_train, y_train)

# Best paramete set
#print('Best parameters found:\n', clfMLP.best_params_)

# All results
#means = clfMLP.cv_results_['mean_test_score']
#stds = clfMLP.cv_results_['std_test_score']
#for mean, std, params in zip(means, stds, clfMLP.cv_results_['params']):
    #print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

predTree = clf.predict(x_test)
pred = knn.predict(x_test)
predGNB = gnbFit.predict(x_test)
clfMLPTest = clfMLPTest.predict(x_test)

#print(pred)

#print(predTree)


from sklearn.metrics import classification_report,confusion_matrix

print("KNN :")
print(confusion_matrix(y_test,pred))
print(classification_report(y_test,pred))
print("PredTree :")
print(confusion_matrix(y_test,predTree))
print(classification_report(y_test,predTree))
#tree.plot_tree(clf.fit(x_train, y_train))
print("GNB :")
print(confusion_matrix(y_test,predGNB))
print(classification_report(y_test,predGNB))
print("MLP :")
print(confusion_matrix(y_test,clfMLPTest))
print(classification_report(y_test,clfMLPTest))
