// Jukebox-Pi-Money - Frontend JavaScript

// Estado da aplicação
let currentBalance = 0;
let currentTransactionId = null;
let paymentCheckInterval = null;

// API Base URL
const API_BASE = '/api';

// Estado da navegação por teclado
let keyboardNavigation = {
    enabled: true,
    currentFocus: 0,
    focusableElements: []
};

// YouTube Player
let youtubePlayer = null;
let isYouTubeAPIReady = false;
let currentPlayingSongId = null;

// ===== YOUTUBE PLAYER =====

// Callback para quando a API do YouTube estiver pronta
function onYouTubeIframeAPIReady() {
    console.log('YouTube IFrame API pronta');
    isYouTubeAPIReady = true;
    initYouTubePlayer();
}

function initYouTubePlayer() {
    if (!isYouTubeAPIReady) {
        console.log('Aguardando YouTube API...');
        return;
    }
    
    youtubePlayer = new YT.Player('youtube-player', {
        height: '100%',
        width: '100%',
        playerVars: {
            'autoplay': 1,
            'controls': 1,
            'modestbranding': 1,
            'rel': 0,
            'showinfo': 0
        },
        events: {
            'onReady': onPlayerReady,
            'onStateChange': onPlayerStateChange
        }
    });
    
    console.log('YouTube Player inicializado');
}

function onPlayerReady(event) {
    console.log('YouTube Player pronto para usar');
}

function onPlayerStateChange(event) {
    // YT.PlayerState.ENDED = 0
    // YT.PlayerState.PLAYING = 1
    // YT.PlayerState.PAUSED = 2
    
    if (event.data === YT.PlayerState.ENDED) {
        console.log('Música terminou, carregando próxima...');
        playNextInQueue();
    } else if (event.data === YT.PlayerState.PLAYING) {
        console.log('Música tocando');
    }
}

async function playVideo(videoId, title) {
    if (!youtubePlayer || !youtubePlayer.loadVideoById) {
        console.error('YouTube Player não está pronto');
        return false;
    }
    
    try {
        youtubePlayer.loadVideoById(videoId);
        
        // Atualiza informações de "tocando agora"
        const nowPlayingInfo = document.getElementById('now-playing-info');
        const nowPlayingTitle = document.getElementById('now-playing-title');
        
        if (nowPlayingInfo && nowPlayingTitle) {
            nowPlayingTitle.textContent = title;
            nowPlayingInfo.style.display = 'block';
        }
        
        console.log(`Tocando: ${title} (${videoId})`);
        return true;
    } catch (error) {
        console.error('Erro ao tocar vídeo:', error);
        return false;
    }
}

async function playNextInQueue() {
    try {
        // Marca a música atual como concluída e busca a próxima
        const response = await fetch(`${API_BASE}/music/complete`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                song_id: currentPlayingSongId
            })
        });
        
        const data = await response.json();
        
        if (data.next_song) {
            // Toca a próxima música
            currentPlayingSongId = data.next_song.id;
            await playVideo(data.next_song.video_id, data.next_song.title);
            
            // Atualiza a fila na interface
            await refreshQueue();
        } else {
            console.log('Fila vazia, nenhuma música para tocar');
            currentPlayingSongId = null;
            
            // Esconde informações de "tocando agora"
            const nowPlayingInfo = document.getElementById('now-playing-info');
            if (nowPlayingInfo) {
                nowPlayingInfo.style.display = 'none';
            }
        }
        
    } catch (error) {
        console.error('Erro ao tocar próxima música:', error);
    }
}

// Torna a função disponível globalmente para o YouTube API
window.onYouTubeIframeAPIReady = onYouTubeIframeAPIReady;

// ===== UTILITÁRIOS =====

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
    
    // Atualiza elementos focáveis quando troca de tela
    setTimeout(() => updateFocusableElements(), 100);
}

function showLoading() {
    document.getElementById('loading-overlay').classList.add('active');
}

function hideLoading() {
    document.getElementById('loading-overlay').classList.remove('active');
}

function showError(message) {
    document.getElementById('error-message').textContent = message;
    showScreen('screen-error');
}

function updateBalanceDisplays(balance) {
    currentBalance = balance;
    document.querySelectorAll('[id^="balance"]').forEach(el => {
        el.textContent = balance.toFixed(2);
    });
}

// ===== INICIALIZAÇÃO =====

async function init() {
    console.log('Inicializando Jukebox...');
    await refreshStatus();
    await loadPaymentMethods();
    
    // Inicializa YouTube Player se API já estiver carregada
    if (typeof YT !== 'undefined' && YT.Player) {
        isYouTubeAPIReady = true;
        // Não inicializa o player ainda, será inicializado quando entrar na tela de busca
    }
    
    // Adiciona listener para Enter na busca
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchMusic();
        }
    });
    
    // Inicializa navegação por teclado
    initKeyboardNavigation();
    
    // Auto-refresh de status a cada 10 segundos
    setInterval(refreshStatus, 10000);
}

// ===== NAVEGAÇÃO POR TECLADO =====

function initKeyboardNavigation() {
    console.log('Inicializando navegação por teclado...');
    
    // Listener global para teclas
    document.addEventListener('keydown', handleKeyboardNavigation);
    
    // Atualiza elementos focáveis
    updateFocusableElements();
    
    console.log('Navegação por teclado ativa! Use setas, Enter, Tab e números (1-9)');
}

function handleKeyboardNavigation(e) {
    // Ignora se estiver digitando em um input de texto
    if (e.target.tagName === 'INPUT' && e.target.type === 'text') {
        // Permite Esc para sair do input
        if (e.key === 'Escape') {
            e.target.blur();
            updateFocusableElements();
        }
        return;
    }
    
    const key = e.key;
    
    // F1 ou ? para mostrar/ocultar ajuda de teclado
    if (key === 'F1' || key === '?') {
        e.preventDefault();
        toggleKeyboardHints();
        return;
    }
    
    // Navegação com setas
    if (key === 'ArrowUp' || key === 'ArrowDown' || key === 'ArrowLeft' || key === 'ArrowRight') {
        e.preventDefault();
        navigateWithArrows(key);
    }
    // Enter ou Espaço para ativar elemento focado
    else if (key === 'Enter' || key === ' ') {
        e.preventDefault();
        activateFocusedElement();
    }
    // Tab para próximo elemento
    else if (key === 'Tab') {
        e.preventDefault();
        moveFocus(e.shiftKey ? -1 : 1);
    }
    // Números 1-9 para seleção rápida
    else if (key >= '1' && key <= '9') {
        e.preventDefault();
        const index = parseInt(key) - 1;
        if (index < keyboardNavigation.focusableElements.length) {
            keyboardNavigation.currentFocus = index;
            focusCurrentElement();
            activateFocusedElement();
        }
    }
    // H para ir ao início (Home)
    else if (key === 'h' || key === 'H') {
        e.preventDefault();
        goToHome();
    }
    // Esc para voltar ou cancelar
    else if (key === 'Escape') {
        e.preventDefault();
        handleEscape();
    }
    // F5 ou R para atualizar
    else if ((key === 'F5') || (key === 'r' || key === 'R')) {
        if (key !== 'F5') e.preventDefault();
        refreshStatus();
    }
}

function toggleKeyboardHints() {
    const hints = document.getElementById('keyboard-hints');
    if (hints.style.display === 'none') {
        hints.style.display = 'block';
    } else {
        hints.style.display = 'none';
    }
}

function navigateWithArrows(key) {
    const elements = keyboardNavigation.focusableElements;
    if (elements.length === 0) return;
    
    // Para setas verticais, move um elemento por vez
    if (key === 'ArrowUp') {
        moveFocus(-1);
    } else if (key === 'ArrowDown') {
        moveFocus(1);
    }
    // Para setas horizontais, tenta mover na mesma linha
    else if (key === 'ArrowLeft') {
        moveFocus(-1);
    } else if (key === 'ArrowRight') {
        moveFocus(1);
    }
}

function moveFocus(direction) {
    const elements = keyboardNavigation.focusableElements;
    if (elements.length === 0) return;
    
    keyboardNavigation.currentFocus += direction;
    
    // Wrap around
    if (keyboardNavigation.currentFocus < 0) {
        keyboardNavigation.currentFocus = elements.length - 1;
    } else if (keyboardNavigation.currentFocus >= elements.length) {
        keyboardNavigation.currentFocus = 0;
    }
    
    focusCurrentElement();
}

function focusCurrentElement() {
    const elements = keyboardNavigation.focusableElements;
    
    // Remove foco visual de todos
    elements.forEach(el => el.classList.remove('keyboard-focus'));
    
    // Adiciona foco visual ao elemento atual
    if (elements[keyboardNavigation.currentFocus]) {
        const el = elements[keyboardNavigation.currentFocus];
        el.classList.add('keyboard-focus');
        el.scrollIntoView({ behavior: 'smooth', block: 'center' });
    }
}

function activateFocusedElement() {
    const elements = keyboardNavigation.focusableElements;
    const el = elements[keyboardNavigation.currentFocus];
    
    if (el) {
        // Se for um botão ou elemento clicável
        if (el.onclick) {
            el.onclick();
        } else if (el.tagName === 'BUTTON' || el.tagName === 'A') {
            el.click();
        } else if (el.tagName === 'INPUT') {
            el.focus();
        }
    }
}

function updateFocusableElements() {
    // Encontra todos os elementos interativos na tela ativa
    const activeScreen = document.querySelector('.screen.active');
    if (!activeScreen) return;
    
    const selectors = [
        'button:not([disabled])',
        '.payment-method',
        '.search-result',
        'input[type="text"]',
        '.queue-item',
        'a'
    ];
    
    keyboardNavigation.focusableElements = Array.from(
        activeScreen.querySelectorAll(selectors.join(','))
    ).filter(el => {
        // Filtra elementos visíveis
        const style = window.getComputedStyle(el);
        return style.display !== 'none' && style.visibility !== 'hidden';
    });
    
    // Reset foco
    keyboardNavigation.currentFocus = 0;
    
    // Foca primeiro elemento se houver
    if (keyboardNavigation.focusableElements.length > 0) {
        focusCurrentElement();
    }
    
    console.log(`Elementos focáveis: ${keyboardNavigation.focusableElements.length}`);
}

function handleEscape() {
    const activeScreenId = document.querySelector('.screen.active').id;
    
    switch(activeScreenId) {
        case 'screen-waiting-payment':
            cancelPayment();
            break;
        case 'screen-search-music':
        case 'screen-success':
        case 'screen-error':
            goToHome();
            break;
        default:
            // Na tela inicial, não faz nada
            break;
    }
}

// ===== STATUS DO SISTEMA =====

async function refreshStatus() {
    try {
        const response = await fetch(`${API_BASE}/status`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Erro ao obter status:', data.error);
            return;
        }
        
        updateBalanceDisplays(data.balance);
        console.log('Status atualizado:', data);
        
    } catch (error) {
        console.error('Erro ao atualizar status:', error);
    }
}

// ===== MÉTODOS DE PAGAMENTO =====

async function loadPaymentMethods() {
    try {
        const response = await fetch(`${API_BASE}/payment/methods`);
        const data = await response.json();
        
        const container = document.getElementById('payment-methods-container');
        container.innerHTML = '';
        
        data.methods.forEach((method, index) => {
            const methodEl = createPaymentMethodElement(method, index);
            container.appendChild(methodEl);
        });
        
        // Atualiza elementos focáveis após carregar
        updateFocusableElements();
        
    } catch (error) {
        console.error('Erro ao carregar métodos de pagamento:', error);
        showError('Erro ao carregar métodos de pagamento');
    }
}

function createPaymentMethodElement(method, index) {
    const div = document.createElement('div');
    div.className = 'payment-method';
    div.onclick = () => selectPaymentMethod(method.method, method.price);
    div.setAttribute('data-keyboard-hint', index + 1);
    
    const icons = {
        'cash': '💵',
        'pix': '📱',
        'debit': '💳',
        'credit': '💳'
    };
    
    const names = {
        'cash': 'Dinheiro',
        'pix': 'PIX',
        'debit': 'Débito',
        'credit': 'Crédito'
    };
    
    div.innerHTML = `
        <div class="keyboard-number">${index + 1}</div>
        <div class="icon">${icons[method.method] || '💰'}</div>
        <div class="name">${names[method.method] || method.method}</div>
        <div class="price">R$ ${method.price.toFixed(2)}</div>
    `;
    
    return div;
}

async function selectPaymentMethod(method, price) {
    console.log('Método selecionado:', method);
    
    if (method === 'cash') {
        // Para dinheiro, vai direto para busca de música
        showLoading();
        await refreshStatus(); // Atualiza saldo
        hideLoading();
        showScreen('screen-search-music');
        
        // Inicializa YouTube Player se ainda não foi inicializado
        if (!youtubePlayer && isYouTubeAPIReady) {
            initYouTubePlayer();
        }
        
        await refreshQueue();
        
        // Verifica se há músicas na fila e começa a tocar a primeira
        await checkAndPlayQueue();
        
        return;
    }
    
    // Para outros métodos, cria pagamento
    await createPayment(method, price);
}

// ===== PAGAMENTOS =====

async function createPayment(method, price) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/payment/create`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                method: method,
                description: 'Crédito para Jukebox'
            })
        });
        
        const data = await response.json();
        
        if (data.error) {
            hideLoading();
            showError(data.error);
            return;
        }
        
        currentTransactionId = data.transaction_id;
        
        // Se for PIX, mostra QR Code
        if (method === 'pix' && data.qr_code_base64) {
            document.getElementById('payment-amount').textContent = data.amount.toFixed(2);
            document.getElementById('qr-code-image').src = `data:image/png;base64,${data.qr_code_base64}`;
            
            hideLoading();
            showScreen('screen-waiting-payment');
            
            // Inicia checagem de status
            startPaymentCheck(data.transaction_id);
        } else {
            hideLoading();
            showError('Método de pagamento não implementado completamente');
        }
        
    } catch (error) {
        hideLoading();
        console.error('Erro ao criar pagamento:', error);
        showError('Erro ao criar pagamento: ' + error.message);
    }
}

function startPaymentCheck(transactionId) {
    // Verifica status a cada 3 segundos
    paymentCheckInterval = setInterval(async () => {
        const status = await checkPaymentStatus(transactionId);
        
        if (status === 'approved') {
            clearInterval(paymentCheckInterval);
            await onPaymentApproved();
        } else if (status === 'rejected' || status === 'cancelled') {
            clearInterval(paymentCheckInterval);
            showError('Pagamento não aprovado');
        }
    }, 3000);
}

async function checkPaymentStatus(transactionId) {
    try {
        const response = await fetch(`${API_BASE}/payment/status/${transactionId}`);
        const data = await response.json();
        
        console.log('Status do pagamento:', data.status);
        return data.status;
        
    } catch (error) {
        console.error('Erro ao verificar status:', error);
        return 'pending';
    }
}

async function onPaymentApproved() {
    await refreshStatus();
    showScreen('screen-search-music');
    
    // Inicializa YouTube Player se ainda não foi inicializado
    if (!youtubePlayer && isYouTubeAPIReady) {
        initYouTubePlayer();
    }
    
    await refreshQueue();
    
    // Verifica se há músicas na fila e começa a tocar a primeira
    await checkAndPlayQueue();
}

async function checkAndPlayQueue() {
    try {
        const response = await fetch(`${API_BASE}/music/queue`);
        const data = await response.json();
        
        if (data.queue && data.queue.length > 0) {
            // Verifica se já há uma música tocando
            const playingSong = data.queue.find(song => song.status === 'playing');
            
            if (!playingSong) {
                // Busca a primeira música na fila e começa a tocar
                const firstSong = data.queue[0];
                if (firstSong.status === 'queued') {
                    currentPlayingSongId = firstSong.id;
                    
                    // Marca como tocando no backend
                    await fetch(`${API_BASE}/music/complete`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ song_id: null })
                    });
                    
                    // Toca o vídeo
                    await playVideo(firstSong.video_id, firstSong.title);
                    
                    console.log('Primeira música da fila começando:', firstSong.title);
                }
            } else {
                // Já tem uma música tocando, atualiza o player se necessário
                currentPlayingSongId = playingSong.id;
                console.log('Já há uma música tocando:', playingSong.title);
            }
        }
    } catch (error) {
        console.error('Erro ao verificar fila:', error);
    }
}

function cancelPayment() {
    if (paymentCheckInterval) {
        clearInterval(paymentCheckInterval);
    }
    goToHome();
}

// ===== BUSCA DE MÚSICAS =====

async function searchMusic() {
    const query = document.getElementById('search-input').value.trim();
    
    if (!query) {
        alert('Digite algo para buscar');
        return;
    }
    
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/music/search`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ query })
        });
        
        const data = await response.json();
        
        if (data.error) {
            hideLoading();
            showError(data.error);
            return;
        }
        
        // Exibe resultado
        displaySearchResult(data);
        hideLoading();
        
    } catch (error) {
        hideLoading();
        console.error('Erro ao buscar música:', error);
        showError('Erro ao buscar música: ' + error.message);
    }
}

function displaySearchResult(result) {
    const container = document.getElementById('search-results');
    container.innerHTML = '';
    
    const resultEl = document.createElement('div');
    resultEl.className = 'search-result';
    resultEl.onclick = () => addMusicToQueue(result);
    
    resultEl.innerHTML = `
        <div class="info">
            <div class="title">${result.title}</div>
            <div class="duration">⏱️ ${result.duration_text || 'Desconhecida'}</div>
        </div>
        <button class="btn-primary">➕ Adicionar</button>
    `;
    
    container.appendChild(resultEl);
    
    // Atualiza elementos focáveis após adicionar resultado
    updateFocusableElements();
}

// ===== FILA DE MÚSICAS =====

async function addMusicToQueue(music) {
    showLoading();
    
    try {
        const response = await fetch(`${API_BASE}/music/add`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                video_id: music.video_id,
                title: music.title,
                duration: music.duration
            })
        });
        
        const data = await response.json();
        
        hideLoading();
        
        if (data.error) {
            if (response.status === 402) {
                showError(`Saldo insuficiente! Necessário: R$ ${data.required.toFixed(2)}`);
            } else {
                showError(data.error);
            }
            return;
        }
        
        // Sucesso!
        document.getElementById('added-song-title').textContent = music.title;
        document.getElementById('balance-after').textContent = data.new_balance.toFixed(2);
        
        // Mostra mensagem adicional sobre a posição na fila
        const successMessage = document.getElementById('success-message');
        if (successMessage) {
            if (data.will_play_immediately) {
                successMessage.textContent = '🎵 Sua música vai tocar agora!';
                
                // Se for tocar imediatamente, inicia o playback
                currentPlayingSongId = data.song_id;
                
                // Aguarda um pouco para marcar como tocando e iniciar
                setTimeout(async () => {
                    await playVideo(music.video_id, music.title);
                }, 500);
            } else {
                successMessage.textContent = `🎵 Música adicionada à fila! Posição: ${data.queue_position}`;
            }
        }
        
        showScreen('screen-success');
        
        await refreshStatus();
        await refreshQueue();
        
    } catch (error) {
        hideLoading();
        console.error('Erro ao adicionar música:', error);
        showError('Erro ao adicionar música: ' + error.message);
    }
}

async function refreshQueue() {
    try {
        const response = await fetch(`${API_BASE}/music/queue`);
        const data = await response.json();
        
        if (data.error) {
            console.error('Erro ao obter fila:', data.error);
            return;
        }
        
        displayQueue(data.queue);
        
    } catch (error) {
        console.error('Erro ao atualizar fila:', error);
    }
}

function displayQueue(queue) {
    const container = document.getElementById('queue-list');
    const countEl = document.getElementById('queue-count');
    
    countEl.textContent = queue.length;
    
    if (queue.length === 0) {
        container.innerHTML = '<p style="text-align: center; opacity: 0.7;">Nenhuma música na fila</p>';
        return;
    }
    
    container.innerHTML = '';
    
    queue.forEach((item, index) => {
        const itemEl = document.createElement('div');
        itemEl.className = 'queue-item';
        
        const statusText = item.status === 'playing' ? '▶️ Tocando' : '⏳ Na fila';
        const statusClass = item.status === 'playing' ? 'playing' : 'queued';
        
        itemEl.innerHTML = `
            <div class="position">#${index + 1}</div>
            <div class="info">
                <div class="title">${item.title}</div>
                <div class="artist">${item.artist || 'Artista desconhecido'}</div>
            </div>
            <div class="status ${statusClass}">${statusText}</div>
        `;
        
        container.appendChild(itemEl);
    });
}

// ===== NAVEGAÇÃO =====

function goToHome() {
    showScreen('screen-payment-selection');
    refreshStatus();
    
    // Limpa busca
    document.getElementById('search-input').value = '';
    document.getElementById('search-results').innerHTML = '';
}

function addAnotherSong() {
    showScreen('screen-search-music');
    document.getElementById('search-input').value = '';
    document.getElementById('search-results').innerHTML = '';
    refreshQueue();
}

// ===== ADMIN CODE =====

// Detecta combinação de teclas para abrir modal admin
let keySequence = [];
const ADMIN_SHORTCUT = ['Control', 'Shift', 'A']; // Ctrl+Shift+A
const SEQUENCE_TIMEOUT = 2000; // 2 segundos para completar sequência
let sequenceTimer = null;

function openAdminModal() {
    const modal = document.getElementById('admin-modal');
    modal.style.display = 'flex';
    
    // Foca no input
    setTimeout(() => {
        const input = document.getElementById('admin-code-input');
        input.value = '';
        input.focus();
        
        // Listener para Enter no input
        input.onkeypress = (e) => {
            if (e.key === 'Enter') {
                submitAdminCode();
            }
        };
    }, 100);
    
    // Esconde erro anterior
    document.getElementById('admin-error').style.display = 'none';
}

function closeAdminModal() {
    const modal = document.getElementById('admin-modal');
    modal.style.display = 'none';
    document.getElementById('admin-code-input').value = '';
    document.getElementById('admin-error').style.display = 'none';
}

async function submitAdminCode() {
    const input = document.getElementById('admin-code-input');
    const code = input.value.trim();
    const errorEl = document.getElementById('admin-error');
    
    if (!code) {
        errorEl.textContent = 'Por favor, digite um código';
        errorEl.style.display = 'block';
        return;
    }
    
    try {
        showLoading();
        
        const response = await fetch(`${API_BASE}/admin/add-credits`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ code })
        });
        
        const data = await response.json();
        hideLoading();
        
        if (response.ok && data.success) {
            // Sucesso - atualiza saldo e fecha modal
            updateBalanceDisplays(data.new_balance);
            closeAdminModal();
            
            // Mostra mensagem de sucesso
            alert(`✅ Créditos adicionados!\nValor: R$ ${data.amount.toFixed(2)}\nNovo saldo: R$ ${data.new_balance.toFixed(2)}`);
            
            console.log('Admin credits added:', data);
        } else {
            // Erro - mostra mensagem
            errorEl.textContent = data.error || 'Código inválido';
            errorEl.style.display = 'block';
            input.value = '';
            input.focus();
        }
        
    } catch (error) {
        hideLoading();
        console.error('Erro ao enviar código admin:', error);
        errorEl.textContent = 'Erro ao processar código';
        errorEl.style.display = 'block';
    }
}

// Detecta sequência de teclas para abrir modal
function detectAdminShortcut(e) {
    // Adiciona tecla à sequência
    if (e.key === 'Control' || e.key === 'Shift' || e.key === 'a' || e.key === 'A') {
        // Verifica se as teclas modificadoras estão pressionadas
        if (e.ctrlKey && e.shiftKey && (e.key === 'a' || e.key === 'A')) {
            e.preventDefault();
            openAdminModal();
        }
    }
}

// Adiciona listener para atalho admin ao init
document.addEventListener('keydown', detectAdminShortcut);

// ===== INICIALIZA APP =====

window.addEventListener('DOMContentLoaded', init);

// Log de depuração
console.log('Jukebox App carregado!');
