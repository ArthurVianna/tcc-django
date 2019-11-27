# flake8: noqa
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
from datetime import date
from joblib import dump, load
import os

class Predict(object):
    """docstring for Predict"""

    dadosEvasao = None
    def __init__(self):
        super(Predict, self).__init__()

    def getDadosEvasao(self):
        if(self.dadosEvasao is not None):
            return self.dadosEvasao
        fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False,semestreEvasao__isnull=False).order_by('alunoEvasao__id')
        aux = fatoEvasaoLista.values('alunoEvasao__id')
        aux = [d['alunoEvasao__id'] for d in aux if 'alunoEvasao__id' in d]
        #print(aux)
        retencoes = FatoMatricula.objects.filter(alunoMatricula__id__in=aux,situacaoMatricula__isnull=True
                ,disciplinaMatricula__isnull=True
                ,cursoMatricula__isnull=True#isnull=True#
                ,semestreMatricula__isnull=True).order_by('alunoMatricula__id')

        perMatApro = [d['coeficienteReprovacao'] for d in retencoes.values('coeficienteReprovacao')]
        df = pd.DataFrame(list(fatoEvasaoLista.values()))
        df = df.drop("coeficienteEvasao",axis=1)
        df = df.drop("alunoEvasao_id",axis=1)
        df = df.drop("cursoEvasao_id",axis=1)
        df = df.drop("semestreEvasao_id",axis=1)
        df = df.drop("quantidadeEvasao",axis=1)
        df = df.drop("coeficienteRetencao",axis=1)
        df = df.drop("semestresCursados",axis=1)

        df = df.drop("id",axis=1)
        df = df.drop("quantidadeRetencoes",axis=1)

        df['porcentagemRetido'] = perMatApro

        mask = df.situacaoEvasao_id != 1
        column_name = 'situacaoEvasao_id'
        df.loc[mask, column_name] = 3
        self.dadosEvasao = df
        return self.dadosEvasao

    def scaleDF(self,df):
        scaler = StandardScaler()

        scaled_features = scaler.fit_transform(df.drop("situacaoEvasao_id",axis=1))
        #print("Scaled features", scaled_features)
        df_feat = pd.DataFrame(scaled_features,columns=['ira','porcentagemRetido'])#,'Retencoes'
        return df_feat


    def getResultFromDF(self,df):
        return df['situacaoEvasao_id']
    def trainTestSplit(self,x,y):
        #x = df_feat
        #y = df['situacaoEvasao_id']
        x_train,x_test,y_train,y_test = train_test_split(x,y,test_size=0.3,random_state=50)
        return x_train,x_test,y_train,y_test


    def testPrediction(self,df):
        predClass = self
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
        mlpTest = MLPClassifier(max_iter=200,activation='relu',alpha=0.001,hidden_layer_sizes=(50,100,50),learning_rate='constant',solver='adam')
        mlpTest = mlpTest.fit(x, y)
        return mlpTest

    def getClassifierFit(self,classifierName):
        switcher = {
            "KNN" : self.fitKNN,
            "MLP": self.fitMLP,
            "DecisionTree": self.fitDecisionTree,
            "GNB": self.fitGNB,
        }
        method =  switcher.get(classifierName,None)
        if(method == None):
            print("Could not find the classifier name : " + str(classifierName))
        return method

    def getClassifier(self,classifierName):
        classifier = self.loadClassifierFromFile(classifierName)
        if(classifier == None):
            classifierFitMethod = self.getClassifierFit(classifierName)
            if(classifierFitMethod == None):
                print("Could not find classifier fit method")
                return None
            df = self.getDadosEvasao()
            scaler = self.getScaler()
            scaledDF = scaler.transform(df.drop("situacaoEvasao_id",axis=1))
            classifier = classifierFitMethod(scaledDF,df['situacaoEvasao_id'])
            self.saveClassifierToFile(classifier,classifierName)
        return classifier

    def predict(self,classifier,df):
        return classifier.predict(df)

    def predictConfusionMatrix(self, prediction, result):
        return confusion_matrix(result,prediction)

    def predictClassificationReport(self, prediction, result):
        return classification_report(result,prediction)

    def saveScalerFile(self,scaler):
        path = self.getPathFromCurrentDate()
        fileName = '/scaler.joblib'
        dump(scaler,path + fileName)

    def getScaler(self):
        path = self.getPathFromCurrentDate()
        fileName = '/scaler.joblib'
        if(os.path.exists(path + fileName)):
            return load(path + fileName)
        else:
            return self.createScaler(self.getDadosEvasao())

    def createScaler(self,df):
        scaler = StandardScaler()
        scaler = scaler.fit(df.drop("situacaoEvasao_id",axis=1))
        self.saveScalerFile(scaler)
        return scaler

    def saveClassifierToFile(self,classifier,classifierName):
        path = self.getPathFromCurrentDate()
        fileName = '/classifier_' + str(classifierName) + '.joblib'
        dump(classifier, path + fileName)

    def loadClassifierFromFile(self,classifierName):
        path = self.getPathFromCurrentDate()
        fileName  = '/classifier_' + str(classifierName) + '.joblib'
        if(os.path.exists(path + fileName)):
            return load(path + fileName)
        return None

    def getPathFromCurrentDate(self):
        today = date.today()
        year = today.year
        semestre = ""
        if(today.month >= 7):
            semestre = "2Semestre"
        else:
            semesrte = "1Semestre"
        path = 'SkLearnFiles/'+str(year) + '/' + semestre
        if(os.path.exists(path) == False):
            os.makedirs(path)
        return path

    def getSituacaoEvasaoById(self,pk):
        situacao = StituacaoEvasao.objects.get(pk=pk)
        return situacao
