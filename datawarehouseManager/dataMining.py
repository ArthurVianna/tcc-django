# flake8: noqa
from pandas import pandas as pd
from datawarehouseManager.dbManager import *
from datetime import datetime
from datawarehouseManager.models import *


class DataMining(object):
    """docstring for DataMining"""

    maxDataAge = 15
    defaultQtdSemestresFormacao = 6
    
    def __init__(self):
        self.maxDataAge = 15
        self.defaultQtdSemestresFormacao = 6
        super(DataMining, self).__init__()


    def buildFatoNameEvasao(self,fato):
        nomeFato = ""
        nomeFato += str(fato.alunoEvasao.id) if fato.alunoEvasao is not None else "None"
        nomeFato += str(fato.situacaoEvasao.id) if fato.situacaoEvasao is not None else "None"
        nomeFato += str(fato.cursoEvasao.id) if fato.cursoEvasao is not None else "None"
        nomeFato += str(fato.semestreEvasao.id) if fato.semestreEvasao is not None else "None"
        return nomeFato

    def buildFatoNameMatricula(self,fato):
        nomeFato = ""
        nomeFato += str(fato.alunoMatricula.id) if fato.alunoMatricula is not None else "None"
        nomeFato += str(fato.situacaoMatricula.id) if fato.situacaoMatricula is not None else "None"
        nomeFato += str(fato.disciplinaMatricula.id) if fato.disciplinaMatricula is not None else "None"
        nomeFato += str(fato.cursoMatricula.id) if fato.cursoMatricula is not None else "None"
        nomeFato += str(fato.semestreMatricula.id) if fato.semestreMatricula is not None else "None"
        return nomeFato


    def insertFatoEvasao(self):
        alunos = getAlunoEvadiram()
        for aluno in alunos:
            sem,created = Semestre.objects.get_or_create(inicioSemestre=aluno.periodo_evasao)
            situacaoEvasao,created = StituacaoEvasao.objects.get_or_create(descricao_evasao=aluno.forma_evasao.descricao_evasao)
            turma,created = Turma.objects.get_or_create(periodo_ingresso=aluno.periodo_ingresso)
            formaIngresso,created = FormaIngresso.objects.get_or_create(descricao_ingresso=aluno.forma_ingresso.descricao_ingresso)
            alu,created = Aluno.objects.get_or_create(grr_aluno=aluno.grr_aluno,forma_ingresso=formaIngresso)
            if(alu.turma == None or alu.turma != turma):
                alu.turma = turma
                alu.save()
            if(created):
                alu.nome_aluno = aluno.nome_aluno
                alu.save()
            cursoAlu = getCursoAluno(alu.grr_aluno)
            curso, created = Curso.objects.get_or_create(codigo_curso=cursoAlu.codigo_curso)
            if(created):
                curso.descricao_curso = cursoAlu.descricao_curso
                curso.save()
            fatoEvasao,created = FatoEvasao.objects.get_or_create(alunoEvasao=alu,situacaoEvasao=situacaoEvasao,cursoEvasao=curso,semestreEvasao=sem)            
            fatoEvasao.quantidadeRetencoes = countRetencoesAluno(alu.grr_aluno)
            fatoEvasao.ira = calculoIra(alu.grr_aluno)
            if situacaoEvasao.descricao_evasao in DescricaoUtil.getListSemConcluirSituacao():
                fatoEvasao.coeficienteEvasao = '1.0'
            else:
                fatoEvasao.coeficienteEvasao = '0.0'
            fatoEvasao.semestresCursados = getQtdSemestres(alu.grr_aluno)
            if (fatoEvasao.situacaoEvasao.descricao_evasao == "Formatura" and  fatoEvasao.semestresCursados < self.defaultQtdSemestresFormacao):
                fatoEvasao.coeficienteRetencao = '0.0'
            else:
                fatoEvasao.coeficienteRetencao = '1.0'
            fatoEvasao.quantidadeEvasao = 1
            fatoEvasao.save()

    def updateFatoEvasao(self):
        fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False,semestreEvasao__isnull=False)
        fatoEvasaoDic = {}

        for fato in fatoEvasaoLista:
            AuxAluno = fato.alunoEvasao
            AuxSituacaoEvasao = fato.situacaoEvasao
            AuxCursoEvasao = fato.cursoEvasao

            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            if (fato.alunoEvasao is None or
                               fato.situacaoEvasao is None or
                               fato.cursoEvasao is None or
                               fato.semestreEvasao is None):
                                nomeFato = self.buildFatoNameEvasao(fato)
                                if nomeFato not in fatoEvasaoDic:
                                    novaFato = FatoEvasao()
                                    novaFato.alunoEvasao = fato.alunoEvasao
                                    novaFato.situacaoEvasao = fato.situacaoEvasao
                                    novaFato.cursoEvasao = fato.cursoEvasao
                                    novaFato.semestreEvasao = fato.semestreEvasao
                                    novaFato.semestresCursados = 0
                                    novaFato.coeficienteRetencao = 0
                                    novaFato.quantidadeRetencoes = 0
                                    novaFato.ira = 0
                                    novaFato.coeficienteEvasao = 0
                                    novaFato.quantidadeEvasao = 0
                                    fatoEvasaoDic[nomeFato] = novaFato
                                else:
                                    novaFato = fatoEvasaoDic[nomeFato]

                                novaFato.quantidadeRetencoes += fato.quantidadeRetencoes
                                novaFato.ira += fato.ira
                                novaFato.coeficienteEvasao += fato.coeficienteEvasao
                                novaFato.semestresCursados += fato.semestresCursados
                                novaFato.coeficienteRetencao += fato.coeficienteRetencao
                                novaFato.quantidadeEvasao += 1
                            fato.alunoEvasao = None
                        #endfor
                        fato.alunoEvasao = AuxAluno
                        fato.situacaoEvasao = None
                    #endFor
                    fato.situacaoEvasao = AuxSituacaoEvasao
                    fato.cursoEvasao = None
                #endFor
                fato.cursoEvasao = AuxCursoEvasao
                fato.semestreEvasao = None
            #endFor

        for item in fatoEvasaoDic:
            fato = fatoEvasaoDic[item]
            fatoBanco = FatoEvasao.objects.get_or_create(alunoEvasao=fato.alunoEvasao,situacaoEvasao=fato.situacaoEvasao,cursoEvasao=fato.cursoEvasao,semestreEvasao=fato.semestreEvasao)
            fatoBanco.ira = fato.ira / fato.quantidadeEvasao
            fatoBanco.coeficienteEvasao = fato.coeficienteEvasao / fato.quantidadeEvasao
            fatoBanco.quantidadeEvasao = fato.quantidadeEvasao
            fatoBanco.semestresCursados = fato.semestresCursados / fato.quantidadeEvasao
            fatoBanco.coeficienteRetencao = fato.coeficienteRetencao / fato.quantidadeEvasao
            fatoBanco.save()


    def updateFatoMatricula(self):
        fatoMatriculaLista = FatoMatricula.objects.filter(alunoMatricula__isnull=False,
            situacaoMatricula__isnull=False,
            disciplinaMatricula__isnull=False,
            cursoMatricula__isnull=False,
            semestreMatricula__isnull=False)
        fatoMatriculaDic = {}
        for fato in fatoMatriculaLista:
            AuxAluno = fato.alunoMatricula
            AuxSituacao = fato.situacaoMatricula
            AuxDisciplina = fato.disciplinaMatricula
            AuxCurso = fato.cursoMatricula
            for i in range(2):
                for j in range(2):
                    for k in range(2):
                        for l in range(2):
                            for m in range(2):
                                if (fato.alunoMatricula is None or
                                   fato.situacaoMatricula is None or
                                   fato.disciplinaMatricula is None or
                                   fato.cursoMatricula is None or
                                   fato.semestreMatricula is None):
                                    nomeFato = self.buildFatoNameMatricula(fato)
                                    #print(nomeFato)
                                    if nomeFato not in fatoMatriculaDic:
                                        novaFato = FatoMatricula()
                                        novaFato.alunoMatricula = fato.alunoMatricula
                                        novaFato.situacaoMatricula = fato.situacaoMatricula
                                        novaFato.disciplinaMatricula = fato.disciplinaMatricula
                                        novaFato.cursoMatricula = fato.cursoMatricula
                                        novaFato.semestreMatricula = fato.semestreMatricula
                                        novaFato.faltasMatricula = 0
                                        novaFato.mediaMatricula = 0
                                        novaFato.coeficienteReprovacao = 0
                                        novaFato.quantidadeMatricula = 0
                                        fatoMatriculaDic[nomeFato] = novaFato
                                    else:
                                        novaFato = fatoMatriculaDic[nomeFato]

                                    novaFato.faltasMatricula += fato.faltasMatricula
                                    novaFato.mediaMatricula += fato.mediaMatricula
                                    novaFato.coeficienteReprovacao += fato.coeficienteReprovacao
                                    novaFato.quantidadeMatricula += 1
                                fato.alunoMatricula = None
                                #endfor
                            fato.alunoMatricula = AuxAluno
                            fato.disciplinaMatricula = None
                            #endFor
                        fato.disciplinaMatricula = AuxDisciplina
                        fato.situacaoMatricula = None
                    #endfor
                    fato.situacaoMatricula = AuxSituacao
                    fato.cursoMatricula = None
                #endFor
                fato.cursoMatricula = AuxCurso
                fato.semestreMatricula = None
            #endFor

        for item in fatoMatriculaDic:
            fato = fatoMatriculaDic[item]
            fatoBanco,created = FatoMatricula.objects.get_or_create(alunoMatricula=fato.alunoMatricula,situacaoMatricula=fato.situacaoMatricula,disciplinaMatricula=fato.disciplinaMatricula,
                                                            cursoMatricula=fato.cursoMatricula,semestreMatricula=fato.semestreMatricula)
            fatoBanco.faltasMatricula = fato.faltasMatricula / fato.quantidadeMatricula
            fatoBanco.mediaMatricula = fato.mediaMatricula / fato.quantidadeMatricula
            fatoBanco.coeficienteReprovacao = fato.coeficienteReprovacao / fato.quantidadeMatricula
            fatoBanco.quantidadeMatricula = fato.quantidadeMatricula
            fatoBanco.save()
            

    def insertFatoMatricula(self):
        matriculas = getMatriculasCompletas()
        for matricula in matriculas:
            sem,created = Semestre.objects.get_or_create(inicioSemestre=matricula.periodo_matricula)
            situacaoMatricula,created = SituacaoMatricula.objects.get_or_create(descricao_situacao_matricula=matricula.situacao_matricula.descricao_situacao_matricula)
            turma,created = Turma.objects.get_or_create(periodo_ingresso=matricula.aluno.periodo_ingresso)
            formaIngresso,created = FormaIngresso.objects.get_or_create(descricao_ingresso=matricula.aluno.forma_ingresso.descricao_ingresso)
            aluno,created = Aluno.objects.get_or_create(grr_aluno=matricula.aluno.grr_aluno,turma=turma,forma_ingresso=formaIngresso)
            if(created):
                aluno.nome_aluno = matricula.aluno.nome_aluno
                aluno.save()
            disciplina, created = Disciplina.objects.get_or_create(codigo_disciplina=matricula.disciplina.codigo_disciplina)
            if(created):
                disciplina.descricao_disciplina = matricula.disciplina.descricao_disciplina
                disciplina.carga_horaria = matricula.disciplina.carga_horaria
                disciplina.save()
            curso, created = Curso.objects.get_or_create(codigo_curso=matricula.curso.codigo_curso)
            if(created):
                curso.descricao_curso = matricula.curso.descricao_curso
                curso.save()
            if not (curso.disciplinas.filter(codigo_disciplina=disciplina.codigo_disciplina).exists()):
                curso.disciplinas.add(disciplina)
                curso.save()
            fatoMatricula,created = FatoMatricula.objects.get_or_create(alunoMatricula=aluno,situacaoMatricula=situacaoMatricula,disciplinaMatricula=disciplina,
                                                                cursoMatricula=curso,semestreMatricula=sem)
            fatoMatricula.faltasMatricula = matricula.faltas_matricula
            fatoMatricula.mediaMatricula = matricula.media_final_matricula
            if situacaoMatricula.descricao_situacao_matricula not in DescricaoUtil.getListMatriculaAprovado():
                fatoMatricula.coeficienteReprovacao = '1.0'
            else:
                fatoMatricula.coeficienteReprovacao = '0.0'
            fatoMatricula.quantidadeMatricula = 1
            fatoMatricula.save()


    def clearData(self):
        today = datetime.today()
        ano = today.year - self.maxDataAge
        
        if(today.month < 7):
            mes = 1
        else:
            mes = 7
        today = datetime(ano,mes,1)
        semestres = Semestre.objects.filter(inicioSemestre__lt=today).order_by('inicioSemestre')
        oldEvasoes = FatoEvasao.objects.filter(semestreEvasao__in=semestres,alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False)

        turmasAfetadas = {}
        formaIngressoAfetado = {}
        #alunosDeletados = []
        for fatoEvasao in oldEvasoes:
            #alunosDeletados += [fatoEvasao.alunoEvasao]
            turmasAfetadas[fatoEvasao.alunoEvasao.turma.periodo_ingresso] = fatoEvasao.alunoEvasao.turma
            formaIngressoAfetado[fatoEvasao.alunoEvasao.forma_ingresso.descricao_ingresso] = fatoEvasao.alunoEvasao.forma_ingresso
            fatoEvasao.alunoEvasao.delete()


        for turma in turmasAfetadas:
            if(Aluno.objects.filter(turma=turmasAfetadas[turma]).values().count() <= 0): # exclude(pk__in=alunosDeletados)
                turma.delete()
                

        for forma in formaIngressoAfetado:
            if(Aluno.objects.filter(forma_ingresso=formaIngressoAfetado[forma]).values().count() <= 0): #exclude(pk__in=alunosDeletados)
                forma.delete()
                

        cursos = Curso.objects.all()
        disciplinas = Disciplina.objects.all()
        situacaoMatriculas = SituacaoMatricula.objects.all()
        situacaoEvasaos = StituacaoEvasao.objects.all()


        for curso in cursos:
            count = FatoMatricula.objects.filter(cursoMatricula=curso,alunoMatricula__isnull=False,
                                        situacaoMatricula__isnull=False,
                                        disciplinaMatricula__isnull=False,
                                        semestreMatricula__isnull=False).values().count()
            count += FatoEvasao.objects.filter(semestreEvasao__isnull=False,alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao=curso).values().count()
            #print("curso : " + curso.codigo_curso + "   Count :" + str(count))
            if(count <= 0):
                curso.delete()
        disciplinaCount = 0
        for disciplina in disciplinas:
            count = FatoMatricula.objects.filter(cursoMatricula__isnull=False,alunoMatricula__isnull=False,
                                        situacaoMatricula__isnull=False,
                                        disciplinaMatricula=disciplina,
                                        semestreMatricula__isnull=False).values().count()
            if(count <= 0):
                disciplina.delete()

        
        for sitMatr in situacaoMatriculas:
            count = FatoMatricula.objects.filter(cursoMatricula__isnull=False,alunoMatricula__isnull=False,
                                        situacaoMatricula=sitMatr,
                                        disciplinaMatricula__isnull=False,
                                        semestreMatricula__isnull=False).values().count()
            if(count <= 0):
                sitMatr.delete()


        for sitEva in situacaoEvasaos:
            count = FatoEvasao.objects.filter(semestreEvasao__isnull=False,alunoEvasao__isnull=False,situacaoEvasao=sitEva,cursoEvasao__isnull=False).values().count()
            if(count <= 0):
                sitEva.delete()

        for semestre in semestres:
            count = FatoMatricula.objects.filter(cursoMatricula__isnull=False,alunoMatricula__isnull=False,
                                        situacaoMatricula__isnull=False,
                                        disciplinaMatricula__isnull=False,
                                        semestreMatricula=semestre).values().count()
            count += FatoEvasao.objects.filter(semestreEvasao=semestre,alunoEvasao__isnull=False,situacaoEvasao__isnull=False,cursoEvasao__isnull=False).values().count()
            if(count <= 0):
                semestre.delete()


        


class DescricaoUtil(object):
    """docstring for DescricaoUtil"""
    def __init__(self, arg):
        super(DescricaoUtil, self).__init__()
        self.arg = arg

    @staticmethod
    def getListMatriculaRetido():
        reprovado =  ['Reprovado por nota'
                , 'Reprovado por Frequência'
                , 'Cancelado'
                , 'Incompleto'
                , 'Reprovado sem nota'
                , 'Matrícula'
                , 'Trancamento Total'
                , 'Disciplina sem Oferta'
                , 'Trancamento Administrativo'
                , 'PROVAR'
                , 'Trancamento CEPE'
                , 'Trancamento Outra IES'
                , 'Suficiente'
                , 'Reprov Conhecimento'
                , 'Reprov Adiantamento'
                , 'Trancamento por amparo Legal'
                , 'Isento por Transferência'
                , 'Desistência de Vaga'
                , 'Processo Administrativo'
                , 'Horas']

        return reprovado

    @staticmethod
    def getListSemConcluirSituacao():
        evadidosSemConcluirSituacao = [ 'Transferência Externa'
                                        , 'Reopção'
                                        , 'Reintegração'
                                        , 'Mudança de Habilitação Interna'
                                        , 'Jubilamento'
                                        , 'Cancelamento Convênio'
                                        , 'Desistência'
                                        , 'Abandono'
                                        , 'Desligamento com Penalidades'
                                        , 'Cancelamento Administrativo'
                                        , 'Cancelamento Judicial'
                                        , 'Cancelamento Pedido'
                                        , 'Mobilidade Acadêmica'
                                        , 'Desistência PROVAR'
                                        , 'Desistência Vestibular'
                                        , 'Falecimento'
                                        , 'Mudança de Campus'
                                        , 'Mudança de Turno'
                                        , 'Novo Vestibular'
                                        , 'Descumprimento Edital'
                                        , 'Cancelamento a Pedido do Calouro'
                                        , 'Não Confirmação de Vaga'
                                        , 'Término de Registro Temporário'
                                        , 'Decisão Administrativa']
        return evadidosSemConcluirSituacao

    @staticmethod
    def getListMatriculaAprovado():
        aprovado = ['Aprovado'
                    , 'Dispensa de Disciplinas (com nota)'
                    , 'Dispensa de Disciplinas (sem nota)'
                    , 'Aprovado sem nota'
                    , 'Equivalência de Disciplina'
                    , 'Adiantamento'
                    , 'Aprov Conhecimento'
                    , 'Aproveitamento de estudos'
                    , 'Aprov Adiantamento'
                    , 'Aproveitamento de Créditos']
        return aprovado
        



