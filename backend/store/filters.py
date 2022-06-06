from django_filters.rest_framework import FilterSet
from .models import Product


class ProductFilter(FilterSet):

    class Meta:
        model = Product
        # the price will be searched by lookup __gt and __lt
        fields = {
            'collection_id': ['exact'],
            'unit_price': ['gt', 'lt']
        }
