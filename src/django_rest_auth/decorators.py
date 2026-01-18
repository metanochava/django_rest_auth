from django.contrib.auth.models import Permission, Group
from rest_framework import permissions
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from .classes.Translate import Translate
import inspect
from .models import *
from functools import wraps


def check_permission(request, role):
    role = role or []

    if not all([
        request.user and request.user.is_authenticated,
        request.tipo_entidade_id,
        request.entidade_id,
        request.sucursal_id,
        request.grupo_id,
        request.lang_id,
    ]):
        return False

    return SucursalUserGroup.objects.filter(
        user=request.user,
        group_id=request.grupo_id,
        sucursal_id=request.sucursal_id,
        sucursal__entidade_id=request.entidade_id,
        sucursal__entidade__tipo_entidade_id=request.tipo_entidade_id,
        group__permissions__codename__in=role,
    ).exists()




def hasPermission(role=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if check_permission(request, role):
                return view_func(self, request, *args, **kwargs)

            txt = Translate.tdc(request, 'Permission denied')
            return Response( {'alert_error': txt}, status=status.HTTP_403_FORBIDDEN )
        return wrapper
    return decorator

def isPermited( request=None, role=None):
    return check_permission(request, role)
