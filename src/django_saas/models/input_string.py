from django.db import models


class InputString(models.Model):
    input = models.ForeignKey(
        "django_saas.Input",
        on_delete=models.CASCADE,
        related_name="input_strings",
    )
    string = models.ForeignKey(
        "django_saas.String",
        on_delete=models.CASCADE,
        related_name="string_inputs",
    )

    class Meta:
        unique_together = ("input", "string")
        verbose_name = "Input ↔ String"
        verbose_name_plural = "Inputs ↔ Strings"

    def __str__(self):
        return f"{self.input.nome} -> {self.string.texto}"
