
from rest_framework import generics, status, permissions
from rest_framework.response import Response

from django_rest_auth.models.user_login import UserLogin
from django_rest_auth.data.user.serializers.login import LoginSerializer

class LoginsAPIView(generics.GenericAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user_login = UserLogin.objects.filter(
            user=request.user
        ).order_by('data', '-hora')

        user_logins = LoginSerializer(
            user_login,
            many=True
        )

        return Response(
            user_logins.data,
            status=status.HTTP_200_OK
        )
