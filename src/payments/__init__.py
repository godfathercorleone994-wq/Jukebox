"""
Módulo de pagamentos digitais
Suporta PIX, Débito e Crédito via gateways de pagamento
"""

from enum import Enum

class PaymentStatus(Enum):
    """Status de uma transação de pagamento"""
    PENDING = "pending"           # Aguardando pagamento
    APPROVED = "approved"         # Pagamento aprovado
    REJECTED = "rejected"         # Pagamento rejeitado
    CANCELLED = "cancelled"       # Cancelado pelo usuário
    REFUNDED = "refunded"         # Estornado
    IN_PROCESS = "in_process"     # Em processamento
