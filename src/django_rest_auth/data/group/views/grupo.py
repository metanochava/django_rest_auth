# =========================
# Python standard library
# =========================
import json


# =========================
# Django
# =========================
from django.contrib.auth.models import Group
from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.http import Http404


# =========================
# Django REST Framework
# =========================
from rest_framework import filters
from rest_framework import status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


# =========================
# Local application (absolute import)
# =========================
from django_rest_auth.data.group.serializers.grupo import GrupoSerializer



class  GrupoAPIView(viewsets.ModelViewSet):
    paginator = None
    search_fields = ['id','name']
    filter_backends = (filters.SearchFilter,)
    serializer_class = GrupoSerializer
    queryset = Group.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by('-codename')
        

    def retrieve(self, request, id, *args, **kwargs):
        try:
            request.query_params['permissions']
            grupo = Group.objects.get(id=id)
            permissions = grupo.permissions.annotate(content_type_model= F('content_type__model'), content_type_app= F('content_type__app_label'))
    
            per = []
            for permission in permissions:
                per.append({'id':permission.id, 'name':permission.name , 'codename':permission.codename, 'content_type':permission.content_type.id, 'content_type_model': permission.content_type_model, 'content_type_app': permission.content_type_app})
            print(per)
            return Response(per)
        except:
           pass

        try:

            transformer = self.get_object()
            grupo = GrupoSerializer(transformer)
            return Response(grupo.data, status=status.HTTP_200_OK)
        except Http404:
            pass
        return Response( status=status.HTTP_404_NOT_FOUND)
    
    def update(self, request,id,  *args, **kwargs):
        g = Group.objects.get(id=id)
        g.name = request.data['name']
        g.save()
        add={'alert_success': '%-'+ request.data['name'] +'-% foi actualizado com sucesso'}
        data = json.loads(json.dumps({'id':g.id}))
        data.update(add)

        return Response(data, status=status.HTTP_202_ACCEPTED)

    def destroy(self, request, id,  *args, **kwargs):
        g = Group.objects.get(id=id)
        nome = g.name
        g.delete()
        add={'alert_success': '<b>'+ nome +'</b> foi apagado com sucesso'}
        return Response(add,status=status.HTTP_202_ACCEPTED)


    @action(
        detail=True,
        methods=['POST'],
    )
    def addPermission(self, request, id):
        grupo = Group.objects.get(id=id)

        content_type, created = ContentType.objects.get_or_create(
            model='uploadloaded',
        )
        custom_permission, created = Permission.objects.get_or_create(content_type= content_type, codename=request.data['codename'], defaults={'name': request.data['name']})
        grupo.permissions.add(custom_permission)
        permission = Permission.objects.get(id=custom_permission.id)

        per= {'id': permission.id, 'nome': permission.codename, 'nomeseparado':permission.name, 'alert_success': 'Permicao <b>' +permission.name + '</b> foi Adicionado consucesso'}
        return Response(per,status.HTTP_201_CREATED )

    
