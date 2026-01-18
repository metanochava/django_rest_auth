import jwt

from django.conf import settings

from rest_framework import status, views
from rest_framework.response import Response

from .models import User
from .serializers import EmailVerificationSerializer
from .classes.Translate import Translate


class VerifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer

    def get(self, request):
        token = request.GET.get('token')
        try:
            payload = jwt.decode(
                token,
                settings.SECRET_KEY,
                algorithms=["HS256"]
            )
            user = User.objects.get(id=payload['user_id'])

            if not user.is_verified:
                user.is_verified = True
                user.save()

            return Response(
                {'alert_success': Translate.tdc(request, 'Conta ativada com sucesso')},
                status=status.HTTP_200_OK
            )

        except jwt.ExpiredSignatureError:
            return Response(
                {'alert_error': Translate.tdc(request, 'Ativação expirada')},
                status=status.HTTP_400_BAD_REQUEST
            )

        except jwt.exceptions.DecodeError:
            return Response(
                {'alert_error': Translate.tdc(request, 'Token inválido')},
                status=status.HTTP_400_BAD_REQUEST
            )
