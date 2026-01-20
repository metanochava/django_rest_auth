from django.urls import include
from django.urls import path

from rest_framework import routers

from rest_framework_simplejwt.views import TokenRefreshView

# ─────────────────────────────
# User / Auth views
# ─────────────────────────────
from django_rest_auth.data.user.views.login import LoginAPIView
from django_rest_auth.data.user.views.logins import LoginsAPIView
from django_rest_auth.data.user.views.logout import LogoutAPIView
from django_rest_auth.data.user.views.me import MeAPIView
from django_rest_auth.data.user.views.verify_email import VerifyEmail
from django_rest_auth.data.user.views.change_password_email import ChangePasswordEmailAPIView
from django_rest_auth.data.user.views.change_password_mobile import ChangePasswordMobileAPIView
from django_rest_auth.data.user.views.request_password_reset_email import RequestPasswordResetEmailAPIView
from django_rest_auth.data.user.views.password_token_check import PasswordTokenCheckAPIView
from django_rest_auth.data.user.views.set_new_password import SetNewPasswordAPIView
from django_rest_auth.data.user.views.mail import MailAPIView

# ─────────────────────────────
# Data / API views
# ─────────────────────────────
from django_rest_auth.data.entidade.views.entidade import EntidadeAPIView
from django_rest_auth.data.tipo_entidade.views.tipo_entidade import TipoEntidadeAPIView
from django_rest_auth.data.group.views.grupo import GrupoAPIView
from django_rest_auth.data.sucursal.views.sucursal import SucursalAPIView
from django_rest_auth.data.string.views.string import StringAPIView
from django_rest_auth.data.input.views.input import InputAPIView
from django_rest_auth.data.traducao.views.traducao import TraducaoAPIView
from django_rest_auth.data.idioma.views.idioma import IdiomaAPIView
from django_rest_auth.data.ficheiro.views.ficheiro import FicheiroAPIView
from django_rest_auth.data.permission.views.permission import PermissionAPIView
from django_rest_auth.data.modelo.views.modelo import ModeloAPIView

# ─────────────────────────────
# Router
# ─────────────────────────────
router = routers.DefaultRouter()

router.register("ficheiros", FicheiroAPIView, basename="ficheiros")
router.register("idiomas", IdiomaAPIView, basename="idiomas")
router.register("traducoes", TraducaoAPIView, basename="traducoes")
router.register("inputs", InputAPIView, basename="inputs")
router.register("strings", StringAPIView, basename="strings")
router.register("entidades", EntidadeAPIView, basename="entidades")
router.register("tipo-entidades", TipoEntidadeAPIView, basename="tipo_entidades")
router.register("sucursais", SucursalAPIView, basename="sucursais")
router.register("grupos", GrupoAPIView, basename="grupos")
router.register("permissions", PermissionAPIView, basename="permissions")
router.register("modelos", ModeloAPIView, basename="modelos")

# ─────────────────────────────
# URL patterns
# ─────────────────────────────
urlpatterns = [
    path("", include(router.urls)),

    path("login/", LoginAPIView.as_view(), name="login"),
    path("logout/", LogoutAPIView.as_view(), name="logout"),
    path("me/", MeAPIView.as_view(), name="me"),

    path("email/verify/", VerifyEmail.as_view(), name="email_verify"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("logins/", LoginsAPIView.as_view(), name="logins"),

    path("password/change/email/", ChangePasswordEmailAPIView.as_view(), name="change_password_email"),
    path("password/change/mobile/", ChangePasswordMobileAPIView.as_view(), name="change_password_mobile"),
    path("password/reset/email/", RequestPasswordResetEmailAPIView.as_view(), name="request_password_reset_email"),
    path("password/reset/<uidb64>/<token>/", PasswordTokenCheckAPIView.as_view(), name="password_reset_confirm"),
    path("password/reset/complete/", SetNewPasswordAPIView.as_view(), name="password_reset_complete"),

    path("mail/", MailAPIView.as_view(), name="mail"),
]
