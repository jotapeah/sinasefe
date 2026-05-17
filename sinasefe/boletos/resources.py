from decimal import Decimal

from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import DateWidget, DecimalWidget, IntegerWidget

from .models import Boleto


class BrDecimalWidget(DecimalWidget):

    def clean(self, value, row=None, **kwargs):

        if value in (None, ''):
            return None

        value = str(value)

        # remove separador de milhar
        value = value.replace('.', '')

        # troca vírgula decimal por ponto
        value = value.replace(',', '.')

        return Decimal(value)

class BoletoResource(ModelResource):
    nome_pagador = Field(attribute="nome_pagador", column_name="Nome Pagador")
    data_baixa = Field(
        attribute="data_baixa",
        column_name="Data Baixa",
        widget=DateWidget(format="%d/%m/%Y"),
    )
    data_pagamento = Field(
        attribute="data_pagamento",
        column_name="Data Pagamento",
        widget=DateWidget(format="%d/%m/%Y"),
    )
    data_vencimento = Field(
        attribute="data_vencimento",
        column_name="Data Vencimento",
        widget=DateWidget(format="%d/%m/%Y"),
    )
    nosso_numero = Field(attribute="nosso_numero", column_name="Nosso Numero")
    seu_numero = Field(attribute="seu_numero", column_name="Seu Numero")
    valor = Field(attribute="valor", column_name="Valor", widget=BrDecimalWidget())
    identificacao = Field(attribute="identificacao", column_name="Identificacao")
    parcela = Field(attribute="parcela", column_name="Parcela", widget=IntegerWidget())
    total_parcelas = Field(
        attribute="total_parcelas", column_name="Total Parcelas", widget=IntegerWidget()
    )
    codigo_pagador = Field(attribute="codigo_pagador", column_name="Cod Pagador")
    valor_liquidacao_titulo = Field(
        attribute="valor_liquidacao_titulo",
        column_name="Valor Liquidacao Titulo",
        widget=BrDecimalWidget(),
    )

    class Meta:
        model = Boleto
        import_id_fields = ["nosso_numero"]
        encoding = "utf-8"
