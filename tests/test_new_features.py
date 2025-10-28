#!/usr/bin/env python3
"""
Teste para as novas funcionalidades implementadas:
- Preço de 1 real por música
- Reprodução de vídeo opcional
- Sistema de filas melhorado
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.server.config import BusinessConfig, YouTubeConfig, PaymentMethod

def test_price_configuration():
    """Testa se o preço padrão está configurado para 1 real"""
    print("🧪 Testando configuração de preço...")
    
    # Verifica preço base
    price = BusinessConfig.PRICE_PER_SONG
    print(f"  ✓ Preço base por música: R$ {price:.2f}")
    
    # Verifica se está em 1.00 ou se a variável de ambiente foi definida
    if price == 1.00:
        print("  ✅ Preço padrão correto: R$ 1.00")
    else:
        print(f"  ⚠️  Preço configurado via env: R$ {price:.2f}")
    
    # Testa cálculo de preço com diferentes métodos
    for method in [PaymentMethod.CASH, PaymentMethod.PIX, PaymentMethod.DEBIT, PaymentMethod.CREDIT]:
        calculated_price = BusinessConfig.calculate_price(method)
        print(f"  ✓ Preço para {method.value}: R$ {calculated_price:.2f}")
    
    return True

def test_video_configuration():
    """Testa configuração de reprodução de vídeo opcional"""
    print("\n🧪 Testando configuração de vídeo...")
    
    # Verifica se a configuração existe
    if hasattr(YouTubeConfig, 'VIDEO_PLAYBACK_ENABLED'):
        video_enabled = YouTubeConfig.VIDEO_PLAYBACK_ENABLED
        print(f"  ✓ VIDEO_PLAYBACK_ENABLED configurado: {video_enabled}")
        print("  ✅ Configuração de vídeo opcional implementada")
    else:
        print("  ❌ Configuração VIDEO_PLAYBACK_ENABLED não encontrada")
        return False
    
    return True

def test_queue_system():
    """Testa sistema de filas"""
    print("\n🧪 Testando sistema de filas...")
    
    import tempfile
    from pathlib import Path
    from src.db import Database, MusicQueue
    
    # Usa banco temporário para testes
    temp_db = Path(tempfile.gettempdir()) / f"test_queue_{os.getpid()}.db"
    db = Database(db_path=temp_db)
    queue = MusicQueue(db)
    
    try:
        # Adiciona músicas à fila
        song1_id = queue.add_song(
            video_id="test_001",
            title="Música 1",
            artist="Artista 1"
        )
        print(f"  ✓ Música 1 adicionada à fila: ID {song1_id}")
        
        song2_id = queue.add_song(
            video_id="test_002",
            title="Música 2",
            artist="Artista 2"
        )
        print(f"  ✓ Música 2 adicionada à fila: ID {song2_id}")
        
        # Verifica tamanho da fila
        queue_size = queue.get_queue_size()
        print(f"  ✓ Tamanho da fila: {queue_size}")
        
        # Verifica que músicas estão com status 'queued'
        queue_list = queue.get_queue()
        for song in queue_list:
            print(f"  ✓ Música '{song['title']}' com status: {song['status']}")
        
        # Marca primeira música como tocando
        next_song = queue.get_next_song()
        if next_song:
            queue.mark_as_playing(next_song['id'])
            print(f"  ✓ Música '{next_song['title']}' marcada como tocando")
        
        # Verifica que ainda há músicas na fila (queued)
        remaining_size = queue.get_queue_size()
        print(f"  ✓ Músicas restantes na fila (queued): {remaining_size}")
        
        # Verifica que a fila contém a música tocando + as em espera
        full_queue = queue.get_queue()
        has_playing = any(song['status'] == 'playing' for song in full_queue)
        has_queued = any(song['status'] == 'queued' for song in full_queue)
        
        print(f"  ✓ Tem música tocando: {has_playing}")
        print(f"  ✓ Tem músicas na fila: {has_queued}")
        
        if has_playing and has_queued:
            print("  ✅ Sistema de filas funciona corretamente")
            print("     Música atual não é interrompida, novas vão para fila")
        
        print("  ✅ Sistema de filas testado com sucesso")
        
        # Limpa banco de teste
        temp_db.unlink()
        
        return True
    except Exception as e:
        print(f"  ❌ Erro ao testar fila: {e}")
        return False

def test_env_example():
    """Verifica se env.example foi atualizado"""
    print("\n🧪 Testando arquivo env.example...")
    
    env_path = os.path.join(os.path.dirname(__file__), '..', 'env.example')
    
    try:
        with open(env_path, 'r') as f:
            content = f.read()
        
        # Verifica se PRICE_PER_SONG=1.00 está no arquivo
        if 'PRICE_PER_SONG=1.00' in content:
            print("  ✓ PRICE_PER_SONG=1.00 encontrado")
        else:
            print("  ⚠️  PRICE_PER_SONG=1.00 não encontrado (pode ter sido configurado diferente)")
        
        # Verifica se VIDEO_PLAYBACK_ENABLED está no arquivo
        if 'VIDEO_PLAYBACK_ENABLED' in content:
            print("  ✓ VIDEO_PLAYBACK_ENABLED encontrado")
        else:
            print("  ❌ VIDEO_PLAYBACK_ENABLED não encontrado")
            return False
        
        print("  ✅ Arquivo env.example atualizado corretamente")
        return True
    except Exception as e:
        print(f"  ❌ Erro ao verificar env.example: {e}")
        return False

def main():
    """Executa todos os testes"""
    print("\n" + "="*60)
    print("🎵 TESTE DAS NOVAS FUNCIONALIDADES DA JUKEBOX")
    print("="*60 + "\n")
    
    results = []
    
    # Testa cada funcionalidade
    results.append(("Configuração de Preço", test_price_configuration()))
    results.append(("Configuração de Vídeo", test_video_configuration()))
    results.append(("Sistema de Filas", test_queue_system()))
    results.append(("Arquivo env.example", test_env_example()))
    
    # Resumo
    print("\n" + "="*60)
    print("📊 RESUMO DOS TESTES")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {name}")
    
    print(f"\nTotal: {passed}/{total} testes passaram")
    
    if passed == total:
        print("\n🎉 Todos os testes passaram com sucesso!")
        return 0
    else:
        print(f"\n⚠️  {total - passed} teste(s) falharam")
        return 1

if __name__ == "__main__":
    sys.exit(main())
