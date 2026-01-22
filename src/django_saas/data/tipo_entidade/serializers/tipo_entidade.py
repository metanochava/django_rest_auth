from rest_framework import serializers

from django_saas.core.base.serializers import BaseSerializer
from django_saas.models.tipo_entidade import TipoEntidade
from django_saas.data.group.serializers.grupo import GrupoSerializer


class TipoEntidadeSerializer(BaseSerializer):
    permanent_fields_files = ['icon']
    estado_display = serializers.CharField(
        source="get_estado_display",
        read_only=True
    )


    groups = serializers.SerializerMethodField()

    def get_groups(self, obj):
        return GrupoSerializer(
            obj.groups.all(),
            many=True
        ).data

    class Meta:
        model = TipoEntidade
        fields = "__all__"
