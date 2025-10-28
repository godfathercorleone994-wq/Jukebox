"""
Aplicação Flask principal do Jukebox
API REST para pagamentos, músicas e hardware
"""

import os
import sys
import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path
from flask import Flask, request, jsonify
from flask_cors import CORS
from dotenv import load_dotenv

# Adiciona diretório raiz ao path
ROOT_DIR = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(ROOT_DIR))

# Carrega variáveis de ambiente
load_dotenv()

# Importa módulos do projeto
from src.server.config import (
    FlaskConfig, BusinessConfig, PaymentMethod,
    PaymentGatewayConfig, LogConfig, AdminConfig
)
from src.db import Database, Transaction, CreditBalance, MusicQueue
from src.hardware import BillAcceptor
from src.youtube import YouTubePlayer, IdleMusicManager
from src.payments import PaymentStatus
from src.payments.mercadopago_gateway import create_gateway

# Configuração de logging
os.makedirs(LogConfig.LOG_FILE.parent, exist_ok=True)
handler = RotatingFileHandler(
    LogConfig.LOG_FILE,
    maxBytes=LogConfig.MAX_BYTES,
    backupCount=LogConfig.BACKUP_COUNT
)
handler.setFormatter(logging.Formatter(LogConfig.FORMAT))

logging.basicConfig(
    level=getattr(logging, LogConfig.LEVEL),
    handlers=[handler, logging.StreamHandler()]
)
logger = logging.getLogger(__name__)

# Inicializa Flask
app = Flask(__name__)
app.config['SECRET_KEY'] = FlaskConfig.SECRET_KEY
CORS(app, origins=FlaskConfig.CORS_ORIGINS)

# Inicializa componentes
db = Database()
transactions = Transaction(db)
credit_balance = CreditBalance(db)
music_queue = MusicQueue(db)

# Inicializa hardware
bill_acceptor = None
youtube_player = None
payment_gateway = None
idle_music_manager = None


def init_hardware():
    """Inicializa módulos de hardware e YouTube"""
    global bill_acceptor, youtube_player, idle_music_manager
    
    # Inicializa aceitador de notas
    bill_acceptor = BillAcceptor(callback=on_cash_received)
    logger.info("Bill acceptor inicializado")
    
    # Inicializa YouTube player se habilitado
    # Requer display conectado - desabilite se rodando em ambiente sem GUI
    youtube_enabled = os.getenv('YOUTUBE_ENABLED', 'false').lower() == 'true'
    
    if youtube_enabled:
        try:
            youtube_player = YouTubePlayer()
            logger.info("YouTube player inicializado")
            
            # Inicializa gerenciador de música idle
            idle_music_manager = IdleMusicManager(youtube_player)
            idle_music_manager.start()
            logger.info("Idle music manager inicializado")
        except Exception as e:
            logger.error(f"Erro ao inicializar YouTube/Idle Music: {e}")
            logger.warning("Sistema funcionará sem YouTube player")
    else:
        logger.info("YouTube player desabilitado (YOUTUBE_ENABLED=false)")


def init_payment_gateway():
    """Inicializa gateway de pagamento"""
    global payment_gateway
    
    if PaymentGatewayConfig.ENABLED:
        try:
            payment_gateway = create_gateway(
                PaymentGatewayConfig.PROVIDER,
                PaymentGatewayConfig.API_KEY,
                PaymentGatewayConfig.ACCESS_TOKEN
            )
            logger.info(f"Gateway de pagamento inicializado: {PaymentGatewayConfig.PROVIDER}")
        except Exception as e:
            logger.error(f"Erro ao inicializar gateway: {e}")


def on_cash_received(amount: float):
    """Callback quando dinheiro é inserido"""
    logger.info(f"Dinheiro recebido: R$ {amount:.2f}")
    
    # Adiciona crédito ao saldo
    new_balance = credit_balance.add_credit(amount)
    
    # Registra transação
    import uuid
    transaction_id = f"cash_{uuid.uuid4().hex[:12]}"
    transactions.create(
        transaction_id=transaction_id,
        payment_method=PaymentMethod.CASH,
        amount=amount,
        status=PaymentStatus.APPROVED
    )
    
    # Atualiza atividade no gerenciador de música idle
    if idle_music_manager:
        idle_music_manager.update_activity()
    
    logger.info(f"Novo saldo: R$ {new_balance:.2f}")


# ===== HELPER FUNCTIONS =====

def safe_error_response(message: str, status_code: int = 500):
    """
    Retorna resposta de erro segura sem expor detalhes internos
    
    Args:
        message: Mensagem genérica de erro
        status_code: Código HTTP
    
    Returns:
        JSON response com erro
    """
    if FlaskConfig.ENV == 'development':
        # Em desenvolvimento, pode mostrar mais detalhes
        return jsonify({"error": message}), status_code
    else:
        # Em produção, mensagem genérica
        error_messages = {
            400: "Requisição inválida",
            401: "Não autorizado",
            402: "Pagamento necessário",
            403: "Acesso negado",
            404: "Recurso não encontrado",
            429: "Muitas requisições",
            500: "Erro interno do servidor",
            503: "Serviço temporariamente indisponível"
        }
        return jsonify({"error": error_messages.get(status_code, "Erro no servidor")}), status_code


# ===== MIDDLEWARE DE AUTENTICAÇÃO =====

def require_hardware_token(f):
    """Decorator para exigir token de hardware"""
    from functools import wraps
    
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('X-Hardware-Token')
        if token != FlaskConfig.HARDWARE_TOKEN:
            return jsonify({"error": "Unauthorized"}), 401
        return f(*args, **kwargs)
    
    return decorated


# ===== ROTAS DA API =====

@app.route('/')
def index():
    """Página inicial"""
    return app.send_static_file('index.html')


@app.route('/api/status')
def api_status():
    """Status do sistema"""
    try:
        balance = credit_balance.get_balance()
        queue_size = music_queue.get_queue_size()
        
        return jsonify({
            "status": "online",
            "balance": balance,
            "queue_size": queue_size,
            "hardware_enabled": bill_acceptor.enabled if bill_acceptor else False,
            "payment_gateway_enabled": payment_gateway is not None,
            "youtube_enabled": youtube_player is not None
        })
    except Exception as e:
        logger.error(f"Erro ao obter status: {e}")
        return safe_error_response("Erro ao obter status do sistema", 500)


@app.route('/api/balance')
def get_balance():
    """Retorna saldo de créditos"""
    try:
        balance = credit_balance.get_balance()
        stats = credit_balance.get_stats()
        
        return jsonify({
            "balance": balance,
            "stats": stats
        })
    except Exception as e:
        logger.error(f"Erro ao obter saldo: {e}")
        return safe_error_response("Erro ao obter saldo", 500)


@app.route('/api/payment/methods')
def get_payment_methods():
    """Lista métodos de pagamento disponíveis"""
    enabled_methods = BusinessConfig.ENABLED_PAYMENT_METHODS
    
    methods = []
    for method_str in enabled_methods:
        try:
            method = PaymentMethod(method_str.strip())
            price = BusinessConfig.calculate_price(method)
            
            methods.append({
                "method": method.value,
                "price": price,
                "base_price": BusinessConfig.PRICE_PER_SONG
            })
        except ValueError:
            continue
    
    return jsonify({"methods": methods})


@app.route('/api/payment/create', methods=['POST'])
def create_payment():
    """Cria novo pagamento"""
    try:
        data = request.json
        method_str = data.get('method')
        description = data.get('description', 'Crédito Jukebox')
        
        # Valida método de pagamento
        try:
            method = PaymentMethod(method_str)
        except ValueError:
            return jsonify({"error": "Método de pagamento inválido"}), 400
        
        # Calcula preço
        amount = BusinessConfig.calculate_price(method)
        
        # Para dinheiro, apenas retorna instruções
        if method == PaymentMethod.CASH:
            return jsonify({
                "method": "cash",
                "amount": amount,
                "message": "Insira dinheiro no aceitador de notas"
            })
        
        # Para pagamentos digitais, usa gateway
        if not payment_gateway:
            return jsonify({"error": "Gateway de pagamento não disponível"}), 503
        
        # Cria pagamento no gateway
        import uuid
        transaction_id = f"{method.value}_{uuid.uuid4().hex[:12]}"
        
        payment_result = payment_gateway.create_payment(
            amount=amount,
            method=method,
            description=description
        )
        
        # Registra transação no banco
        transactions.create(
            transaction_id=transaction_id,
            payment_method=method,
            amount=amount,
            status=PaymentStatus.PENDING,
            payment_data=str(payment_result)
        )
        
        # Atualiza atividade no gerenciador de música idle
        if idle_music_manager:
            idle_music_manager.update_activity()
        
        return jsonify({
            "transaction_id": transaction_id,
            "payment_id": payment_result.get('payment_id'),
            "amount": amount,
            "method": method.value,
            "status": payment_result.get('status'),
            "qr_code": payment_result.get('qr_code'),
            "qr_code_base64": payment_result.get('qr_code_base64')
        })
        
    except Exception as e:
        logger.error(f"Erro ao criar pagamento: {e}")
        return safe_error_response("Erro ao processar pagamento", 500)


@app.route('/api/payment/status/<transaction_id>')
def check_payment_status(transaction_id):
    """Verifica status de pagamento"""
    try:
        transaction = transactions.get_by_id(transaction_id)
        
        if not transaction:
            return jsonify({"error": "Transação não encontrada"}), 404
        
        return jsonify({
            "transaction_id": transaction_id,
            "status": transaction['status'],
            "amount": transaction['amount'],
            "method": transaction['payment_method']
        })
        
    except Exception as e:
        logger.error(f"Erro ao verificar status: {e}")
        return safe_error_response("Erro ao verificar status do pagamento", 500)


@app.route('/api/webhook', methods=['POST'])
def webhook_handler():
    """Recebe webhooks do gateway de pagamento"""
    try:
        data = request.json
        signature = request.headers.get('x-signature', '')
        
        # Valida webhook
        if payment_gateway and payment_gateway.validate_webhook(data, signature):
            # Processa webhook
            payment_id = data.get('data', {}).get('id')
            
            if payment_id:
                status = payment_gateway.check_payment_status(payment_id)
                
                # Atualiza transação se aprovado
                if status == PaymentStatus.APPROVED.value:
                    # Busca transação relacionada
                    # TODO: Implementar busca por payment_id
                    logger.info(f"Pagamento aprovado: {payment_id}")
                
                return jsonify({"status": "processed"}), 200
        
        return jsonify({"status": "invalid"}), 400
        
    except Exception as e:
        logger.error(f"Erro ao processar webhook: {e}")
        return safe_error_response("Erro ao processar notificação", 500)


@app.route('/api/music/search', methods=['POST'])
def search_music():
    """Busca música no YouTube"""
    try:
        data = request.json
        query = data.get('query')
        
        if not query:
            return jsonify({"error": "Query não fornecida"}), 400
        
        # Por enquanto, retorna mock (YouTube player precisa de display)
        # if youtube_player:
        #     result = youtube_player.search_and_play(query)
        #     return jsonify(result)
        
        # Mock para testes sem YouTube
        import hashlib
        video_id = hashlib.md5(query.encode()).hexdigest()[:11]
        
        return jsonify({
            "video_id": video_id,
            "title": query,
            "duration_text": "3:45"
        })
        
    except Exception as e:
        logger.error(f"Erro ao buscar música: {e}")
        return safe_error_response("Erro ao buscar música", 500)


@app.route('/api/music/add', methods=['POST'])
def add_to_queue():
    """Adiciona música à fila"""
    try:
        data = request.json
        video_id = data.get('video_id')
        title = data.get('title')
        
        if not video_id or not title:
            return jsonify({"error": "Dados incompletos"}), 400
        
        # Verifica saldo
        price = BusinessConfig.PRICE_PER_SONG
        balance = credit_balance.get_balance()
        
        if balance < price:
            return jsonify({
                "error": "Saldo insuficiente",
                "balance": balance,
                "required": price
            }), 402
        
        # Verifica tamanho da fila
        if music_queue.get_queue_size() >= BusinessConfig.MAX_QUEUE_SIZE:
            return jsonify({"error": "Fila cheia"}), 429
        
        # Deduz crédito
        if not credit_balance.deduct_credit(price):
            return jsonify({"error": "Erro ao deduzir crédito"}), 500
        
        # Adiciona à fila (com status 'queued' - não interrompe música atual)
        song_id = music_queue.add_song(
            video_id=video_id,
            title=title,
            artist=data.get('artist'),
            duration=data.get('duration')
        )
        
        # Atualiza atividade no gerenciador de música idle
        if idle_music_manager:
            idle_music_manager.update_activity()
        
        # Se não há música tocando, pode começar a tocar esta imediatamente
        queue = music_queue.get_queue()
        has_playing = any(song['status'] == 'playing' for song in queue)
        
        return jsonify({
            "message": "Música adicionada à fila",
            "song_id": song_id,
            "new_balance": credit_balance.get_balance(),
            "queue_position": music_queue.get_queue_size(),
            "will_play_immediately": not has_playing
        })
        
    except Exception as e:
        logger.error(f"Erro ao adicionar música: {e}")
        return safe_error_response("Erro ao adicionar música à fila", 500)


@app.route('/api/music/queue')
def get_queue():
    """Retorna fila de músicas"""
    try:
        queue = music_queue.get_queue()
        queue_size = music_queue.get_queue_size()
        
        # Busca música atualmente tocando
        current_song = None
        if queue and len(queue) > 0:
            for song in queue:
                if song['status'] == 'playing':
                    current_song = song
                    break
        
        return jsonify({
            "queue": queue,
            "queue_size": queue_size,
            "current_song": current_song
        })
    except Exception as e:
        logger.error(f"Erro ao obter fila: {e}")
        return safe_error_response("Erro ao obter fila de músicas", 500)


@app.route('/api/music/next', methods=['POST'])
@require_hardware_token
def play_next():
    """Toca próxima música da fila"""
    try:
        next_song = music_queue.get_next_song()
        
        if not next_song:
            return jsonify({"message": "Fila vazia"}), 404
        
        # Marca como tocando
        music_queue.mark_as_playing(next_song['id'])
        
        # Toca no YouTube (se disponível)
        # if youtube_player:
        #     youtube_player.play_video(next_song['video_id'])
        
        return jsonify({
            "message": "Música tocando",
            "song": next_song
        })
        
    except Exception as e:
        logger.error(f"Erro ao tocar música: {e}")
        return safe_error_response("Erro ao tocar próxima música", 500)


@app.route('/api/hardware/simulate-cash', methods=['POST'])
def simulate_cash():
    """Simula inserção de dinheiro (apenas para testes)"""
    if FlaskConfig.ENV != 'development':
        return jsonify({"error": "Disponível apenas em desenvolvimento"}), 403
    
    try:
        data = request.json
        count = data.get('count', 1)
        
        if bill_acceptor:
            bill_acceptor.simulate_pulse(count)
            return jsonify({
                "message": f"{count} pulso(s) simulado(s)",
                "new_balance": credit_balance.get_balance()
            })
        
        return jsonify({"error": "Hardware não disponível"}), 503
        
    except Exception as e:
        logger.error(f"Erro ao simular dinheiro: {e}")
        return safe_error_response("Erro ao simular inserção de dinheiro", 500)


@app.route('/api/admin/add-credits', methods=['POST'])
def admin_add_credits():
    """Adiciona créditos usando código de administrador"""
    if not AdminConfig.ADMIN_ENABLED:
        return jsonify({"error": "Funcionalidade admin não habilitada"}), 403
    
    try:
        data = request.json
        code = data.get('code', '')
        
        # Valida código admin
        if code != AdminConfig.ADMIN_CODE:
            logger.warning("Tentativa de uso de código admin inválido")
            return jsonify({"error": "Código inválido"}), 401
        
        # Adiciona crédito configurado
        amount = AdminConfig.ADMIN_CREDIT_AMOUNT
        new_balance = credit_balance.add_credit(amount)
        
        # Registra transação especial para auditoria
        import uuid
        transaction_id = f"admin_{uuid.uuid4().hex[:12]}"
        transactions.create(
            transaction_id=transaction_id,
            payment_method=PaymentMethod.CASH,  # Usa CASH como tipo base
            amount=amount,
            status=PaymentStatus.APPROVED
        )
        
        # Atualiza atividade no gerenciador de música idle
        if idle_music_manager:
            idle_music_manager.update_activity()
        
        logger.info(f"Créditos admin adicionados: R$ {amount:.2f} - Novo saldo: R$ {new_balance:.2f}")
        
        return jsonify({
            "success": True,
            "message": "Créditos adicionados com sucesso",
            "amount": amount,
            "new_balance": new_balance
        })
        
    except Exception as e:
        logger.error(f"Erro ao adicionar créditos admin: {e}")
        return safe_error_response("Erro ao processar código admin", 500)


@app.route('/api/idle/status')
def get_idle_status():
    """Retorna status do sistema de música idle"""
    try:
        if not idle_music_manager:
            return jsonify({
                "enabled": False,
                "message": "Idle music manager não inicializado"
            })
        
        return jsonify({
            "enabled": YouTubeConfig.IDLE_MUSIC_ENABLED,
            "timeout": YouTubeConfig.IDLE_MUSIC_TIMEOUT,
            "idle_time": idle_music_manager.get_idle_time(),
            "is_idle": idle_music_manager.is_idle(),
            "categories": YouTubeConfig.IDLE_MUSIC_QUERIES
        })
    except Exception as e:
        logger.error(f"Erro ao obter status idle: {e}")
        return safe_error_response("Erro ao obter status do sistema idle", 500)


@app.route('/api/idle/trigger', methods=['POST'])
def trigger_idle_music():
    """Força reprodução de música idle (apenas para testes)"""
    if FlaskConfig.ENV != 'development':
        return jsonify({"error": "Disponível apenas em desenvolvimento"}), 403
    
    try:
        if not youtube_player:
            return jsonify({"error": "YouTube player não disponível"}), 503
        
        result = youtube_player.play_random_music()
        
        if result:
            return jsonify({
                "message": "Música idle tocada com sucesso",
                "video": result
            })
        
        return jsonify({"error": "Falha ao tocar música idle"}), 500
        
    except Exception as e:
        logger.error(f"Erro ao tocar música idle: {e}")
        return safe_error_response("Erro ao tocar música idle", 500)


# ===== INICIALIZAÇÃO =====

def initialize_app():
    """Inicializa componentes da aplicação"""
    logger.info("Inicializando Jukebox...")
    
    init_hardware()
    init_payment_gateway()
    
    logger.info("Jukebox inicializado com sucesso!")


# ===== MAIN =====

if __name__ == '__main__':
    initialize_app()
    
    app.run(
        host=FlaskConfig.HOST,
        port=FlaskConfig.PORT,
        debug=(FlaskConfig.ENV == 'development')
    )
