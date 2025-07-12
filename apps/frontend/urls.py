from django.urls import path
from apps.frontend.views import (
    LoginView, ClientesView, EstatisticasView, VendasView
)

urlpatterns = [
    path('login/', LoginView.as_view(), name='login'),
    path('clientes/', ClientesView.as_view(), name='clientes'),
    path('clientes/estatisticas/', EstatisticasView.as_view(), name='estatisticas'),

    path('clientes/vendas/', VendasView.as_view(), name='vendas'),
]
