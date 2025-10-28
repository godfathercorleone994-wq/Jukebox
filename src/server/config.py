"""
Configurações centralizadas do sistema Jukebox
Suporta múltiplos métodos de pagamento: Dinheiro, Débito, Crédito e PIX
"""

import os
from pathlib import Path
from enum import Enum

# Diretório raiz do projeto
BASE_DIR = Path(__file__).resolve().parent.parent.parent


# === ENUMS PARA MÉTODOS DE PAGAMENTO ===
class PaymentMethod(Enum):
    """Métodos de pagamento aceitos pelo sistema"""
    CASH = "cash"           # Dinheiro físico (aceitador de notas)
    DEBIT = "debit"         # Cartão de débito
    CREDIT = "credit"       # Cartão de crédito
    PIX = "pix"             # PIX


# === CONFIGURAÇÕES DE HARDWARE ===
class HardwareConfig:
    """Configurações do Raspberry Pi e periféricos"""
    
    # GPIO do aceitador de notas (pino físico 11 = GPIO 17)
    GPIO_BILL_ACCEPTOR = int(os.getenv('GPIO_BILL_ACCEPTOR', '17'))
    
    # Valor monetário de cada pulso recebido
    PULSE_VALUE = float(os.getenv('PULSE_VALUE', '2.00'))
    
    # Tempo mínimo entre pulsos para evitar ruído (milissegundos)
    DEBOUNCE_MS = int(os.getenv('DEBOUNCE_MS', '200'))
    
    # Ativar módulo de hardware (True/False)
    ENABLED = os.getenv('HARDWARE_ENABLED', 'true').lower() == 'true'


# === CONFIGURAÇÕES DE PAGAMENTO DIGITAL ===
class PaymentGatewayConfig:
    """Configurações do gateway de pagamento (Mercado Pago, Stone, etc.)"""
    
    # Provedor do gateway (mercadopago, stone, pagseguro)
    PROVIDER = os.getenv('PAYMENT_PROVIDER', 'mercadopago')
    
    # Credenciais da API
    API_KEY = os.getenv('PAYMENT_API_KEY', '')
    ACCESS_TOKEN = os.getenv('PAYMENT_ACCESS_TOKEN', '')
    
    # URL de callback para webhooks
    WEBHOOK_URL = os.getenv('PAYMENT_WEBHOOK_URL', 'https://seu-dominio.com/webhook')
    
    # Timeout para requisições (segundos)
    TIMEOUT = int(os.getenv('PAYMENT_TIMEOUT', '30'))
    
    # Ativar pagamento digital (True/False)
    ENABLED = os.getenv('PAYMENT_DIGITAL_ENABLED', 'true').lower() == 'true'


# === CONFIGURAÇÕES DE NEGÓCIO ===
class BusinessConfig:
    """Regras de negócio da Jukebox"""
    
    # Preço base por música
    PRICE_PER_SONG = float(os.getenv('PRICE_PER_SONG', '5.00'))
    
    # Taxa adicional para cartão de crédito (percentual)
    CREDIT_CARD_FEE = float(os.getenv('CREDIT_CARD_FEE', '3.99'))  # 3.99%
    
    # Taxa adicional para débito (percentual)
    DEBIT_CARD_FEE = float(os.getenv('DEBIT_CARD_FEE', '1.99'))  # 1.99%
    
    # Taxa para PIX (geralmente zero)
    PIX_FEE = float(os.getenv('PIX_FEE', '0.00'))
    
    # Taxa para dinheiro (zero)
    CASH_FEE = float(os.getenv('CASH_FEE', '0.00'))
    
    # Limite de músicas na fila de espera
    MAX_QUEUE_SIZE = int(os.getenv('MAX_QUEUE_SIZE', '10'))
    
    # Tempo de inatividade antes de voltar à tela inicial (segundos)
    IDLE_TIMEOUT = int(os.getenv('IDLE_TIMEOUT', '300'))
    
    # Métodos de pagamento habilitados (separados por vírgula)
    ENABLED_PAYMENT_METHODS = os.getenv(
        'ENABLED_PAYMENT_METHODS', 
        'cash,debit,credit,pix'
    ).split(',')
    
    @classmethod
    def calculate_price(cls, payment_method: PaymentMethod) -> float:
        """Calcula o preço final com base no método de pagamento"""
        base_price = cls.PRICE_PER_SONG
        
        fee_map = {
            PaymentMethod.CASH: cls.CASH_FEE,
            PaymentMethod.DEBIT: cls.DEBIT_CARD_FEE,
            PaymentMethod.CREDIT: cls.CREDIT_CARD_FEE,
            PaymentMethod.PIX: cls.PIX_FEE
        }
        
        fee_percent = fee_map.get(payment_method, 0.0)
        return round(base_price * (1 + fee_percent / 100), 2)


# === CONFIGURAÇÕES DO FLASK ===
class FlaskConfig:
    """Configurações do servidor web"""
    
    ENV = os.getenv('FLASK_ENV', 'production')
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key-CHANGE-THIS')
    
    # Token para autenticar requisições do hardware
    HARDWARE_TOKEN = os.getenv('HARDWARE_TOKEN', 'hardware-token-123')
    
    # Token para validar webhooks do gateway
    WEBHOOK_SECRET = os.getenv('WEBHOOK_SECRET', 'webhook-secret-456')
    
    PORT = int(os.getenv('FLASK_PORT', '5000'))
    HOST = os.getenv('FLASK_HOST', '0.0.0.0')
    
    # CORS permitido (para testes locais)
    CORS_ORIGINS = os.getenv('CORS_ORIGINS', '*')


# === CONFIGURAÇÕES DO YOUTUBE ===
class YouTubeConfig:
    """Configurações do player YouTube com Selenium"""
    
    CHROME_DRIVER_PATH = os.getenv('CHROME_DRIVER_PATH', '/usr/bin/chromedriver')
    AUTOPLAY = os.getenv('YOUTUBE_AUTOPLAY', 'true').lower() == 'true'
    WAIT_TIMEOUT = int(os.getenv('SELENIUM_TIMEOUT', '10'))
    
    # User-Agent para evitar detecção de bot
    USER_AGENT = os.getenv(
        'CHROME_USER_AGENT',
        'Mozilla/5.0 (X11; Linux armv7l) AppleWebKit/537.36 Chrome/120.0.0.0'
    )
    
    # Configurações de música idle (quando não há atividade)
    IDLE_MUSIC_ENABLED = os.getenv('IDLE_MUSIC_ENABLED', 'true').lower() == 'true'
    IDLE_MUSIC_TIMEOUT = int(os.getenv('IDLE_MUSIC_TIMEOUT', '600'))  # 10 minutos em segundos
    
    # Lista de categorias/termos de busca para músicas aleatórias
    # Focado em música real para evitar outros tipos de conteúdo
    IDLE_MUSIC_QUERIES = os.getenv(
        'IDLE_MUSIC_QUERIES',
        'top hits 2024,best pop songs,rock classics,jazz music,bossa nova,MPB brasileira,'
        'samba clássico,música internacional,best songs,hit songs'
    ).split(',')
    
    # Habilitar ad-blocking avançado
    ADBLOCK_ENABLED = os.getenv('ADBLOCK_ENABLED', 'true').lower() == 'true'


# === CONFIGURAÇÕES DO BANCO DE DADOS ===
class DatabaseConfig:
    """Configurações do SQLite"""
    
    DB_PATH = Path(os.getenv('DB_PATH', BASE_DIR / 'src' / 'db' / 'jukebox.db'))
    DB_PATH.parent.mkdir(parents=True, exist_ok=True)


# === CONFIGURAÇÕES DE LOGGING ===
class LogConfig:
    """Configurações de logs do sistema"""
    
    LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_FILE = Path(os.getenv('LOG_FILE', BASE_DIR / 'logs' / 'jukebox.log'))
    LOG_FILE.parent.mkdir(parents=True, exist_ok=True)
    
    # Formato das mensagens
    FORMAT = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    
    # Rotação de logs (tamanho máximo 10MB)
    MAX_BYTES = int(os.getenv('LOG_MAX_BYTES', '10485760'))
    BACKUP_COUNT = int(os.getenv('LOG_BACKUP_COUNT', '5'))
