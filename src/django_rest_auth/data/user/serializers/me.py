from django_rest_auth.core.base.serializers import BaseSerializer
from django_rest_auth.models.user import User


class MeSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'perfil', 'mobile']
