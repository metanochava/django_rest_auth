from django_rest_auth.core.base.serializers import BaseSerializer
from django_rest_auth.models.ficheiro import Ficheiro


class FicheiroGravarSerializer(BaseSerializer):
    class Meta:
        model = Ficheiro
        fields = [
            'id',
            'ficheiro',
            'size',
            'modelo',
            'estado',
            'chamador',
            'funcionalidade',
            'sucursal',
            'entidade',
            'created_at',
            'updated_at',
            'created_at_time',
            'updated_at_time',
            'is_deleted',
        ]
