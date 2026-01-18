from django.db.models import Q
from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import User
from .classes.Translate import Translate
from .base import BaseSerializer


class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'password', 'mobile')

    def validate(self, attrs):
        request = self.context.get('request')
        username = attrs.get('username', '')

        if not username.isalnum():
            raise serializers.ValidationError({
                'username': Translate.tdc(
                    request,
                    'O nome de utilizador deve conter apenas caracteres alfanuméricos'
                )
            })
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


def authenticate(value=None, password=None):
    UserModel = get_user_model()
    try:
        user = UserModel.objects.get(
            Q(email=value) | Q(username=value) | Q(mobile=value)
        )
    except UserModel.DoesNotExist:
        return None

    if user.check_password(password):
        return user

    return None


class LoginSerializer(serializers.Serializer):
    identifier = serializers.CharField()
    password = serializers.CharField(write_only=True)
    tokens = serializers.SerializerMethodField(read_only=True)

    def get_tokens(self, obj):
        return obj['tokens']

    def validate(self, attrs):
        request = self.context.get('request')

        identifier = attrs.get('identifier', '').strip()
        password = attrs.get('password')

        user = authenticate(value=identifier, password=password)

        if not user:
            raise AuthenticationFailed(
                Translate.tdc(request, 'Credenciais inválidas')
            )

        if not user.is_active:
            raise AuthenticationFailed(
                Translate.tdc(request, 'Conta desativada')
            )

        if not user.is_verified:
            raise AuthenticationFailed(
                Translate.tdc(request, 'Email não verificado')
            )

        return {
            'id': user.id,
            'email': user.email,
            'username': user.username,
            'mobile': user.mobile,
            'tokens': user.tokens(),
        }


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.request = self.context.get('request')
        self.token = attrs['refresh']
        return attrs

    def save(self, **kwargs):
        try:
            RefreshToken(self.token).blacklist()
        except TokenError:
            raise AuthenticationFailed(
                Translate.tdc(self.request, 'Token inválido ou expirado')
            )


class MeSerializer(BaseSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'username', 'perfil', 'mobile']
