import re

from rest_framework import generics, status
from rest_framework.response import Response

from django_rest_auth.core.utils.translate import Translate
from django_rest_auth.models.user_login import UserLogin
from django_rest_auth.data.user.serializers.login import LoginSerializer
from django_rest_auth.data.user.serializers.logins import LoginSerializer


def is_valid_email(email):
    regex = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return re.match(regex, email) is not None


class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        if not is_valid_email(request.data.get('email')):
            request.data['email'] = (
                request.data['email'] + '@paravalidar.com'
            )

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)

        data = request.data.copy()
        data['user'] = serializer.data['id']

        user_login = LoginSerializer(data=data)
        user_login.is_valid(raise_exception=True)
        user_login.save()

        return Response(
            {
                'alert_success': Translate.tdc(
                    request,
                    'Login efectuado com sucesso'
                ),
                'data': serializer.data
            },
            status=status.HTTP_200_OK
        )
