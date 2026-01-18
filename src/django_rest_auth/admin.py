from django.contrib import admin
from django.contrib.auth.models import Permission

# django_rest_auth/models/__init__.py


from .models.traducao import Traducao
from .models.idioma import Idioma
from .models.entidade import Entidade, EntidadeUser, EntidadeModulo, EntidadeGroup
from .models.sucursal import Sucursal, SucursalUser, SucursalUserGroup, SucursalGroup
from .models.tipo_entidade import TipoEntidade, TipoEntidadeModulo
from .models.ficheiro import Ficheiro
from .models.user import UserLogin
from .models.modulo import Modulo
from .models.front_end import FrontEnd
from django.contrib.auth import get_user_model
User = get_user_model()

admin.site.site_title = 'Auth'
admin.site.index_title = 'Mytech Auth Rest'


@admin.register(Traducao)
class TraducaoAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id',)
    



@admin.register(EntidadeGroup)
class EntidadeGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id',)



@admin.register(Ficheiro)
class FicheiroAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id',)
    


@admin.register(Permission)
class PermissionAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id',)
    search_fields = ['id', 'name']


@admin.register(FrontEnd)
class FrontEndAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]


@admin.register(Idioma)
class IdiomaAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', )
    search_fields = ['id',  'nome' ]



@admin.register(TipoEntidade)
class TipoEntidadeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'nome',)
    search_fields = ['nome']



@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'username', 'email')
    search_fields = ['username', 'mobile', 'email', 'nome', 'nome_meio', 'apelido']



@admin.register(UserLogin)
class UserLoginAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', )
    search_fields = ['local_nome', 'dispositivo', 'user' ]



@admin.register(Entidade)
class EntidadeAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'nome',)
    search_fields = ['nome']

    def admin_list(self, obj):
        return ", ".join(
            [u.username for u in obj.admins.all()]
        )
    admin_list.short_description = "admins"



@admin.register(EntidadeUser)
class EntidadeUserAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'user',)
    search_fields = ['user']



@admin.register(Sucursal)
class SucursalAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'nome',)
    search_fields = ['nome']


@admin.register(SucursalGroup)
class SucursalGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'sucursal',  'group',)
    search_fields = ['sucursal', 'group']



@admin.register(SucursalUser)
class SucursalUserAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'sucursal',  'user',)
    search_fields = ['sucursal', 'user']



@admin.register(SucursalUserGroup)
class SucursalUserGroupAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'sucursal',  'user','group', )
    search_fields = ['sucursal', 'user', 'group']



@admin.register(EntidadeModulo)
class EntidadeModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'entidade', 'modulo',)
    search_fields = ['entidade', 'modulo',]



@admin.register(TipoEntidadeModulo)
class TipoEntidadeModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]
    list_display_links = ('id', 'tipo_entidade', 'modulo',)
    search_fields = ['tipo_entidade', 'modulo',]


@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    def get_list_display(self, request):
        return [field.name for field in self.model._meta.fields]