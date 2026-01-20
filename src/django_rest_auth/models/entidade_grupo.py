import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType
from django_rest_auth.models.entidade import Entidade


class EntidadeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entidade = models.ForeignKey(Entidade, on_delete=models.CASCADE)
    group = models.ForeignKey('auth.Group', on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f'{self.entidade.nome} | {self.group.name}'

