from django.db.models import Count
from rest_framework import viewsets, mixins
from .models import Collection
from .serializers import CollectionSerializer
from .permissions import IsAdminOrReadOnly


class CollectionViewSet(viewsets.ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.products.count() > 0:
            return {'error': 'Collection can not be deleted has related products'}
        return super().destroy(request, *args, **kwargs)
