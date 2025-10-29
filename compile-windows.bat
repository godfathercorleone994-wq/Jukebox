@echo off
REM ========================================================================
REM Script de Compilação Completa para Windows - Jukebox Pi Money
REM ========================================================================
REM Este script faz a compilação completa do Jukebox para Windows:
REM 1. Verifica e instala dependências
REM 2. Compila o executável standalone com PyInstaller
REM 3. Cria o instalador profissional com Inno Setup
REM
REM Requisitos:
REM - Python 3.9 ou superior
REM - Inno Setup 6.0 ou superior (https://jrsoftware.org/isinfo.php)
REM
REM Uso:
REM   compile-windows.bat [opções]
REM
REM Opções:
REM   --exe-only      Compila apenas o executável
REM   --installer-only Cria apenas o instalador (requer executável já compilado)
REM   --clean         Limpa builds anteriores antes de compilar
REM   --help          Mostra esta mensagem de ajuda
REM ========================================================================

setlocal enabledelayedexpansion

REM ========================================================================
REM Configurações e Variáveis
REM ========================================================================

set "SCRIPT_VERSION=1.0.0"
set "APP_NAME=Jukebox Pi Money"
set "APP_VERSION=2.3.0"
set "INNO_PATH=C:\Program Files (x86)\Inno Setup 6\ISCC.exe"
set "INNO_PATH_ALT=C:\Program Files\Inno Setup 6\ISCC.exe"

set "BUILD_EXE=1"
set "BUILD_INSTALLER=1"
set "CLEAN_BUILD=0"

REM ========================================================================
REM Banner e Início
REM ========================================================================

cls
echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║   🎵 JUKEBOX PI MONEY - COMPILADOR WINDOWS v%SCRIPT_VERSION%                 ║
echo ║                                                                       ║
echo ║   Script completo de compilação para Windows                         ║
echo ║   Cria executável standalone e instalador profissional               ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.

REM ========================================================================
REM Processamento de Argumentos
REM ========================================================================

:parse_args
if "%~1"=="" goto :args_done
if /i "%~1"=="--exe-only" (
    set "BUILD_INSTALLER=0"
    shift
    goto :parse_args
)
if /i "%~1"=="--installer-only" (
    set "BUILD_EXE=0"
    shift
    goto :parse_args
)
if /i "%~1"=="--clean" (
    set "CLEAN_BUILD=1"
    shift
    goto :parse_args
)
if /i "%~1"=="--help" (
    goto :show_help
)
echo ⚠️ Argumento desconhecido: %~1
goto :show_help

:args_done

REM ========================================================================
REM Verificações Iniciais
REM ========================================================================

echo 📋 FASE 1: Verificações Iniciais
echo ═══════════════════════════════════════════════════════════════════════
echo.

REM Verificar se está no diretório raiz do projeto
if not exist "src\server\app.py" (
    echo ❌ ERRO: Este script deve ser executado do diretório raiz do projeto
    echo.
    echo    Estrutura esperada:
    echo    - src\server\app.py
    echo    - requirements.txt
    echo    - jukebox.spec
    echo.
    exit /b 1
)
echo ✅ Diretório raiz do projeto verificado

REM Verificar Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ ERRO: Python não encontrado
    echo.
    echo    Instale Python 3.9 ou superior:
    echo    💡 https://www.python.org/downloads/
    echo.
    exit /b 1
)

for /f "tokens=2" %%i in ('python --version 2^>^&1') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% encontrado

REM Verificar se PyInstaller será necessário
if %BUILD_EXE%==1 (
    pip show pyinstaller >nul 2>&1
    if errorlevel 1 (
        echo ℹ️ PyInstaller será instalado durante o build
    ) else (
        echo ✅ PyInstaller já instalado
    )
)

REM Verificar Inno Setup (se necessário)
if %BUILD_INSTALLER%==1 (
    if exist "%INNO_PATH%" (
        echo ✅ Inno Setup encontrado: %INNO_PATH%
    ) else if exist "%INNO_PATH_ALT%" (
        set "INNO_PATH=%INNO_PATH_ALT%"
        echo ✅ Inno Setup encontrado: %INNO_PATH%
    ) else (
        echo ❌ ERRO: Inno Setup não encontrado
        echo.
        echo    Inno Setup é necessário para criar o instalador.
        echo    💡 Baixe e instale em: https://jrsoftware.org/isinfo.php
        echo.
        echo    Ou compile apenas o executável com:
        echo    compile-windows.bat --exe-only
        echo.
        exit /b 1
    )
)

echo.

REM ========================================================================
REM Limpeza (Opcional)
REM ========================================================================

if %CLEAN_BUILD%==1 (
    echo 🧹 FASE 2: Limpando Builds Anteriores
    echo ═══════════════════════════════════════════════════════════════════════
    echo.
    
    if exist "build" (
        echo 🗑️ Removendo diretório build\...
        rmdir /s /q "build" 2>nul
    )
    
    if exist "dist" (
        echo 🗑️ Removendo diretório dist\...
        rmdir /s /q "dist" 2>nul
    )
    
    if exist "installers" (
        echo 🗑️ Removendo diretório installers\...
        rmdir /s /q "installers" 2>nul
    )
    
    echo ✅ Limpeza concluída
    echo.
)

REM ========================================================================
REM Build do Executável
REM ========================================================================

if %BUILD_EXE%==1 (
    echo 🔨 FASE 3: Compilando Executável Standalone
    echo ═══════════════════════════════════════════════════════════════════════
    echo.
    
    REM Criar/ativar ambiente virtual
    if not exist "venv" (
        echo 📦 Criando ambiente virtual...
        python -m venv venv
        if errorlevel 1 (
            echo ❌ ERRO: Falha ao criar ambiente virtual
            exit /b 1
        )
        echo ✅ Ambiente virtual criado
    )
    
    echo 🔄 Ativando ambiente virtual...
    call venv\Scripts\activate.bat
    
    REM Instalar dependências (sem RPi.GPIO)
    echo 📦 Instalando dependências do projeto...
    echo    (Isso pode demorar alguns minutos...)
    
    REM Criar requirements temporário sem RPi.GPIO
    findstr /v "RPi.GPIO" requirements.txt > %TEMP%\requirements-build.txt
    
    pip install --quiet --upgrade pip
    pip install --quiet -r %TEMP%\requirements-build.txt
    del %TEMP%\requirements-build.txt
    
    if errorlevel 1 (
        echo ❌ ERRO: Falha ao instalar dependências
        exit /b 1
    )
    echo ✅ Dependências instaladas
    
    REM Instalar PyInstaller
    echo 📦 Instalando PyInstaller...
    pip install --quiet pyinstaller
    if errorlevel 1 (
        echo ❌ ERRO: Falha ao instalar PyInstaller
        exit /b 1
    )
    echo ✅ PyInstaller instalado
    
    REM Compilar com PyInstaller
    echo.
    echo 🔨 Compilando com PyInstaller...
    echo    Arquivo: src\server\app.py
    echo    Especificação: jukebox.spec
    echo.
    
    pyinstaller --clean jukebox.spec
    
    if errorlevel 1 (
        echo.
        echo ❌ ERRO: Falha na compilação do executável
        echo.
        echo    Verifique os logs acima para mais detalhes.
        exit /b 1
    )
    
    REM Verificar se o executável foi criado
    if not exist "dist\jukebox.exe" (
        echo ❌ ERRO: Executável não foi criado em dist\jukebox.exe
        exit /b 1
    )
    
    REM Obter tamanho do executável
    for %%A in ("dist\jukebox.exe") do set "EXE_SIZE=%%~zA"
    set /a EXE_SIZE_MB=%EXE_SIZE% / 1048576
    
    echo.
    echo ╔═══════════════════════════════════════════════════════════════════════╗
    echo ║  ✅ EXECUTÁVEL COMPILADO COM SUCESSO!                                ║
    echo ╚═══════════════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 Localização: dist\jukebox.exe
    echo 📊 Tamanho: ~%EXE_SIZE_MB% MB
    echo.
) else (
    REM Verificar se o executável existe (necessário para o instalador)
    if %BUILD_INSTALLER%==1 (
        if not exist "dist\jukebox.exe" (
            echo ❌ ERRO: Executável não encontrado em dist\jukebox.exe
            echo.
            echo    Para criar apenas o instalador, você precisa primeiro
            echo    compilar o executável. Execute:
            echo.
            echo    compile-windows.bat --exe-only
            echo.
            exit /b 1
        )
    )
)

REM ========================================================================
REM Build do Instalador
REM ========================================================================

if %BUILD_INSTALLER%==1 (
    echo.
    echo 📦 FASE 4: Criando Instalador Profissional (Inno Setup)
    echo ═══════════════════════════════════════════════════════════════════════
    echo.
    
    REM Criar diretório de saída
    if not exist "installers" (
        echo 📁 Criando diretório installers\...
        mkdir installers
    )
    
    REM Compilar com Inno Setup
    echo 🔨 Compilando instalador com Inno Setup...
    echo    Arquivo: installer-windows.iss
    echo.
    
    "%INNO_PATH%" "installer-windows.iss"
    
    if errorlevel 1 (
        echo.
        echo ❌ ERRO: Falha ao criar instalador
        echo.
        echo    Verifique:
        echo    1. O arquivo installer-windows.iss está correto
        echo    2. Todos os arquivos necessários existem em dist\
        echo    3. Os caminhos no .iss estão corretos
        echo.
        exit /b 1
    )
    
    REM Verificar se o instalador foi criado
    if not exist "installers\jukebox-setup-windows-x64.exe" (
        echo ❌ ERRO: Instalador não foi criado
        exit /b 1
    )
    
    REM Obter tamanho do instalador
    for %%A in ("installers\jukebox-setup-windows-x64.exe") do set "INST_SIZE=%%~zA"
    set /a INST_SIZE_MB=%INST_SIZE% / 1048576
    
    echo.
    echo ╔═══════════════════════════════════════════════════════════════════════╗
    echo ║  ✅ INSTALADOR CRIADO COM SUCESSO!                                   ║
    echo ╚═══════════════════════════════════════════════════════════════════════╝
    echo.
    echo 📦 Localização: installers\jukebox-setup-windows-x64.exe
    echo 📊 Tamanho: ~%INST_SIZE_MB% MB
    echo.
)

REM ========================================================================
REM Resumo Final e Instruções
REM ========================================================================

echo.
echo ╔═══════════════════════════════════════════════════════════════════════╗
echo ║                                                                       ║
echo ║  🎉 COMPILAÇÃO CONCLUÍDA COM SUCESSO!                                ║
echo ║                                                                       ║
echo ╚═══════════════════════════════════════════════════════════════════════╝
echo.
echo 📦 ARQUIVOS GERADOS:
echo ═══════════════════════════════════════════════════════════════════════

if %BUILD_EXE%==1 (
    echo.
    echo 1. EXECUTÁVEL STANDALONE (Para usuários avançados)
    echo    📁 dist\jukebox.exe
    echo.
    echo    Como usar:
    echo    - Copie o executável para qualquer lugar
    echo    - Crie um arquivo .env no mesmo diretório
    echo    - Execute jukebox.exe
    echo    - Acesse http://localhost:5000
    echo.
)

if %BUILD_INSTALLER%==1 (
    echo.
    echo 2. INSTALADOR PROFISSIONAL (Recomendado para distribuição)
    echo    📁 installers\jukebox-setup-windows-x64.exe
    echo.
    echo    Como distribuir:
    echo    - Envie o arquivo installers\jukebox-setup-windows-x64.exe
    echo    - Usuários devem apenas executar o instalador
    echo    - Instalação automática com assistente de configuração
    echo    - Cria atalhos no Desktop e Menu Iniciar
    echo    - Inclui desinstalador integrado
    echo.
)

echo.
echo 💡 PRÓXIMOS PASSOS:
echo ═══════════════════════════════════════════════════════════════════════
echo.
echo Para testar o executável:
echo    cd dist
echo    copy ..\env.example .env
echo    jukebox.exe
echo.
echo Para testar o instalador:
echo    installers\jukebox-setup-windows-x64.exe
echo.
echo Para distribuir:
echo    - Hospede o instalador no GitHub Releases
echo    - Ou envie diretamente para os usuários
echo.
echo 📚 DOCUMENTAÇÃO:
echo    - INSTALLER.md    : Guia completo de instaladores
echo    - BUILD.md        : Documentação de build
echo    - README.md       : Documentação principal
echo.
echo.
echo ✨ Compilação completa! Bom uso do %APP_NAME% v%APP_VERSION%!
echo.

goto :eof

REM ========================================================================
REM Função de Ajuda
REM ========================================================================

:show_help
echo.
echo COMPILADOR WINDOWS - JUKEBOX PI MONEY v%SCRIPT_VERSION%
echo.
echo USO:
echo    compile-windows.bat [opções]
echo.
echo OPÇÕES:
echo    --exe-only       Compila apenas o executável standalone
echo    --installer-only Cria apenas o instalador (requer exe já compilado)
echo    --clean          Limpa builds anteriores antes de compilar
echo    --help           Mostra esta mensagem de ajuda
echo.
echo EXEMPLOS:
echo    compile-windows.bat
echo        Compilação completa (executável + instalador)
echo.
echo    compile-windows.bat --clean
echo        Limpa tudo e recompila do zero
echo.
echo    compile-windows.bat --exe-only
echo        Compila apenas o executável
echo.
echo    compile-windows.bat --installer-only
echo        Cria apenas o instalador (após já ter o executável)
echo.
echo REQUISITOS:
echo    - Python 3.9 ou superior
echo    - Inno Setup 6.0 ou superior (para --installer)
echo.
echo DOCUMENTAÇÃO:
echo    Para mais informações, consulte:
echo    - INSTALLER.md  : Guia de instaladores
echo    - BUILD.md      : Documentação de build
echo    - README.md     : Documentação principal
echo.
exit /b 0
