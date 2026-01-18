import uuid

from django.db import models


class Ficheiro(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    ficheiro = models.FileField(upload_to='ficheiros', null=True, blank=True)
    size = models.FloatField(null=False)
    modelo = models.CharField(max_length=100, null=True)

    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo'))
    )

    ESCOLHA = (
        ('File', 'File'),
        ('Perfil', 'Perfil'),
        ('Logo', 'Logo'),
        ('Foto', 'Foto'),
        ('CapaSite', 'CapaSite'),
    )

    funcionalidade = models.CharField(
        max_length=100,
        null=True,
        default='File',
        choices=ESCOLHA
    )

    chamador = models.CharField(max_length=100, null=True, blank=True)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.ficheiro.name if self.ficheiro else ''
