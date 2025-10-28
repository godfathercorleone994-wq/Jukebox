#!/usr/bin/env python3
"""
Script de teste para o Jukebox
Verifica funcionalidade básica do sistema
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.db import Database, Transaction, CreditBalance, MusicQueue
from src.server.config import PaymentMethod
from src.payments import PaymentStatus

def test_database():
    """Testa operações do banco de dados"""
    print("🧪 Testando banco de dados...")
    
    # Cria banco de teste
    db = Database()
    transactions = Transaction(db)
    balance = CreditBalance(db)
    queue = MusicQueue(db)
    
    # Testa saldo
    print("  ✓ Saldo inicial:", balance.get_balance())
    
    # Adiciona crédito
    balance.add_credit(10.0)
    print("  ✓ Crédito adicionado: R$ 10.00")
    print("  ✓ Novo saldo:", balance.get_balance())
    
    # Cria transação
    tx_id = transactions.create(
        transaction_id="test_001",
        payment_method=PaymentMethod.CASH,
        amount=10.0,
        status=PaymentStatus.APPROVED
    )
    print(f"  ✓ Transação criada: ID {tx_id}")
    
    # Adiciona música à fila
    song_id = queue.add_song(
        video_id="dQw4w9WgXcQ",
        title="Never Gonna Give You Up",
        artist="Rick Astley"
    )
    print(f"  ✓ Música adicionada à fila: ID {song_id}")
    
    # Lista fila
    queue_list = queue.get_queue()
    print(f"  ✓ Tamanho da fila: {len(queue_list)}")
    
    print("✅ Banco de dados funcionando!\n")
    return True


def test_config():
    """Testa configurações"""
    print("🧪 Testando configurações...")
    
    from src.server.config import BusinessConfig, PaymentMethod
    
    # Testa cálculo de preços
    for method in PaymentMethod:
        price = BusinessConfig.calculate_price(method)
        print(f"  ✓ Preço para {method.value}: R$ {price:.2f}")
    
    print("✅ Configurações funcionando!\n")
    return True


def test_hardware():
    """Testa módulo de hardware"""
    print("🧪 Testando hardware...")
    
    from src.hardware import BillAcceptor
    
    credits_received = []
    
    def callback(amount):
        credits_received.append(amount)
    
    acceptor = BillAcceptor(callback=callback)
    print(f"  ✓ Bill acceptor inicializado (enabled: {acceptor.enabled})")
    
    # Simula pulsos
    acceptor.simulate_pulse(2)
    print(f"  ✓ Pulsos simulados: {len(credits_received)}")
    print(f"  ✓ Total recebido: R$ {sum(credits_received):.2f}")
    
    acceptor.cleanup()
    print("✅ Hardware funcionando!\n")
    return True


def test_payments():
    """Testa módulo de pagamentos"""
    print("🧪 Testando módulo de pagamentos...")
    
    from src.payments import PaymentStatus
    from src.payments.base_gateway import BasePaymentGateway
    
    print(f"  ✓ Status de pagamento disponíveis:")
    for status in PaymentStatus:
        print(f"    - {status.value}")
    
    print("✅ Módulo de pagamentos funcionando!\n")
    return True


def main():
    """Executa todos os testes"""
    print("=" * 50)
    print("🎵 JUKEBOX-PI-MONEY - TESTES")
    print("=" * 50)
    print()
    
    tests = [
        ("Configurações", test_config),
        ("Banco de Dados", test_database),
        ("Hardware", test_hardware),
        ("Pagamentos", test_payments),
    ]
    
    results = []
    
    for name, test_func in tests:
        try:
            result = test_func()
            results.append((name, result))
        except Exception as e:
            print(f"❌ Erro em {name}: {e}\n")
            results.append((name, False))
    
    # Resumo
    print("=" * 50)
    print("📊 RESUMO DOS TESTES")
    print("=" * 50)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASSOU" if result else "❌ FALHOU"
        print(f"{status}: {name}")
    
    print()
    print(f"Total: {passed}/{total} testes passaram")
    print("=" * 50)
    
    return passed == total


if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
