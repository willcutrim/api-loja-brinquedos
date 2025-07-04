from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    path('api/clientes/', include('apps.clientes.urls')),
    path('api/vendas/', include('apps.vendas.urls')),
    path('api/usuarios/', include('apps.usuarios.urls')),
    path('', include('apps.frontend.urls')),
]
