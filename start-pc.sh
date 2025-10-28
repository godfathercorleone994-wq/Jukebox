#!/bin/bash
# Script para iniciar o Jukebox em PC/Linux (sem Raspberry Pi)
# Este script detecta automaticamente o ambiente e ajusta as configurações

set -e

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🎵 Jukebox-Pi-Money - Modo PC/Linux         ║${NC}"
echo -e "${BLUE}║  Executando em ambiente de desenvolvimento    ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "src/server/app.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Detectar sistema operacional
OS=$(uname -s)
echo -e "${YELLOW}🖥️  Sistema detectado: $OS${NC}"

# Detectar se é Raspberry Pi
IS_RASPBERRY_PI=false
if [ -f /proc/cpuinfo ]; then
    if grep -q "Raspberry Pi" /proc/cpuinfo 2>/dev/null; then
        IS_RASPBERRY_PI=true
    fi
fi

if [ "$IS_RASPBERRY_PI" = true ]; then
    echo -e "${GREEN}✓ Raspberry Pi detectado${NC}"
else
    echo -e "${YELLOW}⚠️  Sistema PC/Linux detectado (não é Raspberry Pi)${NC}"
    echo -e "${YELLOW}   Hardware GPIO será desabilitado automaticamente${NC}"
fi

# Verificar se o ambiente virtual existe
if [ ! -d "venv" ]; then
    echo -e "${YELLOW}⚠️  Ambiente virtual não encontrado${NC}"
    echo -e "${YELLOW}Criando ambiente virtual...${NC}"
    python3 -m venv venv
    echo -e "${GREEN}✅ Ambiente virtual criado${NC}"
fi

# Ativar ambiente virtual
echo -e "${YELLOW}🔄 Ativando ambiente virtual...${NC}"
source venv/bin/activate

# Instalar dependências (exceto RPi.GPIO em ambientes não-Raspberry Pi)
if [ "$IS_RASPBERRY_PI" = false ]; then
    echo -e "${YELLOW}📦 Instalando dependências (modo PC)...${NC}"
    
    # Cria arquivo temporário de requirements sem RPi.GPIO
    grep -v "RPi.GPIO" requirements.txt > /tmp/requirements-pc.txt
    
    if ! python3 -c "import flask" 2>/dev/null; then
        pip install -q -r /tmp/requirements-pc.txt
        echo -e "${GREEN}✅ Dependências instaladas (sem RPi.GPIO)${NC}"
    else
        echo -e "${GREEN}✓ Dependências já instaladas${NC}"
    fi
    
    rm -f /tmp/requirements-pc.txt
else
    echo -e "${YELLOW}📦 Verificando dependências...${NC}"
    if ! python3 -c "import flask" 2>/dev/null; then
        echo -e "${YELLOW}Instalando dependências completas...${NC}"
        pip install -q -r requirements.txt
        echo -e "${GREEN}✅ Dependências instaladas${NC}"
    else
        echo -e "${GREEN}✓ Dependências já instaladas${NC}"
    fi
fi

# Configurar arquivo .env para modo PC
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    echo -e "${YELLOW}Copiando .env.example para .env...${NC}"
    cp env.example .env
    echo -e "${GREEN}✅ Arquivo .env criado${NC}"
fi

# Ajustar configurações para modo PC
if [ "$IS_RASPBERRY_PI" = false ]; then
    echo -e "${YELLOW}🔧 Configurando para modo PC...${NC}"
    
    # Desabilitar hardware GPIO
    if grep -q "^HARDWARE_ENABLED=" .env; then
        sed -i 's/^HARDWARE_ENABLED=.*/HARDWARE_ENABLED=false/' .env
    else
        echo "HARDWARE_ENABLED=false" >> .env
    fi
    
    # Desabilitar YouTube por padrão (pode ser habilitado se tiver display)
    if grep -q "^YOUTUBE_ENABLED=" .env; then
        sed -i 's/^YOUTUBE_ENABLED=.*/YOUTUBE_ENABLED=false/' .env
    else
        echo "YOUTUBE_ENABLED=false" >> .env
    fi
    
    # Configurar ambiente de desenvolvimento
    if grep -q "^FLASK_ENV=" .env; then
        sed -i 's/^FLASK_ENV=.*/FLASK_ENV=development/' .env
    else
        echo "FLASK_ENV=development" >> .env
    fi
    
    echo -e "${GREEN}✅ Configurações ajustadas para modo PC${NC}"
fi

# Criar diretórios necessários
mkdir -p logs src/db

# Opção de executar testes
if [ "$1" == "--test" ]; then
    echo -e "${YELLOW}🧪 Executando testes...${NC}"
    python3 tests/test_jukebox.py
    echo ""
fi

# Mostrar informações de acesso
echo ""
echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🚀 Iniciando Jukebox em modo PC/Linux       ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""
echo -e "${GREEN}✨ Funcionalidades disponíveis:${NC}"
echo -e "   ✓ Interface web completa com navegação por teclado"
echo -e "   ✓ Simulação de pagamentos para testes"
echo -e "   ✓ Fila de músicas"
echo -e "   ✓ API REST completa"

if [ "$IS_RASPBERRY_PI" = false ]; then
    echo -e "   ${YELLOW}⚠️  Hardware GPIO: DESABILITADO${NC}"
    echo -e "   ${YELLOW}⚠️  YouTube Player: DESABILITADO (pode habilitar no .env)${NC}"
fi

echo ""
echo -e "${GREEN}🌐 Acesse:${NC}"
echo -e "   • Interface: ${BLUE}http://localhost:5000${NC}"
echo -e "   • API Docs:  ${BLUE}API.md${NC}"
echo ""
echo -e "${YELLOW}⌨️  Navegação por teclado:${NC}"
echo -e "   • Tecle ${BLUE}F1${NC} ou ${BLUE}?${NC} na interface para ver os atalhos"
echo -e "   • Use setas (↑↓←→) para navegar"
echo -e "   • Use números (1-9) para seleção rápida"
echo -e "   • Enter para selecionar, Esc para voltar"
echo ""
echo -e "${YELLOW}💡 Dica: Use Ctrl+C para parar o servidor${NC}"
echo ""

# Iniciar servidor
python3 src/server/app.py
