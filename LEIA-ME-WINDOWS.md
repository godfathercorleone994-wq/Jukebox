# 🪟 Script de Compilação Windows - Guia Rápido

## Como Compilar o Jukebox para Windows

### 📦 Opção 1: Compilação Completa (Recomendado)

Compile o executável e crie o instalador profissional em um único comando:

```cmd
compile-windows.bat
```

Este comando irá:
- ✅ Criar o executável standalone (`dist\jukebox.exe`)
- ✅ Criar o instalador Inno Setup (`installers\jukebox-setup-windows-x64.exe`)
- ✅ Instalar todas as dependências automaticamente
- ✅ Configurar tudo que é necessário

### 📋 Pré-requisitos

Antes de executar o script, você precisa ter instalado:

1. **Python 3.9+**: https://www.python.org/downloads/
2. **Inno Setup 6.0+**: https://jrsoftware.org/isinfo.php (apenas para criar o instalador)

### ⚙️ Opções Avançadas

```cmd
REM Compilar apenas o executável (não precisa do Inno Setup)
compile-windows.bat --exe-only

REM Criar apenas o instalador (precisa já ter compilado o executável)
compile-windows.bat --installer-only

REM Limpar tudo e recompilar do zero
compile-windows.bat --clean

REM Ver ajuda completa
compile-windows.bat --help
```

### 📁 Arquivos Gerados

Após a compilação bem-sucedida, você terá:

```
Jukebox/
├── dist/
│   └── jukebox.exe                         (~80-100 MB)
└── installers/
    └── jukebox-setup-windows-x64.exe       (~80-100 MB)
```

### 🚀 Como Usar

**Para testar o executável:**
```cmd
cd dist
copy ..\env.example .env
jukebox.exe
```

**Para instalar usando o instalador:**
```cmd
installers\jukebox-setup-windows-x64.exe
```

### 📚 Documentação Completa

Para informações detalhadas, consulte:

- **[COMPILACAO_WINDOWS.md](COMPILACAO_WINDOWS.md)** - Guia completo em português
- **[BUILD.md](BUILD.md)** - Documentação de build multi-plataforma
- **[INSTALLER.md](INSTALLER.md)** - Guia de instaladores

### 🐛 Problemas?

Se encontrar erros, consulte a seção "Solução de Problemas" em [COMPILACAO_WINDOWS.md](COMPILACAO_WINDOWS.md).

---

**Desenvolvido com ❤️ para a comunidade Jukebox Pi Money**
