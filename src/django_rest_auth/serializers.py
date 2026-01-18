import os

from django.db import models
from django.db.models import Q
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.exceptions import TokenError

from .models import *
from .classes.FullPath import FullPath
from .classes.Translate import Translate



# --------------------------------------------------
# AUTH HELPERS
# --------------------------------------------------

def authenticate(value=None, password=None):
    User = get_user_model()
    try:
        user = User.objects.get(
            Q(email=value) | Q(username=value) | Q(mobile=value)
        )
    except User.DoesNotExist:
        return None

    if user.check_password(password):
        return user

    return None

def authenticate_iexact(identifier=None, password=None):
    User = get_user_model()

    try:
        user = User.objects.get(
            Q(email__iexact=identifier) |
            Q(username__iexact=identifier) |
            Q(mobile=identifier)
        )
    except User.DoesNotExist:
        return None

    if user.check_password(password):
        return user

    return None


# --------------------------------------------------
# AUTH SERIALIZERS
# --------------------------------------------------









# --------------------------------------------------
# DOMAIN SERIALIZERS
# --------------------------------------------------



















