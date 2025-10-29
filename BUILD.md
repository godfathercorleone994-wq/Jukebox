# 📦 Guia de Criação de Executáveis

Este guia explica como criar executáveis standalone do Jukebox para Linux e Windows.

## 🎯 Visão Geral

Os executáveis criados são aplicações standalone que incluem:
- ✅ Python runtime embutido
- ✅ Todas as dependências Python
- ✅ Arquivos estáticos (HTML, CSS, JS)
- ✅ Configurações padrão
- ✅ Não requer instalação de Python no sistema alvo

## 📋 Pré-requisitos

### Para Build Linux
- Sistema operacional: Linux (qualquer distribuição moderna)
- Python 3.9 ou superior instalado
- Acesso à internet para baixar dependências

### Para Build Windows
- Sistema operacional: Windows 7/8/10/11
- Python 3.9 ou superior instalado
- Acesso à internet para baixar dependências

## 🔨 Construindo o Executável Linux

### Passo 1: Prepare o ambiente

```bash
# Clone o repositório (se ainda não tiver)
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox
```

### Passo 2: Execute o script de build

```bash
# Torne o script executável
chmod +x build-linux.sh

# Execute o build
./build-linux.sh
```

### Passo 3: Aguarde a conclusão

O processo de build pode levar alguns minutos. Você verá:
- Criação do ambiente virtual
- Instalação de dependências
- Construção do executável com PyInstaller

### Passo 4: Localize o executável

O executável será criado em:
```
dist/jukebox
```

### Tamanho aproximado
- Executável: ~80-100 MB (inclui Python runtime + todas as dependências)

## 🔨 Construindo o Executável Windows

### Método 1: Script Unificado (Recomendado - Novo!)

Use o novo script `compile-windows.bat` que compila o executável e cria o instalador Inno Setup:

```cmd
REM Clone o repositório (se ainda não tiver)
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox

REM Compile tudo (executável + instalador)
compile-windows.bat

REM Ou compile apenas o executável
compile-windows.bat --exe-only

REM Ou limpe tudo e recompile
compile-windows.bat --clean
```

📖 **Guia completo em português**: [COMPILACAO_WINDOWS.md](COMPILACAO_WINDOWS.md)

### Método 2: Scripts Separados

#### Passo 1: Prepare o ambiente

```cmd
REM Clone o repositório (se ainda não tiver)
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox
```

#### Passo 2: Execute o script de build

```cmd
REM Execute o build do executável
build-windows.bat
```

#### Passo 3: Aguarde a conclusão

O processo de build pode levar alguns minutos. Você verá:
- Criação do ambiente virtual
- Instalação de dependências
- Construção do executável com PyInstaller

#### Passo 4: (Opcional) Crie o instalador

```cmd
REM Crie o instalador profissional com Inno Setup
build-windows-installer.bat
```

#### Passo 5: Localize os arquivos

Os arquivos serão criados em:
```
dist\jukebox.exe                           (executável)
installers\jukebox-setup-windows-x64.exe   (instalador)
```

### Tamanho aproximado
- Executável: ~80-100 MB (inclui Python runtime + todas as dependências)
- Instalador: ~80-100 MB (inclui o executável + arquivos de configuração)

## 🚀 Usando o Executável

### Linux

1. **Copie o executável** para onde quiser:
   ```bash
   # Opção 1: Instalar globalmente
   sudo cp dist/jukebox /usr/local/bin/
   
   # Opção 2: Manter no diretório atual
   cp dist/jukebox ~/jukebox/
   ```

2. **Crie um arquivo .env** no mesmo diretório:
   ```bash
   cp env.example .env
   nano .env  # Edite conforme necessário
   ```

3. **Execute o jukebox**:
   ```bash
   # Se instalou globalmente
   jukebox
   
   # Se está no diretório
   ./jukebox
   ```

4. **Acesse** no navegador:
   ```
   http://localhost:5000
   ```

### Windows

1. **Copie o executável** para onde quiser:
   ```
   dist\jukebox.exe
   ```

2. **Crie um arquivo .env** no mesmo diretório:
   ```cmd
   copy env.example .env
   notepad .env  REM Edite conforme necessário
   ```

3. **Execute o jukebox**:
   - Duplo clique em `jukebox.exe`
   - Ou via linha de comando: `jukebox.exe`

4. **Acesse** no navegador:
   ```
   http://localhost:5000
   ```

## 📦 Distribuindo o Executável

### Linux

Crie um arquivo tar.gz com o executável:

```bash
# Criar arquivo compactado
tar -czf jukebox-linux-x64.tar.gz -C dist jukebox

# Ou incluir também o .env.example
tar -czf jukebox-linux-x64.tar.gz -C dist jukebox ../env.example
```

### Windows

Crie um arquivo ZIP com o executável:

1. Selecione `dist/jukebox.exe` e `env.example`
2. Clique com botão direito → "Enviar para" → "Pasta compactada"
3. Renomeie para `jukebox-windows-x64.zip`

## 🔧 Configuração do .env

O arquivo `.env` deve estar no **mesmo diretório** do executável. Principais configurações:

```bash
# Flask
FLASK_ENV=production
SECRET_KEY=sua_chave_secreta_aqui

# Hardware (desabilitar para PC)
HARDWARE_ENABLED=false

# YouTube (opcional)
YOUTUBE_ENABLED=false

# Pagamentos
PAYMENT_PROVIDER=mercadopago
PAYMENT_API_KEY=sua_api_key
PAYMENT_ACCESS_TOKEN=seu_token

# Negócio
PRICE_PER_SONG=5.00
CREDIT_CARD_FEE=3.99
PIX_FEE=0.00

# Admin (código de operador)
ADMIN_ENABLED=true
ADMIN_CODE=seu_codigo_secreto
ADMIN_CREDIT_AMOUNT=20.00
```

## ⚙️ Recursos Avançados

### Build com ícone customizado (Linux)

Edite `jukebox.spec` e adicione:

```python
exe = EXE(
    # ... outras opções ...
    icon='icon.ico',  # Adicione seu ícone aqui
)
```

### Build com ícone customizado (Windows)

Mesma configuração no `jukebox.spec`:

```python
exe = EXE(
    # ... outras opções ...
    icon='icon.ico',  # Adicione seu ícone aqui
)
```

### Build otimizado (menor tamanho)

Para reduzir o tamanho do executável, edite `jukebox.spec`:

```python
# Desabilitar UPX compression (pode aumentar velocidade de inicialização)
exe = EXE(
    # ... outras opções ...
    upx=False,
)
```

### Excluir módulos não utilizados

Em `jukebox.spec`, adicione à lista `excludes`:

```python
a = Analysis(
    # ... outras opções ...
    excludes=['tkinter', 'matplotlib', 'numpy'],  # Módulos não usados
)
```

## 🐛 Resolução de Problemas

### Erro: "PyInstaller not found"

```bash
# Instale manualmente
pip install pyinstaller
```

### Erro: "Failed to execute script"

1. Verifique se o arquivo `.env` está no mesmo diretório do executável
2. Execute o executável via terminal para ver mensagens de erro detalhadas:
   ```bash
   # Linux
   ./jukebox
   
   # Windows
   jukebox.exe
   ```

### Executável muito grande

O tamanho é normal (80-100MB) pois inclui:
- Python runtime completo
- Todas as bibliotecas (Flask, Selenium, etc.)
- ChromeDriver (se incluído)

Para reduzir:
1. Remova dependências não utilizadas do `requirements.txt`
2. Desabilite UPX compression no `.spec`
3. Use `excludes` para módulos não necessários

### Erro de permissão (Linux)

```bash
# Torne o executável executável
chmod +x jukebox
```

### Windows Defender bloqueia o executável

Isso é comum com executáveis criados pelo PyInstaller. Soluções:

1. Adicione exceção no Windows Defender
2. Assine digitalmente o executável (para distribuição profissional)
3. Comprove que não é malware (publique hash SHA256)

### Erro "No module named 'src'"

O executável precisa encontrar os módulos. Certifique-se de que:
1. O build foi feito a partir do diretório raiz
2. O `jukebox.spec` inclui todos os `datas` necessários

## 📊 Comparação: Executável vs Script Python

| Característica | Executável | Script Python |
|----------------|------------|---------------|
| Requer Python instalado | ❌ Não | ✅ Sim |
| Tamanho | ~80-100 MB | ~2 MB |
| Velocidade de inicialização | Mais lento | Mais rápido |
| Fácil de distribuir | ✅ Muito | Médio |
| Fácil de atualizar | Médio | ✅ Muito |
| Debugging | Difícil | ✅ Fácil |

## 🎯 Quando usar cada opção?

### Use Executável quando:
- ✅ Distribuir para usuários finais sem conhecimento técnico
- ✅ Sistema alvo não tem Python instalado
- ✅ Quer simplificar instalação
- ✅ Precisa de instalador profissional

### Use Script Python quando:
- ✅ Desenvolvimento ativo
- ✅ Sistema alvo tem Python
- ✅ Precisa de atualizações frequentes
- ✅ Debugging e manutenção facilitada

## 📚 Recursos Adicionais

- [Documentação PyInstaller](https://pyinstaller.readthedocs.io/)
- [Guia de Deploy](DEPLOY.md)
- [Documentação da API](API.md)
- [README principal](README.md)

## 🆘 Suporte

Se encontrar problemas:
1. Verifique a seção de troubleshooting acima
2. Consulte os logs em `logs/jukebox.log`
3. Abra uma issue no GitHub com:
   - Sistema operacional e versão
   - Versão do Python
   - Mensagem de erro completa
   - Passos para reproduzir

---

**Desenvolvido com ❤️ para facilitar a distribuição do Jukebox**
