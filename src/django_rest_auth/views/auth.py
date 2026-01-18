import re

from django.utils import timezone

from rest_framework import generics, status, permissions
from rest_framework.response import Response

from .models import UserLogin
from .serializers import LoginSerializer, LogoutSerializer, UserLoginSerializer


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if not is_valid_email(request.data.get('email')):
            request.data['email'] = request.data['email'] + '@paravalidar.com'

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        data = request.data.copy()
        data['user'] = serializer.data['id']

        user_login = UserLoginSerializer(data=data)
        user_login.is_valid(raise_exception=True)
        user_login.save()

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )


class LoginsAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_login = UserLogin.objects.filter(
            user=request.user
        ).order_by('data', '-hora')

        user_logins = UserLoginSerializer(
            user_login,
            many=True
        )

        return Response(
            user_logins.data,
            status=status.HTTP_200_OK
        )


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer
    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
