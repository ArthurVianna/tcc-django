from tccStudentRegistration.models import *
from datawarehouseManager.dataMining import *
from tccStudentRegistration.PredictionFacade import *
from datawarehouseManager.dbManager import *

class ImportDataFacade(object):
    """docstring for ImportDataFacade"""
    def __init__(self, arg):
        super(ImportDataFacade, self).__init__()
        self.arg = arg
    
    @staticmethod
    def __importCSV(path=""):
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
    def importNewData(path="",classifierName="MLP"):
        ImportDataFacade.__importCSV(path)
        ImportDataFacade.__deleteOldDWData()
        ImportDataFacade.__mineData()
        ImportDataFacade.__deleteAlunosEvasao()
        ImportDataFacade.makePredictions(classifierName)
  
    @staticmethod
    def __deleteOldDWData():
        dm = DataMining()
        dm.clearData()



#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()