from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import String, Input, InputString
from .serializers import StringSerializer, InputSerializer
from .classes.Translate import Translate



class StringAPIView(viewsets.ModelViewSet):
    search_fields = ['id', 'texto']
    filter_backends = (filters.SearchFilter,)
    serializer_class = StringSerializer
    queryset = String.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        self._paginator = None

        input_nome = self.request.query_params.get('input')
        if input_nome:
            resposta = []
            relacionamentos = InputString.objects.filter(input__nome=input_nome)

            for rel in relacionamentos:
                serializer = StringSerializer(rel.string)
                resposta.append(serializer.data)

            return resposta

        return self.queryset.order_by('texto')

    @action(detail=True, methods=['GET'])
    def inputs(self, request, id):
        resposta = []
        relacionamentos = InputString.objects.filter(string__id=id)

        for rel in relacionamentos:
            serializer = InputSerializer(rel.input)
            resposta.append(serializer.data)

        return Response(resposta, status=status.HTTP_200_OK)

    @action(detail=True, methods=['POST'])
    def addToInput(self, request, id):
        string = String.objects.get(id=id)
        input_obj = Input.objects.get(id=request.data['id'])

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

    @action(detail=True, methods=['POST'])
    def removeFromInput(self, request, id):
        InputString.objects.get(
            string__id=id,
            input__id=request.data['id']
        ).delete()

        return Response(
            {
                'id': id,
                'alert_info': Translate.tdc(
                    request,
                    'Permissão removida com sucesso'
                )
            },
            status=status.HTTP_201_CREATED
        )