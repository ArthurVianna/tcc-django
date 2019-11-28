# flake8: noqa
from tccStudentRegistration.models import *
from datawarehouseManager.dataMining import *
from tccStudentRegistration.PredictionFacade import *
from tccStudentRegistration.importCSV import *
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
    def importNewData(path="",classifierName="MLP"):
        print("Start")
        ImportDataFacade.__importHistorico(path)
        ImportDataFacade.__deleteOldDWData()
        ImportDataFacade.__mineData()
        ImportDataFacade.__deleteAlunosEvasao()
        ImportDataFacade.makePredictions(classifierName)

    @staticmethod
    def importNewDataThread(path="",classifierName="MLP"):
        thread = threading.Thread(target=ImportDataFacade.importNewData, args=(path,classifierName))
        thread.daemon = True #Faz ser possivel interromper o servidor enquanto essa thread estiver rodando
        thread.start()


    @staticmethod
    def __deleteOldDWData():
        dm = DataMining()
        dm.clearData()

    @staticmethod
    def validateFile(path=""):
        vh = ValidateHistorico()
        return vh.validateHistorico(path)

    @staticmethod
    def testSomething(path="",classifierName=""):
        dm = DataMining()
        deleteFatoEvasaoNull()
        dm.insertFatoEvasao()
        dm.updateFatoEvasao()


    @staticmethod
    def testSomething2(path="",classifierName=""):
        alunosFormados = Aluno.objects.filter(forma_evasao=FormaEvasao.objects.get(descricao_evasao='Formatura'))
        print(alunosFormados.count())
        formadosPeriodizados = 0
        for aluno in alunosFormados:
            semestres = getQtdSemestres(aluno.grr_aluno)
            #print(semestres)
            if(semestres <= 6):
                formadosPeriodizados+=1
        print(formadosPeriodizados)





#from tccStudentRegistration.importCSV import *
#importHistorico = ImportHistorico()
#importHistorico.importHistorico()
