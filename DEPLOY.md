# 🚀 Guia de Deploy - Jukebox-Pi-Money

## 📋 Pré-requisitos

### Hardware
- Raspberry Pi 4 (4GB RAM mínimo)
- Display Touchscreen 7" ou maior
- Aceitador de notas JCM WBA10 (conectado via GPIO)
- Conexão à Internet

### Software
- Raspberry Pi OS Lite (64-bit) - versão Bullseye ou superior
- Python 3.9+
- Chrome/Chromium Browser
- ChromeDriver

## 🔧 Instalação no Raspberry Pi

### 1. Atualizar Sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Instalar Dependências do Sistema

```bash
# Python e pip
sudo apt install -y python3 python3-pip python3-venv

# Chrome e ChromeDriver para YouTube
sudo apt install -y chromium-browser chromium-chromedriver

# Bibliotecas de sistema
sudo apt install -y libgpiod2
```

### 3. Clonar Repositório

```bash
cd /home/pi
git clone https://github.com/seu-usuario/Jukebox-Pi-Money.git
cd Jukebox-Pi-Money
```

### 4. Criar Ambiente Virtual

```bash
python3 -m venv venv
source venv/bin/activate
```

### 5. Instalar Dependências Python

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### 6. Configurar Variáveis de Ambiente

```bash
# Copiar template
cp env.example .env

# Editar configurações
nano .env
```

**Configurações obrigatórias:**

```bash
# Gateway de Pagamento (obter em https://www.mercadopago.com.br/developers)
PAYMENT_API_KEY=seu_api_key_aqui
PAYMENT_ACCESS_TOKEN=seu_access_token_aqui

# Tokens de segurança (gerar strings aleatórias)
SECRET_KEY=$(openssl rand -hex 32)
HARDWARE_TOKEN=$(openssl rand -hex 16)
WEBHOOK_SECRET=$(openssl rand -hex 16)

# URL pública para webhooks (usar ngrok para testes)
PAYMENT_WEBHOOK_URL=https://seu-dominio.com/api/webhook
```

### 7. Testar Instalação

```bash
# Executar testes
python3 tests/test_jukebox.py

# Deve mostrar: "Total: 4/4 testes passaram"
```

### 8. Iniciar Servidor

```bash
# Modo desenvolvimento
python3 src/server/app.py

# Ou usando variável de ambiente
FLASK_ENV=production python3 src/server/app.py
```

O servidor estará disponível em:
- Local: http://localhost:5000
- Rede: http://IP_DO_SEU_PI:5000

## 🔄 Configurar Inicialização Automática (Systemd)

### 1. Criar arquivo de serviço

```bash
sudo nano /etc/systemd/system/jukebox.service
```

### 2. Adicionar configuração

```ini
[Unit]
Description=Jukebox-Pi-Money Server
After=network.target

[Service]
Type=simple
User=pi
WorkingDirectory=/home/pi/Jukebox-Pi-Money
Environment="PATH=/home/pi/Jukebox-Pi-Money/venv/bin"
ExecStart=/home/pi/Jukebox-Pi-Money/venv/bin/python3 src/server/app.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

### 3. Ativar serviço

```bash
# Recarregar systemd
sudo systemctl daemon-reload

# Ativar serviço
sudo systemctl enable jukebox

# Iniciar serviço
sudo systemctl start jukebox

# Verificar status
sudo systemctl status jukebox
```

### 4. Comandos úteis

```bash
# Ver logs
sudo journalctl -u jukebox -f

# Reiniciar serviço
sudo systemctl restart jukebox

# Parar serviço
sudo systemctl stop jukebox
```

## 🌐 Configurar Acesso Externo (Opcional)

### Usando ngrok (para testes)

```bash
# Instalar ngrok
wget https://bin.equinox.io/c/bNyj1mQVY4c/ngrok-v3-stable-linux-arm64.tgz
tar xvzf ngrok-v3-stable-linux-arm64.tgz
sudo mv ngrok /usr/local/bin/

# Autenticar (obter token em https://ngrok.com)
ngrok config add-authtoken SEU_TOKEN

# Expor servidor
ngrok http 5000
```

### Usando DNS Dinâmico + Port Forwarding

1. Configure port forwarding no seu roteador (porta 5000 → IP do Pi)
2. Use serviço de DNS dinâmico (No-IP, DuckDNS, etc.)
3. Configure HTTPS com Let's Encrypt (recomendado para produção)

## 🖥️ Configurar Modo Kiosk (Tela Cheia)

### 1. Instalar Chromium

```bash
sudo apt install -y chromium-browser unclutter xdotool
```

### 2. Criar script de inicialização

```bash
nano ~/kiosk.sh
```

```bash
#!/bin/bash
xset s noblank
xset s off
xset -dpms

unclutter -idle 0.5 -root &

sed -i 's/"exited_cleanly":false/"exited_cleanly":true/' ~/.config/chromium/Default/Preferences
sed -i 's/"exit_type":"Crashed"/"exit_type":"Normal"/' ~/.config/chromium/Default/Preferences

/usr/bin/chromium-browser \
  --noerrdialogs \
  --disable-infobars \
  --kiosk \
  http://localhost:5000
```

```bash
chmod +x ~/kiosk.sh
```

### 3. Configurar autostart

```bash
mkdir -p ~/.config/lxsession/LXDE-pi
nano ~/.config/lxsession/LXDE-pi/autostart
```

Adicionar:
```
@lxpanel --profile LXDE-pi
@pcmanfm --desktop --profile LXDE-pi
@xscreensaver -no-splash
@point-rpi
@/home/pi/kiosk.sh
```

## 🔧 GPIO - Aceitador de Notas

### Conexão Física

```
Aceitador JCM WBA10:
- Sinal → GPIO 17 (pino físico 11)
- VCC → 5V (pino 2 ou 4)
- GND → Ground (pino 6, 9, 14, 20, 25, 30, 34, 39)
```

### Testar GPIO

```python
# No Python
from src.hardware import BillAcceptor

def on_cash(amount):
    print(f"Recebido: R$ {amount}")

acceptor = BillAcceptor(callback=on_cash)

# Insira uma nota no aceitador
# Deve imprimir: "Recebido: R$ 2.00"
```

## 📊 Monitoramento

### Verificar Status

```bash
# Status da aplicação
curl http://localhost:5000/api/status

# Saldo de créditos
curl http://localhost:5000/api/balance

# Fila de músicas
curl http://localhost:5000/api/music/queue
```

### Logs

```bash
# Logs da aplicação
tail -f logs/jukebox.log

# Logs do systemd
sudo journalctl -u jukebox -f
```

## 🐛 Troubleshooting

### Servidor não inicia

```bash
# Verificar se porta 5000 está em uso
sudo lsof -i :5000

# Testar manualmente
cd /home/pi/Jukebox-Pi-Money
source venv/bin/activate
python3 src/server/app.py
```

### GPIO não funciona

```bash
# Verificar se usuário está no grupo gpio
groups

# Adicionar ao grupo se necessário
sudo usermod -a -G gpio pi

# Testar GPIO manualmente
python3 -c "import RPi.GPIO as GPIO; print('GPIO OK')"
```

### YouTube não funciona

```bash
# Verificar ChromeDriver
which chromedriver

# Testar Selenium
python3 -c "from selenium import webdriver; driver = webdriver.Chrome(); print('Selenium OK'); driver.quit()"
```

### Webhook não recebe pagamentos

1. Verifique se URL pública está acessível
2. Configure webhook no painel do Mercado Pago
3. Valide o WEBHOOK_SECRET no .env

## 🔐 Segurança

### Recomendações para Produção

1. **Altere todos os tokens** no arquivo `.env`
2. **Use HTTPS** com certificado SSL válido
3. **Configure firewall** (UFW):
   ```bash
   sudo ufw allow ssh
   sudo ufw allow 5000/tcp
   sudo ufw enable
   ```
4. **Atualizações regulares**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```
5. **Backup do banco de dados**:
   ```bash
   cp src/db/jukebox.db backups/jukebox_$(date +%Y%m%d).db
   ```

## 📞 Suporte

Para problemas ou dúvidas:
- Abra uma issue no GitHub
- Consulte a documentação oficial do Raspberry Pi
- Visite o fórum da comunidade

## 📄 Licença

Este projeto está licenciado sob a MIT License - veja o arquivo LICENSE para detalhes.
