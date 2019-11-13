# flake8: noqa
# runScript in shell
import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "tcc.settings")

import django
django.setup()

# your imports, e.g. Django models
#from tccStudentRegistration.models import *


#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()

from datawarehouseManager.dataMining import *


#dm = DataMining()
#print("StartFatoEvasao")
#dm.updateFatoEvasao()
#print("StartFatoMatricula")
#dm.updateFatoMatriculaFact()

#clfMLPTest = MLPClassifier(activation='relu',alpha=0.01,hidden_layer_sizes=(50, 100, 50),learning_rate='adaptive',solver='adam',max_iter=100)#solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=0


#predClass = Predict()
#df = predClass.getDadosEvasao()
#predClass.testPrediction(df)


from tccStudentRegistration.PredictionFacade import *

PredictionFacade.updatePrediction("KNN")


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
