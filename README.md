# 🧸 API - Loja de Brinquedos

Este projeto é uma aplicação completa (Back + Front) para gerenciamento de **clientes e vendas** de uma loja de brinquedos. Ele permite autenticação via JWT, cadastro e listagem de clientes, controle de vendas, estatísticas visuais e mais.

---

## 🚀 Tecnologias Utilizadas

- Python 3.10+
- Django 4+
- Django Rest Framework
- SimpleJWT
- Bootstrap 5 (layout)
- Chart.js (gráficos)
- SQLite (como banco principal)
- Postman ou Insomnia (para testes)

---

## ⚙️ Instalação e Execução

### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/projeto-loja-brinquedos.git
cd projeto-loja-brinquedos
```

### 2. Crie e ative o ambiente virtual

```bash
python -m venv venv
source venv/bin/activate  # Linux/Mac
venv\Scripts\activate   # Windows
```

### 3. Instale as dependências

```bash
pip install -r requirements.txt
```

> **Requisitos principais:**
> - django
> - djangorestframework
> - djangorestframework-simplejwt
> - django-filter

### 4. Rode as migrações

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Crie um superusuário (opcional)

```bash
python manage.py createsuperuser
```

### 6. Execute o servidor

```bash
python manage.py runserver
```

---

## 🧪 Executar os Testes

### Rodar todos os testes:

```bash
python manage.py test
```

### Rodar por app:

```bash
python manage.py test apps.clientes.tests
python manage.py test apps.vendas.tests
```

---

## 📬 Payloads úteis (Postman/Insomnia)

🔐 **Login JWT**

```
POST /api/usuarios/token/
```

```json
{
  "username": "admin",
  "password": "admin"
}
```

📥 **Criar cliente**

```
POST /api/clientes/
```

```json
{
  "nome": "João Teste",
  "email": "joao@example.com",
  "nascimento": "1990-10-10"
}
```

💰 **Criar venda**

```
POST /api/vendas/
```

```json
{
  "cliente": 1,
  "data": "2024-01-15",
  "valor": 150.0
}
```

📊 **Estatísticas de vendas**

```
GET /api/vendas/estatisticas/total-por-dia/
GET /api/vendas/estatisticas/destaques/
```

---

## 📊 Funcionalidades

- Cadastro e listagem de clientes com filtro
- Registro de vendas com data e valor
- Estatísticas:
  - Total por dia (gráfico)
  - Cliente com maior volume
  - Cliente com maior média
  - Cliente com maior frequência de compra
- Identificação da letra do alfabeto ausente no nome do cliente

---

## 🧩 Observação sobre o banco de dados

> ⚠️ **Nota:** Embora o PostgreSQL seja o banco mais comum para produção, utilizei o SQLite por questões técnicas locais.

Durante o desenvolvimento, enfrentei um problema no ambiente com o PostgreSQL, por isso optei por SQLite. Ele funciona perfeitamente com Django e permite focar na lógica e entrega do projeto.

Caso deseje trocar para PostgreSQL:

```python
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'nome_do_banco',
    'USER': 'usuario',
    'PASSWORD': 'senha',
    'HOST': 'localhost',
    'PORT': '5432',
  }
}
```