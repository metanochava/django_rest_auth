from django.conf import settings
from django.db import models
import uuid
# good


class TimeModel(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    estado = models.IntegerField(
        default=0,
        null=True,
        choices=((0, 'Inativo'), (1, 'Ativo')),
    )
    created_at = models.DateField(auto_now_add=True, null=True)
    updated_at = models.DateField(auto_now=True, null=True)
    created_at_time = models.DateTimeField(auto_now_add=True, null=True)
    updated_at_time = models.DateTimeField(auto_now=True, null=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True

class BaseModel(TimeModel):
    entidade = models.ForeignKey(
        "django_saas.Entidade",
        on_delete=models.CASCADE,
        related_name="%(class)s_entidade"
    )

    sucursal = models.ForeignKey(
        "django_saas.Sucursal",
        on_delete=models.CASCADE,
        related_name="%(class)s_sucursal"
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_created",
        
    )

    updated_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="%(class)s_updated"
    )

    class Meta:
        abstract = True



