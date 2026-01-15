from django.contrib.auth.models import Permission, Group
from rest_framework import permissions
from rest_framework import status
from django.conf import settings
from rest_framework.response import Response
from .classes.Translate import Translate
import inspect
from .models import *
from functools import wraps



def check_permission(role, request):
    role = role or []

    tipo_entidade_id = request.headers.get('ET')
    entidade_id = request.headers.get('E')
    sucursal_id = request.headers.get('S')
    grupo_id = request.headers.get('G')

    if not Entidade.objects.filter( id=entidade_id, tipo_entidade__id=tipo_entidade_id ).exists():
        return False

    if not EntidadeUser.objects.filter( user=request.user, entidade_id=entidade_id ).exists():
        return False

    if not Sucursal.objects.filter( id=sucursal_id, entidade__tipo_entidade__groups__id=grupo_id ).exists():
        return False

    if not SucursalUser.objects.filter( user=request.user, sucursal_id=sucursal_id ).exists():
        return False

    if not SucursalUserGroup.objects.filter( user=request.user, sucursal_id=sucursal_id, group_id=grupo_id ).exists():
        return False

    try:
        grupo = Group.objects.get(id=grupo_id)
    except Group.DoesNotExist:
        return False

    return grupo.permissions.filter(codename__in=role).exists()



def hasPermission(role=None):
    def decorator(view_func):
        @wraps(view_func)
        def wrapper(self, request, *args, **kwargs):
            if check_permission(role, request):
                return view_func(self, request, *args, **kwargs)

            txt = Translate.tdc( request.query_params.get('lang'), 'Permission denied')
            return Response( {'alert_error': txt}, status=status.HTTP_403_FORBIDDEN )
        return wrapper
    return decorator

def isPermited(role=None, request=None):
    return check_permission(role, request)
