from django_saas.core.base.serializers import BaseSerializer
from django_saas.models.user import User


class MeSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'perfil', 'mobile']
