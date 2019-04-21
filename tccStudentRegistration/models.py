from django.db import models


# Create your models here.


class FormaEvasao(models.Model):
    """FormaEvasao objects model.

    Used to keep track of FormaEvasao objects information.
    """

    descricao_evasao = models.CharField(
        max_length=255,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )

    def __str__(self):
        return self.descricao_evasao


class FormaIngresso(models.Model):
    """FormaIngresso objects model.

    Used to keep track of FormaIngresso objects information.
    """

    descricao_ingresso = models.CharField(
        max_length=255,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )

    def __str__(self):
        return self.descricao_ingresso


class Disciplina(models.Model):
    """Disciplina objects model.

    Used to keep track of Disciplina objects information.
    """

    codigo_disciplina = models.CharField(
        max_length=45,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    descricao_disciplina = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    carga_horaria = models.CharField(
        max_length=45,
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )

    def __str__(self):
        return self.descricao_disciplina


class Curso(models.Model):
    """Curso objects model.

    Used to keep track of Curso objects information.
    """

    codigo_curso = models.CharField(
        max_length=45,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    descricao_curso = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    disciplinas = models.ManyToManyField(
        Disciplina,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )

    def __str__(self):
        return self.descricao_curso


class SituacaoMatricula(models.Model):
    """SituacaoMatricula objects model.

    Used to keep track of SituacaoMatricula objects information.
    """

    descricao_situacao_matricula = models.CharField(
        max_length=100,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )

    def __str__(self):
        return self.descricao_situacao_matricula


class Aluno(models.Model):
    """Aluno objects model.

    Used to keep track of Aluno objects information.
    """

    grr_aluno = models.CharField(
        max_length=45,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    nome_aluno = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    periodo_ingresso = models.DateField(
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    periodo_evasao = models.DateField(
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    forma_ingresso = models.ForeignKey(
        FormaIngresso,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        on_delete=models.CASCADE
        )
    forma_evasao = models.ForeignKey(
        FormaEvasao,
        null=True,
        blank=True,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return self.nome_aluno


class Matricula(models.Model):
    """Matricula objects model.

    Used to keep track of Matricula objects information.
    """

    media_final_matricula = models.FloatField(
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    faltas_matricula = models.IntegerField(
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    periodo_matricula = models.DateField(
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        )
    aluno = models.ForeignKey(
        Aluno,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        on_delete=models.CASCADE
        )
    disciplina = models.ForeignKey(
        Disciplina,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        on_delete=models.CASCADE
        )
    situacao_matricula = models.ForeignKey(
        SituacaoMatricula,
        # verbose_name=_('CLLB201'),
        # help_text=_('CLHT201'),
        on_delete=models.CASCADE
        )
