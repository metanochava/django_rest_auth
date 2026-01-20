from rest_framework import serializers

from django_rest_auth.core.base.serializers import BaseSerializer
from django_rest_auth.models.tipo_entidade import TipoEntidade
from django_rest_auth.data.group.serializers.grupo import GrupoSerializer


class TipoEntidadeSerializer(BaseSerializer):
    permanent_fields_files = ['icon']

    groups = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return GrupoSerializer(
            obj.groups.all(),
            many=True
        ).data

    class Meta:
        model = TipoEntidade
        fields = [
            'id',
            'nome',
            'estado',
            'icon',
            'label',
            'groups',
            'criar_entidade',
            'created_at',
            'created_at_time',
            'updated_at',
            'updated_at_time',
            'is_deleted',
        ]
