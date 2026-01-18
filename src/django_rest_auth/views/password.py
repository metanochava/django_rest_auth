import os
import base64

from django.conf import settings
from django.contrib import auth
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.core.mail import EmailMultiAlternatives
from django.http import HttpResponsePermanentRedirect
from django.urls import reverse
from django.utils.encoding import (
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)

from rest_framework import generics, status
from rest_framework.response import Response

import pyotp

from .models import User
from .serializers import (
    ResetPasswordEmailRequestSerializer,
    SetNewPasswordSerializer,
)
from .classes.Translate import Translate
from .utils.templates import render_email_template
from .utils.generateKey import generateKey





class ChangePasswordMobileAPIView(generics.GenericAPIView):
    def post(self, request):
        phone = request.data.get('mobile')
        user = User.objects.get(mobile=phone)

        keygen = generateKey()
        key = base64.b32encode(
            keygen.returnValue(phone).encode()
        )
        otp = pyotp.HOTP(key)

        if otp.verify(request.data.get("otp"), user.counter):
            user.set_password(request.data.get('password'))
            user.save()
            return Response(
                {
                    'alert_success': Translate.tdc(
                        request,
                        'Senha redefinida com sucesso'
                    )
                },
                status=status.HTTP_202_ACCEPTED
            )

        return Response(
            {
                'alert_error': Translate.tdc(
                    request,
                    'OTP inválido ou expirado'
                )
            },
            status=status.HTTP_400_BAD_REQUEST
        )


class ChangePasswordEmailAPIView(generics.GenericAPIView):
    def post(self, request):
        user = auth.authenticate(
            email=request.data.get('email'),
            password=request.data.get('password')
        )

        if not user:
            return Response(
                {
                    'alert_error': Translate.tdc(
                        request,
                        'A senha atual está incorreta'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if len(request.data.get('passwordNova', '')) < 8:
            return Response(
                {
                    'alert_error': Translate.tdc(
                        request,
                        'A senha deve ter no mínimo 8 caracteres'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        user = User.objects.get(id=user.id)
        user.set_password(request.data.get('passwordNova'))
        user.save()

        return Response(
            {
                'alert_success': Translate.tdc(
                    request,
                    'Senha alterada com sucesso'
                )
            },
            status=status.HTTP_202_ACCEPTED
        )




class RequestPasswordResetEmail(generics.GenericAPIView):
    serializer_class = ResetPasswordEmailRequestSerializer

    def post(self, request):
        nome = str(
            str(request.META['HTTP_ORIGIN'])
            .split('.')[0]
            .upper()
        ).split('/')[-1]

        serializer = self.serializer_class(data=request.data)
        email = request.data.get('email', '')

        if User.objects.filter(email=email).exists():
            user = User.objects.get(email=email)

            uidb64 = urlsafe_base64_encode(
                smart_bytes(user.id)
            )
            token = PasswordResetTokenGenerator().make_token(user)

            relative_link = reverse(
                'password-reset-confirm',
                kwargs={'uidb64': uidb64, 'token': token}
            )

            redirect_url = request.data.get('redirect_url', '')

            try:
                absurl = (
                    '\n'
                    + request.META['HTTP_ORIGIN']
                    + '/#/resetpassword'
                    + relative_link
                )
            except Exception:
                absurl = (
                    '\nhttp://mws.mytech.co.mz/#/resetpassword'
                    + relative_link
                )

            email_body = absurl + "?redirect_url=" + redirect_url

            html_message = render_email_template(
                'PASSWORD_RESET',
                {
                    'link': email_body,
                    'username': user.username,
                    'logo': 'logo'
                }
            )

            try:
                mail = EmailMultiAlternatives(
                    subject=Translate.tdc(
                        request,
                        'Redefinição de senha'
                    ),
                    body='',
                    to=[email],
                )
                mail.attach_alternative(
                    html_message,
                    "text/html"
                )
                mail.send()

            except Exception as e:
                return Response(
                    {'alert_error': str(e)},
                    status=status.HTTP_500_INTERNAL_SERVER_ERROR
                )

        return Response(
            {
                'alert_success': Translate.tdc(
                    request,
                    'Enviámos um link para redefinir a sua senha'
                )
            },
            status=status.HTTP_200_OK
        )



class CustomRedirect(HttpResponsePermanentRedirect):
    allowed_schemes = [os.environ.get('APP_SCHEME'), 'http', 'https']

class PasswordTokenCheckAPI(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer

    def get(self, request, uidb64, token):

        redirect_url = request.GET.get('redirect_url')

        try:
            id = smart_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(id=id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                if len(redirect_url) > 3:
                    return CustomRedirect(redirect_url+'?token_valid=False')
                else:
                    return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

            if redirect_url and len(redirect_url) > 3:
                return CustomRedirect(redirect_url+'?token_valid=True&message=Credentials Valid&uidb64='+uidb64+'&token='+token)
            else:
                return CustomRedirect(os.environ.get('FRONTEND_URL', '')+'?token_valid=False')

        except DjangoUnicodeDecodeError as identifier:
            try:
                if not PasswordResetTokenGenerator().check_token(user):
                    return CustomRedirect(redirect_url+'?token_valid=False')
                    
            except UnboundLocalError as e:
                return Response({'alert_error': 'O token não é válido, solicite um novo'}, status=status.HTTP_400_BAD_REQUEST)


class SetNewPasswordAPIView(generics.GenericAPIView):
    serializer_class = SetNewPasswordSerializer
    def patch(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response({'alert_success': True, 'message': 'Senha redefinida com sucesso'}, status=status.HTTP_200_OK)
