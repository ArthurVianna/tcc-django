from tccStudentRegistration.models import *
from datawarehouseManager.dataMining import *
from tccStudentRegistration.PredictionFacade import *

class ImportDataFacade(object):
    """docstring for ImportDataFacade"""
    def __init__(self, arg):
        super(ImportDataFacade, self).__init__()
        self.arg = arg
    
    @staticmethod
    def importCSV(path=""):
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
    def mineData():
        dm = DataMining()
        dm.updateFatoEvasao()
        dm.updateFatoMatricula()

    @staticmethod
    def makePredictions(classifierName="MLP"):
        PredictionFacade.updatePrediction(classifierName)

    @staticmethod
    def importingDoingEveryProcedure(path="",classifierName="MLP"):
        ImportDataFacade.importCSV(path)
        ImportDataFacade.mineData()
        ImportDataFacade.makePredictions(classifierName)

#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()