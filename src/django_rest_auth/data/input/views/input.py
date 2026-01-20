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
from django_rest_auth.core.utils.translate import Translate

from django_rest_auth.models.input import Input
from django_rest_auth.models.input_string import InputString
from django_rest_auth.models.string import String

from django_rest_auth.data.input.serializers.input import InputSerializer
from django_rest_auth.data.string.serializers.string import StringSerializer


class InputAPIView(viewsets.ModelViewSet):
    search_fields = ['id', 'nome']
    filter_backends = (filters.SearchFilter,)
    serializer_class = InputSerializer
    queryset = Input.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        self._paginator = None
        return self.queryset.order_by('nome')

    @action(detail=True, methods=['GET'])
    def strings(self, request, id):
        resposta = []
        strings = InputString.objects.filter(input__id=id)

        for item in strings:
            serializer = StringSerializer(item.string)
            resposta.append(serializer.data)

        return Response(resposta, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def addString(self, request, id):
        string = String.objects.create(texto=request.data['texto'])
        input_obj = Input.objects.get(id=id)

        InputString.objects.create(string=string, input=input_obj)

        return Response(
            {
                'id': string.id,
                'nome': string.texto,
                'nomeseparado': input_obj.nome,
                'alert_info': Translate.tdc(
                    request,
                    f'Permissão "{string.texto}" adicionada com sucesso'
                )
            },
            status=status.HTTP_201_CREATED
        )

