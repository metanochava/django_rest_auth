from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from django.contrib.contenttypes.models import ContentType

from .serializers import ContentTypeSerializer


class ModeloAPIView(viewsets.ModelViewSet):
    search_fields = ['id']
    filter_backends = (filters.SearchFilter,)
    serializer_class = ContentTypeSerializer
    queryset = ContentType.objects.all()
    lookup_field = "id"

    def get_queryset(self):
        return self.queryset.order_by('app_label', 'model')

    def list(self, request, *args, **kwargs):
        self._paginator = None
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)