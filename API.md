# 📡 API Documentation - Jukebox-Pi-Money

API REST para controle do sistema Jukebox.

**Base URL:** `http://localhost:5000/api`

## 🔐 Autenticação

Alguns endpoints requerem autenticação via header:

```
X-Hardware-Token: seu_hardware_token_aqui
```

## 📊 Status e Informações

### GET /api/status

Retorna status geral do sistema.

**Response:**
```json
{
  "status": "online",
  "balance": 10.0,
  "queue_size": 3,
  "hardware_enabled": true,
  "payment_gateway_enabled": true,
  "youtube_enabled": true
}
```

### GET /api/balance

Retorna saldo de créditos e estatísticas.

**Response:**
```json
{
  "balance": 10.0,
  "stats": {
    "id": 1,
    "balance": 10.0,
    "total_deposited": 50.0,
    "total_spent": 40.0,
    "updated_at": "2025-10-28 15:00:00"
  }
}
```

## 💳 Pagamentos

### GET /api/payment/methods

Lista métodos de pagamento disponíveis com preços.

**Response:**
```json
{
  "methods": [
    {
      "method": "cash",
      "price": 5.0,
      "base_price": 5.0
    },
    {
      "method": "pix",
      "price": 5.0,
      "base_price": 5.0
    },
    {
      "method": "debit",
      "price": 5.1,
      "base_price": 5.0
    },
    {
      "method": "credit",
      "price": 5.2,
      "base_price": 5.0
    }
  ]
}
```

### POST /api/payment/create

Cria novo pagamento.

**Request:**
```json
{
  "method": "pix",
  "description": "Crédito para Jukebox"
}
```

**Response (PIX):**
```json
{
  "transaction_id": "pix_a1b2c3d4e5f6",
  "payment_id": "12345678",
  "amount": 5.0,
  "method": "pix",
  "status": "pending",
  "qr_code": "00020126580014br.gov.bcb.pix...",
  "qr_code_base64": "iVBORw0KGgoAAAANSUhEUgA..."
}
```

**Response (Dinheiro):**
```json
{
  "method": "cash",
  "amount": 5.0,
  "message": "Insira dinheiro no aceitador de notas"
}
```

**Errors:**
- `400` - Método de pagamento inválido
- `503` - Gateway de pagamento não disponível

### GET /api/payment/status/{transaction_id}

Verifica status de um pagamento.

**Response:**
```json
{
  "transaction_id": "pix_a1b2c3d4e5f6",
  "status": "approved",
  "amount": 5.0,
  "method": "pix"
}
```

**Status possíveis:**
- `pending` - Aguardando pagamento
- `approved` - Pagamento aprovado
- `rejected` - Pagamento rejeitado
- `cancelled` - Cancelado pelo usuário
- `in_process` - Em processamento
- `refunded` - Estornado

### POST /api/webhook

Recebe notificações de pagamento do gateway.

**Headers:**
```
x-signature: assinatura_do_webhook
```

**Request (Mercado Pago):**
```json
{
  "type": "payment",
  "data": {
    "id": "12345678"
  }
}
```

**Response:**
```json
{
  "status": "processed"
}
```

## 🎵 Músicas

### POST /api/music/search

Busca música no YouTube.

**Request:**
```json
{
  "query": "Bohemian Rhapsody - Queen"
}
```

**Response:**
```json
{
  "video_id": "fJ9rUzIMcZQ",
  "title": "Queen – Bohemian Rhapsody (Official Video Remastered)",
  "duration_text": "5:55"
}
```

**Errors:**
- `400` - Query não fornecida
- `500` - Erro ao buscar música

### POST /api/music/add

Adiciona música à fila de reprodução.

**Request:**
```json
{
  "video_id": "fJ9rUzIMcZQ",
  "title": "Queen – Bohemian Rhapsody",
  "artist": "Queen",
  "duration": 355
}
```

**Response:**
```json
{
  "message": "Música adicionada à fila",
  "song_id": 42,
  "new_balance": 5.0
}
```

**Errors:**
- `400` - Dados incompletos
- `402` - Saldo insuficiente
  ```json
  {
    "error": "Saldo insuficiente",
    "balance": 2.0,
    "required": 5.0
  }
  ```
- `429` - Fila cheia

### GET /api/music/queue

Lista músicas na fila.

**Response:**
```json
{
  "queue": [
    {
      "id": 1,
      "video_id": "fJ9rUzIMcZQ",
      "title": "Queen – Bohemian Rhapsody",
      "artist": "Queen",
      "duration": 355,
      "status": "playing",
      "transaction_id": "cash_abc123",
      "created_at": "2025-10-28 15:00:00",
      "played_at": "2025-10-28 15:05:00"
    },
    {
      "id": 2,
      "video_id": "dQw4w9WgXcQ",
      "title": "Rick Astley - Never Gonna Give You Up",
      "artist": "Rick Astley",
      "duration": 212,
      "status": "queued",
      "transaction_id": "pix_def456",
      "created_at": "2025-10-28 15:02:00",
      "played_at": null
    }
  ]
}
```

**Status das músicas:**
- `queued` - Na fila, aguardando
- `playing` - Tocando agora
- `played` - Já foi tocada

### POST /api/music/next

🔒 **Requer autenticação (X-Hardware-Token)**

Toca próxima música da fila.

**Response:**
```json
{
  "message": "Música tocando",
  "song": {
    "id": 2,
    "video_id": "dQw4w9WgXcQ",
    "title": "Rick Astley - Never Gonna Give You Up",
    "artist": "Rick Astley"
  }
}
```

**Errors:**
- `401` - Token inválido
- `404` - Fila vazia

## 🔧 Hardware

### POST /api/hardware/simulate-cash

🔒 **Apenas em modo desenvolvimento**

Simula inserção de dinheiro.

**Request:**
```json
{
  "count": 2
}
```

**Response:**
```json
{
  "message": "2 pulso(s) simulado(s)",
  "new_balance": 14.0
}
```

**Errors:**
- `403` - Disponível apenas em desenvolvimento
- `503` - Hardware não disponível

## 📝 Códigos de Erro HTTP

| Código | Descrição |
|--------|-----------|
| 200 | Sucesso |
| 400 | Requisição inválida |
| 401 | Não autorizado |
| 402 | Saldo insuficiente |
| 403 | Proibido |
| 404 | Não encontrado |
| 429 | Muitas requisições (fila cheia) |
| 500 | Erro interno do servidor |
| 503 | Serviço indisponível |

## 🔄 Webhooks

### Configurando Webhooks do Mercado Pago

1. Acesse: https://www.mercadopago.com.br/developers/panel
2. Vá em "Webhooks" → "Configurar notificações"
3. Adicione a URL: `https://seu-dominio.com/api/webhook`
4. Eventos: `payment` (pagamentos)
5. Salve o secret gerado no `.env` como `WEBHOOK_SECRET`

### Validação de Webhooks

O sistema valida webhooks verificando:
- Assinatura no header `x-signature`
- Presença dos campos obrigatórios
- Correspondência com transações registradas

## 📊 Exemplos de Uso

### Fluxo completo: Adicionar música com PIX

```bash
# 1. Criar pagamento PIX
curl -X POST http://localhost:5000/api/payment/create \
  -H "Content-Type: application/json" \
  -d '{"method":"pix","description":"Crédito Jukebox"}'

# Resposta: { "transaction_id": "pix_abc123", "qr_code_base64": "..." }

# 2. Cliente escaneia QR Code e paga

# 3. Webhook é recebido automaticamente

# 4. Verificar saldo atualizado
curl http://localhost:5000/api/balance

# 5. Buscar música
curl -X POST http://localhost:5000/api/music/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Imagine Dragons - Believer"}'

# 6. Adicionar à fila
curl -X POST http://localhost:5000/api/music/add \
  -H "Content-Type: application/json" \
  -d '{"video_id":"xyz","title":"Imagine Dragons - Believer"}'

# 7. Verificar fila
curl http://localhost:5000/api/music/queue
```

### Fluxo completo: Adicionar música com dinheiro

```bash
# 1. Selecionar método dinheiro (retorna instruções)
curl -X POST http://localhost:5000/api/payment/create \
  -H "Content-Type: application/json" \
  -d '{"method":"cash"}'

# 2. Cliente insere nota no aceitador
# Hardware detecta automaticamente e adiciona crédito

# 3. Verificar saldo
curl http://localhost:5000/api/balance

# 4. Buscar e adicionar música (mesmo fluxo acima)
```

## 🧪 Testando a API

### Usando cURL

```bash
# Status
curl http://localhost:5000/api/status

# Métodos de pagamento
curl http://localhost:5000/api/payment/methods

# Fila de músicas
curl http://localhost:5000/api/music/queue
```

### Usando Python

```python
import requests

BASE_URL = "http://localhost:5000/api"

# Verificar status
response = requests.get(f"{BASE_URL}/status")
print(response.json())

# Buscar música
response = requests.post(
    f"{BASE_URL}/music/search",
    json={"query": "The Beatles - Hey Jude"}
)
print(response.json())
```

### Usando Postman

Importe a coleção de endpoints disponível em `docs/postman_collection.json`.

## 📞 Suporte

Para dúvidas sobre a API:
- Consulte a documentação completa em `README.md`
- Abra uma issue no GitHub
- Entre em contato com o suporte técnico
