from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from apps.vendas.models import Venda
from apps.vendas.serializers import VendaSerializer
from apps.vendas.services import VendaService


class VendaViewSet(viewsets.ModelViewSet):
    queryset = Venda.objects.all().select_related('cliente')
    serializer_class = VendaSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        venda = VendaService.criar_venda(serializer.validated_data)
        return Response(self.get_serializer(venda).data, status=status.HTTP_201_CREATED)

    @action(detail=False, methods=['get'], url_path='estatisticas/total-por-dia')
    def total_vendas_por_dia(self, request):
        data = VendaService.total_vendas_por_dia()
        return Response(data)

    @action(detail=False, methods=['get'], url_path='estatisticas/destaques')
    def destaques(self, request):
        destaques = VendaService.destaques_clientes()
        return Response(destaques)
