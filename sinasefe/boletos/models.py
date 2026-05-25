from django.db import models


class Boleto(models.Model):
    quitado_com_boleto = models.ForeignKey(
        to="self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        help_text="Indique o boleto que quita esse valor",
    )
    nome_pagador = models.CharField(verbose_name="Nome do pagador", max_length=512)
    data_baixa = models.DateField(verbose_name="Data de baixa", null=True, blank=True)
    data_pagamento = models.DateField(
        verbose_name="Data de pagamento", null=True, blank=True
    )
    data_vencimento = models.DateField(
        verbose_name="Data de vencimento", null=True, blank=True
    )
    nosso_numero = models.CharField(verbose_name="Nosso número", max_length=64)
    seu_numero = models.CharField(verbose_name="Seu número", max_length=64)
    valor = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2)
    identificacao = models.CharField(verbose_name="Identificação", max_length=128)
    parcela = models.PositiveSmallIntegerField(
        verbose_name="Parcela", null=True, blank=True
    )
    total_parcelas = models.PositiveSmallIntegerField(
        verbose_name="Total de parcelas", null=True, blank=True
    )
    codigo_pagador = models.CharField(verbose_name="Código pagador", max_length=16)
    valor_liquidacao_titulo = models.DecimalField(
        verbose_name="Valor Liquidacao Titulo",
        max_digits=10,
        decimal_places=2,
        null=True,
        blank=True,
    )
    observacao = models.TextField(verbose_name="Observação", null=True, blank=True)
    considerar_pago = models.BooleanField(verbose_name="Considerar Pago", default=False)

    class Meta:
        verbose_name = "Boleto"
        verbose_name_plural = "Boletos"

    def __str__(self) -> str:
        return f"({self.identificacao}) - {self.nome_pagador}"
