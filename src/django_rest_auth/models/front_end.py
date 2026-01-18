import uuid

from django.db import models

from ..base import BaseModel


class FrontEnd(BaseModel):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    nome = models.CharField(max_length=100, null=True)
    fek = models.CharField(max_length=300, null=True)
    fep = models.CharField(max_length=300, null=True)

    ACCESS_CHOICES = (
        ('read', 'Read'),
        ('write', 'Write'),
        ('readwrite', 'Read & Write'),
        ('super', 'Super (all) 😎'),
    )

    access = models.CharField(max_length=100, null=True, choices=ACCESS_CHOICES)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.nome
