from django.db import models
from apps.core.models import BaseModel
from apps.clientes.models import Cliente


class Venda(BaseModel):
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name='vendas')
    data = models.DateField()
    valor = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.cliente.nome} - {self.data} - R$ {self.valor}"

    class Meta:
        verbose_name = 'Venda'
        verbose_name_plural = 'Vendas'
        ordering = ['-data']