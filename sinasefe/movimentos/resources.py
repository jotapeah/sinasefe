from boletos.resources import BRDecimalWidget
from import_export.fields import Field
from import_export.resources import ModelResource
from import_export.widgets import DateWidget

from .models import Movimento


class MovimentoResource(ModelResource):
    data_movimento = Field(
        attribute="data_movimento",
        column_name="Data",
        widget=DateWidget(format="%d/%m/%Y"),
    )
    descricao = Field(attribute="descricao", column_name="Descricao")
    documento = Field(attribute="documento", column_name="Documento")
    valor = Field(attribute="valor", column_name="Valor", widget=BRDecimalWidget())

    def before_import_row(self, row, **kwargs):
        print(row["Data"])

    class Meta:
        model = Movimento
        import_id_fields = ["data_movimento", "descricao", "valor"]
        encoding = "utf-8"
