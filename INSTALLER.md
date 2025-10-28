# 📦 Guia de Instaladores do Jukebox

Este guia explica como usar e criar instaladores profissionais do Jukebox para Linux e Windows.

## 🎯 Visão Geral

Existem duas formas de distribuir o Jukebox para usuários finais:

1. **Executáveis Standalone** - Arquivo único, requer configuração manual
2. **Instaladores** - Instala automaticamente, cria atalhos, configura tudo ✨

## 📥 Para Usuários Finais

### 🐧 Linux - Instalador Debian (.deb)

#### Instalação

```bash
# Baixe o instalador do GitHub Releases
wget https://github.com/godfathercorleone994-wq/Jukebox/releases/latest/download/jukebox-pi-money_2.3.0_amd64.deb

# Instale o pacote
sudo dpkg -i jukebox-pi-money_2.3.0_amd64.deb

# Se houver erros de dependências, corrija com:
sudo apt-get install -f
```

#### Configuração

Após a instalação, edite o arquivo de configuração:

```bash
sudo nano /etc/jukebox/.env
```

Configure ao menos:
- `SECRET_KEY` - Mude para algo aleatório e secreto
- `ADMIN_CODE` - Se quiser habilitar código de operador

#### Uso

```bash
# Execute o Jukebox
jukebox

# Acesse no navegador
# http://localhost:5000
```

#### Desinstalação

```bash
# Remover o programa
sudo apt-get remove jukebox-pi-money

# Remover programa e configurações
sudo apt-get purge jukebox-pi-money
```

#### O que o instalador faz:

- ✅ Instala o executável em `/usr/local/bin/jukebox`
- ✅ Cria arquivo de configuração em `/etc/jukebox/.env`
- ✅ Cria diretórios de logs em `/var/log/jukebox/`
- ✅ Cria diretórios de dados em `/var/lib/jukebox/`
- ✅ Instala documentação em `/usr/share/doc/jukebox/`
- ✅ Cria atalho no menu de aplicativos
- ✅ Torna o comando `jukebox` disponível globalmente

### 🪟 Windows - Instalador (.exe)

#### Instalação

1. **Baixe o instalador** do GitHub Releases:
   ```
   jukebox-setup-windows-x64.exe
   ```

2. **Execute o instalador** (duplo clique)

3. **Siga o assistente**:
   - Escolha o diretório de instalação
   - Configure opções básicas:
     - Chave secreta (ou deixe vazio para gerar automaticamente)
     - Habilitar código de operador (sim/não)
     - Código de operador (se habilitou)
   - Escolha criar atalhos (Desktop/Menu Iniciar)

4. **Finalize a instalação**

#### Uso

Após a instalação, você pode:

- **Executar pelo atalho** no Desktop ou Menu Iniciar
- **Ou executar manualmente**:
  ```
  C:\Program Files\Jukebox\jukebox.exe
  ```

- **Acessar no navegador**:
  ```
  http://localhost:5000
  ```

#### Configuração Pós-Instalação

O arquivo `.env` é criado automaticamente em:
```
C:\Program Files\Jukebox\.env
```

Para editar:
```
notepad "C:\Program Files\Jukebox\.env"
```

#### Desinstalação

Use o Painel de Controle ou Configurações do Windows:
- Configurações → Apps → Jukebox Pi Money → Desinstalar

Ou execute:
```
C:\Program Files\Jukebox\unins000.exe
```

#### O que o instalador faz:

- ✅ Instala o executável em `C:\Program Files\Jukebox\`
- ✅ Cria arquivo `.env` com configuração inicial
- ✅ Cria atalhos no Desktop e Menu Iniciar (opcional)
- ✅ Registra no Painel de Controle para desinstalação
- ✅ Inclui documentação completa
- ✅ Interface de configuração durante instalação

## 🔨 Para Desenvolvedores - Criar os Instaladores

### Pré-requisitos

#### Linux
- Sistema Linux (Ubuntu, Debian, etc.)
- Python 3.9+
- Ferramentas de build: `dpkg`, `fakeroot`
- Instalação: `sudo apt-get install dpkg fakeroot`

#### Windows
- Windows 7/8/10/11
- Python 3.9+
- Inno Setup 6.0+: https://jrsoftware.org/isinfo.php

### 🐧 Criar Instalador Linux (.deb)

```bash
# Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

# Execute o script de build do instalador
chmod +x build-linux-installer.sh
./build-linux-installer.sh
```

O instalador será criado em:
```
installers/jukebox-pi-money_2.3.0_amd64.deb
```

### 🪟 Criar Instalador Windows (.exe)

```cmd
REM Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

REM Execute o script de build do instalador
build-windows-installer.bat
```

O instalador será criado em:
```
installers\jukebox-setup-windows-x64.exe
```

## 📦 Estrutura dos Instaladores

### Linux (.deb)

```
jukebox-pi-money_2.3.0_amd64.deb
├── /usr/local/bin/jukebox              # Executável
├── /etc/jukebox/.env                    # Configuração
├── /var/log/jukebox/                    # Logs
├── /var/lib/jukebox/                    # Dados
├── /usr/share/doc/jukebox/              # Documentação
│   ├── README.md
│   ├── BUILD.md
│   ├── QUICKSTART_EXECUTABLE.md
│   └── LICENSE
└── /usr/share/applications/jukebox.desktop  # Atalho
```

### Windows (.exe)

```
jukebox-setup-windows-x64.exe
└── Instalador Inno Setup contendo:
    ├── jukebox.exe                      # Executável
    ├── .env                              # Configuração (gerada)
    ├── README.md                         # Documentação
    ├── QUICKSTART_EXECUTABLE.md
    ├── LICENSE
    └── unins000.exe                      # Desinstalador
```

## 🚀 Fluxo de Release

Para criar uma release completa com executáveis e instaladores:

### 1. Preparar a Release

```bash
# Atualize a versão nos arquivos:
# - setup.py
# - installer-windows.iss
# - debian/DEBIAN/control (em build-linux-installer.sh)
# - build-linux-installer.sh (nome do .deb)

# Commit as mudanças
git add .
git commit -m "Bump version to 2.3.0"
```

### 2. Criar Tag

```bash
# Crie uma tag de versão
git tag -a v2.3.0 -m "Release v2.3.0 - Executáveis e Instaladores"

# Push da tag
git push origin v2.3.0
```

### 3. Build Automático via GitHub Actions

A workflow `.github/workflows/build-executables.yml` será acionada automaticamente e:

- ✅ Construirá executáveis para Linux e Windows
- ✅ Criará arquivos compactados (.tar.gz e .zip)
- ✅ Criará uma release no GitHub
- ✅ Anexará os arquivos à release

### 4. Build Manual dos Instaladores (Opcional)

Se quiser adicionar os instaladores à release:

#### Linux
```bash
./build-linux-installer.sh
# Upload manual: installers/jukebox-pi-money_2.3.0_amd64.deb
```

#### Windows
```cmd
build-windows-installer.bat
REM Upload manual: installers\jukebox-setup-windows-x64.exe
```

## 🔧 Personalização dos Instaladores

### Linux (.deb)

Edite `build-linux-installer.sh`:

```bash
# Mudar versão
cat > "$DEB_DIR/DEBIAN/control" << 'EOF'
Version: 2.4.0  # ← Mude aqui
...
```

Personalize scripts:
- `postinst` - Executado após instalação
- `prerm` - Executado antes de remover
- `postrm` - Executado após remover

### Windows (Inno Setup)

Edite `installer-windows.iss`:

```iss
#define MyAppVersion "2.4.0"  // ← Mude aqui

[Setup]
SetupIconFile=icon.ico  // ← Adicione ícone customizado

[Files]
Source: "meu_arquivo.txt"; DestDir: "{app}"; Flags: ignoreversion  // ← Adicione arquivos

[Code]
// Adicione código Pascal para lógica customizada
```

## 🎨 Adicionar Ícone

### Linux
Adicione um arquivo `icon.png` (48x48 ou 256x256) e modifique o `.desktop`:

```ini
Icon=/usr/share/pixmaps/jukebox.png
```

### Windows
Crie um arquivo `icon.ico` e configure no `installer-windows.iss`:

```iss
SetupIconFile=icon.ico
```

## 📊 Comparação: Executável vs Instalador

| Característica | Executável | Instalador |
|----------------|------------|------------|
| Facilidade de distribuição | Boa | ⭐ Excelente |
| Experiência do usuário | Básica | ⭐ Profissional |
| Configuração automática | ❌ Não | ✅ Sim |
| Atalhos no menu | ❌ Não | ✅ Sim |
| Desinstalação fácil | Difícil | ⭐ Fácil |
| Tamanho do arquivo | ~80-100MB | ~80-100MB |
| Requer privilégios admin | ❌ Não | ✅ Sim (Linux) / Opcional (Windows) |
| Melhor para | Testes, Dev | ⭐ Produção, Usuários Finais |

## 🐛 Resolução de Problemas

### Linux

#### Erro: "dpkg-deb: command not found"
```bash
sudo apt-get install dpkg fakeroot
```

#### Erro: "fakeroot: command not found"
```bash
sudo apt-get install fakeroot
```

#### Erro ao instalar: "dependency problems"
```bash
sudo apt-get install -f
```

### Windows

#### Inno Setup não encontrado
1. Baixe em: https://jrsoftware.org/isinfo.php
2. Instale com opções padrão
3. Execute o script novamente

#### Erro de compilação do instalador
Verifique:
1. Todos os arquivos em `dist/` existem
2. O arquivo `installer-windows.iss` está correto
3. Caminhos dos arquivos estão corretos

### Ambos

#### Executável não funciona após instalação
1. Verifique se o arquivo `.env` foi criado
2. Teste executar manualmente para ver erros
3. Consulte logs do sistema

## 📚 Recursos Adicionais

- [Inno Setup Documentation](https://jrsoftware.org/ishelp/)
- [Debian Packaging Guide](https://www.debian.org/doc/manuals/maint-guide/)
- [PyInstaller Manual](https://pyinstaller.readthedocs.io/)
- [BUILD.md](BUILD.md) - Criação de executáveis
- [README.md](README.md) - Documentação principal

## 🆘 Suporte

Se encontrar problemas:

1. Verifique esta documentação
2. Consulte os logs em:
   - Linux: `/var/log/jukebox/`
   - Windows: `C:\Program Files\Jukebox\logs\`
3. Abra uma issue no GitHub: https://github.com/godfathercorleone994-wq/Jukebox/issues

---

**Desenvolvido com ❤️ para facilitar a distribuição do Jukebox**
