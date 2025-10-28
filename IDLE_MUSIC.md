# 🎵 Sistema de Música Idle e Ad-Blocking - Documentação

## 📋 Visão Geral

Este documento descreve as novas funcionalidades adicionadas ao Jukebox:

1. **Sistema de Música Idle** - Reprodução automática de músicas quando não há atividade
2. **Ad-Blocking Avançado** - Sistema melhorado de bloqueio de anúncios no YouTube

## 🎧 Sistema de Música Idle

### O que é?

O sistema de música idle garante que a jukebox nunca fique em silêncio. Quando ninguém adiciona créditos ou músicas por um período configurável (padrão: 10 minutos), o sistema automaticamente reproduz músicas aleatórias de categorias pré-definidas.

### Funcionalidades

- ✅ Monitoramento contínuo de atividade do usuário
- ✅ Reprodução automática após período de inatividade
- ✅ Categorias de música personalizáveis
- ✅ Foco em música real (evita outros tipos de conteúdo)
- ✅ Configuração flexível via variáveis de ambiente

### Como Funciona

1. **Monitoramento**: Uma thread em background monitora a última atividade do usuário
2. **Detecção**: Quando o tempo idle ultrapassa o timeout configurado (padrão: 600s)
3. **Reprodução**: O sistema escolhe aleatoriamente uma categoria de música
4. **Busca**: Busca e reproduz automaticamente no YouTube
5. **Reset**: Atualiza o timer de atividade para evitar reproduções múltiplas seguidas

### Atividades que Resetam o Timer

- Inserção de dinheiro no aceitador de notas
- Criação de pagamentos (PIX, débito, crédito)
- Adição de músicas à fila

### Configuração

No arquivo `.env`:

```bash
# Habilitar YouTube player (requer display conectado)
YOUTUBE_ENABLED=true

# Habilitar/desabilitar sistema de música idle
IDLE_MUSIC_ENABLED=true

# Tempo de espera antes de tocar música (em segundos)
# Padrão: 600 (10 minutos)
IDLE_MUSIC_TIMEOUT=600

# Categorias de música (separadas por vírgula)
IDLE_MUSIC_QUERIES=top hits 2024,best pop songs,rock classics,jazz music,bossa nova,MPB brasileira,samba clássico,música internacional,best songs,hit songs
```

### Categorias Padrão

As categorias foram cuidadosamente escolhidas para garantir música de qualidade:

- **top hits 2024** - Sucessos atuais
- **best pop songs** - Melhores músicas pop
- **rock classics** - Clássicos do rock
- **jazz music** - Jazz
- **bossa nova** - Bossa nova
- **MPB brasileira** - Música Popular Brasileira
- **samba clássico** - Samba clássico
- **música internacional** - Variedades internacionais
- **best songs** - Melhores músicas
- **hit songs** - Músicas de sucesso

Você pode personalizar essas categorias editando a variável `IDLE_MUSIC_QUERIES`.

### API Endpoints

#### GET /api/idle/status

Retorna informações sobre o sistema idle:

```json
{
  "enabled": true,
  "timeout": 600,
  "idle_time": 120.5,
  "is_idle": false,
  "categories": ["top hits 2024", "best pop songs", ...]
}
```

#### POST /api/idle/trigger (Desenvolvimento)

Força reprodução de música idle para testes.

### Arquivos Modificados/Criados

- `src/server/config.py` - Adicionadas configurações do YouTube idle
- `src/youtube/idle_music_manager.py` - **NOVO** - Gerenciador de música idle
- `src/youtube/youtube_player.py` - Adicionado método `play_random_music()`
- `src/server/app.py` - Integração do gerenciador idle
- `env.example` - Novas variáveis de configuração

## 🚫 Sistema de Ad-Blocking Avançado

### O que é?

Sistema melhorado de bloqueio de anúncios no YouTube, combinando múltiplas técnicas para garantir uma experiência sem interrupções.

### Técnicas Implementadas

1. **Configuração do Chrome**
   - Desabilitação de background networking
   - Bloqueio de notificações
   - Bloqueio de pop-ups
   - Configurações de privacidade otimizadas

2. **JavaScript Injection**
   - Script injetado que remove elementos de anúncio do DOM
   - Remoção de overlays de anúncio
   - Remoção de banners
   - Aceleração de anúncios de vídeo (quando não puláveis)

3. **Múltiplos Seletores de Skip**
   - Suporte a diferentes versões de botões "Pular"
   - `.ytp-ad-skip-button`
   - `.ytp-ad-skip-button-modern`
   - `.ytp-skip-ad-button`
   - `button[aria-label*='Skip']`

4. **Execução Contínua**
   - Script roda a cada 1 segundo para bloquear anúncios dinamicamente
   - Funciona com anúncios que aparecem durante a reprodução

### Como Funciona

1. **Inicialização**: Configurações de ad-blocking são aplicadas ao Chrome
2. **Script Injection**: Script JavaScript é injetado na página
3. **Monitoramento**: Script executa continuamente em background
4. **Bloqueio**: Remove elementos de anúncio assim que detectados
5. **Skip Automático**: Clica automaticamente em botões de pular

### Configuração

No arquivo `.env`:

```bash
# Habilitar/desabilitar ad-blocking
ADBLOCK_ENABLED=true
```

### Limitações

- Não bloqueia 100% dos anúncios (YouTube atualiza constantemente)
- Alguns anúncios podem aparecer brevemente antes de serem bloqueados
- Funciona melhor com Chrome/Chromium atualizado

### Código JavaScript Injetado

```javascript
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
```

### Arquivos Modificados

- `src/server/config.py` - Configuração `ADBLOCK_ENABLED`
- `src/youtube/youtube_player.py` - Melhorias no `_skip_ad_if_present()` e novo `_inject_adblock_script()`

## 🧪 Testes

Os testes foram atualizados para incluir verificações das novas funcionalidades:

```bash
python3 tests/test_jukebox.py
```

Novos testes incluem:
- `test_youtube_config()` - Verifica configurações do YouTube
- `test_idle_music()` - Testa gerenciador de música idle

## 📊 Impacto no Sistema

### Performance

- **Thread adicional**: Uma thread em background para monitoramento idle (~10KB memória)
- **Polling intervalo**: Verificação a cada 30 segundos quando não idle
- **CPU mínimo**: < 0.1% de uso de CPU em estado ocioso
- **Script JavaScript**: ~2KB injetado na página do YouTube

### Compatibilidade

- ✅ Raspberry Pi 3 e 4
- ✅ Chrome/Chromium 80+
- ✅ Python 3.9+
- ✅ Selenium 4.x

## 🔧 Troubleshooting

### Música idle não está tocando

1. Verifique se o YouTube player está habilitado: `YOUTUBE_ENABLED=true` no `.env`
2. Verifique se está habilitado: `IDLE_MUSIC_ENABLED=true`
3. Certifique-se de que o Raspberry Pi tem um display conectado
4. Verifique o timeout: aguarde pelo menos `IDLE_MUSIC_TIMEOUT` segundos
5. Verifique logs: `tail -f logs/jukebox.log`
6. Procure por mensagens de erro durante a inicialização

### Anúncios ainda aparecem

1. Verifique se está habilitado: `ADBLOCK_ENABLED=true`
2. Atualize o Chrome/Chromium para versão mais recente
3. Alguns anúncios podem aparecer brevemente (normal)
4. YouTube atualiza constantemente - pode ser necessário ajustar seletores

### Sistema não detecta atividade

1. Verifique que os callbacks estão sendo chamados nos logs
2. Confirme que `idle_music_manager` foi inicializado
3. Teste manualmente: `curl http://localhost:5000/api/idle/status`

## 📝 Changelog

### v2.0.0 - Sistema Idle e Ad-Blocking

**Novas Funcionalidades:**
- Sistema de música idle com reprodução automática
- Ad-blocking avançado com múltiplas técnicas
- Novos endpoints de API para controle idle
- Configurações personalizáveis

**Arquivos Novos:**
- `src/youtube/idle_music_manager.py`

**Arquivos Modificados:**
- `src/server/config.py`
- `src/youtube/youtube_player.py`
- `src/youtube/__init__.py`
- `src/server/app.py`
- `tests/test_jukebox.py`
- `README.md`
- `API.md`
- `env.example`

## 🎯 Próximos Passos

Sugestões para melhorias futuras:

1. **Machine Learning**: Aprender preferências do local e tocar músicas similares
2. **Horários**: Diferentes categorias em diferentes horários do dia
3. **Volume adaptativo**: Ajustar volume baseado no horário
4. **Blacklist**: Permitir que o proprietário bloqueie músicas específicas
5. **Analytics**: Dashboard com estatísticas de reprodução idle

## 📞 Suporte

Para questões sobre essas funcionalidades:
- Consulte os logs: `logs/jukebox.log`
- Abra uma issue no GitHub
- Verifique a documentação da API em `API.md`

---

**Desenvolvido com ❤️ para evitar silêncios constrangedores na jukebox**
