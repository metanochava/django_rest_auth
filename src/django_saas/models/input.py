from django.db import models
from django_saas.core.base.models import TimeModel

class Input(TimeModel):
    nome = models.CharField(max_length=100, unique=True)
    class Meta:
        ordering = ["nome"]

    def __str__(self):
        return self.nome
