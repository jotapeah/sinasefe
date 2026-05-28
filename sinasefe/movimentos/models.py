from django.db import models


# Create your models here.
class Movimento(models.Model):
    data_movimento = models.DateField(verbose_name="Data")
    descricao = models.CharField(verbose_name="Descrição", max_length=256)
    documento = models.CharField(
        verbose_name="Documento", max_length=64, null=True, blank=True
    )
    valor = models.DecimalField(verbose_name="Valor", max_digits=10, decimal_places=2)

    class Meta:
        verbose_name = "Movimento"
        verbose_name_plural = "Movimento"

    def __str__(self) -> str:
        return f"({self.descricao}) - {self.valor}"
