from django.db import models
from django.utils.translation import gettext_lazy as _


class FormaEvasao(models.Model):
    """FormaEvasao objects model.

    Used to keep track of FormaEvasao objects information.
    """
    descricao_evasao = models.CharField(
        max_length=255,
        verbose_name=_('Descrição evasão'),
        help_text=_('Nome da forma de evasão do aluno'),
        )
    cod_tabela = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Codigo na tabela do historico'),
        help_text=_('Codigo na tabela do historico'),
        )

    def __str__(self):
        return self.descricao_evasao


class FormaIngresso(models.Model):
    """FormaIngresso objects model.

    Used to keep track of FormaIngresso objects information.
    """

    descricao_ingresso = models.CharField(
        max_length=255,
        verbose_name=_('Descrição ingresso'),
        help_text=_('Nome da forma de ingresso do aluno'),
        )
    cod_tabela = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Codigo na tabela do historico'),
        help_text=_('Codigo na tabela do historico'),
        )

    def __str__(self):
        return self.descricao_ingresso


class Disciplina(models.Model):
    """Disciplina objects model.

    Used to keep track of Disciplina objects information.
    """

    codigo_disciplina = models.CharField(
        max_length=45,
        verbose_name=_('Código da disciplina'),
        help_text=_('Código de identificação da disciplina'),
        )
    descricao_disciplina = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Descrição da disciplina'),
        help_text=_('Nome da disciplina'),
        )
    carga_horaria = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Carga horária da disciplina'),
        help_text=_('Carga horária da disciplina'),
        )

    def __str__(self):
        return '%s/%s' % (self.codigo_disciplina, self.descricao_disciplina)


class Curso(models.Model):
    """Curso objects model.

    Used to keep track of Curso objects information.
    """

    codigo_curso = models.CharField(
        max_length=45,
        verbose_name=_('Código do curso'),
        help_text=_('Carga de identificação do curso'),
        )
    descricao_curso = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Descrição do curso'),
        help_text=_('Nome do curso'),
        )
    disciplinas = models.ManyToManyField(
        Disciplina,
        verbose_name=_('Disciplinas'),
        help_text=_('Disciplinas relacionadas ao curso'),
        )

    def __str__(self):
        return '%s/%s' % (self.codigo_curso, self.descricao_curso)


class SituacaoMatricula(models.Model):
    """SituacaoMatricula objects model.

    Used to keep track of SituacaoMatricula objects information.
    """

    descricao_situacao_matricula = models.CharField(
        max_length=100,
        verbose_name=_('Descrição da situação da matrícula'),
        help_text=_('Nome da situação da matrícula'),
        )
    cod_tabela = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Codigo na tabela do historico'),
        help_text=_('Codigo na tabela do historico'),
        )

    def __str__(self):
        return self.descricao_situacao_matricula


class Aluno(models.Model):
    """Aluno objects model.

    Used to keep track of Aluno objects information.
    """

    grr_aluno = models.CharField(
        max_length=45,
        verbose_name=_('GRR do aluno'),
        help_text=_('GRR do aluno'),
        )
    nome_aluno = models.CharField(
        max_length=255,
        null=True,
        blank=True,
        verbose_name=_('Nome do aluno'),
        help_text=_('Nome do aluno'),
        )
    periodo_ingresso = models.DateField(
        verbose_name=_('Período de ingresso'),
        help_text=_('Período de ingresso do aluno no curso'),
        )
    periodo_evasao = models.DateField(
        null=True,
        blank=True,
        verbose_name=_('Período evasão'),
        help_text=_('Período de evasão do aluno do curso'),
        )
    forma_ingresso = models.ForeignKey(
        FormaIngresso,
        verbose_name=_('Forma de ingresso'),
        help_text=_('Forma de ingresso do aluno no curso'),
        on_delete=models.CASCADE
        )
    forma_evasao = models.ForeignKey(
        FormaEvasao,
        null=True,
        blank=True,
        verbose_name=_('Forma de evasão'),
        help_text=_('Forma de evasão do aluno do curso'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '%s/%s' % (self.grr_aluno, self.nome_aluno)


class Matricula(models.Model):
    """Matricula objects model.

    Used to keep track of Matricula objects information.
    """

    media_final_matricula = models.FloatField(
        verbose_name=_('Média final da matrícula'),
        help_text=_('Média final na disciplina'),
        )
    faltas_matricula = models.IntegerField(
        verbose_name=_('Faltas da matrícula'),
        help_text=_('Faltas totais na disciplina'),
        )
    periodo_matricula = models.DateField(
        verbose_name=_('Período da matrícula'),
        help_text=_('Período em que ocorreu a matrícula na disciplina'),
        )
    aluno = models.ForeignKey(
        Aluno,
        verbose_name=_('Nome do aluno'),
        help_text=_('GRR e nome do aluno'),
        on_delete=models.CASCADE
        )
    disciplina = models.ForeignKey(
        Disciplina,
        verbose_name=_('Disciplina'),
        help_text=_('Disciplina em que o aluno está matriculado'),
        on_delete=models.CASCADE
        )
    situacao_matricula = models.ForeignKey(
        SituacaoMatricula,
        verbose_name=_('Situação da matrícula'),
        help_text=_('Situação da matrícula do aluno na disciplina'),
        on_delete=models.CASCADE
        )
    curso = models.ForeignKey(
        Curso,
        verbose_name=_('Curso'),
        help_text=_('Curso em que a matricula foi feita'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '%s' % (self.aluno)



class PredicaoEvasao(models.Model):
    """Matricula objects model.

    Used to keep track of Matricula objects information.
    """

    
    periodo_predicao = models.DateField(
        verbose_name=_('Período em que a predicao foi feita'),
        help_text=_('Período em que o script fez a predicao'),
        )
    script_predicao = models.CharField(
        max_length=45,
        verbose_name=_('Script predicao'),
        help_text=_('Nome do script de predicao utilizado'),
        )
    aluno = models.ForeignKey(
        Aluno,
        verbose_name=_('Nome do aluno'),
        help_text=_('GRR e nome do aluno'),
        on_delete=models.CASCADE
        )
    forma_evasao = models.ForeignKey(
        FormaEvasao,
        null=True,
        blank=True,
        verbose_name=_('Forma de evasão'),
        help_text=_('Forma de evasão do aluno do curso'),
        on_delete=models.CASCADE
        )
    def __str__(self):
        return '%s/%s/%s/%s' % (self.aluno,self.forma_evasao,self.script_predicao,self.periodo_predicao)


class Usuario(models.Model):
    """docstring for Usuario"""
    nome_usuario = models.CharField(
        max_length=255,
        verbose_name=_('Nome'),
        help_text=_('Nome do Usuario cadastrado'),
        )
    email_usuario = models.CharField(
        max_length=255,
        verbose_name=_('Email'),
        help_text=_('Email do Usuario cadastrado'),
        )
    senha_usuario = models.CharField(
        max_length=255,
        verbose_name=_('Senha'),
        help_text=_('Senha do Usuario cadastrado'),
        )
    admin_usuario = models.BooleanField(default=False)
    #models.BooleanField(default=True)

    def __str__(self):
        return '%s/%s/%s/%s' % (self.aluno,self.forma_evasao,self.script_predicao,self.periodo_predicao)
        