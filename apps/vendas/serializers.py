from rest_framework import serializers
from apps.vendas.models import Venda
from apps.clientes.serializers import ClienteSerializer


class VendaSerializer(serializers.ModelSerializer):
    cliente = ClienteSerializer(read_only=True)
    cliente_id = serializers.PrimaryKeyRelatedField(
        queryset=Venda._meta.get_field('cliente').related_model.objects.all(),
        source='cliente',
        write_only=True
    )

    class Meta:
        model = Venda
        fields = ['id', 'cliente', 'cliente_id', 'data', 'valor']
