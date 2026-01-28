# =========================
# Django
# =========================
from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Permission


# =========================
# ds – models
# =========================
from django_saas.models.traducao import Traducao
from django_saas.models.idioma import Idioma
from django_saas.models.entidade import Entidade
from django_saas.models.entidade_user import EntidadeUser
from django_saas.models.entidade_modulo import EntidadeModulo
from django_saas.models.entidade_group import EntidadeGroup

from django_saas.models.sucursal import Sucursal
from django_saas.models.sucursal_user import SucursalUser
from django_saas.models.sucursal_user_group import SucursalUserGroup
from django_saas.models.sucursal_group import SucursalGroup

from django_saas.models.tipo_entidade import TipoEntidade
from django_saas.models.tipo_entidade_modulo import TipoEntidadeModulo
from django_saas.models.ficheiro import Ficheiro
from django_saas.models.user_login import UserLogin
from django_saas.models.modulo import Modulo
from django_saas.models.front_end import FrontEnd


# =========================
# User model
# =========================
User = get_user_model()



User = get_user_model()

admin.site.site_title = 'Auth'
admin.site.index_title = 'Mytech Auth Rest'


def all_fields(model):
    return [field.name for field in model._meta.fields]


@admin.register(Traducao)
class TraducaoAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)


@admin.register(EntidadeGroup)
class EntidadeGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)


@admin.register(Ficheiro)
class FicheiroAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)
    search_fields = ['id', 'name']


@admin.register(FrontEnd)
class FrontEndAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)


@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)
    search_fields = ['id', 'nome']


@admin.register(TipoEntidade)
class TipoEntidadeAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'nome')
    search_fields = ['nome']


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'username', 'email')
    search_fields = ['username', 'mobile', 'email']


@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id',)
    search_fields = ['local_nome', 'dispositivo', 'user']


@admin.register(Entidade)
class EntidadeAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'nome')
    search_fields = ['nome']

    def admin_list(self, obj):
        return ', '.join(u.username for u in obj.admins.all())
    admin_list.short_description = 'admins'


@admin.register(EntidadeUser)
class EntidadeUserAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'user')
    search_fields = ['user']


@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'nome')
    search_fields = ['nome']


@admin.register(SucursalGroup)
class SucursalGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'sucursal', 'group')
    search_fields = ['sucursal', 'group']


@admin.register(SucursalUser)
class SucursalUserAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'sucursal', 'user')
    search_fields = ['sucursal', 'user']


@admin.register(SucursalUserGroup)
class SucursalUserGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'sucursal', 'user', 'group')
    search_fields = ['sucursal', 'user', 'group']


@admin.register(EntidadeModulo)
class EntidadeModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'entidade', 'modulo')
    search_fields = ['entidade', 'modulo']


@admin.register(TipoEntidadeModulo)
class TipoEntidadeModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
    list_display_links = ('id', 'tipo_entidade', 'modulo')
    search_fields = ['tipo_entidade', 'modulo']


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request): return all_fields(self.model)
