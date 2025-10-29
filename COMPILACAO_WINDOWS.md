# 🪟 Guia Completo de Compilação para Windows

Este guia explica como compilar o Jukebox Pi Money para Windows, criando um executável standalone e um instalador profissional usando Inno Setup.

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Pré-requisitos](#pré-requisitos)
3. [Compilação Rápida](#compilação-rápida)
4. [Compilação Passo a Passo](#compilação-passo-a-passo)
5. [Opções Avançadas](#opções-avançadas)
6. [Estrutura de Arquivos](#estrutura-de-arquivos)
7. [Solução de Problemas](#solução-de-problemas)
8. [Distribuição](#distribuição)

## 🎯 Visão Geral

O processo de compilação para Windows gera dois tipos de arquivos:

1. **Executável Standalone** (`jukebox.exe`)
   - Arquivo único que contém todas as dependências
   - Tamanho: ~80-100 MB
   - Portátil, não requer instalação
   - Ideal para usuários avançados

2. **Instalador Profissional** (`jukebox-setup-windows-x64.exe`)
   - Instalador criado com Inno Setup
   - Assistente de instalação com interface gráfica
   - Cria atalhos automáticos no Desktop e Menu Iniciar
   - Inclui desinstalador integrado
   - Ideal para usuários finais

## 🛠️ Pré-requisitos

### Software Necessário

#### 1. Python 3.9 ou Superior

Baixe e instale o Python:
- **Site oficial**: https://www.python.org/downloads/
- **Versões testadas**: 3.9, 3.10, 3.11, 3.12

**Durante a instalação:**
- ✅ Marque "Add Python to PATH"
- ✅ Marque "Install pip"

**Verificar instalação:**
```cmd
python --version
pip --version
```

#### 2. Inno Setup 6.0 ou Superior (Opcional - Apenas para Instalador)

Necessário apenas se você quiser criar o instalador profissional.

- **Site oficial**: https://jrsoftware.org/isinfo.php
- **Download direto**: https://jrsoftware.org/download.php/is.exe
- **Versão recomendada**: Inno Setup 6.2.2 ou superior

**Instalação:**
1. Execute o instalador baixado
2. Siga o assistente com as opções padrão
3. O instalador será colocado em `C:\Program Files (x86)\Inno Setup 6\`

**Verificar instalação:**
```cmd
dir "C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
```

### Hardware Recomendado

- **RAM**: 4 GB mínimo, 8 GB recomendado
- **Disco**: 2 GB de espaço livre
- **Processador**: Qualquer processador x64 moderno

## 🚀 Compilação Rápida

### Método 1: Script Unificado (Recomendado)

Use o novo script `compile-windows.bat` que faz tudo automaticamente:

```cmd
REM Clone o repositório (se ainda não tiver)
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

REM Compile tudo (executável + instalador)
compile-windows.bat
```

**Resultado:**
- Executável em: `dist\jukebox.exe`
- Instalador em: `installers\jukebox-setup-windows-x64.exe`

### Método 2: Scripts Separados

Se preferir usar os scripts individuais:

```cmd
REM Passo 1: Compilar o executável
build-windows.bat

REM Passo 2: Criar o instalador
build-windows-installer.bat
```

## 📖 Compilação Passo a Passo

### Passo 1: Preparar o Ambiente

```cmd
REM 1. Clone o repositório
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

REM 2. Verifique que os arquivos essenciais existem
dir src\server\app.py
dir requirements.txt
dir jukebox.spec
```

### Passo 2: Compilar o Executável

O script `compile-windows.bat` faz automaticamente:

1. ✅ Cria um ambiente virtual Python
2. ✅ Instala todas as dependências necessárias (exceto RPi.GPIO)
3. ✅ Instala PyInstaller
4. ✅ Compila o projeto usando PyInstaller
5. ✅ Gera o executável em `dist\jukebox.exe`

**Comando:**
```cmd
compile-windows.bat
```

**Ou apenas o executável:**
```cmd
compile-windows.bat --exe-only
```

**Tempo estimado:** 5-10 minutos (dependendo da velocidade do computador)

### Passo 3: Criar o Instalador (Opcional)

Se você tem o Inno Setup instalado:

```cmd
REM Se já compilou o executável antes
compile-windows.bat --installer-only

REM Ou compile tudo junto
compile-windows.bat
```

**Tempo estimado:** 1-2 minutos

### Passo 4: Testar o Resultado

#### Testar o Executável:

```cmd
REM 1. Navegue até o diretório dist
cd dist

REM 2. Copie o arquivo de exemplo de configuração
copy ..\env.example .env

REM 3. Edite o .env com suas configurações
notepad .env

REM 4. Execute o Jukebox
jukebox.exe

REM 5. Acesse no navegador
REM http://localhost:5000
```

#### Testar o Instalador:

```cmd
REM 1. Execute o instalador
installers\jukebox-setup-windows-x64.exe

REM 2. Siga o assistente de instalação

REM 3. Use o atalho criado no Desktop ou Menu Iniciar

REM 4. Acesse no navegador
REM http://localhost:5000
```

## ⚙️ Opções Avançadas

### Opções do Script compile-windows.bat

```cmd
REM Compilação completa (padrão)
compile-windows.bat

REM Apenas executável
compile-windows.bat --exe-only

REM Apenas instalador (requer executável já compilado)
compile-windows.bat --installer-only

REM Limpar tudo e recompilar do zero
compile-windows.bat --clean

REM Ver ajuda
compile-windows.bat --help
```

### Personalizar a Compilação

#### Modificar a Versão

Edite os seguintes arquivos para mudar a versão:

**1. setup.py:**
```python
version="2.3.0",  # ← Mude aqui
```

**2. installer-windows.iss:**
```iss
#define MyAppVersion "2.3.0"  // ← Mude aqui
```

**3. compile-windows.bat:**
```batch
set "APP_VERSION=2.3.0"  REM ← Mude aqui
```

#### Adicionar Arquivos ao Instalador

Edite `installer-windows.iss` na seção `[Files]`:

```iss
[Files]
Source: "dist\{#MyAppExeName}"; DestDir: "{app}"; Flags: ignoreversion
Source: "meu_arquivo.txt"; DestDir: "{app}"; Flags: ignoreversion
Source: "minha_pasta\*"; DestDir: "{app}\pasta"; Flags: ignoreversion recursesubdirs
```

#### Adicionar Ícone Customizado

1. Crie um arquivo `icon.ico` (256x256 recomendado)
2. Edite `installer-windows.iss`:

```iss
[Setup]
SetupIconFile=icon.ico
```

3. Edite `jukebox.spec`:

```python
exe = EXE(
    ...
    icon='icon.ico',
)
```

#### Modificar Dependências

Edite `requirements.txt` para adicionar ou remover dependências:

```txt
flask==3.0.0
flask-cors==4.0.0
# Adicione suas dependências aqui
```

## 📁 Estrutura de Arquivos

### Antes da Compilação

```
Jukebox/
├── src/
│   ├── server/
│   │   ├── app.py              ← Arquivo principal
│   │   ├── config.py
│   │   └── static/
│   ├── db/
│   ├── hardware/
│   ├── payments/
│   └── youtube/
├── requirements.txt             ← Dependências
├── jukebox.spec                 ← Config PyInstaller
├── installer-windows.iss        ← Config Inno Setup
├── compile-windows.bat          ← Script principal ✨
├── build-windows.bat            ← Script de exe
└── build-windows-installer.bat  ← Script de instalador
```

### Depois da Compilação

```
Jukebox/
├── venv/                        ← Ambiente virtual (criado)
├── build/                       ← Arquivos temporários (criado)
├── dist/                        ← Executável (criado)
│   └── jukebox.exe             ← ~80-100 MB
└── installers/                  ← Instalador (criado)
    └── jukebox-setup-windows-x64.exe  ← ~80-100 MB
```

## 🐛 Solução de Problemas

### Erro: "Python não encontrado"

**Problema:** Python não está instalado ou não está no PATH.

**Solução:**
```cmd
REM Verificar se Python está instalado
python --version

REM Se não estiver, baixe e instale:
REM https://www.python.org/downloads/
REM Importante: Marque "Add Python to PATH" durante instalação
```

### Erro: "Inno Setup não encontrado"

**Problema:** Inno Setup não está instalado ou não está no caminho padrão.

**Solução:**
```cmd
REM Opção 1: Instale o Inno Setup
REM https://jrsoftware.org/isinfo.php

REM Opção 2: Compile apenas o executável
compile-windows.bat --exe-only

REM Opção 3: Se instalou em local diferente, edite compile-windows.bat
REM e mude a linha:
REM set "INNO_PATH=C:\Seu\Caminho\ISCC.exe"
```

### Erro: "src\server\app.py não encontrado"

**Problema:** Script executado do diretório errado.

**Solução:**
```cmd
REM Navegue até o diretório raiz do projeto
cd C:\Caminho\Para\Jukebox

REM Verifique que está no lugar certo
dir src\server\app.py

REM Execute o script
compile-windows.bat
```

### Erro: "Falha ao instalar dependências"

**Problema:** Problema com pip ou dependências conflitantes.

**Solução:**
```cmd
REM 1. Limpe o ambiente
compile-windows.bat --clean

REM 2. Atualize pip
python -m pip install --upgrade pip

REM 3. Tente novamente
compile-windows.bat
```

### Erro: "Executável não funciona"

**Problema:** Falta arquivo .env ou configuração incorreta.

**Solução:**
```cmd
REM 1. Navegue até o diretório do executável
cd dist

REM 2. Crie arquivo .env
copy ..\env.example .env

REM 3. Edite o .env
notepad .env

REM Configure ao menos:
REM SECRET_KEY=seu_secret_key_aleatorio_aqui
REM FLASK_ENV=production

REM 4. Execute novamente
jukebox.exe
```

### Erro: "Import Error" ao executar

**Problema:** Módulo não foi incluído no executável.

**Solução:**

Edite `jukebox.spec` e adicione o módulo em `hiddenimports`:

```python
hiddenimports = [
    'flask',
    'flask_cors',
    # ... outros módulos ...
    'seu_modulo_aqui',  # ← Adicione aqui
]
```

Recompile:
```cmd
compile-windows.bat --clean
```

### Erro: Antivírus bloqueia o executável

**Problema:** Falso positivo do antivírus.

**Solução:**
1. Adicione exceção no antivírus para o arquivo `jukebox.exe`
2. Ou assine digitalmente o executável (para distribuição profissional)

### Compilação muito lenta

**Problema:** PyInstaller pode ser lento em máquinas antigas.

**Solução:**
- Feche outros programas
- Tenha pelo menos 4 GB de RAM livre
- Use SSD se possível
- Aguarde pacientemente (primeira compilação pode levar 10+ minutos)

## 📦 Distribuição

### Opção 1: GitHub Releases (Recomendado)

```cmd
REM 1. Compile os arquivos
compile-windows.bat

REM 2. Crie uma release no GitHub
REM 3. Faça upload dos arquivos:
REM    - installers\jukebox-setup-windows-x64.exe
REM    - dist\jukebox.exe (opcionalmente)
```

### Opção 2: Compactação ZIP

```cmd
REM Para o executável standalone
powershell Compress-Archive -Path dist\* -DestinationPath jukebox-windows-x64.zip

REM Para o instalador (já é um único arquivo)
REM Apenas envie: installers\jukebox-setup-windows-x64.exe
```

### Opção 3: Hospedagem Direta

- Upload para Google Drive, Dropbox, OneDrive
- Ou servidor web próprio
- Compartilhe o link de download

### Checklist de Distribuição

Antes de distribuir, verifique:

- [ ] Testou o executável em uma máquina limpa (sem Python instalado)
- [ ] Testou o instalador do início ao fim
- [ ] Arquivo .env.example está incluído
- [ ] Documentação (README.md) está incluída
- [ ] Versão está correta em todos os arquivos
- [ ] Licença (LICENSE) está incluída
- [ ] Testou em Windows 10 e/ou Windows 11

## 📚 Arquivos de Configuração

### jukebox.spec

Configuração do PyInstaller. Define:
- Arquivo principal (app.py)
- Dependências a incluir
- Arquivos de dados (static, templates)
- Opções de compilação

### installer-windows.iss

Configuração do Inno Setup. Define:
- Informações do aplicativo
- Arquivos a instalar
- Atalhos a criar
- Assistente de configuração
- Scripts de pós-instalação

### requirements.txt

Lista de dependências Python necessárias para o projeto.

## 🔗 Links Úteis

- **Inno Setup**: https://jrsoftware.org/isinfo.php
- **PyInstaller**: https://pyinstaller.org/
- **Python**: https://www.python.org/
- **Documentação do Projeto**: 
  - [README.md](README.md) - Documentação principal
  - [INSTALLER.md](INSTALLER.md) - Guia de instaladores
  - [BUILD.md](BUILD.md) - Build multi-plataforma

## 💡 Dicas

### Para Desenvolvedores

1. **Use `--clean` regularmente** para evitar problemas de cache:
   ```cmd
   compile-windows.bat --clean
   ```

2. **Teste em máquina virtual** antes de distribuir

3. **Mantenha requirements.txt atualizado** com versões fixas:
   ```txt
   flask==3.0.0  # ← Use versões específicas
   ```

4. **Versione corretamente** seguindo semver (X.Y.Z)

### Para Usuários Finais

1. **Instalador é mais fácil** que o executável standalone
2. **Não precisa instalar Python** - tudo está incluído
3. **Use o .env** para configurar sem recompilar
4. **Leia QUICKSTART_EXECUTABLE.md** após instalar

## 🆘 Suporte

Se encontrar problemas:

1. **Consulte esta documentação** primeiro
2. **Verifique os logs** em `logs/jukebox.log`
3. **Veja Issues no GitHub**: https://github.com/godfathercorleone994-wq/Jukebox/issues
4. **Abra uma nova Issue** se necessário
5. **Entre em contato**: godfathercorleone994@gmail.com

## 🎉 Conclusão

Agora você sabe como:
- ✅ Compilar o executável Windows
- ✅ Criar instalador profissional com Inno Setup
- ✅ Personalizar a compilação
- ✅ Resolver problemas comuns
- ✅ Distribuir para usuários finais

**Boa compilação! 🚀**

---

**Desenvolvido com ❤️ para a comunidade Jukebox Pi Money**
