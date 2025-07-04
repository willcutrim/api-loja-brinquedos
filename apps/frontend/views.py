from django.views.generic import TemplateView
from django.contrib.auth.mixins import LoginRequiredMixin

class LoginView(TemplateView):
    template_name = 'frontend/login.html'


class ClientesView(TemplateView):
    template_name = 'frontend/clientes/lista.html'


class EstatisticasView(TemplateView):
    template_name = 'frontend/clientes/estatisticas.html'
