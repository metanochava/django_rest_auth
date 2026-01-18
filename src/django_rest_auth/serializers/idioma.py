
from rest_framework import serializers
from ..models.idioma import Idioma

class IdiomaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idioma
        fields = ['id', 'nome', 'code', 'estado']