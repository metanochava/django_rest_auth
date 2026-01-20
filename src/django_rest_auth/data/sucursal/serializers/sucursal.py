
from rest_framework import serializers


from django_rest_auth.models.sucursal import Sucursal


class SucursalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sucursal
        fields = [
            'id',
            'nome',
            'entidade',
        ]
