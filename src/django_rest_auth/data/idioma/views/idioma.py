# =========================
# Python standard library
# =========================
import importlib
import json


# =========================
# Django
# =========================
from django.apps import apps
from django.core.cache import cache
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
# Local application (absolute imports)
# =========================
from django_rest_auth.models.idioma import Idioma
from django_rest_auth.models.traducao import Traducao
from django_rest_auth.data.idioma.serializers.idioma import IdiomaSerializer


class  IdiomaAPIView(viewsets.ModelViewSet):
    paginator = None
    search_fields = ['id','nome']
    filter_backends = (filters.SearchFilter,)
    serializer_class = IdiomaSerializer
    queryset = Idioma.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by('nome')


    def retrieve(self, request, id, *args, **kwargs):
        try:
            transformer = self.get_object()
            idioma = IdiomaSerializer(transformer)
            return Response(idioma.data, status=status.HTTP_200_OK)
        except Http404:
            pass
        return Response( status=status.HTTP_404_NOT_FOUND)


    def destroy(self, request, id, *args, **kwargs):
        try:
            instance = self.get_object()
            self.perform_destroy(instance)
        except Http404:
            pass
        return Response(status=status.HTTP_204_NO_CONTENT)


    def update(self, request,id,  *args, **kwargs):
        transformer = self.get_object()

        idioma = IdiomaSerializer(transformer, data=request.data)
        if idioma.is_valid(raise_exception=True):
            idioma.save()
            add={'alert_success': '%-'+ request.data['nome'] +'-% foi actualizado com sucesso'}
            data = json.loads(json.dumps(idioma.data))
            data.update(add)

            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(idioma.errors, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request, *args, **kwargs):
        request.data['admin'] = request.user.id
        idioma = IdiomaSerializer(data=request.data)
        if idioma.is_valid(raise_exception=True):
            idioma.save()
            add = {'alert_success': '%-'+ request.data['nome'] +'-% foi criado com sucesso'}
            data = json.loads(json.dumps(idioma.data))
            data.update(add)

            return Response(data, status=status.HTTP_202_ACCEPTED)
        else:
            return Response(idioma.errors, status=status.HTTP_400_BAD_REQUEST)


    @action(detail=True, methods=['GET'])
    def traducaos(self, request, *args, **kwargs):
        CACHE_TIMEOUT = 60 * 60  # 1 hora
        transformer = self.get_object()
        lang_code = str(transformer.code).lower().replace('-', '')
        cache_key = f"traducao:{lang_code}"

        # 1️⃣ Tenta obter do cache
        cached = cache.get(cache_key)
        if cached is not None:
            return Response(cached, status=status.HTTP_200_OK)

        # 2️⃣ Caso não exista cache, constrói as traduções
        traducoes = {}

        # Base de dados
        db_traducoes = Traducao.objects.filter(idioma_id=transformer.id)
        for tra in db_traducoes:
            traducoes[tra.chave] = tra.traducao

        # Módulos lang
        for app in apps.get_app_configs():
            module_name = f"{app.name}.lang.{lang_code}"

            try:
                modulo = importlib.import_module(module_name)
            except ModuleNotFoundError:
                continue

            if hasattr(modulo, "key_value"):
                traducoes.update(modulo.key_value)

        # 3️⃣ Guarda no cache
        cache.set(cache_key, traducoes, CACHE_TIMEOUT)

        return Response(traducoes, status=status.HTTP_200_OK)

