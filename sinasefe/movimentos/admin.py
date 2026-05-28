from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from .models import Movimento
from .resources import MovimentoResource


@admin.register(Movimento)
class MovimentoAdmin(ImportExportModelAdmin):
    list_display = ["data_movimento", "descricao", "documento", "valor"]
    search_fields = ["data_movimento", "descricao", "documento", "valor"]
    list_per_page = 1000
    resource_classes = [MovimentoResource]
