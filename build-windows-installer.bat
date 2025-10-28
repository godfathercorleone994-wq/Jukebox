@echo off
REM Build script for creating Windows installer (.exe with Inno Setup)
REM Requires Inno Setup 6.0 or later installed: https://jrsoftware.org/isinfo.php

setlocal enabledelayedexpansion

echo ╔═══════════════════════════════════════════════╗
echo ║  🎵 Jukebox - Build Windows Installer        ║
echo ╚═══════════════════════════════════════════════╝
echo.

REM Check if running from project root
if not exist "src\server\app.py" (
    echo ❌ Execute este script do diretório raiz do projeto
    exit /b 1
)

REM Check if executable exists
if not exist "dist\jukebox.exe" (
    echo ⚠️ Executável não encontrado. Construindo...
    call build-windows.bat
)

if not exist "dist\jukebox.exe" (
    echo ❌ Falha ao construir executável
    exit /b 1
)

REM Check if Inno Setup is installed
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
if not exist "%INNO_PATH%" (
    echo ⚠️ Inno Setup não encontrado em: %INNO_PATH%
    echo.
    echo Tentando localizar Inno Setup...
    
    REM Try alternative paths
    set "INNO_PATH=C:\Program Files\Inno Setup 6\ISCC.exe"
    if not exist "!INNO_PATH!" (
        echo.
        echo ❌ Inno Setup não encontrado!
        echo.
        echo Para criar o instalador, você precisa instalar o Inno Setup:
        echo 💡 Baixe em: https://jrsoftware.org/isinfo.php
        echo.
        echo Após instalar, execute este script novamente.
        exit /b 1
    )
)

echo ✅ Inno Setup encontrado: %INNO_PATH%
echo.

REM Create installers directory
if not exist "installers" mkdir installers

REM Build installer with Inno Setup
echo 🔨 Construindo instalador com Inno Setup...
"%INNO_PATH%" "installer-windows.iss"

if %errorlevel% equ 0 (
    echo.
    echo ╔═══════════════════════════════════════════════╗
    echo ║  ✅ Instalador criado com sucesso!           ║
    echo ╚═══════════════════════════════════════════════╝
    echo.
    echo 📦 Instalador criado em: installers\jukebox-setup-windows-x64.exe
    echo.
    echo 📋 Como distribuir o instalador:
    echo.
    echo 1. Envie o arquivo installers\jukebox-setup-windows-x64.exe
    echo.
    echo 2. Usuários devem apenas executar o instalador
    echo.
    echo 3. O instalador irá:
    echo    • Instalar o Jukebox em Arquivos de Programas
    echo    • Criar atalhos no Menu Iniciar e Desktop
    echo    • Gerar arquivo .env automaticamente
    echo    • Configurar o sistema para uso imediato
    echo.
    echo 💡 Dicas:
    echo    • Instalador inclui interface de configuração
    echo    • Tamanho aproximado: ~80-100MB
    echo    • Suporta instalação por usuário ou sistema
    echo    • Inclui opção de desinstalação no Painel de Controle
    echo.
) else (
    echo ❌ Erro ao criar instalador
    exit /b 1
)
