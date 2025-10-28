"""
Gerenciador de música idle para a Jukebox
Toca músicas aleatórias quando não há atividade do usuário
"""

import logging
import threading
import time
from typing import Optional
from datetime import datetime, timedelta
from src.server.config import YouTubeConfig

logger = logging.getLogger(__name__)

# Constantes de configuração
MONITOR_INTERVAL_SECONDS = 30  # Intervalo de verificação do monitor
IDLE_RETRY_FACTOR = 0.5  # Fator para calcular próximo retry (metade do timeout)
THREAD_SHUTDOWN_TIMEOUT = 5  # Timeout para desligar thread em segundos


class IdleMusicManager:
    """
    Gerencia a reprodução automática de músicas quando não há atividade
    Evita silêncio prolongado na jukebox
    """
    
    def __init__(self, youtube_player=None):
        """
        Inicializa o gerenciador de música idle
        
        Args:
            youtube_player: Instância do YouTubePlayer
        """
        self.youtube_player = youtube_player
        self.config = YouTubeConfig
        self.last_activity = datetime.now()
        self.running = False
        self.thread = None
        self._lock = threading.Lock()
        
        logger.info("Idle Music Manager inicializado")
    
    def update_activity(self):
        """Atualiza o timestamp da última atividade do usuário"""
        with self._lock:
            self.last_activity = datetime.now()
            logger.debug("Atividade do usuário registrada")
    
    def get_idle_time(self) -> float:
        """
        Retorna o tempo em segundos desde a última atividade
        
        Returns:
            Tempo em segundos desde a última atividade
        """
        with self._lock:
            return (datetime.now() - self.last_activity).total_seconds()
    
    def is_idle(self) -> bool:
        """
        Verifica se o sistema está ocioso (sem atividade por mais tempo que o configurado)
        
        Returns:
            True se está ocioso, False caso contrário
        """
        return self.get_idle_time() >= self.config.IDLE_MUSIC_TIMEOUT
    
    def _monitor_loop(self):
        """Loop de monitoramento que roda em background"""
        logger.info("Thread de monitoramento iniciada")
        
        while self.running:
            try:
                # Verifica se está ocioso
                if self.is_idle() and self.config.IDLE_MUSIC_ENABLED:
                    idle_time = self.get_idle_time()
                    logger.info(f"Sistema ocioso por {idle_time:.0f}s - tocando música aleatória")
                    
                    # Toca música aleatória
                    if self.youtube_player:
                        try:
                            result = self.youtube_player.play_random_music()
                            if result:
                                logger.info(f"Música idle tocada com sucesso: {result.get('title')}")
                            else:
                                logger.warning("Falha ao tocar música idle")
                        except Exception as e:
                            logger.error(f"Erro ao tocar música idle: {e}")
                    
                    # Atualiza atividade para evitar múltiplas reproduções seguidas
                    # Aguarda pelo menos metade do timeout antes da próxima música
                    self.update_activity()
                    time.sleep(self.config.IDLE_MUSIC_TIMEOUT * IDLE_RETRY_FACTOR)
                else:
                    # Verifica a cada intervalo configurado
                    time.sleep(MONITOR_INTERVAL_SECONDS)
                    
            except Exception as e:
                logger.error(f"Erro no loop de monitoramento: {e}")
                time.sleep(30)
        
        logger.info("Thread de monitoramento finalizada")
    
    def start(self):
        """Inicia o monitoramento de inatividade"""
        if not self.config.IDLE_MUSIC_ENABLED:
            logger.info("Música idle desabilitada na configuração")
            return
        
        if self.running:
            logger.warning("Gerenciador já está em execução")
            return
        
        if not self.youtube_player:
            logger.warning("YouTube player não configurado - idle music não será iniciado")
            return
        
        self.running = True
        self.thread = threading.Thread(target=self._monitor_loop, daemon=True)
        self.thread.start()
        
        logger.info(
            f"Idle Music Manager iniciado (timeout: {self.config.IDLE_MUSIC_TIMEOUT}s)"
        )
    
    def stop(self):
        """Para o monitoramento de inatividade"""
        if not self.running:
            return
        
        logger.info("Parando Idle Music Manager...")
        self.running = False
        
        if self.thread:
            self.thread.join(timeout=THREAD_SHUTDOWN_TIMEOUT)
            self.thread = None
        
        logger.info("Idle Music Manager parado")
    
    def __del__(self):
        """Destrutor - garante que a thread seja parada"""
        self.stop()
