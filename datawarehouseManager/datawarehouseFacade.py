# flake8: noqa
from datawarehouseManager.models import *
from datawarehouseManager.dataMining import DescricaoUtil
import json

class datawarehouseFacade(object):
    """docstring for datawarehouseFacade"""
    def __init__(self, arg):
        super(datawarehouseFacade, self).__init__()
        self.arg = arg

    @staticmethod
    def getAlunoDetalhesMatricula(grr_aluno):
        aluno = Aluno.objects.filter(grr_aluno=grr_aluno)
        detalheAluno = None
        if aluno :
            FatoDoAluno = FatoMatricula.objects.get(alunoMatricula__grr_aluno=grr_aluno,
                situacaoMatricula__isnull=True,
                disciplinaMatricula__isnull=True,
                cursoMatricula__isnull=True,
                semestreMatricula__isnull=True)

            calculo = (1- FatoDoAluno.coeficienteReprovacao) *  FatoDoAluno.quantidadeMatricula

            detalheAluno = {
                'porcentagemReprovacao' : round(FatoDoAluno.coeficienteReprovacao * 100,2),
                'qtdMatriculas'         : FatoDoAluno.quantidadeMatricula,
                'qtdMatriculasCompletas': int(calculo)
            }
        return detalheAluno
    @staticmethod
    def getDisciplinaDetalhesMatricula(cod_disciplina):
        disciplina = Disciplina.objects.filter(codigo_disciplina=cod_disciplina)
        detalheDisciplina = None
        if disciplina :
            FatoDaDisciplina = FatoMatricula.objects.get(alunoMatricula__isnull=True,
                situacaoMatricula__isnull=True,
                disciplinaMatricula__isnull=disciplina,
                cursoMatricula__isnull=True,
                semestreMatricula__isnull=True)

            detalheDisciplina = {
                'porcentagemReprovacao' : round(FatoDaDisciplina.coeficienteReprovacao * 100,2)
            }
        return detalheDisciplina

    #def createDataWithPercentage(percentage,Name1,Name2):
    #    percentageSecondData = 100 - percentage
    #    data = [
    #        [Name1,percentage],
    #        [Name2,percentageSecondData]
    #    ]
    #    return data

    #def getSemiCircleDonutChart(data,title):
    #    chart = {
    #        "chart": {"type": "column"},
    #        "title": {"text": title},
    #        "plotOptions": {
    #            "pie": {
    #                "dataLabels": {
    #                    "enabled": "true",
    #                    "style": {
    #                        "fontWeight": 'bold',
    #                        "color": 'white'
    #                    }
    #                },
    #                "startAngle": -90,
    #                "endAngle": 90,
    #                "center": ['50%', '75%']
    ##            }
    #        },
    #        "series":[{
    #            'type': 'pie',
    ##            'name': 'Browser share',
    #            'data': data
    #        }]
    #    }
    #    return chart

    @staticmethod
    def getFatoEvasaoPorcentagemRetidosSemestre():
        chart = None
        fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=True,
            situacaoEvasao=StituacaoEvasao.objects.get(descricao_evasao="Formatura"),
            cursoEvasao__isnull=True,
            semestreEvasao__isnull=False)
        if(fatoEvasaoLista):
            fatoEvasaoLista = fatoEvasaoLista.order_by("semestreEvasao__inicioSemestre")
            semestreRetidos = []
            semestreNaoRetidos = []
            series = []
            categories = []
            for fato in fatoEvasaoLista:
                print(fato.situacaoEvasao)
                porcentagem = round(fato.coeficienteRetencao * 100)
                semestreRetidos += [porcentagem]
                semestreNaoRetidos += [100-porcentagem]


                categories += [str(fato.semestreEvasao.inicioSemestre)]


            series = [{
                   "name" : "Retidos",
                    "data" : semestreRetidos
                },{
                    "name" : "Não retidos",
                    "data" : semestreNaoRetidos
                }]

            chart = {
                "chart": {"type": "column"},
                "title": {"text": "Porcentagem Retencao por semestre"},
                "xAxis": {"categories": categories},
                "yAxis": {
                    "min": 0,
                    "title": {
                        "text": "PorcentagemRetencao"
                    },
                    "stackLabels": {
                        "enabled": "true",
                        "style": {
                            "fontWeight": "bold"
                            #"color": ( // theme
                            #    Highcharts.defaultOptions.title.style &&
                            #    Highcharts.defaultOptions.title.style.color
                            #) || "gray"
                        }
                    }
                },
                "plotOptions": {
                    "column": {
                        "stacking": 'normal',
                        "dataLabels": {
                            "enabled": "true"
                        }
                    }
                },
                "series": series
            }

            chart = json.dumps(chart)

        return chart

    @staticmethod
    def getFatoEvasaoPorcentagemFormadosSemestre():
        chart = None
        fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=True,
            situacaoEvasao__isnull=True,
            cursoEvasao__isnull=True,
            semestreEvasao__isnull=False)
        if(fatoEvasaoLista):
            fatoEvasaoLista = fatoEvasaoLista.order_by("semestreEvasao__inicioSemestre")
            semestreRetidos = []
            semestreNaoRetidos = []
            series = []
            categories = []
            for fato in fatoEvasaoLista:
                print(fato.situacaoEvasao)
                porcentagem = round(fato.coeficienteEvasao * 100)
                semestreRetidos += [porcentagem]
                semestreNaoRetidos += [100-porcentagem]


                categories += [str(fato.semestreEvasao.inicioSemestre)]


            series = [{
                   "name" : "Evasão",
                    "data" : semestreRetidos
                },{
                    "name" : "Formados",
                    "data" : semestreNaoRetidos
                }]

            chart = {
                "chart": {"type": "column"},
                "title": {"text": "Porcentagem Tipo de Evasão por semestre"},
                "xAxis": {"categories": categories},
                "yAxis": {
                    "min": 0,
                    "title": {
                        "text": "PorcentagemRetencao"
                    },
                    "stackLabels": {
                        "enabled": "true",
                        "style": {
                            "fontWeight": "bold"
                            #"color": ( // theme
                            #    Highcharts.defaultOptions.title.style &&
                            #    Highcharts.defaultOptions.title.style.color
                            #) || "gray"
                        }
                    }
                },
                "plotOptions": {
                    "column": {
                        "stacking": 'normal',
                        "dataLabels": {
                            "enabled": "true"
                        }
                    }
                },
                "series": series
            }

            chart = json.dumps(chart)

        return chart