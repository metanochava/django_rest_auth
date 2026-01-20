from django.db import models

from django_rest_auth.models.user import User
from django_rest_auth.models.entidade import Entidade
from django_rest_auth.models.sucursal import Sucursal


class AuditLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    action = models.CharField(max_length=50)
    model = models.CharField(max_length=100)
    object_id = models.CharField(max_length=100)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    sucursal = models.ForeignKey(Sucursal, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
