#!/bin/bash
# Script de exemplo para testar o sistema de música idle

echo "🎵 Testando Sistema de Música Idle"
echo "=================================="
echo ""

BASE_URL="http://localhost:5000/api"

# 1. Verificar status do sistema
echo "1. Verificando status do sistema idle..."
curl -s "$BASE_URL/idle/status" | python3 -m json.tool
echo ""

# 2. Verificar status geral da jukebox
echo "2. Status geral da jukebox..."
curl -s "$BASE_URL/status" | python3 -m json.tool
echo ""

# 3. Simular atividade do usuário (apenas em desenvolvimento)
echo "3. Simulando inserção de dinheiro..."
curl -s -X POST "$BASE_URL/hardware/simulate-cash" \
  -H "Content-Type: application/json" \
  -d '{"count": 2}' | python3 -m json.tool
echo ""

# 4. Verificar status idle após atividade
echo "4. Verificando status idle após atividade..."
curl -s "$BASE_URL/idle/status" | python3 -m json.tool
echo ""

# 5. Forçar música idle (apenas em desenvolvimento)
echo "5. Forçando reprodução de música idle..."
curl -s -X POST "$BASE_URL/idle/trigger" | python3 -m json.tool
echo ""

echo "✅ Teste concluído!"
echo ""
echo "💡 Dicas:"
echo "  - O sistema toca música automaticamente após 10 minutos sem atividade"
echo "  - Configure categorias em .env (IDLE_MUSIC_QUERIES)"
echo "  - Ajuste o timeout em .env (IDLE_MUSIC_TIMEOUT)"
echo "  - Desabilite com IDLE_MUSIC_ENABLED=false se necessário"
