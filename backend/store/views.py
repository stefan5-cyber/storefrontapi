from ast import Is
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import viewsets, mixins
from .models import Collection, Product, OrderItem, Review
from .serializers import CollectionSerializer, ProductSerializer, ReviewSerializer
from .permissions import IsAdminOrReadOnly
from .filters import ProductFilter


class CollectionViewSet(viewsets.ModelViewSet):

    queryset = Collection.objects.annotate(products_count=Count('products'))
    serializer_class = CollectionSerializer
    permission_classes = [IsAdminOrReadOnly]

    def destroy(self, request, *args, **kwargs):
        if Collection.objects.products.count() > 0:
            return {'error': 'Collection can not be deleted has related products'}
        return super().destroy(request, *args, **kwargs)


class ProductViewSet(viewsets.ModelViewSet):

    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAdminOrReadOnly]
    filter_backends = [DjangoFilterBackend, SearchFilter]
    filterset_class = ProductFilter
    search_fields = ['title', 'description']

    def destroy(self, request, *args, **kwargs):
        if OrderItem.objects.filter(product_id=kwargs['product_pk']).count() > 0:
            return {'error': 'Product can not be deleted has related order'}
        return super().destroy(request, *args, **kwargs)


class ReviewViewSet(viewsets.ModelViewSet):

    serializer_class = ReviewSerializer

    def get_queryset(self):
        return Review.objects.filter(product_id=self.kwargs['product_pk']).order_by('-date', '-id')

    def get_serializer_context(self):
        return {'product_id': self.kwargs['product_pk']}
