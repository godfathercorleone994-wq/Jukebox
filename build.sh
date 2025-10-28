#!/bin/bash
# Cross-platform build helper script
# Detects platform and runs appropriate build script

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m'

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🎵 Jukebox - Build Helper                   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Detect OS
OS=$(uname -s)
case "$OS" in
    Linux*)
        echo -e "${GREEN}✓ Linux detectado${NC}"
        echo -e "${YELLOW}Executando build-linux.sh...${NC}"
        echo ""
        ./build-linux.sh
        ;;
    Darwin*)
        echo -e "${YELLOW}⚠️  macOS detectado${NC}"
        echo -e "${YELLOW}Construindo executável Linux (sem suporte a macOS por enquanto)${NC}"
        echo ""
        ./build-linux.sh
        ;;
    MINGW*|MSYS*|CYGWIN*)
        echo -e "${GREEN}✓ Windows detectado (Git Bash/MSYS)${NC}"
        echo -e "${YELLOW}Por favor, execute build-windows.bat diretamente${NC}"
        echo -e "${YELLOW}ou use o prompt de comando do Windows${NC}"
        exit 1
        ;;
    *)
        echo -e "${RED}❌ Sistema operacional não reconhecido: $OS${NC}"
        echo ""
        echo -e "${YELLOW}Use manualmente:${NC}"
        echo -e "  Linux:   ./build-linux.sh"
        echo -e "  Windows: build-windows.bat"
        exit 1
        ;;
esac
