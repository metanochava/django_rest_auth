import uuid

from django.db import models

class TipoEntidadeModulo(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    tipo_entidade = models.ForeignKey("django_rest_auth.TipoEntidade", on_delete=models.CASCADE)
    modulo = models.ForeignKey("django_rest_auth.Modulo", on_delete=models.CASCADE)
    STATUS = (
        (0, 'Inativo'),
        (1, 'Activo')
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

