from django.contrib import admin
from .models import FormaEvasao, FormaIngresso, Disciplina, Curso, Aluno
from .models import SituacaoMatricula, Matricula, PredicaoEvasao, Comentario


class ReadOnlyAdmin():
    """Read only model admin."""

    def has_delete_permission(self, request, obj=None):
        """Disable delete permission."""
        return False

    def has_add_permission(self, request, obj=None):
        """Disable create permission."""
        return False

    def change_view(self, request, object_id, extra_context=None):
        """Change the base view."""
        extra_context = extra_context or {}
        extra_context['show_save_and_continue'] = False
        extra_context['show_save'] = False
        extra_context['show_save_and_add_another'] = False
        return super(ReadOnlyAdmin, self).change_view(
            request, object_id, extra_context=extra_context)


@admin.register(FormaEvasao)
class FormaEvasao(admin.ModelAdmin):
    list_display = ('descricao_evasao', 'id',)
    search_fields = ('descricao_evasao',)


@admin.register(FormaIngresso)
class FormaIngresso(admin.ModelAdmin):
    list_display = ('descricao_ingresso', 'id',)
    search_fields = ('descricao_ingresso',)


@admin.register(Disciplina)
class Disciplina(admin.ModelAdmin):
    list_display = ('codigo_disciplina', 'descricao_disciplina',
                    'carga_horaria', 'id',)
    search_fields = ('codigo_disciplina', 'descricao_disciplina',
                     'carga_horaria',)


@admin.register(Curso)
class Curso(admin.ModelAdmin):
    list_display = ('codigo_curso', 'descricao_curso', 'id')
    search_fields = ('codigo_curso', 'descricao_curso',)
    filter_horizontal = ('disciplinas',)


@admin.register(SituacaoMatricula)
class SituacaoMatricula(admin.ModelAdmin):
    list_display = ('descricao_situacao_matricula', 'id',)
    search_fields = ('descricao_situacao_matricula',)


@admin.register(Aluno)
class Aluno(ReadOnlyAdmin, admin.ModelAdmin):
    list_display = ('grr_aluno', 'nome_aluno', 'periodo_ingresso',
                    'periodo_evasao', 'forma_ingresso', 'forma_evasao', 'id',)
    search_fields = ('grr_aluno', 'nome_aluno', 'periodo_ingresso',
                     'periodo_evasao', 'forma_ingresso__descricao_ingresso',
                     'forma_evasao__descricao_evasao',)
    autocomplete_fields = ('forma_ingresso', 'forma_evasao',)
    readonly_fields = ('grr_aluno', 'nome_aluno', 'periodo_ingresso',
                       'periodo_evasao', 'forma_ingresso', 'forma_evasao',)


@admin.register(Matricula)
class Matricula(ReadOnlyAdmin, admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'media_final_matricula',
                    'faltas_matricula', 'periodo_matricula',
                    'situacao_matricula', 'curso', 'id',)
    search_fields = ('media_final_matricula', 'faltas_matricula',
                     'periodo_matricula', 'aluno__nome_aluno',
                     'disciplina__codigo_disciplina',
                     'situacao_matricula__descricao_situacao_matricula',
                     'curso',)
    autocomplete_fields = ('aluno', 'disciplina', 'situacao_matricula',
                           'curso',)
    readonly_fields = ('aluno', 'disciplina', 'media_final_matricula',
                       'faltas_matricula', 'periodo_matricula',
                       'situacao_matricula', 'curso',)


@admin.register(PredicaoEvasao)
class PredicaoEvasao(ReadOnlyAdmin, admin.ModelAdmin):
    list_display = ('aluno', 'forma_evasao', 'periodo_predicao',
                    'script_predicao', 'id',)
    search_fields = ('aluno__nome_aluno', 'forma_evasao__descricao_evasao',
                     'periodo_predicao', 'script_predicao',)
    autocomplete_fields = ('aluno', 'forma_evasao',)
    readonly_fields = ('periodo_predicao', 'script_predicao', 'aluno',
                       'forma_evasao',)


@admin.register(Comentario)
class Comentario(ReadOnlyAdmin, admin.ModelAdmin):
    list_display = ('user', 'aluno', 'texto_comentario', 'data_comentario',
                    'id',)
    search_fields = ('user__username', 'aluno__nome_aluno',
                     'texto_comentario', 'data_comentario',)
    autocomplete_fields = ('user', 'aluno',)
    readonly_fields = ('user', 'aluno', 'texto_comentario', 'data_comentario',)
