# flake8: noqa
from datawarehouseManager.dbManager import *
from tccStudentRegistration.Predict import *
from tccStudentRegistration.models import *
from datetime import date

class PredictionFacade(object):
    """docstring for PredictionFacade"""
    def __init__(self, arg):
        super(PredictionFacade, self).__init__()
        self.arg = arg

    @staticmethod
    def updatePrediction(classifierName):
        predClass = Predict()
        dfAlunos = PredictionFacade.getDFAlunosMatriculados()
        df = dfAlunos.drop("grr",axis=1)
        scaler = predClass.getScaler()

        fittedMLP = predClass.getClassifier(classifierName)
        scaledDF = pd.DataFrame(scaler.transform(df),columns=['ira','porcentagemRetido'])

        prediction = predClass.predict(fittedMLP,scaledDF)
        resultadoPredicaoDic = {}
        today = date.today()

        for index,row in dfAlunos.iterrows():
            predicao = PredicaoEvasao()
            #print("Grr = " + str(row['grr']) + " - ira = " + str(row['ira']) + " - %Retido = " + str(row['porcentagemRetido']) + " - predicao = " + str(prediction[index]))
            if prediction[index] not in resultadoPredicaoDic:
                resultadoPredicaoDic[prediction[index]] = FormaEvasao.objects.get(descricao_evasao=predClass.getSituacaoEvasaoById(prediction[index]).descricao_evasao)
            predicao.forma_evasao = resultadoPredicaoDic[prediction[index]]
            predicao.aluno = Aluno.objects.get(grr_aluno=str(row['grr']))
            predicao.script_predicao = classifierName
            predicao.periodo_predicao = today
            #print(predicao)
            predicao.save()

    @staticmethod
    def getDFAlunosMatriculados():
        alunosNaoEvadiram = Aluno.objects.filter(forma_evasao=FormaEvasao.objects.get(descricao_evasao='Sem evasão')).exclude(periodo_ingresso=getLatestIngresso()).order_by('grr_aluno').values()
        grr = []
        ira = []
        porcentagemRetencao = []
        #print(alunosNaoEvadiram)
        for aluno in alunosNaoEvadiram:
            grr += [aluno['grr_aluno']]
            ira += [calculoIra(aluno['grr_aluno'])]
            porcentagemRetencao += [countRetencoesAluno(aluno['grr_aluno'])/countMatriculasAluno(aluno['grr_aluno'])]

        data = list(zip(grr, ira, porcentagemRetencao))

        df = pd.DataFrame(data, columns = ['grr', 'ira', 'porcentagemRetido'])

        return df
