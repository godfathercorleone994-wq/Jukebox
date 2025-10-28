# 📱 Jukebox Android APK

Este guia explica como compilar e instalar o aplicativo Android do Jukebox no seu celular.

## 📋 Pré-requisitos

Para compilar o APK, você precisará de:

1. **JDK (Java Development Kit) 11 ou superior**
   ```bash
   # Ubuntu/Debian
   sudo apt install openjdk-11-jdk
   
   # Verificar instalação
   java -version
   ```

2. **Android SDK** (opcional, o Gradle baixará automaticamente se necessário)

## 🚀 Como Compilar o APK

### Opção 1: Script Automático (Recomendado)

```bash
# No diretório raiz do projeto
./build-android.sh
```

O APK será gerado em: `android/app/build/outputs/apk/release/app-release-unsigned.apk`

### Opção 2: Manualmente

```bash
# Entre no diretório android
cd android

# Dê permissão de execução ao gradlew (primeira vez)
chmod +x gradlew

# Compile o APK
./gradlew assembleRelease

# O APK estará em: app/build/outputs/apk/release/app-release-unsigned.apk
```

### Opção 3: Compilar APK Debug (para testes)

```bash
cd android
./gradlew assembleDebug

# APK em: app/build/outputs/apk/debug/app-debug.apk
```

## 📲 Como Instalar no Celular

### Método 1: Via USB (ADB)

1. **Ative o modo desenvolvedor no Android:**
   - Configurações → Sobre o telefone → Toque 7x em "Número da versão"
   
2. **Ative a depuração USB:**
   - Configurações → Opções do desenvolvedor → Depuração USB

3. **Instale via ADB:**
   ```bash
   # Instale o ADB se não tiver
   sudo apt install adb
   
   # Conecte o celular via USB
   # Instale o APK
   adb install android/app/build/outputs/apk/release/app-release-unsigned.apk
   ```

### Método 2: Transferir APK Diretamente

1. **Copie o APK para o celular:**
   - Conecte via USB e copie o arquivo APK
   - Ou envie por e-mail, WhatsApp, etc.

2. **Instale no celular:**
   - Abra o gerenciador de arquivos
   - Navegue até o APK
   - Toque no arquivo
   - Permita instalação de fontes desconhecidas (se solicitado)
   - Confirme a instalação

## ⚙️ Configuração do App

### URL do Servidor

O app precisa se conectar ao servidor Flask do Jukebox. Por padrão, está configurado para `http://localhost:5000`.

Para alterar a URL do servidor, você tem duas opções:

#### Opção 1: Antes de Compilar

Edite o arquivo `android/app/src/main/java/com/jukebox/app/MainActivity.java`:

```java
private static final String DEFAULT_URL = "http://SEU_IP:5000";
```

Exemplos:
- Servidor na rede local: `http://192.168.1.100:5000`
- Servidor remoto: `https://seu-dominio.com`

#### Opção 2: Depois de Instalar (Avançado)

O app usa SharedPreferences para armazenar a URL. Você pode criar uma Activity de configuração ou usar adb:

```bash
adb shell "run-as com.jukebox.app \
  echo 'http://192.168.1.100:5000' > shared_prefs/JukeboxPrefs.xml"
```

## 🔧 Cenários de Uso

### Cenário 1: Servidor no Celular (Termux)

Se você executar o servidor Flask no próprio celular usando Termux:

1. Instale o Termux na Play Store
2. No Termux, instale Python e execute o servidor:
   ```bash
   pkg install python
   cd jukebox
   python src/server/app.py
   ```
3. Use a URL padrão: `http://localhost:5000`

### Cenário 2: Servidor em Outro Dispositivo na Rede

Se o servidor está em um Raspberry Pi ou PC na mesma rede:

1. Descubra o IP do servidor:
   ```bash
   # No servidor
   hostname -I
   ```

2. Configure o app para usar esse IP:
   - Edite `MainActivity.java` antes de compilar
   - Ou use a URL: `http://IP_DO_SERVIDOR:5000`

3. Certifique-se de que o firewall permite conexões na porta 5000

### Cenário 3: Servidor Remoto (Internet)

Se você tem o Jukebox hospedado na internet:

1. Configure o app para usar sua URL/domínio
2. Recomenda-se usar HTTPS para segurança
3. Configure CORS no servidor Flask para aceitar requisições do app

## 🔒 Assinatura do APK (Opcional)

Para distribuir o APK publicamente ou na Play Store, você precisa assiná-lo:

```bash
# Gerar keystore (primeira vez)
keytool -genkey -v -keystore jukebox-release-key.jks \
  -keyalg RSA -keysize 2048 -validity 10000 \
  -alias jukebox

# Assinar o APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore jukebox-release-key.jks \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  jukebox

# Otimizar o APK
zipalign -v 4 \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  app/build/outputs/apk/release/app-release-signed.apk
```

## 📱 Requisitos do Dispositivo Android

- **Android 7.0 (Nougat)** ou superior (API 24+)
- Conexão com internet (Wi-Fi ou dados móveis)
- Permissões necessárias:
  - Internet
  - Acesso ao estado da rede

## 🐛 Solução de Problemas

### Erro: "App não instalado"

- Verifique se o espaço de armazenamento está disponível
- Desinstale versões antigas do app
- Ative "Fontes desconhecidas" nas configurações

### Erro: "Não foi possível carregar a página"

- Verifique se o servidor Flask está rodando
- Confirme que a URL está correta
- Teste a URL em um navegador primeiro
- Verifique se o firewall não está bloqueando a conexão

### Erro durante compilação

```bash
# Limpe o build e tente novamente
cd android
./gradlew clean
./gradlew assembleRelease
```

### Problema de compatibilidade Java

```bash
# Instale Java 11
sudo apt install openjdk-11-jdk

# Configure o JAVA_HOME
export JAVA_HOME=/usr/lib/jvm/java-11-openjdk-amd64
```

## 📊 Tamanho do APK

- APK Debug: ~2-5 MB
- APK Release (sem assinar): ~2-4 MB
- APK Release (assinado): ~2-4 MB

## 🎯 Próximos Passos

Após instalar o app:

1. **Configure o servidor Flask** para aceitar conexões externas
2. **Teste a conectividade** entre o app e o servidor
3. **Personalize a interface** se desejar (cores, logo, etc.)
4. **Configure métodos de pagamento** no servidor

## 📚 Recursos Adicionais

- [Documentação do Jukebox](../README.md)
- [API REST](../API.md)
- [Deploy do Servidor](../DEPLOY.md)
- [Android Developer Guide](https://developer.android.com)

## 💡 Dicas

- Use APK Debug durante desenvolvimento (mais rápido de compilar)
- Use APK Release para produção (otimizado e menor)
- Mantenha o código do servidor atualizado
- Configure SSL/HTTPS para conexões seguras em produção
- Considere usar Firebase ou serviço similar para notificações push

## 🤝 Suporte

Problemas ou dúvidas? Abra uma issue no GitHub:
https://github.com/godfathercorleone994-wq/Jukebox/issues

---

**Desenvolvido com ❤️ para a comunidade Jukebox**
