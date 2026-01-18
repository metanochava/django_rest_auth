from rest_framework import viewsets, filters, status
from rest_framework.decorators import action
from rest_framework.response import Response

from django.http import Http404

from .models import Ficheiro, Ficheiros
from .serializers import FicheiroSerializer, FicheiroGravarSerializer
from .classes.Translate import Translate
from .utils.DiscManegar import DiscManegar




class FicheiroAPIView(viewsets.ModelViewSet):

    search_fields = ['id', 'ficheiro']
    filter_backends = (filters.SearchFilter,)
    serializer_class = FicheiroSerializer
    queryset = Ficheiro.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.filter().order_by('-id')

    def retrieve(self, request, id, *args, **kwargs):
        try:
            ficheiro = self.get_object()
            serializer = FicheiroSerializer(ficheiro)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Http404:
            return Response(
                {'alert_error': Translate.tdc(request, 'Ficheiro não encontrado')},
                status=status.HTTP_404_NOT_FOUND
            )

    def destroy(self, request, id, *args, **kwargs):
        try:
            instance = self.get_object()
            DiscManegar.recoverSpace(instance.entidade.id, instance)
            self.perform_destroy(instance)
        except Http404:
            pass

        return Response(
            {'alert_success': Translate.tdc(request, 'Ficheiro removido com sucesso')},
            status=status.HTTP_204_NO_CONTENT
        )

    def list(self, request, *args, **kwargs):
        self._paginator = None
        queryset = self.filter_queryset(self.get_queryset())
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, id, *args, **kwargs):
        ficheiro = self.get_object()
        serializer = FicheiroSerializer(ficheiro, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED
        )

    def create(self, request, *args, **kwargs):
        entidade_id = request.headers.get('E')
        sucursal_id = request.headers.get('S')

        request.data['entidade'] = entidade_id
        request.data['sucursal'] = sucursal_id

        uploaded_file = request.FILES['ficheiro']
        request.data['size'] = uploaded_file.size

        if entidade_id:
            DiscManegar.freeSpace(entidade_id, uploaded_file)

        serializer = FicheiroGravarSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        ficheiro = FicheiroSerializer(
            Ficheiros.objects.get(id=serializer.data['id'])
        )

        return Response(
            ficheiro.data,
            status=status.HTTP_201_CREATED
        )

    @action(detail=True, methods=['GET'])
    def sucursais(self, request, id):
        sucursais = Ficheiro.objects.filter(entidade__id=id)
        resposta = []

        for sucursal in sucursais:
            resposta.append({
                'id': sucursal.id,
                'nome': sucursal.nome
            })

        return Response(resposta, status=status.HTTP_200_OK)

