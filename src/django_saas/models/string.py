from django.db import models
from django_saas.core.base.models import TimeModel

class String(TimeModel):
    texto = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["texto"]

    def __str__(self):
        return self.texto
