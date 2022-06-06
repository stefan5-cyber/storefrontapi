from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet, basename='collections')
router.register('products', views.ProductViewSet, basename='products')

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product'
)
product_router.register('reviews', views.ReviewViewSet, basename='product-reviews')


urlpatterns = [
    path('', include(router.urls))
]
