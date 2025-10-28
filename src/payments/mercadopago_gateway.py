"""
Implementação do gateway Mercado Pago
Suporta PIX, Débito e Crédito
"""

import logging
from typing import Dict, Optional

try:
    import mercadopago
    MERCADOPAGO_AVAILABLE = True
except ImportError:
    MERCADOPAGO_AVAILABLE = False
    mercadopago = None

from src.payments.base_gateway import BasePaymentGateway
from src.server.config import PaymentMethod
from src.payments import PaymentStatus

logger = logging.getLogger(__name__)


class MercadoPagoGateway(BasePaymentGateway):
    """Gateway de pagamento Mercado Pago"""
    
    def __init__(self, api_key: str, access_token: str):
        if not MERCADOPAGO_AVAILABLE:
            raise ImportError("Mercado Pago SDK não está instalado")
        
        super().__init__(api_key, access_token)
        self.sdk = mercadopago.SDK(access_token)
        logger.info("Mercado Pago SDK inicializado")
    
    def create_payment(
        self,
        amount: float,
        method: PaymentMethod,
        description: str,
        customer_email: Optional[str] = None
    ) -> Dict:
        """
        Cria pagamento no Mercado Pago
        
        Returns:
            Dict com payment_id, qr_code (se PIX), status, etc.
        """
        try:
            payment_data = {
                "transaction_amount": amount,
                "description": description,
                "payment_method_id": self._get_payment_method_id(method),
                "payer": {
                    "email": customer_email or "customer@jukebox.com"
                }
            }
            
            # Para PIX, adiciona configurações específicas
            if method == PaymentMethod.PIX:
                payment_data["payment_method_id"] = "pix"
            
            # Cria pagamento
            result = self.sdk.payment().create(payment_data)
            payment = result.get("response", {})
            
            response = {
                "payment_id": payment.get("id"),
                "status": self._map_status(payment.get("status")),
                "amount": payment.get("transaction_amount"),
                "method": method.value
            }
            
            # Se for PIX, adiciona QR Code
            if method == PaymentMethod.PIX:
                point_of_interaction = payment.get("point_of_interaction", {})
                transaction_data = point_of_interaction.get("transaction_data", {})
                
                response["qr_code"] = transaction_data.get("qr_code")
                response["qr_code_base64"] = transaction_data.get("qr_code_base64")
                response["ticket_url"] = transaction_data.get("ticket_url")
            
            logger.info(f"Pagamento criado: {response['payment_id']} - {method.value}")
            return response
            
        except Exception as e:
            logger.error(f"Erro ao criar pagamento: {e}")
            raise
    
    def check_payment_status(self, payment_id: str) -> str:
        """Verifica status de pagamento"""
        try:
            result = self.sdk.payment().get(payment_id)
            payment = result.get("response", {})
            status = payment.get("status")
            
            logger.info(f"Status do pagamento {payment_id}: {status}")
            return self._map_status(status)
            
        except Exception as e:
            logger.error(f"Erro ao verificar status: {e}")
            return PaymentStatus.PENDING.value
    
    def validate_webhook(self, payload: Dict, signature: str) -> bool:
        """
        Valida webhook do Mercado Pago
        
        Note: Implementação básica - em produção, validar assinatura HMAC
        """
        try:
            # Mercado Pago envia 'x-signature' no header
            # Em produção, validar com secret do webhook
            
            # Validação básica: verifica se tem campos obrigatórios
            required_fields = ["type", "data"]
            return all(field in payload for field in required_fields)
            
        except Exception as e:
            logger.error(f"Erro ao validar webhook: {e}")
            return False
    
    def _get_payment_method_id(self, method: PaymentMethod) -> str:
        """Mapeia PaymentMethod para ID do Mercado Pago"""
        mapping = {
            PaymentMethod.PIX: "pix",
            PaymentMethod.CREDIT: "credit_card",
            PaymentMethod.DEBIT: "debit_card"
        }
        return mapping.get(method, "")
    
    def _map_status(self, mp_status: str) -> str:
        """Mapeia status do Mercado Pago para PaymentStatus"""
        mapping = {
            "approved": PaymentStatus.APPROVED.value,
            "pending": PaymentStatus.PENDING.value,
            "in_process": PaymentStatus.IN_PROCESS.value,
            "rejected": PaymentStatus.REJECTED.value,
            "cancelled": PaymentStatus.CANCELLED.value,
            "refunded": PaymentStatus.REFUNDED.value
        }
        return mapping.get(mp_status, PaymentStatus.PENDING.value)


def create_gateway(provider: str, api_key: str, access_token: str) -> BasePaymentGateway:
    """
    Factory para criar gateway de pagamento
    
    Args:
        provider: Nome do provedor (mercadopago, stone, etc.)
        api_key: Chave API
        access_token: Token de acesso
    
    Returns:
        Instância do gateway
    """
    if provider.lower() == "mercadopago":
        if not MERCADOPAGO_AVAILABLE:
            raise ImportError("Mercado Pago SDK não está instalado. Instale com: pip install mercadopago")
        return MercadoPagoGateway(api_key, access_token)
    else:
        raise ValueError(f"Provedor não suportado: {provider}")
