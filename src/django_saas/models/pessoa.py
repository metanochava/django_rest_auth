import uuid
from django.db import models
from django_saas.core.base.models import TimeModel

from django.contrib.contenttypes.fields import GenericRelation



class Pessoa(TimeModel):
    nome = models.CharField(max_length=100, null=True)
    apelido = models.CharField(max_length=100, null=True)
    endereco = models.ForeignKey('django_saas.Endereco', on_delete=models.CASCADE, null=True, blank=True)
    documentos = GenericRelation('django_saas.Documento')

    class Meta:
        verbose_name = 'Pessoa'
        verbose_name_plural = 'Pessoas'
        permissions = ()
        

    def __str__(self):
        return self.nome