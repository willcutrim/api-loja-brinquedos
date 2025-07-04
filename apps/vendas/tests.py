from datetime import date

from django.contrib.auth.models import User
from rest_framework.test import APITestCase
from rest_framework import status

from apps.clientes.models import Cliente
from apps.vendas.models import Venda


class VendasEstatisticasTests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.force_authenticate(user=self.user)

        self.cliente1 = Cliente.objects.create(nome="Cliente 1", email="c1@example.com", nascimento="1990-01-01")
        self.cliente2 = Cliente.objects.create(nome="Cliente 2", email="c2@example.com", nascimento="1991-01-01")

        Venda.objects.create(cliente=self.cliente1, data=date(2024, 1, 1), valor=100)
        Venda.objects.create(cliente=self.cliente1, data=date(2024, 1, 2), valor=50)
        Venda.objects.create(cliente=self.cliente2, data=date(2024, 1, 1), valor=200)

    def test_total_vendas_por_dia(self):
        url = '/api/vendas/estatisticas/total-por-dia/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(any(v['total'] > 0 for v in response.data))

    def test_estatisticas_destaques(self):
        url = '/api/vendas/estatisticas/destaques/'
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['maior_volume']['nome'], "Cliente 2")
        self.assertEqual(response.data['maior_media']['nome'], "Cliente 2")
        self.assertEqual(response.data['maior_frequencia']['nome'], "Cliente 1")

