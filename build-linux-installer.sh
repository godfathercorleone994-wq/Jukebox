#!/bin/bash
# Build script for creating Linux installer (.deb package)
# This script creates a Debian package that can be installed on any Debian-based Linux

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}╔═══════════════════════════════════════════════╗${NC}"
echo -e "${BLUE}║  🎵 Jukebox - Build Linux Installer (.deb)   ║${NC}"
echo -e "${BLUE}╚═══════════════════════════════════════════════╝${NC}"
echo ""

# Check if we're on Linux
if [[ "$OSTYPE" != "linux-gnu"* ]]; then
    echo -e "${RED}❌ Este script deve ser executado em Linux${NC}"
    exit 1
fi

# Check if running from project root
if [ ! -f "src/server/app.py" ]; then
    echo -e "${RED}❌ Execute este script do diretório raiz do projeto${NC}"
    exit 1
fi

# Check if executable exists
if [ ! -f "dist/jukebox" ]; then
    echo -e "${YELLOW}⚠️  Executável não encontrado. Construindo...${NC}"
    chmod +x build-linux.sh
    ./build-linux.sh
fi

if [ ! -f "dist/jukebox" ]; then
    echo -e "${RED}❌ Falha ao construir executável${NC}"
    exit 1
fi

echo -e "${YELLOW}📦 Preparando estrutura do pacote Debian...${NC}"

# Create debian package structure
DEB_DIR="debian"
rm -rf "$DEB_DIR"
mkdir -p "$DEB_DIR/DEBIAN"
mkdir -p "$DEB_DIR/usr/local/bin"
mkdir -p "$DEB_DIR/usr/share/applications"
mkdir -p "$DEB_DIR/usr/share/doc/jukebox"
mkdir -p "$DEB_DIR/etc/jukebox"

# Copy executable
echo -e "${YELLOW}📁 Copiando arquivos...${NC}"
cp dist/jukebox "$DEB_DIR/usr/local/bin/"
chmod 755 "$DEB_DIR/usr/local/bin/jukebox"

# Copy documentation
cp README.md "$DEB_DIR/usr/share/doc/jukebox/"
cp BUILD.md "$DEB_DIR/usr/share/doc/jukebox/" 2>/dev/null || true
cp QUICKSTART_EXECUTABLE.md "$DEB_DIR/usr/share/doc/jukebox/" 2>/dev/null || true
cp LICENSE "$DEB_DIR/usr/share/doc/jukebox/" 2>/dev/null || true
cp env.example "$DEB_DIR/usr/share/doc/jukebox/"

# Create control file
echo -e "${YELLOW}📝 Criando arquivo de controle...${NC}"
cat > "$DEB_DIR/DEBIAN/control" << 'EOF'
Package: jukebox-pi-money
Version: 2.3.0
Section: sound
Priority: optional
Architecture: amd64
Maintainer: godfathercorleone994 <godfathercorleone994@gmail.com>
Homepage: https://github.com/godfathercorleone994-wq/Jukebox
Description: Sistema embarcado de Jukebox com YouTube Music
 Jukebox Pi Money é um sistema de jukebox moderno que permite reproduzir
 músicas do YouTube com múltiplos métodos de pagamento incluindo PIX,
 cartão de crédito/débito e dinheiro.
 .
 Características principais:
  * Reprodução automática de músicas do YouTube
  * Suporte a múltiplos métodos de pagamento
  * Interface web responsiva com navegação por teclado
  * Sistema de código de operador para administradores
  * Música ambiente automática quando em espera
  * Bloqueio avançado de anúncios
 .
 Executável standalone que não requer Python instalado.
EOF

# Create postinst script
cat > "$DEB_DIR/DEBIAN/postinst" << 'EOF'
#!/bin/bash
set -e

# Create config directory
CONFIG_DIR="/etc/jukebox"
mkdir -p "$CONFIG_DIR"
chmod 755 "$CONFIG_DIR"

# Create .env if it doesn't exist
if [ ! -f "$CONFIG_DIR/.env" ]; then
    cat > "$CONFIG_DIR/.env" << 'ENVEOF'
# Configuração do Jukebox Pi Money
FLASK_ENV=production
SECRET_KEY=CHANGE_THIS_TO_A_RANDOM_SECRET_KEY
HARDWARE_ENABLED=false
YOUTUBE_ENABLED=false
PRICE_PER_SONG=5.00
ADMIN_ENABLED=false
ADMIN_CREDIT_AMOUNT=20.00
ENVEOF
    chmod 644 "$CONFIG_DIR/.env"
fi

# Create directories
mkdir -p /var/log/jukebox
mkdir -p /var/lib/jukebox
chmod 755 /var/log/jukebox
chmod 755 /var/lib/jukebox

echo ""
echo "╔═══════════════════════════════════════════════╗"
echo "║  Jukebox Pi Money instalado com sucesso!     ║"
echo "╚═══════════════════════════════════════════════╝"
echo ""
echo "📝 Configure: sudo nano /etc/jukebox/.env"
echo "🚀 Execute: jukebox"
echo "🌐 Acesse: http://localhost:5000"
echo ""

exit 0
EOF
chmod 755 "$DEB_DIR/DEBIAN/postinst"

# Create prerm script
cat > "$DEB_DIR/DEBIAN/prerm" << 'EOF'
#!/bin/bash
set -e
pkill -f "jukebox" 2>/dev/null || true
exit 0
EOF
chmod 755 "$DEB_DIR/DEBIAN/prerm"

# Create postrm script
cat > "$DEB_DIR/DEBIAN/postrm" << 'EOF'
#!/bin/bash
set -e
if [ "$1" = "purge" ]; then
    rm -rf /etc/jukebox
    rm -rf /var/log/jukebox
    rm -rf /var/lib/jukebox
fi
exit 0
EOF
chmod 755 "$DEB_DIR/DEBIAN/postrm"

# Create desktop entry
cat > "$DEB_DIR/usr/share/applications/jukebox.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Jukebox Pi Money
Comment=Sistema de Jukebox com YouTube Music
Exec=jukebox
Terminal=true
Categories=AudioVideo;Audio;Player;
Keywords=jukebox;music;youtube;player;
EOF

# Build the package
echo -e "${YELLOW}🔨 Construindo pacote .deb...${NC}"
mkdir -p installers
fakeroot dpkg-deb --build "$DEB_DIR" installers/jukebox-pi-money_2.3.0_amd64.deb

if [ $? -eq 0 ]; then
    echo ""
    echo -e "${GREEN}╔═══════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║  ✅ Instalador criado com sucesso!           ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════╝${NC}"
    echo ""
    echo -e "${GREEN}📦 Instalador criado em: ${BLUE}installers/jukebox-pi-money_2.3.0_amd64.deb${NC}"
    echo ""
    echo -e "${YELLOW}📋 Como instalar o pacote:${NC}"
    echo ""
    echo -e "  ${GREEN}sudo dpkg -i installers/jukebox-pi-money_2.3.0_amd64.deb${NC}"
    echo ""
    echo -e "${YELLOW}📋 Como usar após instalação:${NC}"
    echo ""
    echo -e "1. ${BLUE}Configure${NC}:"
    echo -e "   ${GREEN}sudo nano /etc/jukebox/.env${NC}"
    echo ""
    echo -e "2. ${BLUE}Execute${NC}:"
    echo -e "   ${GREEN}jukebox${NC}"
    echo ""
    echo -e "3. ${BLUE}Acesse${NC}:"
    echo -e "   ${GREEN}http://localhost:5000${NC}"
    echo ""
    echo -e "${YELLOW}💡 Dicas:${NC}"
    echo -e "   • O pacote instala o executável em /usr/local/bin/"
    echo -e "   • Configuração em /etc/jukebox/.env"
    echo -e "   • Logs em /var/log/jukebox/"
    echo -e "   • Documentação em /usr/share/doc/jukebox/"
    echo ""
else
    echo -e "${RED}❌ Erro ao criar pacote .deb${NC}"
    exit 1
fi

# Clean up
rm -rf "$DEB_DIR"
