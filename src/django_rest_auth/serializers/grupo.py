
from rest_framework import serializers
from .models.grupo import Grupo

class GrupoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']