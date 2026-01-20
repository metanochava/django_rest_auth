from django.conf import settings
from django.db import models
# good

class BaseModel(models.Model):
    estado = models.IntegerField(
        default=1,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo')),
    )

    entidade = models.ForeignKey(
        "django_rest_auth.Entidade",
        on_delete=models.CASCADE,
        related_name="%(class)s_entidade"
    )

    sucursal = models.ForeignKey(
        "django_rest_auth.Sucursal",
        on_delete=models.CASCADE,
        related_name="%(class)s_sucursal"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created"
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True
