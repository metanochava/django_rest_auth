import uuid

from django.db import models
from django.contrib.auth.models import Group

from django_rest_auth.core.base.models import BaseModel
from django_rest_auth.models.endereco import Endereco


class Sucursal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)

    entidade = models.ForeignKey('django_rest_auth.Entidade', on_delete=models.CASCADE)
    endereco = models.ForeignKey(Endereco, on_delete=models.SET_NULL, null=True, blank=True)

    rodape = models.CharField(max_length=600, default='.', null=True)
    icon = models.CharField(max_length=100, default='.', null=True)
    label = models.CharField(max_length=100, default='.', null=True)

    groups = models.ManyToManyField(Group, blank=True)

    estado = models.IntegerField(default=1, null=True, choices=((0, 'Inactivo'), (1, 'Activo')))

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome or ''

