from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied
from .classes.Translate import Translate

from .decorators import check_permission


class HasAppPermission(BasePermission):
    """
    Permission base do DRF integrada com o sistema multi-tenant.

    Usa o mesmo motor de permissões:
    - headers (ET, E, S, G, L)
    - grupos
    - permissões do Django
    - uma única query
    """

    message = 'Permission denied'

    def has_permission(self, request, view):
        """
        Verificação antes da execução da view.
        A view deve definir `permission_codename`.
        """

        # A view precisa declarar explicitamente a permissão
        codename = getattr(view, 'permission_codename', None)

        if not codename:
            # Segurança: se não declarou, não passa
            return False

        allowed = check_permission(
            request=request,
            role=[codename]
        )

        if not allowed:
            # mantém compatibilidade com DRF
            raise PermissionDenied(Translate.tdc(request,self.message))

        return True
