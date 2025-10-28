// Jukebox-Pi-Money - Frontend JavaScript

// Estado da aplicação
let currentBalance = 0;
let currentTransactionId = null;
let paymentCheckInterval = null;

// API Base URL
const API_BASE = '/api';

// ===== UTILITÁRIOS =====

function showScreen(screenId) {
    document.querySelectorAll('.screen').forEach(screen => {
        screen.classList.remove('active');
    });
    document.getElementById(screenId).classList.add('active');
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
    
    // Adiciona listener para Enter na busca
    document.getElementById('search-input').addEventListener('keypress', (e) => {
        if (e.key === 'Enter') {
            searchMusic();
        }
    });
    
    // Auto-refresh de status a cada 10 segundos
    setInterval(refreshStatus, 10000);
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
        
        data.methods.forEach(method => {
            const methodEl = createPaymentMethodElement(method);
            container.appendChild(methodEl);
        });
        
    } catch (error) {
        console.error('Erro ao carregar métodos de pagamento:', error);
        showError('Erro ao carregar métodos de pagamento');
    }
}

function createPaymentMethodElement(method) {
    const div = document.createElement('div');
    div.className = 'payment-method';
    div.onclick = () => selectPaymentMethod(method.method, method.price);
    
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
        await refreshQueue();
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
    await refreshQueue();
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
        showScreen('screen-success');
        
        await refreshStatus();
        
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

// ===== INICIALIZA APP =====

window.addEventListener('DOMContentLoaded', init);

// Log de depuração
console.log('Jukebox App carregado!');
