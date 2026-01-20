import uuid

from django.db import models

class SucursalUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    sucursal = models.ForeignKey('django_rest_auth.Sucursal', on_delete=models.CASCADE)
    user = models.ForeignKey('django_rest_auth.User', on_delete=models.CASCADE)

    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f'{self.sucursal.nome} | {self.user.username}'
