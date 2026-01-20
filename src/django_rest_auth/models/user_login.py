import uuid
from django.db import models
from django_rest_auth.models.user import User


class UserLogin(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    dispositivo = models.TextField(null=True)
    mobile = models.CharField(max_length=100, null=True)
    info = models.TextField(null=True)
    local_lat = models.CharField(max_length=100, null=True)
    local_lon = models.CharField(max_length=100, null=True)
    local_nome = models.CharField(max_length=100, null=True)
    data = models.DateField(null=True, auto_now_add=True)
    hora = models.TimeField(null=True, auto_now_add=True)
    is_blocked = models.BooleanField(default=False)

    class Meta:
        permissions = ()

    def __str__(self):
        return self.dispositivo or ''
