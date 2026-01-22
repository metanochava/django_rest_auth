import uuid
from django.db import models


class Testee(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    latitude = models.DecimalField(
        max_digits=9, decimal_places=6, null=True, blank=True
    )
    