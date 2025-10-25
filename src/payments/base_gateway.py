"""
Classe base abstrata para gateways de pagamento
Todos os provedores (Mercado Pago, Stone, etc.) devem implementar esta interface
"""

from abc import ABC, abstractmethod
from typing import Dict, Optional
from src.server.config import PaymentMethod

class BasePaymentGateway(ABC):
    """Interface para gateways de pagamento"""
    
    def __init__(self, api_key: str, access_token: str):
        self.api_key = api_key
        self.access_token = access_token
    
    @abstractmethod
    def create_payment(
        self, 
        amount: float, 
        method: PaymentMethod, 
        description: str,
        customer_email: Optional[str] = None
    ) -> Dict:
        """
        Cria uma nova cobrança
        
        Args:
            amount: Valor em reais
            method: Método de pagamento (PIX, Débito, Crédito)
            description: Descrição da compra
            customer_email: Email do cliente (opcional)
        
        Returns:
            Dict com: payment_id, qr_code (se PIX), status, etc.
        """
        pass
    
    @abstractmethod
    def check_payment_status(self, payment_id: str) -> str:
        """
        Verifica status de um pagamento
        
        Args:
            payment_id: ID da transação
        
        Returns:
            Status: approved, pending, rejected, etc.
        """
        pass
    
    @abstractmethod
    def validate_webhook(self, payload: Dict, signature: str) -> bool:
        """
        Valida autenticidade de um webhook
        
        Args:
            payload: Dados recebidos
            signature: Assinatura enviada no header
        
        Returns:
            True se válido, False caso contrário
        """
        pass
