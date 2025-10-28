#!/usr/bin/env python3
"""
Script de verificação manual do sistema de código admin
Demonstra o funcionamento do sistema
"""

import sys
import os

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.server.config import AdminConfig, FlaskConfig
from src.db import Database, CreditBalance
import tempfile
from pathlib import Path

def main():
    print("=" * 60)
    print("🔐 VERIFICAÇÃO DO SISTEMA DE CÓDIGO ADMIN")
    print("=" * 60)
    print()
    
    # Mostra configuração
    print("📋 Configuração Atual:")
    print(f"  - Admin habilitado: {AdminConfig.ADMIN_ENABLED}")
    print(f"  - Código: {'*' * len(AdminConfig.ADMIN_CODE)}")
    print(f"  - Valor por uso: R$ {AdminConfig.ADMIN_CREDIT_AMOUNT:.2f}")
    print()
    
    # Cria banco temporário para demonstração
    temp_db = Path(tempfile.gettempdir()) / "demo_admin.db"
    
    try:
        print("🧪 Simulando uso do código admin...")
        print()
        
        db = Database(db_path=temp_db)
        credit_balance = CreditBalance(db)
        
        # Estado inicial
        initial_balance = credit_balance.get_balance()
        print(f"1️⃣ Saldo inicial: R$ {initial_balance:.2f}")
        
        # Simula adição de crédito admin
        print(f"2️⃣ Operador usa código admin (simulação)...")
        amount = AdminConfig.ADMIN_CREDIT_AMOUNT
        new_balance = credit_balance.add_credit(amount)
        print(f"3️⃣ Sistema adiciona créditos: R$ {amount:.2f}")
        print(f"4️⃣ Novo saldo: R$ {new_balance:.2f}")
        
        # Verifica saldo
        assert new_balance == initial_balance + amount, "Erro: saldo incorreto!"
        
        print()
        print("✅ Sistema funcionando corretamente!")
        print()
        
        print("📝 Como usar no Jukebox:")
        print("  1. Abra o Jukebox no navegador")
        print("  2. Pressione Ctrl+Shift+A")
        print("  3. Digite o código configurado")
        print("  4. Créditos serão adicionados")
        print("  5. Use os créditos para adicionar músicas")
        print()
        
        print("⚠️  LEMBRE-SE:")
        print("  - Mantenha o código em segredo")
        print("  - Apenas operadores devem ter acesso")
        print("  - Todas as transações são registradas")
        print("  - Monitore os logs regularmente")
        print()
        
        print("📚 Mais informações: ADMIN_CODE.md")
        
    finally:
        # Limpa banco temporário
        if temp_db.exists():
            temp_db.unlink()
    
    print()
    print("=" * 60)

if __name__ == '__main__':
    try:
        main()
        sys.exit(0)
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
