from django.contrib import admin
from .models import FormaEvasao, FormaIngresso, Disciplina, Curso, Aluno
from .models import SituacaoMatricula, Matricula


@admin.register(FormaEvasao)
class FormaEvasao(admin.ModelAdmin):
    list_display = ('descricao_evasao', 'id')
    search_fields = ('descricao_evasao',)


@admin.register(FormaIngresso)
class FormaIngresso(admin.ModelAdmin):
    list_display = ('descricao_ingresso', 'id')
    search_fields = ('descricao_ingresso',)


@admin.register(Disciplina)
class Disciplina(admin.ModelAdmin):
    list_display = ('codigo_disciplina', 'descricao_disciplina',
                    'carga_horaria', 'id')
    search_fields = ('codigo_disciplina', 'descricao_disciplina',
                     'carga_horaria',)


@admin.register(Curso)
class Curso(admin.ModelAdmin):
    list_display = ('codigo_curso', 'descricao_curso', 'id')
    search_fields = ('codigo_curso', 'descricao_curso',)
    filter_horizontal = ('disciplinas',)


@admin.register(SituacaoMatricula)
class SituacaoMatricula(admin.ModelAdmin):
    list_display = ('descricao_situacao_matricula', 'id')
    search_fields = ('descricao_situacao_matricula',)


@admin.register(Aluno)
class Aluno(admin.ModelAdmin):
    list_display = ('grr_aluno', 'nome_aluno', 'periodo_ingresso',
                    'periodo_evasao', 'forma_ingresso', 'forma_evasao', 'id')
    search_fields = ('grr_aluno', 'nome_aluno', 'periodo_ingresso',
                     'periodo_evasao', 'forma_ingresso__descricao_ingresso',
                     'forma_evasao__descricao_evasao',)
    autocomplete_fields = ('forma_ingresso', 'forma_evasao',)


@admin.register(Matricula)
class Matricula(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'media_final_matricula',
                    'faltas_matricula', 'periodo_matricula',
                    'situacao_matricula', 'id')
    search_fields = ('media_final_matricula', 'faltas_matricula',
                     'periodo_matricula', 'aluno__nome_aluno',
                     'disciplina__codigo_disciplina',
                     'situacao_matricula__descricao_situacao_matricula',)
    autocomplete_fields = ('aluno', 'disciplina', 'situacao_matricula',)
