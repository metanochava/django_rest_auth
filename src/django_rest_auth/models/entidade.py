import uuid

from django.db import models
from django.contrib.auth.models import Group
from django.contrib.contenttypes.models import ContentType

from ..models.traducao import Traducao
from ..models.idioma import Idioma



def logo_path(instance, file_name):
    return f'{instance.tipo_entidade.nome}/{instance.nome}/{file_name}'


class Entidade(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True, default='-')

    logo = models.FileField(upload_to=logo_path, default='logo.png', blank=True)
    display_logo = models.BooleanField(default=True, null=True, blank=True)
    display_bar = models.BooleanField(default=True, null=True, blank=True)
    display_qr = models.BooleanField(default=True, null=True, blank=True)

    tipo_entidade = models.ForeignKey("django_rest_auth.TipoEntidade", on_delete=models.CASCADE)

    groups = models.ManyToManyField("auth.Group", blank=True)
    modelos = models.ManyToManyField(ContentType, blank=True)
    admins = models.ManyToManyField("django_rest_auth.User", blank=False)

    rodape = models.CharField(max_length=2000, null=True)

    disc_space = models.FloatField(default=1048576.0, null=True)
    disc_used_space = models.FloatField(default=0.0, null=True)
    disc_free_space = models.FloatField(default=1048576.0, null=True)

    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo'))
    )

    def save(self, *args, **kwargs):
        if self.disc_free_space is None or self.disc_free_space > self.disc_space:
            self.disc_free_space = self.disc_space - self.disc_used_space
        super().save(*args, **kwargs)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome


class EntidadeGroup(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entidade = models.ForeignKey("django_rest_auth.Entidade", on_delete=models.CASCADE)
    group = models.ForeignKey("auth.Group", on_delete=models.CASCADE)
    created_at = models.DateField(null=True, auto_now_add=True)
    updated_at = models.DateField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.entidade.nome}  |  {self.group.name}"


class EntidadeUser(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entidade = models.ForeignKey("django_rest_auth.Entidade", on_delete=models.CASCADE)
    user = models.ForeignKey("django_rest_auth.User", on_delete=models.CASCADE)
    created_at = models.DateField(null=True, auto_now_add=True)
    updated_at = models.DateField(null=True, auto_now=True)
    created_at_time = models.DateField(null=True, auto_now_add=True)
    updated_at_time = models.DateField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.entidade.nome}  |  {self.user.username}"


class EntidadeModulo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    entidade = models.ForeignKey("django_rest_auth.Entidade", on_delete=models.CASCADE)
    modulo = models.ForeignKey("django_rest_auth.Modulo", on_delete=models.CASCADE)
    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo'))
    )
    created_at = models.DateField(null=True, auto_now_add=True)
    updated_at = models.DateField(null=True, auto_now=True)
    created_at_time = models.DateField(null=True, auto_now_add=True)
    updated_at_time = models.DateField(null=True, auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return f"{self.entidade.nome}  |  {self.modulo.nome}"
