"""
Controlador do YouTube com Selenium
Busca e reproduz músicas automaticamente
"""

import logging
import time
import random
from typing import Optional, List, Dict
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from src.server.config import YouTubeConfig

logger = logging.getLogger(__name__)


class YouTubePlayer:
    """
    Controlador do YouTube para buscar e reproduzir músicas
    Usa Selenium WebDriver
    """
    
    def __init__(self):
        self.driver: Optional[webdriver.Chrome] = None
        self.config = YouTubeConfig
        self.current_video_id: Optional[str] = None
        self._initialize_driver()
    
    def _initialize_driver(self):
        """Inicializa Chrome WebDriver com opções otimizadas"""
        try:
            options = webdriver.ChromeOptions()
            
            # Opções para modo kiosk/embedded
            options.add_argument('--start-maximized')
            options.add_argument('--disable-infobars')
            options.add_argument('--disable-notifications')
            options.add_argument('--disable-popup-blocking')
            options.add_argument(f'user-agent={self.config.USER_AGENT}')
            
            # Desabilita automação detectável
            options.add_experimental_option("excludeSwitches", ["enable-automation"])
            options.add_experimental_option('useAutomationExtension', False)
            
            # Para Raspberry Pi - otimizações de performance
            options.add_argument('--disable-gpu')
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
            
            # Ad-blocking avançado se habilitado
            if self.config.ADBLOCK_ENABLED:
                # Bloqueia domínios de anúncios conhecidos
                options.add_argument('--disable-background-networking')
                options.add_argument('--disable-default-apps')
                options.add_argument('--disable-sync')
                
                # Preferências para bloquear anúncios
                prefs = {
                    'profile.default_content_setting_values': {
                        'notifications': 2,
                        'media_stream': 2,
                    }
                }
                options.add_experimental_option('prefs', prefs)
            
            self.driver = webdriver.Chrome(options=options)
            self.wait = WebDriverWait(self.driver, self.config.WAIT_TIMEOUT)
            
            # Injeta script para bloquear anúncios adicionalmente
            if self.config.ADBLOCK_ENABLED:
                self._inject_adblock_script()
            
            log_msg = "Chrome WebDriver inicializado"
            if self.config.ADBLOCK_ENABLED:
                log_msg += " com ad-blocking"
            logger.info(log_msg)
            
        except Exception as e:
            logger.error(f"Erro ao inicializar WebDriver: {e}")
            self.driver = None
    
    def search_and_play(self, query: str) -> Optional[Dict]:
        """
        Busca música no YouTube e reproduz o primeiro resultado
        
        Args:
            query: Termo de busca (ex: "Nome da Música - Artista")
        
        Returns:
            Dict com video_id, title, duration (ou None se falhar)
        """
        if not self.driver:
            logger.error("WebDriver não inicializado")
            return None
        
        try:
            # Navega para YouTube
            self.driver.get("https://www.youtube.com")
            time.sleep(2)
            
            # Busca campo de pesquisa
            search_box = self.wait.until(
                EC.presence_of_element_located((By.NAME, "search_query"))
            )
            
            # Digita query e pressiona Enter
            search_box.clear()
            search_box.send_keys(query)
            search_box.send_keys(Keys.RETURN)
            
            # Aguarda resultados
            time.sleep(3)
            
            # Clica no primeiro vídeo (não anúncio)
            video_element = self.wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, "ytd-video-renderer"))
            )
            
            # Extrai informações do vídeo
            video_info = self._extract_video_info(video_element)
            
            # Clica no vídeo
            video_link = video_element.find_element(By.ID, "video-title")
            video_link.click()
            
            # Aguarda carregamento do vídeo
            time.sleep(3)
            
            # Tenta pular anúncio se aparecer
            self._skip_ad_if_present()
            
            # Extrai video_id da URL
            current_url = self.driver.current_url
            video_id = self._extract_video_id_from_url(current_url)
            
            if video_id:
                self.current_video_id = video_id
                video_info['video_id'] = video_id
                logger.info(f"Reproduzindo: {video_info.get('title')} ({video_id})")
                return video_info
            
        except TimeoutException:
            logger.error("Timeout ao buscar música")
        except Exception as e:
            logger.error(f"Erro ao buscar e reproduzir: {e}")
        
        return None
    
    def play_video(self, video_id: str) -> bool:
        """
        Reproduz vídeo diretamente pelo ID
        
        Args:
            video_id: ID do vídeo do YouTube
        
        Returns:
            True se sucesso, False caso contrário
        """
        if not self.driver:
            return False
        
        try:
            url = f"https://www.youtube.com/watch?v={video_id}"
            self.driver.get(url)
            time.sleep(3)
            
            self._skip_ad_if_present()
            self.current_video_id = video_id
            
            logger.info(f"Reproduzindo vídeo: {video_id}")
            return True
            
        except Exception as e:
            logger.error(f"Erro ao reproduzir vídeo: {e}")
            return False
    
    def _skip_ad_if_present(self):
        """Tenta pular anúncio se estiver presente"""
        try:
            # Aguarda botão "Pular anúncio" (máximo 5 segundos)
            skip_button = WebDriverWait(self.driver, 5).until(
                EC.element_to_be_clickable((By.CLASS_NAME, "ytp-ad-skip-button"))
            )
            skip_button.click()
            logger.info("Anúncio pulado")
        except TimeoutException:
            # Sem anúncio ou não pode pular ainda
            pass
        except Exception as e:
            logger.debug(f"Erro ao pular anúncio: {e}")
        
        # Tenta outros seletores de botão de pular anúncio
        try:
            skip_selectors = [
                ".ytp-ad-skip-button-modern",
                ".ytp-skip-ad-button",
                "button[aria-label*='Skip']",
                "button.ytp-ad-skip-button"
            ]
            for selector in skip_selectors:
                try:
                    skip_btn = self.driver.find_element(By.CSS_SELECTOR, selector)
                    if skip_btn.is_displayed():
                        skip_btn.click()
                        logger.info(f"Anúncio pulado via seletor: {selector}")
                        break
                except:
                    continue
        except Exception as e:
            logger.debug(f"Erro ao tentar seletores adicionais: {e}")
    
    def _inject_adblock_script(self):
        """Injeta script JavaScript para bloquear anúncios"""
        if not self.driver:
            return
        
        adblock_js = """
        // Script para bloquear elementos de anúncio no YouTube
        (function() {
            const blockAds = () => {
                // Remove overlays de anúncio
                const adOverlays = document.querySelectorAll('.ytp-ad-overlay-container, .ytp-ad-text-overlay');
                adOverlays.forEach(el => el.remove());
                
                // Remove banners de anúncio
                const adBanners = document.querySelectorAll('[id*="ad-"], [class*="ad-"]');
                adBanners.forEach(el => {
                    if (el.tagName !== 'VIDEO' && el.offsetHeight < 200) {
                        el.remove();
                    }
                });
                
                // Acelera anúncios de vídeo (se houver)
                const video = document.querySelector('video');
                if (video && document.querySelector('.ad-showing, .video-ads')) {
                    video.playbackRate = 16;
                    video.muted = true;
                }
            };
            
            // Executa periodicamente
            setInterval(blockAds, 1000);
            blockAds();
        })();
        """
        
        try:
            self.driver.execute_script(adblock_js)
            logger.info("Script de ad-blocking injetado")
        except Exception as e:
            logger.debug(f"Erro ao injetar script de adblock: {e}")
    
    def _extract_video_info(self, element) -> Dict:
        """Extrai informações do vídeo do elemento de resultado"""
        try:
            title_element = element.find_element(By.ID, "video-title")
            title = title_element.get_attribute("title")
            
            # Tenta extrair duração
            try:
                duration_element = element.find_element(By.CLASS_NAME, "ytd-thumbnail-overlay-time-status-renderer")
                duration_text = duration_element.text
            except:
                duration_text = "Desconhecida"
            
            return {
                "title": title,
                "duration_text": duration_text
            }
        except Exception as e:
            logger.error(f"Erro ao extrair informações: {e}")
            return {"title": "Desconhecido", "duration_text": "Desconhecida"}
    
    def _extract_video_id_from_url(self, url: str) -> Optional[str]:
        """Extrai video_id da URL do YouTube"""
        try:
            if "watch?v=" in url:
                return url.split("watch?v=")[1].split("&")[0]
        except:
            pass
        return None
    
    def is_playing(self) -> bool:
        """Verifica se há vídeo tocando"""
        if not self.driver or not self.current_video_id:
            return False
        
        try:
            # Verifica se player está presente e tocando
            player = self.driver.find_element(By.CLASS_NAME, "html5-video-player")
            player_state = player.get_attribute("class")
            
            # Se contém "playing-mode", está tocando
            return "playing-mode" in player_state
            
        except Exception:
            return False
    
    def pause(self):
        """Pausa reprodução"""
        if not self.driver:
            return
        
        try:
            video = self.driver.find_element(By.TAG_NAME, "video")
            self.driver.execute_script("arguments[0].pause()", video)
            logger.info("Vídeo pausado")
        except Exception as e:
            logger.error(f"Erro ao pausar: {e}")
    
    def resume(self):
        """Retoma reprodução"""
        if not self.driver:
            return
        
        try:
            video = self.driver.find_element(By.TAG_NAME, "video")
            self.driver.execute_script("arguments[0].play()", video)
            logger.info("Vídeo retomado")
        except Exception as e:
            logger.error(f"Erro ao retomar: {e}")
    
    def set_volume(self, level: int):
        """
        Define volume (0-100)
        
        Args:
            level: Nível de volume (0-100)
        """
        if not self.driver:
            return
        
        try:
            volume = max(0, min(100, level)) / 100.0
            video = self.driver.find_element(By.TAG_NAME, "video")
            self.driver.execute_script(f"arguments[0].volume = {volume}", video)
            logger.info(f"Volume definido: {level}%")
        except Exception as e:
            logger.error(f"Erro ao definir volume: {e}")
    
    def play_random_music(self) -> Optional[Dict]:
        """
        Reproduz uma música aleatória de uma categoria musical
        Usado para evitar silêncio quando não há atividade
        
        Returns:
            Dict com informações do vídeo ou None se falhar
        """
        if not self.driver:
            logger.error("WebDriver não inicializado")
            return None
        
        try:
            # Escolhe uma categoria aleatória
            queries = self.config.IDLE_MUSIC_QUERIES
            if not queries:
                logger.warning("Nenhuma categoria de música idle configurada")
                return None
            
            query = random.choice(queries).strip()
            logger.info(f"Tocando música aleatória da categoria: {query}")
            
            # Busca e reproduz
            result = self.search_and_play(query)
            
            if result:
                logger.info(f"Música idle reproduzida: {result.get('title')}")
            
            return result
            
        except Exception as e:
            logger.error(f"Erro ao tocar música aleatória: {e}")
            return None
    
    def close(self):
        """Fecha navegador e limpa recursos"""
        if self.driver:
            try:
                self.driver.quit()
                logger.info("WebDriver fechado")
            except Exception as e:
                logger.error(f"Erro ao fechar WebDriver: {e}")
            finally:
                self.driver = None
                self.current_video_id = None
    
    def __del__(self):
        """Destrutor - garante fechamento do driver"""
        self.close()
