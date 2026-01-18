import uuid

from django.db import models


class Idioma(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)
    code = models.CharField(max_length=100, null=True)

    STATUS = (
        ('Activo', 'Activo'),
        ('Desativado', 'Desativado')
    )

    class Meta:
        permissions = ()

    def __str__(self):
        return self.code
