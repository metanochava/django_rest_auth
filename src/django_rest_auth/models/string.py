from django.db import models


class String(models.Model):
    texto = models.CharField(max_length=255, unique=True)

    class Meta:
        ordering = ["texto"]

    def __str__(self):
        return self.texto
