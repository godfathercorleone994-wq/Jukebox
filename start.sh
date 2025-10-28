#!/bin/bash
# Script para iniciar o Jukebox-Pi-Money

set -e

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${GREEN}🎵 Jukebox-Pi-Money - Iniciando...${NC}"
echo ""

# Verificar se está no diretório correto
if [ ! -f "src/server/app.py" ]; then
    echo -e "${RED}❌ Erro: Execute este script do diretório raiz do projeto${NC}"
    exit 1
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

# Verificar se dependências estão instaladas
if ! python3 -c "import flask" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  Dependências não instaladas${NC}"
    echo -e "${YELLOW}Instalando dependências...${NC}"
    pip install -q -r requirements.txt
    echo -e "${GREEN}✅ Dependências instaladas${NC}"
fi

# Verificar se .env existe
if [ ! -f ".env" ]; then
    echo -e "${YELLOW}⚠️  Arquivo .env não encontrado${NC}"
    echo -e "${YELLOW}Copiando .env.example para .env...${NC}"
    cp env.example .env
    echo -e "${RED}⚠️  IMPORTANTE: Configure o arquivo .env antes de usar em produção!${NC}"
fi

# Criar diretórios necessários
mkdir -p logs src/db

# Executar testes (opcional)
if [ "$1" == "--test" ]; then
    echo -e "${YELLOW}🧪 Executando testes...${NC}"
    python3 tests/test_jukebox.py
    echo ""
fi

# Iniciar servidor
echo -e "${GREEN}🚀 Iniciando servidor Flask...${NC}"
echo -e "${GREEN}Acesse: http://localhost:5000${NC}"
echo ""
echo -e "${YELLOW}Pressione Ctrl+C para parar${NC}"
echo ""

python3 src/server/app.py
