import uuid
from django.db import models


class Idioma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    nome = models.CharField(max_length=100)
    code = models.CharField(max_length=10, unique=True)

    estado = models.IntegerField(
        default=1,
        choices=((0, 'Inativo'), (1, 'Ativo')),
    )

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome
