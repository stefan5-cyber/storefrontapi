from django.urls import path, include
from rest_framework_nested import routers
from . import views


router = routers.DefaultRouter()
router.register('collections', views.CollectionViewSet, basename='collections')
router.register('products', views.ProductViewSet, basename='products')
router.register('customers', views.CustomerViewSet, basename='customers')
router.register('cart', views.CartViewSet, basename='cart')
router.register('orders', views.OrderViewSet, basename='orders')

product_router = routers.NestedDefaultRouter(
    router, 'products', lookup='product'
)
product_router.register(
    'reviews', views.ReviewViewSet, basename='product-reviews'
)

cart_router = routers.NestedDefaultRouter(
    router, 'cart', lookup='cart'
)
cart_router.register(
    'items', views.CartItemViewSet, basename='cart-items'
)


urlpatterns = [
    path('', include(router.urls)),
    path('', include(product_router.urls)),
    path('', include(cart_router.urls))
]
