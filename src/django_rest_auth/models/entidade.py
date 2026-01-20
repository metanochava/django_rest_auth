import uuid

from django.db import models
from django.contrib.contenttypes.models import ContentType

from django_rest_auth.models.user import User
from django_rest_auth.models.tipo_entidade import TipoEntidade


def logo_path(instance, file_name):
    return f'{instance.tipo_entidade.nome}/{instance.nome}/{file_name}'


class Entidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True, default='-')

    logo = models.FileField(upload_to=logo_path, default='logo.png', blank=True)
    display_logo = models.BooleanField(default=True, null=True, blank=True)
    display_bar = models.BooleanField(default=True, null=True, blank=True)
    display_qr = models.BooleanField(default=True, null=True, blank=True)

    tipo_entidade = models.ForeignKey(TipoEntidade, on_delete=models.CASCADE)

    groups = models.ManyToManyField('auth.Group', blank=True)
    modelos = models.ManyToManyField(ContentType, blank=True)
    admins = models.ManyToManyField(User)

    rodape = models.CharField(max_length=2000, null=True)

    disc_space = models.FloatField(default=1048576.0, null=True)
    disc_used_space = models.FloatField(default=0.0, null=True)
    disc_free_space = models.FloatField(default=1048576.0, null=True)

    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inactivo'), (1, 'Activo'))
    )

    class Meta:
        permissions = ()

    def save(self, *args, **kwargs):
        if self.disc_free_space is None or self.disc_free_space > self.disc_space:
            self.disc_free_space = self.disc_space - self.disc_used_space
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nome or ''

