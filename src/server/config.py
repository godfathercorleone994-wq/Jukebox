"""
Configurações centralizadas do sistema Jukebox
Carrega variáveis de ambiente e define constantes do projeto
"""

import os
from pathlib import Path

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent

# === CONFIGURAÇÕES DE HARDWARE ===
class HardwareConfig:
    """Configurações do Raspberry Pi e periféricos"""
    
    # GPIO do aceitador de notas (pino físico 11 = GPIO 17)
    GPIO_BILL_ACCEPTOR = int(os.getenv('GPIO_BILL_ACCEPTOR', '17'))
    
    # Valor monetário de cada pulso recebido
    PULSE_VALUE = float(os.getenv('PULSE_VALUE', '2.00'))
    
    # Tempo mínimo entre pulsos para evitar ruído (milissegundos)
    DEBOUNCE_MS = int(os.getenv('DEBOUNCE_MS', '200'))


# === CONFIGURAÇÕES DE NEGÓCIO ===
class BusinessConfig:
    """Regras de negócio da Jukebox"""
    
    # Preço cobrado por música
    PRICE_PER_SONG = float(os.getenv('PRICE_PER_SONG', '5.00'))
    
    # Limite de músicas na fila de espera
    MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE', '10'))
    
    # Tempo de inatividade antes de voltar à tela inicial (segundos)
    IDLE_TIMEOUT = int(os.getenv('IDLE_TIMEOUT', '300'))


# === CONFIGURAÇÕES DO FLASK ===
class FlaskConfig:
    """Configurações do servidor web"""
    
    # Modo de execução (development, production)
    ENV = os.getenv('FLASK_ENV', 'production')
    
    # Chave secreta para sessões (MUDE EM PRODUÇÃO!)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-THIS')
    
    # Token para autenticar requisições do hardware
    HARDWARE_TOKEN = os.getenv('HARDWARE_TOKEN', 'hardware-token-123')
    
    # Porta do servidor
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    
    # Host (0.0.0.0 permite acesso externo)
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')


# === CONFIGURAÇÕES DO YOUTUBE ===
class YouTubeConfig:
    """Configurações do player YouTube com Selenium"""
    
    # Caminho do ChromeDriver
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    
    # Ativar autoplay da próxima música
    AUTOPLAY = os.getenv('YOUTUBE_AUTOPLAY', 'true').lower() == 'true'
    
    # Tempo máximo de espera por elementos (segundos)
    WAIT_TIMEOUT = int(os.getenv('SELENIUM_TIMEOUT', '10'))


# === CONFIGURAÇÕES DO BANCO DE DADOS ===
class DatabaseConfig:
    """Configurações do SQLite"""
    
    # Caminho do arquivo do banco de dados
    DB_PATH = Path(os.getenv('DB_PATH', BASE_DIR / 'src' / 'db' / 'jukebox.db'))
    
    # Criar diretório se não existir
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# === CONFIGURAÇÕES DE LOGGING ===
class LogConfig:
    """Configurações de logs do sistema"""
    
    # Nível de log (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    
    # Arquivo de log
    LOG_FILE = Path(os.getenv('LOG_FILE', BASE_DIR / 'logs' / 'jukebox.log'))
    
    # Criar diretório de logs se não existir
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Formato das mensagens de log
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
