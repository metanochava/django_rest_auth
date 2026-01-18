from rest_framework import serializers

from .models import TipoEntidade
from .serializers import GrupoSerializer
from .base import BaseSerializer


class TipoEntidadeSerializer(BaseSerializer):
    permanent_fields_files = ['icon']

    groups = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return GrupoSerializer(obj.groups.all(), many=True).data

    class Meta:
        model = TipoEntidade
        fields = [ 'id', 'nome', 'estado', 'icon', 'label', 'groups', 'crair_entidade', 'created_at', 'created_at_time', 'updated_at', 'updated_at_time', 'is_deleted', ]
