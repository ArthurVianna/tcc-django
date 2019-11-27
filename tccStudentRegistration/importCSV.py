# flake8: noqa
from pandas import pandas as pd
from tccStudentRegistration.models import *
from datetime import datetime
import csv
# data = pd.read_csv("src/main/db/csv/historico.csv")

class ImportCSV(object):
    """docstring for ImportCSV"""
    def __init__(self):
        super(ImportCSV, self).__init__()

    def getCSVData(self,path):
        return pd.read_csv(path)

class ImportModel(object):

    defaultModel = None
    defaultKwargs = None
    defaultPath = ""
    def __init__(self):
        super(ImportModel, self).__init__()

    def getModelList(self):
        modelList = self.defaultModel.objects.all()
        if(modelList.count() == 0):
            self.updateModelList(self.getFromCsv(self.defaultPath))
            modelList = self.defaultModel.objects.all()
        return modelList

    def getFromCsv(self,path):
        importcsv = ImportCSV()
        return importcsv.getCSVData(path)

    def updateModelList(self,csvImported):
        importcsv = ImportCSV()
        for index, row in csvImported.iterrows():
            if(row["IND_ATIVO"] == 'S' and row["ITEM_TABELA"] != 0):
                tempEvasao,created = self.defaultModel.objects.get_or_create(**self.createKwarg(row))
                if not created:
                    tempEvasao.cod_tabela = row["ITEM_TABELA"]
                    tempEvasao.save()


    def createKwarg(self,row):
        newKwarg = {}
        for key,values in self.defaultKwargs.items():
            if "descricao" in key:
                newKwarg[key] = row["DESCRICAO"]
            else:
                newKwarg[key] = row["ITEM_TABELA"]
        #print(newKwarg)
        return newKwarg



class ImportTipoEvasao(ImportModel):

    CONST_TIPO_EVASAO_DEFAULT_PATH = "tccStudentRegistration/evasao.csv"
    
    def __init__(self):
        self.defaultModel = FormaEvasao
        self.defaultKwargs = {"descricao_evasao" : "row[\"DESCRICAO\"]", "cod_tabela" : "row[\"ITEM_TABELA\"]"}
        self.defaultPath = self.CONST_TIPO_EVASAO_DEFAULT_PATH
        super(ImportModel, self).__init__()

    def buildDictionary(self,modelList):
        dictionary = {}
        for obj in modelList:
            dictionary[obj.cod_tabela] = obj
        return dictionary
    def getDictionary(self, path=""):
        if(path):
            self.updateModelList(self.getFromCsv(path))
        return self.buildDictionary(self.getModelList())




class ImportTipoIngresso(ImportModel):
    CONST_TIPO_IGRESSO_DEFAULT_PATH = "tccStudentRegistration/ingresso.csv"
    
    def __init__(self):
        self.defaultModel = FormaIngresso
        self.defaultKwargs = {"descricao_ingresso" : "row[\"DESCRICAO\"]", "cod_tabela" : "row[\"ITEM_TABELA\"]"}
        self.defaultPath = self.CONST_TIPO_IGRESSO_DEFAULT_PATH
        super(ImportModel, self).__init__()

    def buildDictionary(self,modelList):
        dictionary = {}
        for obj in modelList:
            dictionary[obj.cod_tabela] = obj
        return dictionary
    def getDictionary(self, path=""):
        if(path):
            self.updateModelList(self.getFromCsv(path))
        return self.buildDictionary(self.getModelList())


class ImportSituacaoDisciplina(ImportModel):
    CONST_SITUACAO_DISCIPLINA_DEFAULT_PATH = "tccStudentRegistration/situacaoDisciplina.csv"
    
    def __init__(self):
        self.defaultModel = SituacaoMatricula
        self.defaultKwargs = {"descricao_situacao_matricula" : "row[\"DESCRICAO\"]", "cod_tabela" : "row[\"ITEM_TABELA\"]"}
        self.defaultPath = self.CONST_SITUACAO_DISCIPLINA_DEFAULT_PATH
        super(ImportModel, self).__init__()

    def buildDictionary(self,modelList):
        dictionary = {}
        for obj in modelList:
            dictionary[obj.cod_tabela] = obj
        return dictionary
    def getDictionary(self, path=""):
        if(path):
            self.updateModelList(self.getFromCsv(path))
        return self.buildDictionary(self.getModelList())

class ValidateHistorico(object):
    CONST_DADOS_NECESSARIOS = ["COD_CURSO","CH_TOTAL","NOME_ATIV_CURRIC","PERIODO_ITEM","SITUACAO_ITEM","MATR_ALUNO",
                               "COD_ATIV_CURRIC","ANO","MEDIA_FINAL","NUM_FALTAS","ID_ALUNO","PERIODO_INGRE_ITEM","PERIODO_EVA_ITEM",
                               "ANO_INGRESSO","ANO_EVASAO","FORMA_EVASAO_ITEM","FORMA_INGRE_ITEM"]
    def __init__(self):
        super(ValidateHistorico,self).__init__()

    def validateHistorico(self,path):
        colunas = set()
        with open(path, 'rt') as fin:
            csvin = csv.reader(fin)
            colunas.update(next(csvin, []))
        fin.close()
        return all(elem in colunas for elem in self.CONST_DADOS_NECESSARIOS)


class ImportHistorico(object):
    """docstring for ImportHistorico"""
    def __init__(self):
        self.evasao = ImportTipoEvasao().getDictionary()
        self.ingresso = ImportTipoIngresso().getDictionary()
        self.sitDisciplina = ImportSituacaoDisciplina().getDictionary()
        super(ImportHistorico, self).__init__()

    def importHistorico(self,path=""):
        if not path:
            path = "tccStudentRegistration/historico.csv"
        importcsv = ImportCSV()
        historico = importcsv.getCSVData(path)
    
        alunoDic = self.updateAluno(historico)
        disciplinaDic = self.updateDisciplina(historico)
        cursoDic = self.updateCursoDisciplina(historico)

        for index, row in historico.iterrows():
            mesMatricula = self.dataItemToMes(row["PERIODO_ITEM"])
            matricula,created = Matricula.objects.get_or_create(
                situacao_matricula=self.sitDisciplina[row["SITUACAO_ITEM"]],
                aluno=alunoDic[row["MATR_ALUNO"]],
                disciplina=disciplinaDic[row["COD_ATIV_CURRIC"]],
                periodo_matricula=datetime(row["ANO"],mesMatricula,1),
                curso=cursoDic[row["COD_CURSO"]],
                media_final_matricula=row["MEDIA_FINAL"],
                faltas_matricula=row["NUM_FALTAS"]
                )
            if(matricula.aluno.periodo_evasao != None and matricula.periodo_matricula > matricula.aluno.periodo_evasao):
                matricula.aluno.periodo_evasao = matricula.periodo_matricula
                matricula.aluno.save()
                alunoDic[row["MATR_ALUNO"]] = matricula.aluno
            if(matricula.aluno.periodo_ingresso != None and matricula.periodo_matricula < matricula.aluno.periodo_ingresso):
                matricula.aluno.periodo_ingresso = matricula.periodo_matricula
                matricula.aluno.save()
                alunoDic[row["MATR_ALUNO"]] = matricula.aluno




    def updateAluno(self,historico):
        listaDadosAlunos = ["MATR_ALUNO","ID_ALUNO","PERIODO_INGRE_ITEM","PERIODO_EVA_ITEM","ANO_INGRESSO","ANO_EVASAO","FORMA_EVASAO_ITEM","FORMA_INGRE_ITEM"]
        dfAlunos = historico[listaDadosAlunos].groupby(["MATR_ALUNO"]).min()
        alunoDic = {}
        for index, row in dfAlunos.iterrows():
            aluno,created = Aluno.objects.get_or_create(grr_aluno=row.name,
                defaults={
                    "periodo_ingresso":datetime(2019,1,1),
                    "forma_ingresso":self.ingresso[2]
                })
            # if(created):
            aluno.nome_aluno = row["ID_ALUNO"]
            mesIngresso = self.dataItemToMes(row["PERIODO_INGRE_ITEM"])
            aluno.periodo_ingresso = datetime(row["ANO_INGRESSO"],mesIngresso,1)
            aluno.forma_ingresso = self.ingresso[row["FORMA_INGRE_ITEM"]]
            if(row["ANO_EVASAO"] > 0):
                mesEvasao = self.dataItemToMes(row["PERIODO_EVA_ITEM"])
                aluno.periodo_evasao = datetime(row["ANO_EVASAO"],mesEvasao,1)
            aluno.forma_evasao = self.evasao[row["FORMA_EVASAO_ITEM"]]
            alunoDic[row.name] = aluno
            aluno.save()
        return alunoDic

    def dataItemToMes(self,item):
        if(item == 201):
            return  1
        else:
            return  7


    def updateDisciplina(self,historico):
        listaDadosDisciplina = ["COD_ATIV_CURRIC","NOME_ATIV_CURRIC","CH_TOTAL"]
        dfDisciplinas = historico[listaDadosDisciplina].groupby(["COD_ATIV_CURRIC"]).max()
        disciplinaDic = {}
        for index, row in dfDisciplinas.iterrows():
            disciplina,created = Disciplina.objects.get_or_create(codigo_disciplina=row.name)
            disciplina.descricao_disciplina = row["NOME_ATIV_CURRIC"]
            disciplina.carga_horaria = row["CH_TOTAL"]
            disciplinaDic[row.name] = disciplina
            disciplina.save()
        return disciplinaDic

    def updateCursoDisciplina(self,historico):
        listaDadosCursoDisciplina = ["COD_ATIV_CURRIC","NOME_ATIV_CURRIC","CH_TOTAL","COD_CURSO"]
        dfCursos = historico[["COD_CURSO"]].groupby(["COD_CURSO"]).min()
        cursoDic = {}
        for index, row in dfCursos.iterrows():
            curso,created = Curso.objects.get_or_create(codigo_curso=row.name)
            # if(created):
            dfCursosDisciplinas = historico[listaDadosCursoDisciplina].where(historico["COD_CURSO"]==row.name).groupby(["COD_CURSO","COD_ATIV_CURRIC"]).max()
            for index2, row2 in dfCursosDisciplinas.iterrows():
                curso.disciplinas.add(Disciplina.objects.get(codigo_disciplina=row2.name[1]))
            cursoDic[row.name] = curso
            curso.save()
        return cursoDic
