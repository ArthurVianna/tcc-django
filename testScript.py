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


#from datawarehouseManager.dataMining import *

#dm = DataMining()
#print("StartFatoEvasao")
#dm.updateFatoEvasao()
#print("StartFatoMatricula")
#dm.updateFatoMatriculaFact()



#clfMLPTest = MLPClassifier(activation='relu',alpha=0.01,hidden_layer_sizes=(50, 100, 50),learning_rate='adaptive',solver='adam',max_iter=100)#solver='lbfgs', alpha=1e-5,hidden_layer_sizes=(5, 2), random_state=0

#from tccStudentRegistration.Predict import *
#predClass = Predict()
#df = predClass.getDadosEvasao()
#predClass.testPrediction(df)


from tccStudentRegistration.ImportDataFacade import *
ImportDataFacade.testSomething()
#ImportDataFacade.testSomething2()
#from datawarehouseManager.dbManager import *

#print(str(getQtdSemestres('2ce8b81062010b3b8fa3379f93f1cc39')))
#ImportDataFacade.testSomething()


