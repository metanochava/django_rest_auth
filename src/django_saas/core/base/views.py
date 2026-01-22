from django.utils import timezone

from rest_framework.viewsets import ModelViewSet
from rest_framework.exceptions import PermissionDenied

from django_saas.core.base.permissions import isPermited
from django_saas.core.utils.translate import Translate


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

