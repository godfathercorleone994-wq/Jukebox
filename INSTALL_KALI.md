# 📦 Como Baixar e Instalar o Jukebox no Kali Linux

Este guia mostra como baixar e instalar o Jukebox Pi Money no seu Kali Linux.

## ✅ O que foi feito

Foi criado um pacote Debian (.deb) profissional do Jukebox Pi Money que pode ser instalado diretamente no Kali Linux, Debian, Ubuntu e distribuições derivadas.

### Arquivos Criados:
- ✅ **jukebox-pi-money_2.3.0_amd64.deb** (29 MB) - Pacote Debian pronto para instalar
- ✅ **releases/README.md** - Guia completo de instalação
- ✅ **releases/RELEASE_NOTES.md** - Notas da versão com changelog

## 🚀 Instalação Rápida (3 passos)

### Passo 1: Download

Existem duas formas de baixar:

**Opção A - Download direto (mais rápido):**
```bash
wget https://raw.githubusercontent.com/godfathercorleone994-wq/Jukebox/main/releases/jukebox-pi-money_2.3.0_amd64.deb
```

**Opção B - Clone o repositório:**
```bash
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox/releases
```

### Passo 2: Instalar

```bash
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb
```

Se aparecer algum erro de dependências faltando, corrija com:
```bash
sudo apt-get install -f
```

### Passo 3: Configurar

```bash
sudo nano /etc/jukebox/.env
```

Configurações mínimas necessárias:
```bash
# Mude para algo aleatório e secreto
SECRET_KEY=CHANGE_THIS_TO_RANDOM_SECRET_KEY

# Para testes no Kali Linux (sem hardware real)
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=false

# Preço por música
PRICE_PER_SONG=5.00

# Código de operador (opcional - para adicionar créditos sem pagar)
ADMIN_ENABLED=true
ADMIN_CODE=123456
ADMIN_CREDIT_AMOUNT=20.00
```

## 🎵 Como Usar

### Executar o Jukebox

```bash
jukebox
```

O servidor vai iniciar e você verá uma mensagem como:
```
 * Running on http://127.0.0.1:5000
```

### Acessar no Navegador

Abra seu navegador e acesse:
```
http://localhost:5000
```

### Usar o Código de Operador (se habilitado)

Na interface web, clique várias vezes rápido em um local específico para abrir o campo do código de operador e digite o código configurado (ex: 123456).

## 📋 O que foi instalado?

O pacote .deb instalou os seguintes arquivos no seu sistema:

| Arquivo/Pasta | Local | Descrição |
|--------------|-------|-----------|
| Executável | `/usr/local/bin/jukebox` | Programa principal (30 MB) |
| Configuração | `/etc/jukebox/.env` | Arquivo de configuração |
| Logs | `/var/log/jukebox/` | Arquivos de log |
| Dados | `/var/lib/jukebox/` | Banco de dados SQLite |
| Documentação | `/usr/share/doc/jukebox/` | Manuais e guias |
| Menu | `/usr/share/applications/jukebox.desktop` | Atalho no menu |

## 🔧 Comandos Úteis

### Ver logs
```bash
sudo tail -f /var/log/jukebox/jukebox.log
```

### Parar o Jukebox
```
Ctrl+C no terminal onde está rodando
```

### Reconfigurar
```bash
sudo nano /etc/jukebox/.env
```

### Desinstalar (mantém configurações)
```bash
sudo dpkg -r jukebox-pi-money
```

### Desinstalar completamente (remove tudo)
```bash
sudo dpkg -P jukebox-pi-money
```

### Ver informações do pacote
```bash
dpkg -l | grep jukebox
dpkg -L jukebox-pi-money
```

## 🎮 Modos de Operação

### Modo Demo (Recomendado para testes no Kali)
```bash
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=false
```
- Interface web completa
- Não toca músicas reais (apenas simulação)
- Não precisa de hardware especial
- Ideal para desenvolvimento e testes

### Modo YouTube (Para reproduzir músicas de verdade)
```bash
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=true
```
- Reproduz músicas do YouTube
- Requer Chrome/Chromium instalado
- Requer ChromeDriver instalado
- Usa Selenium para automação

### Modo Produção (Raspberry Pi com hardware)
```bash
HARDWARE_ENABLED=true
YOUTUBE_ENABLED=true
```
- Modo completo com GPIO
- Requer Raspberry Pi
- Requer aceitador de notas conectado

## ✨ Características

- 💰 Múltiplos métodos de pagamento
- 🎵 Reproduz músicas do YouTube
- 🎧 Música ambiente automática
- 🚫 Bloqueio de anúncios
- ⌨️ Navegação por teclado
- 🔐 Código de operador secreto
- 📱 Interface responsiva
- 💾 Banco de dados SQLite
- 🔒 API REST com autenticação

## 🌐 Testar Online (Sem Instalar)

Se quiser apenas testar a interface sem instalar:
https://godfathercorleone994-wq.github.io/Jukebox/

## 🆘 Problemas Comuns

### "dpkg: error processing package"
```bash
sudo apt-get install -f
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb
```

### "Permission denied"
Use `sudo` antes dos comandos de instalação.

### Servidor não inicia
Verifique se a porta 5000 está livre:
```bash
sudo netstat -tlnp | grep :5000
```

### Não consegue acessar no navegador
Verifique se o firewall permite conexões na porta 5000:
```bash
sudo ufw allow 5000
```

## 📖 Documentação Adicional

- [README principal](../README.md) - Visão geral completa
- [BUILD.md](../BUILD.md) - Como construir do código fonte
- [INSTALLER.md](../INSTALLER.md) - Guia de instaladores
- [API.md](../API.md) - Documentação da API REST
- [PC-LINUX.md](../PC-LINUX.md) - Guia para PC/Linux

## 📧 Suporte

- **Issues**: https://github.com/godfathercorleone994-wq/Jukebox/issues
- **Email**: godfathercorleone994@gmail.com

## 🎉 Pronto!

Agora você tem o Jukebox Pi Money instalado e funcionando no seu Kali Linux!

Para iniciar: `jukebox`
Para acessar: `http://localhost:5000`

**Bom teste! 🎵**
