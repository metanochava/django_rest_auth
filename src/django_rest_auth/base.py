
import os

from django.conf import settings
from django.db import models
from django.utils import timezone


from rest_framework import serializers
from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied


from .decorators import isPermited
from .classes.FullPath import FullPath
from .classes.Translate import Translate





class BaseSerializer(serializers.ModelSerializer):
    """
    Serializer base que protege automaticamente
    todos os FileField e ImageField.
    """

    permanent_fields_files = []

    def to_representation(self, instance):
        data = super().to_representation(instance)
        request = self.context.get('request')

        if not request:
            return data

        permanent = set(getattr(self, 'permanent_fields_files', []))

        for field in instance._meta.fields:
            if not isinstance(field, (models.FileField, models.ImageField)):
                continue

            file = getattr(instance, field.name)
            if not file:
                data[field.name] = None
                continue

            temporary = field.name not in permanent

            try:
                url = FullPath.url(request, file.url, temporary=temporary)
                filename = os.path.basename(file.name)
                ext = os.path.splitext(filename)[1].lstrip('.').lower()

                data[field.name] = {
                    'url': url,
                    'name': filename,
                    'ext': ext,
                    'size': getattr(file, 'size', None)
                }
            except Exception:
                data[field.name] = None

        return data



class BaseViewSet(ModelViewSet):
    """
    ViewSet base multi-tenant com controlo automático de permissões.
    """

    permission_action_map = {
        'list': 'list',
        'retrieve': 'view',
        'create': 'add',
        'update': 'change',
        'partial_update': 'change',
        'destroy': 'delete',
    }

    def get_method_permission(self):
        custom_map = getattr(self, 'method_permission', {})
        return {**self.permission_action_map, **custom_map}

    def initial(self, request, *args, **kwargs):
        super().initial(request, *args, **kwargs)

        action = self.action
        model = self.get_queryset().model

        perm_map = self.get_method_permission()
        perm_prefix = perm_map.get(action)

        if not perm_prefix:
            raise PermissionDenied(
                Translate.tdc(request, 'Permissão não definida para esta ação')
            )

        codename = f'{perm_prefix}_{model._meta.model_name}'

        if not isPermited(request=request, role=[codename]):
            raise PermissionDenied(
                Translate.tdc(request, 'Não autorizado')
            )

    def get_queryset(self):
        return super().get_queryset().filter(
            entidade_id=self.request.entidade_id,
            sucursal_id=self.request.sucursal_id,
            deleted_at__isnull=True
        )

    def perform_create(self, serializer):
        serializer.save(
            entidade_id=self.request.entidade_id,
            sucursal_id=self.request.sucursal_id,
            created_by=self.request.user,
            updated_by=self.request.user
        )

    def perform_update(self, serializer):
        serializer.save(updated_by=self.request.user)

    def perform_destroy(self, instance):
        instance.deleted_at = timezone.now()
        instance.updated_by = self.request.user
        instance.save()



class BaseModel(models.Model):
    estado = models.IntegerField( default=1, null=True, choices=( (0, 'Inativo'), (1, 'Ativo'), ))
    entidade = models.ForeignKey("django_rest_auth.Entidade", on_delete=models.CASCADE, related_name="%(class)s_entidade")
    sucursal = models.ForeignKey("django_rest_auth.Sucursal", on_delete=models.CASCADE, related_name="%(class)s_sucursal")

    created_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  on_delete=models.SET_NULL, related_name="%(class)s_created")
    updated_by = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True,  on_delete=models.SET_NULL, related_name="%(class)s_updated")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        abstract = True