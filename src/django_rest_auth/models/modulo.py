import uuid

from django.db import models


class Modulo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome
