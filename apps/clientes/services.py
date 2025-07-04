from apps.clientes.models import Cliente


class ClienteService:
    @staticmethod
    def criar_cliente(validated_data):
        return Cliente.objects.create(**validated_data)

    @staticmethod
    def atualizar_cliente(cliente, validated_data):
        print(validated_data, cliente)
        for attr, value in validated_data.items():
            setattr(cliente, attr, value)
        cliente.save()
        return cliente

    @staticmethod
    def deletar_cliente(cliente):
        cliente.delete()
