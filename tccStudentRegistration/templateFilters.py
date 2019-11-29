from django.template.defaulttags import register

@register.filter
def getPredicaoEvasao(dictionary,item):
    return dictionary.get(item).forma_evasao.descricao_evasao