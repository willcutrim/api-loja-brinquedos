from rest_framework.test import APITestCase
from rest_framework import status

from django.urls import reverse
from django.contrib.auth.models import User

from apps.clientes.models import Cliente


class ClienteAPITests(APITestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='admin', password='admin')
        self.client.force_authenticate(user=self.user)
        self.url = reverse('clientes-list')

    def test_criar_cliente(self):
        payload = {
            "nome": "Maria Teste",
            "email": "maria@example.com",
            "nascimento": "1990-01-01"
        }
        response = self.client.post(self.url, payload, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['email'], "maria@example.com")

    def test_listar_clientes(self):
        Cliente.objects.create(nome="Ana", email="ana@a.com", nascimento="1992-02-02")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(len(response.data) >= 1)

    def test_filtro_por_nome(self):
        Cliente.objects.create(nome="Carlos", email="carlos@x.com", nascimento="1995-05-05")
        response = self.client.get(self.url + '?nome=Carlos')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data[0]['nome'], "Carlos")

    def test_editar_cliente(self):
        cliente = Cliente.objects.create(nome="Editável", email="edit@a.com", nascimento="1999-09-09")
        payload = {"nome": "Editado"}
        url = reverse('clientes-detail', args=[cliente.id])
        response = self.client.patch(url, payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['nome'], "Editado")

    def test_deletar_cliente(self):
        cliente = Cliente.objects.create(nome="Excluir", email="x@x.com", nascimento="1980-08-08")
        url = reverse('clientes-detail', args=[cliente.id])
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)