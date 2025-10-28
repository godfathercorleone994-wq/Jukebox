#!/bin/bash
# Build script for creating Linux executable of Jukebox
# This script builds a standalone executable that can run on any Linux system

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🎵 Jukebox - Build Linux Executable         ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ Este script deve ser executado em Linux${NC}"
    echo -e "${YELLOW}💡 Para Windows, use build-windows.sh no Windows ou WSL${NC}"
    exit 1
fi

# Check if running from project root
if [ ! -f "src/server/app.py" ]; then
    echo -e "${RED}❌ Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Create/activate virtual environment
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}📦 Criando ambiente virtual...${NC}"
    python3 -m venv venv
fi

echo -e "${YELLOW}🔄 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Install dependencies (excluding RPi.GPIO for non-Raspberry Pi)
echo -e "${YELLOW}📦 Instalando dependências...${NC}"

# Detect if Raspberry Pi
IS_RASPBERRY_PI=false
if [ -f /proc/cpuinfo ]; then
    if grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
        IS_RASPBERRY_PI=true
    fi
fi

if [ "$IS_RASPBERRY_PI" = false ]; then
    # Create temporary requirements without RPi.GPIO
    grep -v "RPi.GPIO" requirements.txt > /tmp/requirements-build.txt
    pip install -q -r /tmp/requirements-build.txt
    rm -f /tmp/requirements-build.txt
    echo -e "${GREEN}✅ Dependências instaladas (sem RPi.GPIO)${NC}"
else
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependências instaladas (completas)${NC}"
fi

# Install PyInstaller
echo -e "${YELLOW}📦 Instalando PyInstaller...${NC}"
pip install -q pyinstaller

# Clean previous builds
echo -e "${YELLOW}🧹 Limpando builds anteriores...${NC}"
rm -rf build dist

# Build executable
echo -e "${YELLOW}🔨 Construindo executável...${NC}"
pyinstaller --clean jukebox.spec

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ Build concluído com sucesso!             ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}📦 Executável criado em: ${BLUE}dist/jukebox${NC}"
    echo ""
    echo -e "${YELLOW}📋 Como usar o executável:${NC}"
    echo ""
    echo -e "1. ${BLUE}Copie o executável${NC} para onde quiser:"
    echo -e "   ${GREEN}cp dist/jukebox /usr/local/bin/${NC}"
    echo -e "   ou mantenha no diretório dist/"
    echo ""
    echo -e "2. ${BLUE}Crie um arquivo .env${NC} no mesmo diretório do executável:"
    echo -e "   ${GREEN}cp env.example .env${NC}"
    echo -e "   Edite o .env conforme necessário"
    echo ""
    echo -e "3. ${BLUE}Execute o jukebox${NC}:"
    echo -e "   ${GREEN}./dist/jukebox${NC}"
    echo -e "   ou"
    echo -e "   ${GREEN}jukebox${NC} (se copiou para /usr/local/bin)"
    echo ""
    echo -e "4. ${BLUE}Acesse${NC} no navegador:"
    echo -e "   ${GREEN}http://localhost:5000${NC}"
    echo ""
    echo -e "${YELLOW}💡 Dicas:${NC}"
    echo -e "   • O executável inclui todas as dependências Python"
    echo -e "   • Funciona em qualquer distribuição Linux (x86_64)"
    echo -e "   • Não requer instalação de Python"
    echo -e "   • Tamanho aproximado: ~80-100MB"
    echo ""
    echo -e "${YELLOW}📦 Para distribuir:${NC}"
    echo -e "   Compacte o diretório dist/ inteiro:"
    echo -e "   ${GREEN}tar -czf jukebox-linux.tar.gz -C dist .${NC}"
    echo ""
else
    echo -e "${RED}❌ Erro durante o build${NC}"
    exit 1
fi
