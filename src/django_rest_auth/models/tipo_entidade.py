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



class TipoEntidadeModulo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_entidade = models.ForeignKey(TipoEntidade, on_delete=models.CASCADE)
    modulo = models.ForeignKey("django_rest_auth.Modulo", on_delete=models.CASCADE)
    STATUS = (
        ('Activo', 'Activo'),
        ('Desativado', 'Desativado')
    )
    estado = models.CharField(max_length=100, null=True, choices=STATUS)
    created_at = models.DateField(null=True, auto_now_add=True)
    updated_at = models.DateField(null=True, auto_now=True)
    created_at_time = models.DateField(null=True, auto_now_add=True)
    updated_at_time = models.DateField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = (
            
        )

    def __str__(self):
        return str(self.tipo_entidade.nome) + "  |  " + str(self.modulo.nome)

