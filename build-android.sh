#!/bin/bash

# Script para compilar o APK do Jukebox Android
# Uso: ./build-android.sh

set -e

echo "🎵 Jukebox Android Build Script"
echo "================================"
echo ""

# Verificar se Java está instalado
if ! command -v java &> /dev/null; then
    echo "❌ Erro: Java não encontrado!"
    echo "Por favor, instale o JDK 11 ou superior:"
    echo "  sudo apt install openjdk-11-jdk"
    exit 1
fi

echo "✅ Java encontrado:"
java -version
echo ""

# Entrar no diretório android
cd "$(dirname "$0")/android"

# Verificar se gradlew existe
if [ ! -f "gradlew" ]; then
    echo "❌ Erro: gradlew não encontrado!"
    exit 1
fi

# Dar permissão de execução ao gradlew
chmod +x gradlew

echo "🔨 Limpando build anterior..."
./gradlew clean

echo ""
echo "🔨 Compilando APK..."
./gradlew assembleRelease

echo ""
echo "✅ Compilação concluída!"
echo ""
echo "📱 APK gerado em:"
echo "   android/app/build/outputs/apk/release/app-release-unsigned.apk"
echo ""
echo "📲 Para instalar no celular:"
echo "   1. Via USB: adb install app/build/outputs/apk/release/app-release-unsigned.apk"
echo "   2. Copiar APK para o celular e instalar manualmente"
echo ""
echo "📖 Veja android/README.md para instruções completas"
echo ""
