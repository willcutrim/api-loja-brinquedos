from django.db.models import Sum, Avg, Count
from apps.vendas.models import Venda
from apps.clientes.models import Cliente

class VendaService:
    @staticmethod
    def criar_venda(validated_data):
        return Venda.objects.create(**validated_data)

    @staticmethod
    def total_vendas_por_dia():
        return (
            Venda.objects.values('data')
            .annotate(total=Sum('valor'))
            .order_by('data')
        )

    @staticmethod
    def destaques_clientes():
        clientes = Cliente.objects.all()

        maior_volume = clientes.annotate(
            total=Sum('vendas__valor')
        ).order_by('-total').first()

        maior_media = clientes.annotate(
            media=Avg('vendas__valor')
        ).order_by('-media').first()

        maior_frequencia = clientes.annotate(
            dias=Count('vendas__data', distinct=True)
        ).order_by('-dias').first()

        return {
            'maior_volume': {
                'id': maior_volume.id,
                'nome': maior_volume.nome
            } if maior_volume else None,
            'maior_media': {
                'id': maior_media.id,
                'nome': maior_media.nome
            } if maior_media else None,
            'maior_frequencia': {
                'id': maior_frequencia.id,
                'nome': maior_frequencia.nome
            } if maior_frequencia else None,
        }

    @staticmethod
    def total_vendas_por_cliente():
        return (
            Venda.objects.values('cliente')
            .annotate(total=Sum('valor'))
            .order_by('-total')
        )