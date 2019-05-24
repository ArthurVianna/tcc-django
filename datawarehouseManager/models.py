from django.db import models
from django.utils.translation import gettext_lazy as _


class StituacaoEvasao(models.Model):
    """FormaEvasao objects model.

    Used to keep track of FormaEvasao objects information.
    """
    descricao_evasao = models.CharField(
        max_length=255,
        verbose_name=_('Descrição evasão'),
        help_text=_('Nome da forma de evasão do aluno'),
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

    def __str__(self):
        return self.descricao_situacao_matricula


class Turma(models.Model):
    periodo_ingresso = models.DateField(
        verbose_name=_('Período de ingresso'),
        help_text=_('Período de ingresso do aluno no curso'),
        )

    def __str__(self):
        return self.periodo_ingresso


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
    turma = models.ForeignKey(
        Turma,
        verbose_name=_('Período de ingresso'),
        help_text=_('Período de ingresso do aluno no curso'),
        on_delete=models.CASCADE
        )
    forma_ingresso = models.ForeignKey(
        FormaIngresso,
        verbose_name=_('Forma de ingresso'),
        help_text=_('Forma de ingresso do aluno no curso'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '%s/%s' % (self.grr_aluno, self.nome_aluno)


class Semestre(models.Model):
    inicioSemestre = models.DateField(
        verbose_name=_('Data do inicio do semestre'),
        help_text=_('Data do inicio do semestre'),
        )

    def __str__(self):
        return self.periodo_ingresso


class FatoMatricula(models.Model):
    faltasMatricula = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Faltas matricula'),
        help_text=_('Quantidade de faltas da matricula'),
        )

    mediaMatricula = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Media matricula'),
        help_text=_('Media final da matricula'),
        )

    coeficienteRetencao = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Porcentagem de retencao'),
        help_text=_('Porcentagem de retencao'),
        )

    semestreMatricula = models.ForeignKey(
        Semestre,
        null=True,
        blank=True,
        verbose_name=_('Semestre matricula'),
        help_text=_('Semestre em que a matricula foi feita'),
        on_delete=models.CASCADE
        )

    situacaoMatricula = models.ForeignKey(
        SituacaoMatricula,
        null=True,
        blank=True,
        verbose_name=_('Situacao matricula'),
        help_text=_('Situacao em que a matricula foi concluida'),
        on_delete=models.CASCADE
        )

    disciplinaMatricula = models.ForeignKey(
        Disciplina,
        null=True,
        blank=True,
        verbose_name=_('Disciplina matricula'),
        help_text=_('Disciplina em que a matricula foi feita'),
        on_delete=models.CASCADE
        )

    alunoMatricula = models.ForeignKey(
        Aluno,
        null=True,
        blank=True,
        verbose_name=_('Aluno matricula'),
        help_text=_('Aluno que fez a matricula'),
        on_delete=models.CASCADE
        )

    cursoMatricula = models.ForeignKey(
        Curso,
        null=True,
        blank=True,
        verbose_name=_('Curso matricula'),
        help_text=_('Curso em que a matricula foi feita'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '%s/%s/%s/%s/%s' (self.semestreMatricula,
                                 self.situacaoMatricula,
                                 self.disciplinaMatricula,
                                 self.alunoMatricula,
                                 self.cursoMatricula)


class FatoEvasao(models.Model):
    quantidadeRetencoes = models.IntegerField(
        null=True,
        blank=True,
        verbose_name=_('Quantidade retencoes'),
        help_text=_('Quantidade de retencoes'),
        )

    ira = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('IRA'),
        help_text=_('Indice de rendimento academico'),
        )

    coeficienteEvasao = models.FloatField(
        null=True,
        blank=True,
        verbose_name=_('Porcentagem de evasao'),
        help_text=_('Porcentagem de evasao'),
        )

    semestreEvasao = models.ForeignKey(
        Semestre,
        null=True,
        blank=True,
        verbose_name=_('Semestre evasao'),
        help_text=_('Semestre em que evadiu'),
        on_delete=models.CASCADE
        )

    situacaoEvasao = models.ForeignKey(
        StituacaoEvasao,
        null=True,
        blank=True,
        verbose_name=_('Situacao evasao'),
        help_text=_('Situacao em que a evasao ocorreu'),
        on_delete=models.CASCADE
        )

    alunoEvasao = models.ForeignKey(
        Aluno,
        null=True,
        blank=True,
        verbose_name=_('Aluno'),
        help_text=_('Aluno que evadiu'),
        on_delete=models.CASCADE
        )

    cursoEvasao = models.ForeignKey(
        Curso,
        null=True,
        blank=True,
        verbose_name=_('Curso evasao'),
        help_text=_('Curso em que evadiu'),
        on_delete=models.CASCADE
        )

    def __str__(self):
        return '%s/%s/%s/%s' (self.semestreEvasao, self.situacaoEvasao,
                              self.alunoEvasao, self.cursoEvasao)
