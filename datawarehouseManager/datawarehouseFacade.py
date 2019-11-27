from datawarehouseManager.models import *
import json

def getFatoEvasaoPorcentagemRetidosSemestreChart():
    fatoEvasaoLista = FatoEvasao.objects.filter(alunoEvasao__isnull=True,
        situacaoEvasao=StituacaoEvasao.objects.get(descricao_evasao="Formatura"),
        cursoEvasao__isnull=True,
        semestreEvasao__isnull=False).order_by("semestreEvasao__inicioSemestre")
    semestreRetidos = []
    semestreNaoRetidos = []
    series = []
    categories = []
    for fato in fatoEvasaoLista:
        
        semestreRetidos += [fato.coeficienteRetencao]
        semestreNaoRetidos += [1 - fato.coeficienteRetencao]

         
        categories += [str(fato.semestreEvasao.inicioSemestre)]


    series = [{
           "name" : "Retidos",
            "data" : semestreRetidos
        },{
            "name" : "Não retidos",
            "data" : semestreNaoRetidos
        }]

    print("series : " + str(series))
    print("categories : " + str(categories))
    print("series : " + str(len(series)))
    print("categories : " + str(len(categories)))

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