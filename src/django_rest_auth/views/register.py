import json
import base64
from datetime import datetime

import pyotp

from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import EmailMultiAlternatives
from django.core.serializers.json import DjangoJSONEncoder

from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from .models import User, TipoEntidade
from .serializers import RegisterSerializer
from .classes.Translate import Translate
from .classes.UserName import UserName
from .utils.templates import render_email_template
from .utils.FullPath import FullPath






class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request):
        origin = request.META.get("HTTP_ORIGIN", 'http://mytech.co.mz')
        nome = str(str(origin).split('.')[0].upper()).split('/')[-1]

        data = request.data.copy()
        data['username'] = UserName.Create(
            str(request.data['username'].replace(' ', '_'))
        )
        data['mobile'] = None

        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        tipoEntidade = TipoEntidade.objects.get(nome=str(nome).capitalize())
        logo = FullPath.url(None, tipoEntidade.icon.name)

        token = RefreshToken.for_user(user).access_token

        html_message = render_email_template(
            'REGISTER_CONFIRM',
            {
                'username': user.username,
                'token': str(token),
                'entidade': nome,
                'tipoentidade': nome,
                'logo': logo,
                'origen': origin
            }
        )

        mail = EmailMultiAlternatives(
            subject=f'{Translate.tdc(request, "Bem-vindo")} {nome}',
            body='',
            to=[user.email],
        )
        mail.attach_alternative(html_message, "text/html")

        try:
            mail.send()
        except Exception as e:
            user.delete()
            return Response(
                {'alert_error': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        return Response(
            {
                'alert_success': Translate.tdc(
                    request,
                    'Conta criada com sucesso'
                ),
                **json.loads(json.dumps(user_data, cls=DjangoJSONEncoder))
            },
            status=status.HTTP_201_CREATED
        )




class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + settings.OTP_KEY


class getPhoneNumberRegistered(APIView):

    @staticmethod
    def post(request):
        phone = str('+' + request.data["mobile"]).replace('+', '')
        try:
            user = User.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            if 'reset_senha' in request.query_params:
                return Response(
                    {
                        'alert_error': Translate.tdc(
                            request,
                            'O número não existe'
                        ) + f' <br><b>{phone}</b>'
                    },
                    status=400
                )

            nome = str(str(request.META['HTTP_ORIGIN']).split('.')[0].upper()).split('/')[-1]
            request.data['username'] = UserName.Create(
                str(request.data['username'].replace(' ', '_'))
            )
            request.data['mobile'] = phone
            request.data['email'] = None

            serializer = RegisterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()

            user = User.objects.get(mobile=phone)
            tipoEntidade = TipoEntidade.objects.get(nome=str(nome).capitalize())

            pessoa = Pessoa()
            pessoa.user = user
            pessoa.save()

        user.counter += 1
        user.save()

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)

        try:
            SMS.send(
                from__='+17244014353',
                to__='+258' + str(phone),
                text__=Translate.tdc(
                    request,
                    'Não partilhe este código'
                ) + f':\nOTP {OTP.at(user.counter)}'
            )
        except Exception as e:
            return Response(
                {
                    'alert_error': Translate.tdc(request, 'Erro') + '<br>' + str(e)
                },
                status=400
            )

        return Response(
            {
                'alert_success': Translate.tdc(
                    request,
                    'Enviámos um OTP para o seu número'
                ) + f' <br><b>{phone}</b>',
                "OTP": OTP.at(user.counter)
            },
            status=201
        )

    @staticmethod
    def put(request):
        phone = str('+' + request.data["mobile"]).replace('+', '')
        try:
            user = User.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            return Response(
                Translate.tdc(request, 'Utilizador não encontrado'),
                status=404
            )

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        OTP = pyotp.HOTP(key)

        if OTP.verify(request.data["otp"], user.counter):
            user.is_verified_mobile = True
            user.save()
            return Response(
                {
                    'alert_success': Translate.tdc(request, 'Autorizado com sucesso'),
                    'id': user.id,
                    'otp': request.data["otp"],
                    'mobile': request.data["mobile"]
                },
                status=202
            )

        return Response(
            {'alert_error': Translate.tdc(request, 'OTP inválido ou expirado')},
            status=400
        )


EXPIRY_TIME = 120  # seconds

class getPhoneNumberRegistered_TimeBased(APIView):

    @staticmethod
    def get(request, phone):
        phone = '+' + str(phone).replace('+', '')
        try:
            mobile = User.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            User.objects.create(mobile=phone)
            mobile = User.objects.get(mobile=phone)

        mobile.save()

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        otp = pyotp.TOTP(key, interval=EXPIRY_TIME)

        try:
            SMS.send(
                from__='+13192205575',
                to__=phone,
                text__=Translate.tdc(
                    request,
                    'Não partilhe este código'
                ) + f':\nOTP {otp.now()}'
            )
        except Exception as e:
            return Response(
                {'alert_error': Translate.tdc(request, 'Erro ao enviar OTP')},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {'otp': otp.now()},
            status=status.HTTP_200_OK
        )

    @staticmethod
    def post(request, phone):
        phone = '+' + str(phone).replace('+', '')
        try:
            mobile = User.objects.get(mobile=phone)
        except ObjectDoesNotExist:
            return Response(
                Translate.tdc(request, 'Utilizador não encontrado'),
                status=status.HTTP_404_NOT_FOUND
            )

        keygen = generateKey()
        key = base64.b32encode(keygen.returnValue(phone).encode())
        otp = pyotp.TOTP(key, interval=EXPIRY_TIME)

        if otp.verify(request.data.get("otp")):
            mobile.isVerified = True
            mobile.save()
            return Response(
                Translate.tdc(request, 'Autorizado com sucesso'),
                status=status.HTTP_200_OK
            )

        return Response(
            Translate.tdc(request, 'OTP inválido ou expirado'),
            status=status.HTTP_400_BAD_REQUEST
        )

