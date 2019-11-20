from tccStudentRegistration.models import *
from datawarehouseManager.dataMining import *
from tccStudentRegistration.PredictionFacade import *
from datawarehouseManager.dbManager import *
import threading
import time


class ImportDataFacade(object):
    """docstring for ImportDataFacade"""
    def __init__(self, arg):
        super(ImportDataFacade, self).__init__()
        self.arg = arg
    
    @staticmethod
    def __importHistorico(path=""):
        importador = ImportHistorico()
        importador.importHistorico(path)

    @staticmethod
    def updateTipoEvasao(path):
        if(path):
            importador = ImportTipoEvasao()
            importador.getDictionary(path)

    @staticmethod
    def updateTipoIngresso(path):
        if(path):
            importador = ImportTipoIngresso()
            importador.getDictionary(path)

    @staticmethod
    def updateSituacaoDisciplina(path):
        if(path):
            importador = ImportSituacaoDisciplina()
            importador.getDictionary(path)

    @staticmethod
    def __mineData():
        dm = DataMining()
        dm.insertFatoEvasao()
        dm.insertFatoMatricula()
        dm.updateFatoEvasao()
        dm.updateFatoMatricula()

    @staticmethod
    def __deleteAlunosEvasao(): 
        #Deleta alunos que já evadiram no banco 1
        deleteAlunosEvadiram()

    @staticmethod
    def makePredictions(classifierName="MLP"):
        PredictionFacade.updatePrediction(classifierName)

    @staticmethod
    def __importNewData(path="",classifierName="MLP"):
        ImportDataFacade.__importHistorico(path)
        ImportDataFacade.__deleteOldDWData()
        ImportDataFacade.__mineData()
        ImportDataFacade.__deleteAlunosEvasao()
        ImportDataFacade.makePredictions(classifierName)
        
    @staticmethod
    def importNewData(path="",classifierName="MLP"):
        thread = threading.Thread(target=ImportDataFacade.__importNewData, args=(path,classifierName))
        thread.daemon = True #Faz ser possivel interromper o servidor enquanto essa thread estiver rodando
        thread.start()
    
        
  
    @staticmethod
    def __deleteOldDWData():
        dm = DataMining()
        dm.clearData()



#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()