# 🔄 Fluxo de Build dos Executáveis

```
┌─────────────────────────────────────────────────────────────────┐
│                     CÓDIGO FONTE JUKEBOX                        │
│                   (Python Flask Application)                    │
└────────────────────┬────────────────────────────────────────────┘
                     │
                     ├───────────────┬───────────────┐
                     │               │               │
                     ▼               ▼               ▼
            ┌────────────┐  ┌────────────┐  ┌────────────┐
            │   Linux    │  │  Windows   │  │   Script   │
            │   Build    │  │   Build    │  │   Python   │
            │            │  │            │  │  (Atual)   │
            └─────┬──────┘  └─────┬──────┘  └─────┬──────┘
                  │               │               │
                  │               │               │
        ┌─────────▼─────────┐     │     ┌─────────▼─────────┐
        │ build-linux.sh    │     │     │  Requer Python    │
        │                   │     │     │  + pip install    │
        │ • Detecta SO      │     │     │  + venv           │
        │ • Cria venv       │     │     └───────────────────┘
        │ • Instala deps    │     │
        │ • PyInstaller     │     │
        └─────────┬─────────┘     │
                  │               │
                  │     ┌─────────▼─────────┐
                  │     │ build-windows.bat │
                  │     │                   │
                  │     │ • Verifica Python │
                  │     │ • Cria venv       │
                  │     │ • Instala deps    │
                  │     │ • PyInstaller     │
                  │     └─────────┬─────────┘
                  │               │
                  ▼               ▼
        ┌───────────────┐   ┌───────────────┐
        │  dist/jukebox │   │dist/jukebox.exe│
        │   (30-80 MB)  │   │  (80-100 MB)  │
        │               │   │               │
        │ ELF 64-bit    │   │  PE32+ x64    │
        │ Standalone    │   │  Standalone   │
        └───────┬───────┘   └───────┬───────┘
                │                   │
                └─────────┬─────────┘
                          │
                          ▼
           ┌──────────────────────────┐
           │   EXECUTÁVEIS PRONTOS    │
           │                          │
           │  ✅ Sem Python           │
           │  ✅ Sem dependências     │
           │  ✅ Arquivo único        │
           │  ✅ Pronto p/ distribuir │
           └──────────────────────────┘
```

## 📦 Componentes do Build

### Entrada
```
src/
├── server/
│   ├── app.py          (Entry point)
│   ├── config.py
│   └── static/
├── db/
├── hardware/
├── payments/
└── youtube/

requirements.txt
jukebox.spec           (Configuração PyInstaller)
```

### Processo
```
1. Análise de Dependências
   └─> PyInstaller detecta imports

2. Coleta de Arquivos
   └─> Static files, templates, configs

3. Empacotamento
   └─> Python runtime + libs + código

4. Compilação
   └─> Executável nativo
```

### Saída
```
dist/
├── jukebox           (Linux)
│   └─> 30-80 MB
│
└── jukebox.exe       (Windows)
    └─> 80-100 MB

Conteúdo incluído:
• Python 3.11 runtime
• Flask + Flask-CORS
• Selenium + WebDriver
• Mercadopago SDK
• SQLite
• Todos os módulos src/
• Arquivos static/
• Templates HTML
```

## 🤖 GitHub Actions Workflow

```
┌─────────────────────────────────────────────────────────────┐
│                     Git Tag Push (v*)                       │
│                    git push origin v2.3.0                   │
└──────────────────────┬──────────────────────────────────────┘
                       │
                       ▼
┌──────────────────────────────────────────────────────────────┐
│              GitHub Actions Workflow Trigger                 │
│           (.github/workflows/build-executables.yml)          │
└──────────────┬───────────────────────────┬───────────────────┘
               │                           │
    ┌──────────▼──────────┐    ┌──────────▼──────────┐
    │   Job: build-linux  │    │ Job: build-windows  │
    │   runs-on: ubuntu   │    │ runs-on: windows    │
    │                     │    │                     │
    │ 1. Checkout code    │    │ 1. Checkout code    │
    │ 2. Setup Python     │    │ 2. Setup Python     │
    │ 3. Run build script │    │ 3. Run build script │
    │ 4. Create tarball   │    │ 4. Create zip       │
    │ 5. Upload artifact  │    │ 5. Upload artifact  │
    └──────────┬──────────┘    └──────────┬──────────┘
               │                           │
               └─────────┬─────────────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   Job: release       │
              │   runs-on: ubuntu    │
              │                      │
              │ 1. Download artifacts│
              │ 2. Create release    │
              │ 3. Upload files      │
              └──────────┬───────────┘
                         │
                         ▼
              ┌──────────────────────┐
              │   GitHub Release     │
              │                      │
              │ • jukebox-linux.tgz  │
              │ • jukebox-windows.zip│
              │ • env.example        │
              │ • QUICKSTART_*.md    │
              └──────────────────────┘
```

## 👥 Fluxo do Usuário

### Opção 1: Desenvolvedor (Build Local)

```
┌──────────────┐
│ Git Clone    │
└──────┬───────┘
       │
       ▼
┌──────────────┐    ┌──────────────┐
│ Linux:       │ OU │ Windows:     │
│ ./build-     │    │ build-       │
│ linux.sh     │    │ windows.bat  │
└──────┬───────┘    └──────┬───────┘
       │                   │
       └─────────┬─────────┘
                 │
                 ▼
         ┌──────────────┐
         │ Executável   │
         │ em dist/     │
         └──────┬───────┘
                │
                ▼
         ┌──────────────┐
         │ ./jukebox    │
         │ ou           │
         │ jukebox.exe  │
         └──────────────┘
```

### Opção 2: Usuário Final (Download de Release)

```
┌──────────────────┐
│ GitHub Releases  │
└────────┬─────────┘
         │
         ▼
┌─────────────────────┐
│ Download executável │
│ (.tar.gz ou .zip)   │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Extrair arquivo     │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Configurar .env     │
│ (copiar env.example)│
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Executar jukebox    │
└────────┬────────────┘
         │
         ▼
┌─────────────────────┐
│ Acessar navegador   │
│ localhost:5000      │
└─────────────────────┘
```

## 📊 Comparação de Métodos

```
╔══════════════╦═══════════════╦═══════════════╦═══════════════╗
║   Método     ║  Executável   ║   Script      ║    Docker     ║
║              ║   Standalone  ║   Python      ║   Container   ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Python       ║      ❌       ║      ✅       ║      ❌       ║
║ Requerido    ║      Não      ║      Sim      ║      Não      ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Tamanho      ║   80-100 MB   ║    ~2 MB      ║   ~500 MB     ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Instalação   ║   Descompactar║  pip install  ║ docker pull   ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Atualização  ║    Média      ║   Fácil       ║    Fácil      ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Debug        ║    Difícil    ║   Fácil       ║    Média      ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Distribuição ║   Muito Fácil ║   Média       ║    Fácil      ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Performance  ║     Boa       ║   Ótima       ║    Boa        ║
╠══════════════╬═══════════════╬═══════════════╬═══════════════╣
║ Uso Ideal    ║  Usuários     ║Desenvolvedores║   Produção    ║
║              ║   Finais      ║               ║   Cloud       ║
╚══════════════╩═══════════════╩═══════════════╩═══════════════╝
```

## 🎯 Casos de Uso

### Caso 1: Cliente sem conhecimento técnico
```
Usuário: "Quero rodar o Jukebox no meu PC"

Solução: Executável Standalone ✅
• Download do executável
• Configuração simples do .env
• Executar e pronto!

❌ NÃO: Script Python (requer conhecimento técnico)
```

### Caso 2: Desenvolvedor fazendo testes
```
Desenvolvedor: "Preciso testar mudanças rápidas"

Solução: Script Python ✅
• git pull
• pip install
• python app.py

❌ NÃO: Executável (lento para iterar)
```

### Caso 3: Deploy em produção (Raspberry Pi)
```
Produção: "Preciso instalar em múltiplos dispositivos"

Solução: Script Python com systemd ✅
• Clone do repo
• Script start.sh
• Systemd service
• Fácil atualizar (git pull)

⚠️  TALVEZ: Executável (menos flexível)
```

### Caso 4: Demonstração para cliente
```
Vendedor: "Preciso demonstrar o produto"

Solução: Executável Standalone ✅
• Leva executável em pendrive
• Executa em qualquer PC
• Sem dependências

✅ TAMBÉM BOM: GitHub Pages (demo online)
```

---

**Este diagrama ajuda a visualizar todo o processo de build e distribuição**
