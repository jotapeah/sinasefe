from datetime import timedelta
from decimal import Decimal

from django.contrib import admin
from django.db.models import Q, Sum
from django.utils import timezone
from import_export.admin import ImportExportModelAdmin

from .models import Boleto
from .resources import BoletoResource


class BoletoCustomFilter(admin.SimpleListFilter):
    title = "Vencido"
    parameter_name = "vencido"

    def lookups(self, request, model_admin):
        return [
            ("mais_60", "60+ dias"),
        ]

    def queryset(self, request, queryset):
        if self.value() == "mais_60":
            data_limite = timezone.now().date() - timedelta(days=60)


            return queryset.filter(
                (
                    Q(data_pagamento__isnull=True)
                    & Q(data_vencimento__lte=data_limite)
                )
            ).order_by("nome_pagador")

        return queryset

class QuitadoComOutroBoletoFilter(admin.SimpleListFilter):
    title = "Pago c/ outro boleto"
    parameter_name = "pago_outro_boleto"

    def lookups(self, request, model_admin):
        return (
            ("sim", "Sim"),
            ("nao", "Não"),
        )

    def queryset(self, request, queryset):
        if self.value() == "sim":
            return queryset.filter(quitado_com_boleto__isnull=False)
        if self.value() == "nao":
            return queryset.filter(quitado_com_boleto__isnull=True)
        return queryset


class BoletoReemitidoFilter(admin.SimpleListFilter):
    title = "Reemitido"
    parameter_name = "reemitido"

    def lookups(self, request, model_admin):
        return (
            ("sim", "Sim"),
        )

    def queryset(self, request, queryset):
        if self.value() == "sim":
            return queryset.filter(seu_numero__icontains="/")
        return queryset

class BaixadoFilter(admin.SimpleListFilter):
    title = "Baixado"
    parameter_name = "baixado"

    def lookups(self, request, model_admin):
        return (
            ("sim", "Sim"),
            ("nao", "Não"),
        )

    def queryset(self, request, queryset):
        if self.value() == "sim":
            return queryset.filter(data_baixa__isnull=False)
        if self.value() == "nao":
            return queryset.filter(data_baixa__isnull=True)
        return queryset


@admin.register(Boleto)
class BoletoAdmin(ImportExportModelAdmin):
    list_display = (
        "nome_pagador",
        "data_vencimento",
        "data_pagamento",
        "data_baixa",
        "nosso_numero",
        "seu_numero",
        "valor",
    )
    list_filter = (
        BoletoCustomFilter,
        BoletoReemitidoFilter,
        QuitadoComOutroBoletoFilter,
        BaixadoFilter,
        "data_pagamento",
    )
    search_fields = ("nome_pagador", "nosso_numero", "seu_numero")
    resource_classes = [BoletoResource]
    ordering = ["nome_pagador", "data_vencimento"]
    date_hierarchy = "data_vencimento"
    list_per_page = 1000
    change_list_template = 'admin/boleto/boleto-changelist.html'
    raw_id_fields = ("quitado_com_boleto",)

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(request, extra_context=extra_context)

        try:
            qs = response.context_data['cl'].queryset
            total = qs.aggregate(total=Sum('valor'))['total'] or Decimal('0')

            total_formatado = (
                f'{total:,.2f}'
                .replace(',', 'X')
                .replace('.', ',')
                .replace('X', '.')
            )

        except (AttributeError, KeyError):
            total_formatado = '0,00'

        response.context_data['total_valor'] = total_formatado

        return response
