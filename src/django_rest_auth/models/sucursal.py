import uuid

from django.db import models
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group

from ..base import BaseModel  # ajusta se o nome for diferente
from .endereco import Endereco

class Sucursal(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)

    entidade = models.ForeignKey(
        "django_rest_auth.Entidade",
        on_delete=models.CASCADE
    )

    endereco = models.ForeignKey(
        Endereco,
        on_delete=models.SET_NULL,
        null=True,
        blank=True
    )

    rodape = models.CharField(max_length=600, default='.', null=True)
    icon = models.CharField(max_length=100, default='.', null=True)
    label = models.CharField(max_length=100, default='.', null=True)

    groups = models.ManyToManyField(Group, blank=True)

    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo'))
    )

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome


class SucursalGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sucursal = models.ForeignKey(
        "django_rest_auth.Sucursal",
        on_delete=models.CASCADE
    )

    group = models.ForeignKey(Group, on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.sucursal.nome} | {self.group.name}"


class SucursalUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sucursal = models.ForeignKey(
        "django_rest_auth.Sucursal",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey("django_rest_auth.User", on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.sucursal.nome} | {self.user.username}"


class SucursalUserGroup(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sucursal = models.ForeignKey(
        "django_rest_auth.Sucursal",
        on_delete=models.CASCADE
    )

    user = models.ForeignKey("django_rest_auth.User", on_delete=models.CASCADE)
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.user.username} | {self.sucursal.nome} | {self.group.name}"
