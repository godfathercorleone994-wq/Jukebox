"""
Controlador do aceitador de notas JCM WBA10
Detecta pulsos GPIO e converte em créditos
"""

import logging
from typing import Callable, Optional
from src.server.config import HardwareConfig

# Inicializa logger
logger = logging.getLogger(__name__)

# Tenta importar RPi.GPIO (disponível apenas no Raspberry Pi)
try:
    import RPi.GPIO as GPIO
    GPIO_AVAILABLE = True
except (ImportError, RuntimeError):
    GPIO_AVAILABLE = False
    logger.warning("RPi.GPIO não disponível - modo simulação ativado")


class BillAcceptor:
    """
    Controlador do aceitador de notas via GPIO
    Detecta pulsos e acumula créditos
    """
    
    def __init__(
        self,
        gpio_pin: int = None,
        pulse_value: float = None,
        debounce_ms: int = None,
        callback: Optional[Callable[[float], None]] = None
    ):
        """
        Args:
            gpio_pin: Número do pino GPIO (padrão: config.GPIO_BILL_ACCEPTOR)
            pulse_value: Valor monetário por pulso (padrão: config.PULSE_VALUE)
            debounce_ms: Tempo de debounce em ms (padrão: config.DEBOUNCE_MS)
            callback: Função chamada quando crédito é detectado
        """
        self.gpio_pin = gpio_pin or HardwareConfig.GPIO_BILL_ACCEPTOR
        self.pulse_value = pulse_value or HardwareConfig.PULSE_VALUE
        self.debounce_ms = debounce_ms or HardwareConfig.DEBOUNCE_MS
        self.callback = callback
        self.enabled = HardwareConfig.ENABLED and GPIO_AVAILABLE
        self._initialized = False
        
        if self.enabled:
            self._setup_gpio()
        else:
            logger.info("Hardware desabilitado ou GPIO não disponível")
    
    def _setup_gpio(self):
        """Configura GPIO para detectar pulsos"""
        try:
            # Configura modo BCM (numeração GPIO)
            GPIO.setmode(GPIO.BCM)
            
            # Configura pino como entrada com pull-down
            GPIO.setup(self.gpio_pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
            
            # Adiciona detector de borda (rising edge)
            GPIO.add_event_detect(
                self.gpio_pin,
                GPIO.RISING,
                callback=self._pulse_detected,
                bouncetime=self.debounce_ms
            )
            
            self._initialized = True
            logger.info(
                f"GPIO configurado - Pino: {self.gpio_pin}, "
                f"Valor por pulso: R$ {self.pulse_value:.2f}"
            )
            
        except Exception as e:
            logger.error(f"Erro ao configurar GPIO: {e}")
            self.enabled = False
    
    def _pulse_detected(self, channel):
        """Callback chamado quando pulso é detectado"""
        logger.info(f"Pulso detectado - Crédito adicionado: R$ {self.pulse_value:.2f}")
        
        if self.callback:
            try:
                self.callback(self.pulse_value)
            except Exception as e:
                logger.error(f"Erro no callback: {e}")
    
    def simulate_pulse(self, count: int = 1):
        """
        Simula pulsos do aceitador (para testes)
        
        Args:
            count: Número de pulsos a simular
        """
        if not self.enabled:
            logger.info(f"Simulando {count} pulso(s)")
            
            for _ in range(count):
                if self.callback:
                    self.callback(self.pulse_value)
        else:
            logger.warning("Simulação não disponível - hardware real ativo")
    
    def cleanup(self):
        """Limpa recursos GPIO"""
        if self.enabled and self._initialized:
            try:
                GPIO.remove_event_detect(self.gpio_pin)
                GPIO.cleanup(self.gpio_pin)
                logger.info("GPIO limpo com sucesso")
            except Exception as e:
                logger.error(f"Erro ao limpar GPIO: {e}")
    
    def __del__(self):
        """Destrutor - garante limpeza do GPIO"""
        self.cleanup()
