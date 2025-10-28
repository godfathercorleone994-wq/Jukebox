#!/usr/bin/env python3
"""
Teste de integração para navegação por teclado
Verifica que os arquivos HTML, CSS e JS possuem os componentes necessários
"""

import sys
import os
from pathlib import Path

# Adiciona src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

def test_html_keyboard_support():
    """Testa se o HTML contém elementos para navegação por teclado"""
    print("🧪 Testando suporte de teclado no HTML...")
    
    html_path = Path(__file__).parent.parent / "src" / "server" / "static" / "index.html"
    
    with open(html_path, 'r') as f:
        html_content = f.read()
    
    # Verifica elementos necessários
    checks = [
        ('keyboard-hints', 'Painel de ajuda de teclado'),
        ('⌨️', 'Ícone de teclado'),
        ('Atalhos de Teclado', 'Texto de atalhos'),
    ]
    
    for check, desc in checks:
        if check in html_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ HTML com suporte a teclado!\n")
    return True


def test_css_keyboard_support():
    """Testa se o CSS contém estilos para navegação por teclado"""
    print("🧪 Testando estilos de teclado no CSS...")
    
    css_path = Path(__file__).parent.parent / "src" / "server" / "static" / "style.css"
    
    with open(css_path, 'r') as f:
        css_content = f.read()
    
    # Verifica estilos necessários
    checks = [
        ('.keyboard-focus', 'Estilo de foco de teclado'),
        ('.keyboard-number', 'Números para seleção rápida'),
        ('.keyboard-hint', 'Painel de dicas'),
    ]
    
    for check, desc in checks:
        if check in css_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ CSS com estilos de teclado!\n")
    return True


def test_js_keyboard_support():
    """Testa se o JavaScript contém funções para navegação por teclado"""
    print("🧪 Testando lógica de teclado no JavaScript...")
    
    js_path = Path(__file__).parent.parent / "src" / "server" / "static" / "app.js"
    
    with open(js_path, 'r') as f:
        js_content = f.read()
    
    # Verifica funções necessárias
    checks = [
        ('keyboardNavigation', 'Estado da navegação por teclado'),
        ('initKeyboardNavigation', 'Função de inicialização'),
        ('handleKeyboardNavigation', 'Handler de eventos de teclado'),
        ('updateFocusableElements', 'Atualização de elementos focáveis'),
        ('moveFocus', 'Movimentação de foco'),
        ('toggleKeyboardHints', 'Toggle de dicas'),
        ('ArrowUp', 'Suporte a seta para cima'),
        ('ArrowDown', 'Suporte a seta para baixo'),
        ('Enter', 'Suporte a tecla Enter'),
        ('Escape', 'Suporte a tecla Esc'),
    ]
    
    for check, desc in checks:
        if check in js_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ JavaScript com navegação por teclado!\n")
    return True


def test_pc_launcher():
    """Testa se o script de lançamento para PC existe e é executável"""
    print("🧪 Testando script de lançamento para PC...")
    
    script_path = Path(__file__).parent.parent / "start-pc.sh"
    
    if not script_path.exists():
        print(f"  ✗ Script start-pc.sh não encontrado")
        return False
    
    print(f"  ✓ Script start-pc.sh existe")
    
    if not os.access(script_path, os.X_OK):
        print(f"  ✗ Script não é executável")
        return False
    
    print(f"  ✓ Script é executável")
    
    # Verifica conteúdo do script
    with open(script_path, 'r') as f:
        script_content = f.read()
    
    checks = [
        ('IS_RASPBERRY_PI', 'Detecção de Raspberry Pi'),
        ('HARDWARE_ENABLED=false', 'Desabilitar hardware no PC'),
        ('YOUTUBE_ENABLED=false', 'Desabilitar YouTube no PC'),
        ('FLASK_ENV=development', 'Modo desenvolvimento'),
        ('grep -v "RPi.GPIO"', 'Exclusão de RPi.GPIO'),
    ]
    
    for check, desc in checks:
        if check in script_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ Script de lançamento para PC configurado!\n")
    return True


def test_documentation():
    """Testa se a documentação para PC existe"""
    print("🧪 Testando documentação...")
    
    doc_path = Path(__file__).parent.parent / "PC-LINUX.md"
    
    if not doc_path.exists():
        print(f"  ✗ Documentação PC-LINUX.md não encontrada")
        return False
    
    print(f"  ✓ Documentação PC-LINUX.md existe")
    
    with open(doc_path, 'r') as f:
        doc_content = f.read()
    
    # Verifica seções importantes
    checks = [
        ('Navegação por Teclado', 'Seção de navegação por teclado'),
        ('start-pc.sh', 'Referência ao script PC'),
        ('Atalhos Disponíveis', 'Tabela de atalhos'),
        ('Raspberry Pi', 'Comparação com Raspberry Pi'),
    ]
    
    for check, desc in checks:
        if check in doc_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ Documentação completa!\n")
    return True


def test_readme_updates():
    """Testa se o README principal foi atualizado"""
    print("🧪 Testando atualização do README...")
    
    readme_path = Path(__file__).parent.parent / "README.md"
    
    with open(readme_path, 'r') as f:
        readme_content = f.read()
    
    # Verifica menções ao suporte PC
    checks = [
        ('PC/Linux', 'Menção a PC/Linux'),
        ('start-pc.sh', 'Referência ao script PC'),
        ('teclado', 'Menção a navegação por teclado'),
        ('PC-LINUX.md', 'Link para documentação PC'),
    ]
    
    for check, desc in checks:
        if check in readme_content:
            print(f"  ✓ {desc} presente")
        else:
            print(f"  ✗ {desc} ausente")
            return False
    
    print("✅ README atualizado!\n")
    return True


def main():
    """Executa todos os testes de integração"""
    print("=" * 50)
    print("🎵 JUKEBOX - TESTES DE NAVEGAÇÃO POR TECLADO")
    print("=" * 50)
    print()
    
    tests = [
        ("HTML - Elementos de Teclado", test_html_keyboard_support),
        ("CSS - Estilos de Teclado", test_css_keyboard_support),
        ("JavaScript - Lógica de Teclado", test_js_keyboard_support),
        ("Script PC Launcher", test_pc_launcher),
        ("Documentação PC/Linux", test_documentation),
        ("README Atualizado", test_readme_updates),
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
