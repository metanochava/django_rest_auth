import uuid

from django.db import models

from ..models.idioma import Idioma


class Traducao(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    idioma = models.ForeignKey(Idioma, on_delete=models.CASCADE)
    chave = models.TextField(null=True, blank=True)
    traducao = models.TextField(null=True, blank=True)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.chave
