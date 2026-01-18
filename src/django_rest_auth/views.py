# =========================
# Python standard library
# =========================
import os
import re
import json
import base64
import smtplib
import jwt
from datetime import datetime
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# =========================
# Django core
# =========================
from django.conf import settings
from django.shortcuts import render, redirect
from django.template import loader
from django.http import HttpResponsePermanentRedirect
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import send_mail, EmailMultiAlternatives
from django.core.serializers.json import DjangoJSONEncoder
from django.contrib import auth
from django.contrib.auth.models import Group
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.utils import timezone
from django.utils.encoding import (
    smart_str,
    smart_bytes,
    DjangoUnicodeDecodeError,
)
from django.utils.http import (
    urlsafe_base64_decode,
    urlsafe_base64_encode,
)


# =========================
# Django REST Framework
# =========================
from rest_framework import generics, status, views, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied
from rest_framework_simplejwt.tokens import RefreshToken


# =========================
# Third-party
# =========================
import pyotp


# =========================
# Local application
# =========================
from .models import User, UserLogin, TipoEntidade
from .serializers import *
from .decorators import isPermited
from .utils.templates import render_email_templateF
from .classes import UserName






class Mail(generics.GenericAPIView):
    """
    Envio de email genérico para redefinição de senha.
    Responsabilidade única: gerar link + enviar email HTML.
    """
    serializer_class = ResetPasswordEmailRequestSerializer

    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response(
                {
                    'alert_error': Translate.tdc(
                        request,
                        'Email não informado'
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        if not User.objects.filter(email=email).exists():
            # resposta neutra por segurança
            return Response(
                {
                    'alert_success': Translate.tdc(
                        request,
                        'Se o email existir, enviaremos instruções'
                    )
                },
                status=status.HTTP_200_OK
            )

        user = User.objects.get(email=email)

        uidb64 = urlsafe_base64_encode(smart_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user)

        relative_link = reverse(
            'password-reset-confirm',
            kwargs={
                'uidb64': uidb64,
                'token': token
            }
        )

        redirect_url = request.GET.get('redirect_url', '')

        try:
            base_url = request.META['HTTP_ORIGIN']
        except KeyError:
            base_url = settings.FRONTEND_URL

        reset_link = (
            f'{base_url}/#/resetpassword{relative_link}'
            f'?redirect_url={redirect_url}'
        )

        html_message = render_email_template(
            'GENERIC_RESET',
            {
                'username': user.username,
                'link': reset_link,
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
                {
                    'alert_error': Translate.tdc(
                        request,
                        'Erro ao enviar email'
                    )
                },
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

