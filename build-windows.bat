@echo off
REM Build script for creating Windows executable of Jukebox
REM This script builds a standalone executable that can run on any Windows system

setlocal enabledelayedexpansion

echo ╔═══════════════════════════════════════════════╗
echo ║  🎵 Jukebox - Build Windows Executable       ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Check if running from project root
if not exist "src\server\app.py" (
    echo ❌ Execute este script do diretório raiz do projeto
    exit /b 1
)

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python não encontrado. Instale Python 3.9 ou superior
    echo 💡 Baixe em: https://www.python.org/downloads/
    exit /b 1
)

REM Create/activate virtual environment
if not exist "venv" (
    echo 📦 Criando ambiente virtual...
    python -m venv venv
)

echo 🔄 Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM Install dependencies (excluding RPi.GPIO for Windows)
echo 📦 Instalando dependências...

REM Create temporary requirements without RPi.GPIO
findstr /v "RPi.GPIO" requirements.txt > %TEMP%\requirements-build.txt
pip install -q -r %TEMP%\requirements-build.txt
del %TEMP%\requirements-build.txt
echo ✅ Dependências instaladas

REM Install PyInstaller
echo 📦 Instalando PyInstaller...
pip install -q pyinstaller

REM Clean previous builds
echo 🧹 Limpando builds anteriores...
if exist "build" rmdir /s /q build
if exist "dist" rmdir /s /q dist

REM Build executable
echo 🔨 Construindo executável...
pyinstaller --clean jukebox.spec

if %errorlevel% equ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════╗
    echo ║  ✅ Build concluído com sucesso!             ║
    echo ╚═══════════════════════════════════════════════╝
    echo.
    echo 📦 Executável criado em: dist\jukebox.exe
    echo.
    echo 📋 Como usar o executável:
    echo.
    echo 1. Copie o executável para onde quiser
    echo    ou mantenha no diretório dist\
    echo.
    echo 2. Crie um arquivo .env no mesmo diretório do executável:
    echo    copy env.example .env
    echo    Edite o .env conforme necessário
    echo.
    echo 3. Execute o jukebox:
    echo    dist\jukebox.exe
    echo.
    echo 4. Acesse no navegador:
    echo    http://localhost:5000
    echo.
    echo 💡 Dicas:
    echo    • O executável inclui todas as dependências Python
    echo    • Funciona em Windows 7/8/10/11 (x64)
    echo    • Não requer instalação de Python
    echo    • Tamanho aproximado: ~80-100MB
    echo.
    echo 📦 Para distribuir:
    echo    Compacte o diretório dist\ inteiro em um arquivo ZIP
    echo.
) else (
    echo ❌ Erro durante o build
    exit /b 1
)
