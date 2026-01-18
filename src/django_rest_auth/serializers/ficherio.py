
from rest_framework import serializers
from ..models.ficheiro import Ficheiro
from ..base import BaseSerializer


class FicheiroSerializer(BaseSerializer):
    class Meta:
        model = Ficheiro
        fields = ['id', 'ficheiro', 'size', 'modelo', 'estado', 'chamador',
                  'funcionalidade', 'sucursal', 'entidade',
                  'created_at', 'updated_at', 'created_at_time',
                  'updated_at_time', 'is_deleted']