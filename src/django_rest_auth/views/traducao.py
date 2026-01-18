from rest_framework import viewsets, filters

from .models import Idioma
from .serializers import IdiomaSerializer


class TraducaoAPIView(viewsets.ModelViewSet):
    filter_backends = (filters.SearchFilter,)
    serializer_class = IdiomaSerializer
    queryset = Idioma.objects.all()

    def get_queryset(self):
        return self.queryset.filter()