import uuid

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType


def icon_path(instance, file_name):
    return f'{instance.nome}/{file_name}'


class TipoEntidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)
    icon = models.FileField(upload_to=icon_path, default='logo.png', blank=True)
    license = models.TextField(default='license')
    label = models.CharField(max_length=100, null=True)
    ordem = models.IntegerField(default=2)
    crair_entidade = models.BooleanField(null=True, default=True)

    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo'))
    )

    groups = models.ManyToManyField(Group, blank=True)
    modelos = models.ManyToManyField(ContentType, blank=True)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome

