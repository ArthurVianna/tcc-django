# flake8: noqa
# runScript in shell
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc.settings")

import django
django.setup()

# your imports, e.g. Django models
from tccStudentRegistration.models import *


#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()

#from datawarehouseManager.dataMining import *


#dm = DataMining()
#print("StartFatoEvasao")
#dm.updateFatoEvasao()
#print("StartFatoMatricula")
#dm.updateFatoMatriculaFact()

from datawarehouseManager.models import *



from pandas import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
#KNN
from sklearn.neighbors import KNeighborsClassifier
#Decision tree
from sklearn import tree
#Gaussian Processes - naive bayes
from sklearn.naive_bayes import GaussianNB
#Multi-layer Perceptron NNM(Neural network models)
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import classification_report,confusion_matrix

class Predict(object):
    """docstring for Predict"""
    def __init__(self):
        super(Predict, self).__init__()

    def GetDadosEvasao(self):
        fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False,semestreEvasao__isnull=False).order_by('alunoEvasao__id')
        aux = fatoEvasaoLista.values('alunoEvasao__id')
        aux = [d['alunoEvasao__id'] for d in aux if 'alunoEvasao__id' in d]
        #print(aux)
        retencoes = FatoMatricula.objects.filter(alunoMatricula__id__in=aux,situacaoMatricula__isnull=True
                ,disciplinaMatricula__isnull=True
                ,cursoMatricula__isnull=True#isnull=True#
                ,semestreMatricula__isnull=True).order_by('alunoMatricula__id')

        perMatApro = [d['coeficienteRetencao'] for d in retencoes.values('coeficienteRetencao')]
        df = pd.DataFrame(list(fatoEvasaoLista.values()))
        df = df.drop("coeficienteEvasao",axis=1)
        df = df.drop("alunoEvasao_id",axis=1)
        df = df.drop("cursoEvasao_id",axis=1)
        df = df.drop("semestreEvasao_id",axis=1)
        df = df.drop("quantidadeEvasao",axis=1)

        df = df.drop("id",axis=1)
        df = df.drop("quantidadeRetencoes",axis=1)

        df['porcentagemNaoRetido'] = perMatApro

        mask = df.situacaoEvasao_id != 1
        column_name = 'situacaoEvasao_id'
        df.loc[mask, column_name] = 3

        return df

    def scaleDF(self,df):
        scaler = StandardScaler()

        scaled_features = scaler.fit_transform(df.drop("situacaoEvasao_id",axis=1))
        #print("Scaled features", scaled_features)
        df_feat = pd.DataFrame(scaled_features,columns=['ira','porcentagemNaoRetido'])#,'Retencoes'
        return df_feat


    def getResultFromDF(self,df):
        return df['situacaoEvasao_id']
    def trainTestSplit(self,x,y):
        #x = df_feat
        #y = df['situacaoEvasao_id']
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=50)
        return x_train,x_test,y_train,y_test


    def testPrediction(self,df):
        dfScaled = predClass.scaleDF(df)
        x_train,x_test,y_train,y_test = predClass.trainTestSplit(dfScaled,predClass.getResultFromDF(df))
        fittedMLP = predClass.fitMLP(x_train,y_train)
        prediction = predClass.predict(fittedMLP,x_test)

        print(predClass.predictConfusionMatrix(prediction,y_test))
        print(predClass.predictClassificationReport(prediction,y_test))
    def fitKNN(self,x,y,n_neigh=1):
        #Default 1 neighbor
        knn = KNeighborsClassifier(n_neighbors=n_neigh)
        knn = knn.fit(x,y)
        return knn

    def fitGNB(self,x,y):
        gnb = GaussianNB()
        gnb = gnb.fit(x, y)
        return gnb

    def fitDecisionTree(self,x,y):
        decisionT = tree.DecisionTreeClassifier()
        decisionT = decisionT.fit(x_train, y_train)
        return decisionT

    def fitMLP(self,x,y):
        mlpTest = MLPClassifier(max_iter=100,activation='relu',alpha=0.001,hidden_layer_sizes=(50,100,50),learning_rate='constant',solver='adam')
        mlpTest = mlpTest.fit(x, y)
        return mlpTest

    def predict(self,classifier,df):
        return classifier.predict(df)

    def predictConfusionMatrix(self, prediction, result):
        return confusion_matrix(result,prediction)

    def predictClassificationReport(self, prediction, result):
        return classification_report(result,prediction)


#clfMLPTest = MLPClassifier(activation='relu',alpha=0.01,hidden_layer_sizes=(50, 100, 50),learning_rate='adaptive',solver='adam',max_iter=100)#solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=0


predClass = Predict()
df = predClass.GetDadosEvasao()
predClass.testPrediction(df)



#Script to find the best mlp config

#from sklearn.model_selection import GridSearchCV
#parameter_space = {
#    'hidden_layer_sizes': [(50,50,50), (50,100,50), (100,)],
#    'activation': ['tanh', 'relu','identity','logistic'],
#    'solver': ['sgd', 'adam','lbfgs'],
#    'alpha': [0.00001,0.0001,0.001,0.01,0.1],
#    'learning_rate': ['constant','adaptive'],
#    #'learning_rate_init' :[0.001,0.01,0.1,0.0001],
#    'power_t' : [0.5,0.1,0.9],
#    #'shuffle ' : [True,False]
#}


#clfMLP = GridSearchCV(mlp, parameter_space, n_jobs=-1, cv=3)
#clfMLP = clfMLP.fit(x_train, y_train)

# Best paramete set
#print('Best parameters found:\n', clfMLP.best_params_)

# All results
#means = clfMLP.cv_results_['mean_test_score']
#stds = clfMLP.cv_results_['std_test_score']
#for mean, std, params in zip(means, stds, clfMLP.cv_results_['params']):
    #print("%0.3f (+/-%0.03f) for %r" % (mean, std * 2, params))

#predTree = clf.predict(x_test)
#pred = knn.predict(x_test)
#predGNB = gnbFit.predict(x_test)
#predMLP = clfMLPTest.predict(x_test)

#print(pred)

#print(predTree)




#print("KNN :")
#print(confusion_matrix(y_test,pred))
#print(classification_report(y_test,pred))
#print("PredTree :")
#print(confusion_matrix(y_test,predTree))
#print(classification_report(y_test,predTree))
#tree.plot_tree(clf.fit(x_train, y_train))
#print("GNB :")
#print(confusion_matrix(y_test,predGNB))
#print(classification_report(y_test,predGNB))







#from django.db import models
print("Ready")

#class studentRegistrationConfig(models.Model):
#   """docstring for studentRegistrationConfig"""
#   evasaoPath= models.CharField()


#test = studentRegistrationConfig()
#test.evasaoPath = "tccStudentRegistration/evasao.csv"

#from django.core import serializers
#data = serializers.serialize("json", test)

#print(data.getValue())
