from django.db import models


# Create your models here.


class FormaEvasao(object):
    """FormaEvasao model."""

    descricao_evasao = models.CharField(max_length=255)


class FormaIngresso(object):
    """FormaIngresso model."""

    descricao_ingresso = models.CharField(max_length=255)
