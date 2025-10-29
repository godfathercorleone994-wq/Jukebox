# 📦 Jukebox Pi Money - Releases

Este diretório contém os builds oficiais do Jukebox Pi Money prontos para instalação.

## 🐧 Download para Kali Linux / Debian / Ubuntu

### Arquivo disponível:
- **jukebox-pi-money_2.3.0_amd64.deb** (29 MB)
  - Versão: 2.3.0
  - Arquitetura: amd64 (x86_64)
  - Compatível com: Kali Linux, Debian, Ubuntu e derivados

## 🚀 Como Instalar no Kali Linux

### Método 1: Download direto do GitHub

```bash
# 1. Clone o repositório ou baixe apenas o arquivo .deb
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox/releases

# Ou baixe direto:
wget https://raw.githubusercontent.com/godfathercorleone994-wq/Jukebox/main/releases/jukebox-pi-money_2.3.0_amd64.deb

# 2. Instale o pacote
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb

# 3. Se houver erros de dependências, corrija com:
sudo apt-get install -f
```

### Método 2: Download do GitHub Releases (quando disponível)

```bash
# Baixe da página de releases
wget https://github.com/godfathercorleone994-wq/Jukebox/releases/latest/download/jukebox-pi-money_2.3.0_amd64.deb

# Instale
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb
```

## ⚙️ Configuração Inicial

Após a instalação, configure o Jukebox:

```bash
# Edite o arquivo de configuração
sudo nano /etc/jukebox/.env
```

Configure pelo menos:
- `SECRET_KEY` - Mude para algo aleatório e secreto
- `HARDWARE_ENABLED` - false (para testes sem hardware)
- `YOUTUBE_ENABLED` - false (para modo demo)
- `ADMIN_CODE` - Código secreto para adicionar créditos (opcional)

## 🎵 Executar o Jukebox

```bash
# Execute o Jukebox
jukebox

# Acesse no navegador
# http://localhost:5000
```

## 📋 O que é instalado?

O pacote .deb instala:
- **Executável**: `/usr/local/bin/jukebox`
- **Configuração**: `/etc/jukebox/.env`
- **Logs**: `/var/log/jukebox/`
- **Dados**: `/var/lib/jukebox/`
- **Documentação**: `/usr/share/doc/jukebox/`

## 🗑️ Desinstalar

```bash
# Remover o pacote (mantém configurações)
sudo dpkg -r jukebox-pi-money

# Remover completamente (incluindo configurações)
sudo dpkg -P jukebox-pi-money
```

## 🔄 Criar uma Nova Release

Para desenvolvedores que querem criar uma nova release:

### Opção 1: Usando GitHub Actions (Recomendado)

1. Crie uma tag com o padrão correto:
```bash
git tag -a v2.3.1 -m "Release v2.3.1"
git push origin v2.3.1
```

ou

```bash
git tag -a Jukebox_py_v2.3.1 -m "Release v2.3.1"
git push origin Jukebox_py_v2.3.1
```

2. O workflow GitHub Actions irá:
   - Construir os executáveis para Linux e Windows
   - Criar os instaladores (.deb e .exe)
   - Publicar automaticamente no GitHub Releases
   - Anexar todos os arquivos necessários

### Opção 2: Build Manual

```bash
# 1. Construir o executável Linux
chmod +x build-linux.sh
./build-linux.sh

# 2. Criar o pacote .deb
chmod +x build-linux-installer.sh
./build-linux-installer.sh

# 3. Copiar para o diretório releases/
cp installers/jukebox-pi-money_2.3.0_amd64.deb releases/

# 4. Commit e push
git add releases/
git commit -m "Add v2.3.0 .deb package"
git push
```

## 📖 Documentação Adicional

- [README principal](../README.md) - Visão geral do projeto
- [BUILD.md](../BUILD.md) - Como construir do código fonte
- [INSTALLER.md](../INSTALLER.md) - Guia completo de instaladores
- [QUICKSTART_EXECUTABLE.md](../QUICKSTART_EXECUTABLE.md) - Guia rápido

## 🆘 Suporte

- **Issues**: https://github.com/godfathercorleone994-wq/Jukebox/issues
- **Email**: godfathercorleone994@gmail.com

## ✨ Características do Jukebox

- 💰 Múltiplos métodos de pagamento (Dinheiro, PIX, Débito, Crédito)
- 🎵 Reproduz músicas do YouTube automaticamente
- 🎧 Música ambiente automática quando em espera
- 🚫 Bloqueio de anúncios integrado
- ⌨️ Navegação completa por teclado
- 🔐 Sistema de código de operador
- 📱 Interface web responsiva e moderna

---

**Desenvolvido com ❤️ para a comunidade**
