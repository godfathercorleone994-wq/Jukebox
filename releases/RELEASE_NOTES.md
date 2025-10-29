# 🎵 Jukebox Pi Money - Release v2.3.0

Data: 29 de Outubro de 2024

## 📦 Arquivos Disponíveis

### 🐧 Linux (x86_64)
- **jukebox-pi-money_2.3.0_amd64.deb** (29 MB)
  - Instalador Debian para Kali Linux, Ubuntu, Debian e derivados
  - Instalação profissional com um comando
  - Configuração automática em `/etc/jukebox/.env`
  - Executável instalado em `/usr/local/bin/jukebox`

## 🚀 Instalação Rápida no Kali Linux

```bash
# Download direto
wget https://raw.githubusercontent.com/godfathercorleone994-wq/Jukebox/main/releases/jukebox-pi-money_2.3.0_amd64.deb

# Instalar
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb

# Configurar
sudo nano /etc/jukebox/.env

# Executar
jukebox

# Acessar
# http://localhost:5000
```

## ✨ Características desta Versão

- 💰 **Múltiplos métodos de pagamento**: Dinheiro, PIX, Débito, Crédito
- 🎵 **Reproduz músicas do YouTube** automaticamente com Selenium
- 🎧 **Música ambiente automática**: Toca músicas aleatórias quando em espera
- 🚫 **Bloqueio de anúncios**: Sistema avançado de ad-blocking integrado
- 📱 **Interface touchscreen responsiva** com design moderno
- ⌨️ **Navegação completa por teclado**: Funciona sem mouse ou touchscreen
- 🔐 **Código de operador**: Sistema secreto para adicionar créditos
- 🖥️ **Suporte para PC/Linux**: Não requer Raspberry Pi
- 💾 **Banco de dados SQLite** para logs e transações
- 🔒 **API REST completa** protegida por token
- 🔌 **Integração com hardware** via GPIO (opcional)
- 💳 **Gateway Mercado Pago** com suporte a PIX

## 📋 Requisitos do Sistema

### Mínimos
- Kali Linux, Debian, Ubuntu ou derivados (x86_64)
- 1 GB RAM
- 500 MB espaço em disco
- Conexão à Internet (opcional para modo offline)

### Recomendados
- 2 GB RAM
- 1 GB espaço em disco
- Raspberry Pi 4 (4GB) para produção
- Display Touchscreen 7" ou superior
- Aceitador de Notas JCM WBA10 (opcional)

## 🔧 Configurações Importantes

Edite `/etc/jukebox/.env` após instalação:

```bash
# Configurações essenciais
FLASK_ENV=production
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY
HARDWARE_ENABLED=false          # true se tiver Raspberry Pi com GPIO
YOUTUBE_ENABLED=false           # true para reproduzir do YouTube
PRICE_PER_SONG=5.00            # Preço por música em R$

# Código de operador (opcional)
ADMIN_ENABLED=false             # true para habilitar código secreto
ADMIN_CODE=123456              # Código secreto para modo admin
ADMIN_CREDIT_AMOUNT=20.00      # Créditos adicionados pelo código

# Mercado Pago (opcional)
MERCADOPAGO_ACCESS_TOKEN=seu_token_aqui
MERCADOPAGO_PUBLIC_KEY=sua_chave_publica_aqui
```

## 🎮 Modos de Operação

### 1. Modo Demo (sem hardware)
```bash
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=false
```
Interface web completa, sem reprodução real de músicas.

### 2. Modo PC/Linux (com YouTube)
```bash
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=true
```
Reproduz músicas do YouTube, sem hardware de pagamento.

### 3. Modo Produção (Raspberry Pi)
```bash
HARDWARE_ENABLED=true
YOUTUBE_ENABLED=true
```
Funcionamento completo com GPIO e aceitador de notas.

## 🐛 Problemas Conhecidos

Nenhum problema conhecido nesta versão.

## 🔄 Changelog

### v2.3.0 (2024-10-29)
- ✅ Build profissional com PyInstaller
- ✅ Instalador Debian (.deb) completo
- ✅ Sistema de código de operador
- ✅ Música ambiente automática
- ✅ Navegação completa por teclado
- ✅ Suporte a PC/Linux sem Raspberry Pi
- ✅ Bloqueio avançado de anúncios
- ✅ Interface web moderna e responsiva
- ✅ API REST protegida por token
- ✅ Integração com Mercado Pago

## 📖 Documentação

- [README principal](../README.md) - Visão geral e features
- [BUILD.md](../BUILD.md) - Compilar do código fonte
- [INSTALLER.md](../INSTALLER.md) - Guia de instaladores
- [API.md](../API.md) - Documentação da API REST
- [QUICKSTART_EXECUTABLE.md](../QUICKSTART_EXECUTABLE.md) - Início rápido

## 🌐 Links Úteis

- **Repositório**: https://github.com/godfathercorleone994-wq/Jukebox
- **Demo Online**: https://godfathercorleone994-wq.github.io/Jukebox/
- **Issues**: https://github.com/godfathercorleone994-wq/Jukebox/issues
- **Email**: godfathercorleone994@gmail.com

## 🆘 Suporte

Se encontrar problemas:

1. Verifique a documentação em `/usr/share/doc/jukebox/`
2. Consulte os logs em `/var/log/jukebox/`
3. Abra uma issue no GitHub
4. Entre em contato via email

## 🙏 Agradecimentos

Obrigado por usar o Jukebox Pi Money! Este projeto é desenvolvido com ❤️ para a comunidade.

## 📄 Licença

Ver arquivo [LICENSE](../LICENSE) para detalhes.

---

**Aproveite o Jukebox! 🎵🎉**
