import importlib
import importlib.util

from django.apps import apps
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from django.conf import settings as dj_settings

from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from firebase_admin import db

from .models import (
    TipoEntidade,
    Entidade,
    EntidadeUser,
    TipoEntidadeModulo,
)
from .serializers import (
    TipoEntidadeSerializer,
    PermissionSerializer,
)
from .classes.Translate import Translate
from .utils.FullPath import FullPath


class TipoEntidadeAPIView(viewsets.ModelViewSet):
    search_fields = ['id','nome']
    filter_backends = (filters.SearchFilter,)
    
    serializer_class =TipoEntidadeSerializer
    queryset =TipoEntidade.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        if (self.request.query_params.get('all')):
            return self.queryset.filter().order_by('ordem')
        else:
            self._paginator = None
            return self.queryset.filter(estado='Activo').order_by('ordem')
    
    

    @action(
        detail=True,
        methods=['GET'],
    )
    def user_entidades(self, request, id):
        entidades = Entidade.objects.filter(tipo_entidade__id=id)
        ent = []
        for entidade in entidades:

            try:
                entidadeUser = EntidadeUser.objects.get( entidade=entidade, user=request.user)
                if entidadeUser:
                    logo = FullPath.url(request, entidade.logo.name)
                    ent.append({'id': entidade.id, 'nome': entidade.nome, 'logo': logo})
            except:
                pass
        return Response(ent , status=status.HTTP_200_OK)


    @action(
        detail=True,
        methods=['GET'],
    )
    def entidades(self, request, id):
        entidades = Entidade.objects.filter(tipo_entidade__id = id)

        ent = []
        for entidade in entidades:
            try:
                logo = str(entidade)
                ent.append({'id': entidade.id, 'nome': entidade.nome})
            except:
                pass
        return Response(ent , status=status.HTTP_200_OK)
    

    @action(
        detail=True,
        methods=['GET'],
    )
    def downloadPermission(self, request, id):
        te = TipoEntidade.objects.get(id=id)
        groups = db.reference('Premissions').child(te.nome).get()
        for key, permissions in groups.items():
            try:
                g = Group.objects.get(name=key)
                te.groups.add(g)
            except:
                g = Group.objects.create(name=key)
                te.groups.add(g)

        for group in te.groups.all():
            datas = db.reference('Premissions').child(te.nome).child(group.name).get()
            gr = Group.objects.get(id=group.id)
            gr.permissions.clear()
            try:
                for permission in datas:
                    try:
                        p = Permission.objects.get(codename=permission['codename'])
                        gr.permissions.add(p)
                    except:

                        content_type, created = ContentType.objects.get_or_create(
                            model='downloaded',
                        )
                        custom_permission, created = Permission.objects.get_or_create(content_type= content_type, codename=permission['codename'], defaults={'name': permission['name']})
                        gr.permissions.add(custom_permission)
            except:
                pass
            gr.save()

            for entidade in Entidade.objects.filter(tipo_entidade_id=id):
                for g in te.groups.all():
                    entidade.groups.add(g)

        te = {'id': te.id, 'nome': te.nome, 'alert_success': 'Permicoes baixadas para<br><b>'+te.nome+'</b>'}
        
        return Response(te , status=status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['GET'],
    )
    def uploadPermission(self, request, id):
        te = TipoEntidade.objects.get(id=id)
        grupos ={}
        for group in te.groups.all():
            ref = db.reference('Premissions').child(te.nome)
            data = PermissionSerializer(group.permissions.all(), many=True).data
            grupos[group.name] = data
        ref.set(grupos)     
        te = {'id': te.id, 'nome': te.nome, 'alert_success': 'Permicoes actualizadas para<br><b>'+te.nome+'</b>'}
        
        return Response(te , status=status.HTTP_200_OK)

    @action(
        detail=True,
        methods=['PUT'],
    )
    def perfilPut(self, request, id):
        group = Group.objects.get(id=request.data['id'])
        group.name = request.data['name']
        group.save()
        
        perfil = {'id': group.id, 'name': group.name, 'alert_success': 'Perfil <b>'+ group.name + ' </b> actualizado com sucesso'}
        return Response(perfil, status.HTTP_201_CREATED)


    @action(detail=True, methods=['POST'],)
    def perfilPost(self, request, id):
        tipoentidade = TipoEntidade.objects.get(id=id)        
        group = Group.objects.create(name=request.data['name'])
        tipoentidade.groups.add(group)
        for entidade in Entidade.objects.filter(tipo_entidade_id=id):
            entidade.groups.add(group)

        perfil = {'id': group.id, 'name': group.name, 'alert_success': 'Perfil <b>'+ group.name + ' </b> criado com sucesso'}
        return Response(perfil, status.HTTP_201_CREATED)
    
    @action(detail=True, methods=['GET'],)
    def apps(self, request, id):
        tipoentidade = TipoEntidade.objects.get(id=id)        
        apps_ = []
        
        for app in apps.get_app_configs():
            apps_.append({'name': app.name, 'label': app.label, 'verbose': app.verbose_name })
            
        for app in dj_settings.INSTALLED_APPS:
            apps_.append(app)


        return Response(apps_, status.HTTP_200_OK)
    

    @action(detail=True,methods=['GET'],)
    def menus(self, request, *args, **kwargs):
        transformer = self.get_object()
        ALL_MENUS = {}
        MENUS =[]
        for app in apps.get_app_configs():
            sidebar = None
            module_name = app.name + ".sidebar"
            if importlib.util.find_spec(module_name):
                sidebar = importlib.import_module(module_name)
            else:       
                continue

            if sidebar:
                MENU = {}
                MENU["app"] = app.label
                MENU["menu"] = sidebar.MENU
                MENU["icon"] = sidebar.ICON
                MENU["role"] = sidebar.ROLE
                MENU["submenu"] = []
                for submenu in sidebar.SUBMENUS:
                    MENU["submenu"].append(submenu) 

                MENUS.append(MENU)

        return Response(MENUS, status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['GET'],
    )
    def modelos(self, request, id):
        tipoentidade = TipoEntidade.objects.get(id=id)        
        modelos = []
        for modelo in tipoentidade.modelos.all():
           modelos.append({'id': modelo.id, 'model': modelo.model, 'app_label':  modelo.app_label })

        return Response(modelos, status.HTTP_200_OK)
    
    @action(
        detail=True,
        methods=['POST'],
    )
    def addModelo(self, request, id):
        tipoentidade = TipoEntidade.objects.get(id=id)        
        modelo = ContentType.objects.get(id=request.data['id'])
        tipoentidade.modelos.add(modelo)
        for entidade in Entidade.objects.filter(tipo_entidade_id=id):
            entidade.modelos.add(modelo)
            
        modelo = {'id': modelo.id, 'model': modelo.model, 'alert_success': 'App <b>'+ modelo.model + ' </b> criado com sucesso'}
        return Response(modelo, status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['POST'],
    )
    def removeModelo(self, request, id):
        tipoentidade = TipoEntidade.objects.get(id=id)        
        modelo = ContentType.objects.get(id=request.data['id'])
        tipoentidade.modelos.remove(modelo)
        for entidade in Entidade.objects.filter(tipo_entidade_id=id):
            entidade.modelos.remove(modelo)

        modelo = {'id': modelo.id, 'model': modelo.model, 'alert_success': 'App <b>'+ modelo.model + ' </b> Removido com sucesso'}
        return Response(modelo, status.HTTP_201_CREATED)

    @action(
        detail=True,
        methods=['GET'],
    )
    def modulos(self, request, *args, **kwargs):
        transformer = self.get_object()
        EntMods = TipoEntidadeModulo.objects.filter(tipo_entidade = transformer.id)        
        modulos = [
            {'id': TiEntMo.modelo.id, 'nome': TiEntMo.modelo.nome}
            for TiEntMo in EntMods
        ]

        return Response(modulos, status=status.HTTP_200_OK)
