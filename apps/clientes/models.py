from django.db import models
from apps.core.models import BaseModel


class Cliente(BaseModel):
    nome = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    nascimento = models.DateField()

    class Meta:
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'
        ordering = ['nome']

    def __str__(self):
        return self.nome
    
