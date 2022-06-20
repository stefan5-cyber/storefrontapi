from django.contrib import admin
from django.urls import path, include
import debug_toolbar

urlpatterns = [
    path('', include('page.urls')),
    path('admin/', admin.site.urls),
    path('store/', include('store.urls')),
    path('auth/', include('djoser.urls')),
    path('auth/', include('djoser.urls.jwt')),
    path('__debug__/', include(debug_toolbar.urls)),
]
