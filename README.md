# 🎵 Jukebox-Pi-Money

Sistema embarcado de Jukebox com aceitador de notas e YouTube Music para Raspberry Pi.

## 🚀 Características

- 💰 Aceita notas de dinheiro via aceitador JCM WBA10
- 🎵 Reproduz músicas do YouTube automaticamente
- 📱 Interface touchscreen responsiva
- 💾 Banco de dados SQLite para logs e créditos
- 🔒 API REST protegida por token

## 📋 Requisitos

- Raspberry Pi 4 (4GB recomendado)
- Display Touchscreen 7"
- Aceitador de Notas JCM WBA10
- Raspberry Pi OS Lite (64-bit)
- Python 3.9+

## 🛠️ Instalação

```bash
# Clone o repositório
git clone https://github.com/seu-usuario/Jukebox-Pi-Money.git
cd Jukebox-Pi-Money

# Crie ambiente virtual
python3 -m venv venv
source venv/bin/activate

# Instale dependências
pip install -r requirements.txt

# Configure variáveis de ambiente
cp .env.example .env
nano .env  # Edite com suas configurações

# Execute
python src/server/app.py
