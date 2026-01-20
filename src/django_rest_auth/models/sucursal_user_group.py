import uuid

from django.db import models

from django_rest_auth.core.base.models import BaseModel


class SucursalUserGroup(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sucursal = models.ForeignKey('django_rest_auth.Sucursal', on_delete=models.CASCADE)
    user = models.ForeignKey('django_rest_auth.User', on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)

    class Meta:
        permissions = ()

    def __str__(self):
        return f'{self.user.username} | {self.sucursal.nome} | {self.group.name}'
