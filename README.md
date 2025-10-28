# 🎵 Jukebox-Pi-Money

Sistema embarcado de Jukebox com aceitador de notas e YouTube Music para Raspberry Pi.

**✨ Novo: Agora funciona em qualquer PC/Linux com navegação por teclado!** 

**🌐 Teste no navegador**: [Experimente a demo online via GitHub Pages!](https://godfathercorleone994-wq.github.io/Jukebox/)

## 🚀 Características

- 💰 **Múltiplos métodos de pagamento**: Dinheiro, PIX, Débito, Crédito
- 🎵 **Reproduz músicas do YouTube** automaticamente com Selenium
- 🎧 **Música ambiente automática**: Toca músicas aleatórias a cada 10 minutos quando não há atividade
- 🚫 **Bloqueio de anúncios**: Sistema avançado de ad-blocking integrado
- 📱 **Interface touchscreen responsiva** com design moderno
- ⌨️ **Navegação completa por teclado**: Funciona sem mouse ou touchscreen
- 🔐 **Código de operador**: Sistema secreto para adicionar créditos sem pagamento
- 🖥️ **Suporte para PC/Linux**: Não requer Raspberry Pi para desenvolvimento/testes
- 💾 **Banco de dados SQLite** para logs, transações e histórico
- 🔒 **API REST completa** protegida por token
- 🔌 **Integração com hardware** via GPIO (aceitador de notas)
- 💳 **Gateway de pagamento Mercado Pago** com suporte a PIX
- 📊 **Sistema de fila de músicas** gerenciado automaticamente
- 🎨 **Interface web moderna** com animações e design responsivo

## 📋 Requisitos

### Opção 1: Raspberry Pi (Produção)

#### Hardware
- Raspberry Pi 4 (4GB RAM recomendado)
- Display Touchscreen 7" ou superior
- Aceitador de Notas JCM WBA10 (opcional)
- Conexão à Internet

#### Software
- Raspberry Pi OS Lite (64-bit) - Bullseye ou superior
- Python 3.9+
- Chrome/Chromium Browser + ChromeDriver

### Opção 2: PC/Linux (Desenvolvimento/Testes)

#### Hardware
- Qualquer PC com Linux (Ubuntu, Debian, Fedora, etc.)
- **Não requer** Raspberry Pi, GPIO ou touchscreen
- Teclado e mouse/touchpad
- Conexão à Internet (opcional)

#### Software
- Linux (qualquer distribuição) ou WSL2 no Windows
- Python 3.9+
- Navegador web moderno

📖 **Veja o guia completo**: [PC-LINUX.md](PC-LINUX.md)

### Opção 3: Instalador Profissional (Para Usuários Finais)

**✨ Novo!** Instaladores profissionais com configuração automática:

#### Linux - Instalador Debian (.deb)
```bash
# Baixar do GitHub Releases
wget https://github.com/godfathercorleone994-wq/Jukebox/releases/latest/download/jukebox-pi-money_2.3.0_amd64.deb

# Instalar
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb

# Configurar
sudo nano /etc/jukebox/.env

# Executar
jukebox
```

#### Windows - Instalador (.exe)
```
1. Baixe jukebox-setup-windows-x64.exe do GitHub Releases
2. Execute o instalador
3. Siga o assistente de configuração
4. Use o atalho criado no Desktop ou Menu Iniciar
```

Vantagens dos Instaladores:
- ✅ **Instalação profissional** com um clique/comando
- ✅ **Configuração guiada** durante a instalação
- ✅ **Atalhos automáticos** no menu do sistema
- ✅ **Fácil desinstalação** via gerenciador de pacotes
- ✅ **Não requer Python** instalado
- ✅ **Ideal para usuários finais** sem conhecimento técnico

📖 **Guia completo**: [INSTALLER.md](INSTALLER.md)

### Opção 4: Executável Standalone (Sem Python)

**Alternativa portátil** - funciona sem instalar:

#### Linux
```bash
# Construir executável
./build-linux.sh

# Executar
./dist/jukebox
```

#### Windows
```cmd
REM Construir executável
build-windows.bat

REM Executar
dist\jukebox.exe
```

Características:
- ✅ **Não requer Python** instalado no sistema
- ✅ **Standalone** - inclui todas as dependências
- ✅ **Portátil** - funciona em qualquer Linux/Windows
- ✅ **Fácil distribuição** - arquivo único de ~80-100MB
- ✅ **Pronto para uso** - apenas executar e acessar http://localhost:5000

📖 **Guia completo de build**: [BUILD.md](BUILD.md)

## 🛠️ Instalação Rápida

### Para Usuários Finais (Mais Fácil)

#### 🐧 Linux (Ubuntu/Debian)
```bash
# Baixe e instale o pacote .deb
wget https://github.com/godfathercorleone994-wq/Jukebox/releases/latest/download/jukebox-pi-money_2.3.0_amd64.deb
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb

# Configure
sudo nano /etc/jukebox/.env

# Execute
jukebox

# Acesse: http://localhost:5000
```

#### 🪟 Windows
1. Baixe `jukebox-setup-windows-x64.exe` do [GitHub Releases](https://github.com/godfathercorleone994-wq/Jukebox/releases/latest)
2. Execute o instalador
3. Siga o assistente
4. Use o atalho no Desktop ou Menu Iniciar
5. Acesse: http://localhost:5000

📖 **Guia completo**: [INSTALLER.md](INSTALLER.md)

### Para Raspberry Pi (Produção)

```bash
# Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

# Execute o script de inicialização
./start.sh

# Acesse: http://localhost:5000
```

📖 **Guia completo de deploy**: [DEPLOY.md](DEPLOY.md)

### Para PC/Linux (Desenvolvimento/Testes)

```bash
# Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

# Execute o script para PC (detecta automaticamente o ambiente)
./start-pc.sh

# Acesse: http://localhost:5000
```

O script `start-pc.sh` automaticamente:
- ✅ Detecta que não é Raspberry Pi
- ✅ Instala apenas dependências necessárias (sem RPi.GPIO)
- ✅ Desabilita hardware GPIO
- ✅ Configura modo desenvolvimento
- ✅ Habilita navegação por teclado

📖 **Guia completo para PC**: [PC-LINUX.md](PC-LINUX.md)

### Opção 5: Testar no Navegador (Sem Instalação)

🌐 **Teste online sem instalar nada!**

Acesse a demo interativa hospedada no GitHub Pages:
```
https://godfathercorleone994-wq.github.io/Jukebox/
```

Disponível:
- ✅ YouTube Player Demo - Teste o player com vídeos do YouTube
- ✅ Interface responsiva e moderna
- ✅ Sem necessidade de instalar Python, Flask ou dependências
- ✅ Funciona em qualquer navegador moderno

📖 **Guia completo**: [GITHUB_PAGES.md](GITHUB_PAGES.md)

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

### ⌨️ Navegação por Teclado

Todas as telas suportam navegação completa por teclado:

- **Setas (↑↓←→)**: Navegar entre elementos
- **Enter**: Selecionar/ativar
- **Tab**: Próximo elemento
- **1-9**: Seleção rápida
- **H**: Voltar ao início
- **Esc**: Voltar/Cancelar
- **F1 ou ?**: Mostrar ajuda de atalhos

Ideal para:
- 🖥️ PCs sem touchscreen
- ⌨️ Uso em terminais/kiosks com teclado
- ♿ Acessibilidade
- 🎮 Controle tipo console

## 🔐 Código de Operador (Admin)

Sistema exclusivo para operadores adicionarem créditos sem pagamento:

### Ativação
Pressione **Ctrl+Shift+A** na tela principal para abrir o modal secreto.

### Configuração
Configure o código no arquivo `.env`:

```bash
ADMIN_ENABLED=true
ADMIN_CODE=seu_codigo_secreto_aqui
ADMIN_CREDIT_AMOUNT=20.00
```

### Uso
1. Pressione **Ctrl+Shift+A**
2. Digite o código secreto
3. Créditos são adicionados instantaneamente
4. Use para tocar músicas sem pagar

**⚠️ IMPORTANTE**: Mantenha o código em segredo! Apenas operadores devem ter acesso.

📖 **Documentação completa**: [ADMIN_CODE.md](ADMIN_CODE.md)

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

## 🌟 Novidades

### v2.3 - Instaladores Profissionais e Executáveis Standalone
- 📦 **Novo!** Instaladores profissionais para Linux (.deb) e Windows (.exe)
- ✨ **Instalação com um clique/comando** - configuração automática
- 🎯 **Atalhos automáticos** no menu do sistema e desktop
- 🔧 **Assistente de configuração** integrado no instalador Windows
- 🐧 **Pacote Debian** completo com scripts de pós-instalação
- 🪟 **Instalador Inno Setup** com interface gráfica profissional
- 📖 **Documentação completa** de instaladores ([INSTALLER.md](INSTALLER.md))
- 🚀 **Build de executáveis** standalone sem necessidade de Python
- 🐧 Suporte completo para Linux (qualquer distribuição x64)
- 🪟 Suporte completo para Windows (7/8/10/11 x64)
- 🚀 Scripts automatizados de build (`build-linux.sh` e `build-windows.bat`)
- 📖 Documentação completa de build e distribuição ([BUILD.md](BUILD.md))
- ✨ Executável único de ~80-100MB com todas as dependências incluídas
- 🎯 Ideal para distribuição a usuários finais sem conhecimento técnico

### v2.2 - Testes no Navegador via GitHub Pages
- 🌐 Deploy automático via GitHub Actions para GitHub Pages
- ✅ Teste o código diretamente no navegador sem instalar nada
- 🎵 Demo interativa do YouTube Player online
- 📖 Documentação completa ([GITHUB_PAGES.md](GITHUB_PAGES.md))
- 🚀 Implantação automática em cada push para main/master

### v2.1 - Sistema de Código Admin
- 🔐 Sistema secreto de código para operadores
- ⚡ Adicione créditos instantaneamente sem pagamento
- 🎵 Toque músicas específicas sem inserir dinheiro
- 📝 Auditoria completa de transações admin
- ⌨️ Ativação via atalho de teclado (Ctrl+Shift+A)
- 🔒 Validação segura no backend

### v2.0 - Suporte PC/Linux e Navegação por Teclado
- ✨ Novo script `start-pc.sh` para executar em qualquer PC/Linux
- ⌨️ Navegação completa por teclado (setas, Enter, Tab, números)
- 🖥️ Detecção automática de ambiente (Raspberry Pi vs PC)
- 📖 Documentação específica para PC ([PC-LINUX.md](PC-LINUX.md))
- ♿ Melhor acessibilidade
- 🎯 Indicadores visuais de foco para teclado
- 🔧 Configuração automática baseada no ambiente

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
- 🌐 Demo Online: [GitHub Pages](https://godfathercorleone994-wq.github.io/Jukebox/)
- 📖 Docs: 
  - [INSTALLER.md](INSTALLER.md) - **Novo!** Instaladores profissionais para usuários finais
  - [BUILD.md](BUILD.md) - Criação de executáveis Linux/Windows
  - [DEPLOY.md](DEPLOY.md) - Deploy em Raspberry Pi
  - [PC-LINUX.md](PC-LINUX.md) - Uso em PC/Linux
  - [GITHUB_PAGES.md](GITHUB_PAGES.md) - Testes no navegador
  - [API.md](API.md) - API REST
  - [ADMIN_CODE.md](ADMIN_CODE.md) - Sistema de código admin

## 🙏 Agradecimentos

- Mercado Pago pelo SDK de pagamentos
- Selenium pelo controle do navegador
- Flask pela simplicidade do framework
- Comunidade Raspberry Pi

---

**Desenvolvido com ❤️ para a comunidade Raspberry Pi**
