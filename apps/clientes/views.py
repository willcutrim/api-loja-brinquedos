from rest_framework import viewsets, filters, status
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.response import Response

from apps.clientes.models import Cliente
from apps.clientes.serializers import ClienteSerializer
from apps.clientes.services import ClienteService


class ClienteViewSet(viewsets.ModelViewSet):
    queryset = Cliente.objects.all()
    serializer_class = ClienteSerializer
    filter_backends = [filters.SearchFilter, DjangoFilterBackend]
    search_fields = ['nome', 'email']
    filterset_fields = ['nome', 'email']

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        cliente = ClienteService.criar_cliente(serializer.validated_data)
        return Response(self.get_serializer(cliente).data, status=status.HTTP_201_CREATED)

    def update(self, request, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        cliente = ClienteService.atualizar_cliente(instance, serializer.validated_data)
        return Response(self.get_serializer(cliente).data)

    def delete(self, request, *args, **kwargs):
        instance = self.get_object()
        ClienteService.deletar_cliente(instance)
        return Response(status=status.HTTP_204_NO_CONTENT)
