# 🎵 Jukebox-Pi-Money

Sistema embarcado de Jukebox com aceitador de notas e YouTube Music para Raspberry Pi.

## 🚀 Características

- 💰 **Múltiplos métodos de pagamento**: Dinheiro, PIX, Débito, Crédito
- 🎵 **Reproduz músicas do YouTube** automaticamente com Selenium
- 🎧 **Música ambiente automática**: Toca músicas aleatórias a cada 10 minutos quando não há atividade
- 🚫 **Bloqueio de anúncios**: Sistema avançado de ad-blocking integrado
- 📱 **Interface touchscreen responsiva** com design moderno
- 💾 **Banco de dados SQLite** para logs, transações e histórico
- 🔒 **API REST completa** protegida por token
- 🔌 **Integração com hardware** via GPIO (aceitador de notas)
- 💳 **Gateway de pagamento Mercado Pago** com suporte a PIX
- 📊 **Sistema de fila de músicas** gerenciado automaticamente
- 🎨 **Interface web moderna** com animações e design responsivo

## 📋 Requisitos

### Hardware
- Raspberry Pi 4 (4GB RAM recomendado)
- Display Touchscreen 7" ou superior
- Aceitador de Notas JCM WBA10 (opcional)
- Conexão à Internet

### Software
- Raspberry Pi OS Lite (64-bit) - Bullseye ou superior
- Python 3.9+
- Chrome/Chromium Browser + ChromeDriver

## 🛠️ Instalação Rápida

```bash
# Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp env.example .env
nano .env  # Edite com suas configurações

# Execute testes
python3 tests/test_jukebox.py

# Inicie o servidor
python3 src/server/app.py
```

Acesse: http://localhost:5000

## 📂 Estrutura do Projeto

```
Jukebox-Pi-Money/
├── src/
│   ├── db/                 # Banco de dados SQLite
│   │   ├── __init__.py
│   │   └── models.py       # Modelos e operações do banco
│   ├── hardware/           # Controle de hardware
│   │   ├── __init__.py
│   │   └── bill_acceptor.py  # Aceitador de notas GPIO
│   ├── payments/           # Gateways de pagamento
│   │   ├── __init__.py
│   │   ├── base_gateway.py    # Interface base
│   │   └── mercadopago_gateway.py  # Mercado Pago
│   ├── server/             # Servidor Flask
│   │   ├── app.py          # Aplicação principal
│   │   ├── config.py       # Configurações
│   │   ├── static/         # Arquivos estáticos (HTML/CSS/JS)
│   │   └── templates/      # Templates HTML
│   └── youtube/            # Controle do YouTube
│       ├── __init__.py
│       └── youtube_player.py  # Player com Selenium
├── tests/                  # Testes automatizados
│   └── test_jukebox.py
├── logs/                   # Logs do sistema
├── .env.example            # Template de variáveis
├── requirements.txt        # Dependências Python
├── README.md               # Este arquivo
├── DEPLOY.md               # Guia completo de deploy
└── API.md                  # Documentação da API

## 🎯 Funcionalidades Implementadas

### Backend
- ✅ Flask API REST completa
- ✅ Banco de dados SQLite com modelos robustos
- ✅ Sistema de transações e créditos
- ✅ Autenticação via token
- ✅ CORS configurado
- ✅ Logging estruturado

### Hardware
- ✅ Controlador GPIO para aceitador de notas
- ✅ Detecção de pulsos com debounce
- ✅ Modo simulação para testes
- ✅ Callbacks assíncronos

### Pagamentos
- ✅ Interface abstrata para gateways
- ✅ Integração com Mercado Pago
- ✅ Suporte a PIX com QR Code
- ✅ Suporte a Débito e Crédito
- ✅ Validação de webhooks
- ✅ Sistema de taxas configurável

### YouTube
- ✅ Busca automática de músicas
- ✅ Reprodução com Selenium
- ✅ Controle de volume e pausa/play
- ✅ Detecção e skip de anúncios
- ✅ Extração de metadados
- ✅ **Sistema de música idle** - Reproduz músicas aleatórias a cada 10 minutos quando não há atividade
- ✅ **Ad-blocking avançado** - Bloqueio inteligente de anúncios com múltiplas técnicas
- ✅ Categorias personalizáveis de música para modo idle

### Frontend
- ✅ Interface responsiva touchscreen
- ✅ Seleção de métodos de pagamento
- ✅ Display de QR Code PIX
- ✅ Busca de músicas
- ✅ Visualização da fila
- ✅ Feedback visual de status
- ✅ Design moderno com gradientes

## 📡 API REST

### Endpoints Principais

```bash
# Status do sistema
GET /api/status

# Saldo de créditos
GET /api/balance

# Métodos de pagamento
GET /api/payment/methods

# Criar pagamento
POST /api/payment/create

# Buscar música
POST /api/music/search

# Adicionar à fila
POST /api/music/add

# Ver fila
GET /api/music/queue
```

📖 **Documentação completa**: [API.md](API.md)

## 🚀 Deploy em Produção

Para instruções completas de instalação e configuração no Raspberry Pi, consulte:

📖 **Guia completo**: [DEPLOY.md](DEPLOY.md)

### Resumo:
1. Instalar dependências do sistema
2. Configurar GPIO e hardware
3. Configurar variáveis de ambiente
4. Configurar gateway de pagamento
5. Configurar serviço systemd
6. Configurar modo kiosk (opcional)

## 🧪 Testes

```bash
# Executar todos os testes
python3 tests/test_jukebox.py

# Resultado esperado:
# ✅ PASSOU: Configurações
# ✅ PASSOU: Banco de Dados
# ✅ PASSOU: Hardware
# ✅ PASSOU: Pagamentos
# Total: 4/4 testes passaram
```

## 🔧 Configuração

Principais variáveis no `.env`:

```bash
# Gateway de Pagamento
PAYMENT_PROVIDER=mercadopago
PAYMENT_API_KEY=seu_api_key
PAYMENT_ACCESS_TOKEN=seu_token

# Hardware
GPIO_BILL_ACCEPTOR=17
PULSE_VALUE=2.00

# Negócio
PRICE_PER_SONG=5.00
CREDIT_CARD_FEE=3.99
PIX_FEE=0.00

# Segurança
SECRET_KEY=sua_chave_secreta
HARDWARE_TOKEN=seu_token_hardware
```

## 🎨 Interface do Usuário

A interface possui 5 telas principais:

1. **Seleção de Pagamento** - Escolha entre Dinheiro, PIX, Débito ou Crédito
2. **Aguardando Pagamento** - Exibe QR Code PIX e aguarda confirmação
3. **Buscar Música** - Campo de busca e visualização da fila
4. **Sucesso** - Confirmação de música adicionada
5. **Erro** - Tratamento de erros com feedback claro

## 💡 Exemplos de Uso

### Simular inserção de dinheiro (desenvolvimento)

```bash
curl -X POST http://localhost:5000/api/hardware/simulate-cash \
  -H "Content-Type: application/json" \
  -d '{"count":2}'
```

### Criar pagamento PIX

```bash
curl -X POST http://localhost:5000/api/payment/create \
  -H "Content-Type: application/json" \
  -d '{"method":"pix"}'
```

### Buscar e adicionar música

```bash
# Buscar
curl -X POST http://localhost:5000/api/music/search \
  -H "Content-Type: application/json" \
  -d '{"query":"Queen - Bohemian Rhapsody"}'

# Adicionar
curl -X POST http://localhost:5000/api/music/add \
  -H "Content-Type: application/json" \
  -d '{"video_id":"abc123","title":"Queen - Bohemian Rhapsody"}'
```

## 🐛 Troubleshooting

### Servidor não inicia
```bash
# Verificar logs
tail -f logs/jukebox.log

# Testar manualmente
python3 src/server/app.py
```

### GPIO não funciona
```bash
# Adicionar usuário ao grupo GPIO
sudo usermod -a -G gpio $USER

# Testar GPIO
python3 -c "import RPi.GPIO as GPIO; print('OK')"
```

### Mais problemas?
Consulte [DEPLOY.md](DEPLOY.md) seção "Troubleshooting"

## 📄 Licença

MIT License - veja [LICENSE](LICENSE) para detalhes.

## 👥 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Fork o projeto
2. Crie uma branch (`git checkout -b feature/nova-funcionalidade`)
3. Commit suas mudanças (`git commit -m 'Adiciona nova funcionalidade'`)
4. Push para a branch (`git push origin feature/nova-funcionalidade`)
5. Abra um Pull Request

## 📞 Suporte

- 📧 Email: godfathercorleone994@gmail.com
- 🐛 Issues: [GitHub Issues](https://github.com/godfathercorleone994-wq/Jukebox/issues)
- 📖 Docs: [DEPLOY.md](DEPLOY.md) | [API.md](API.md)

## 🙏 Agradecimentos

- Mercado Pago pelo SDK de pagamentos
- Selenium pelo controle do navegador
- Flask pela simplicidade do framework
- Comunidade Raspberry Pi

---

**Desenvolvido com ❤️ para a comunidade Raspberry Pi**
