# 📱 Guia Rápido - APK Android do Jukebox

## 🎯 O que é?

Este é um aplicativo Android WebView que permite acessar o Jukebox diretamente do seu celular Android. O app funciona como um navegador dedicado que se conecta ao servidor Flask do Jukebox.

## 🏗️ Arquitetura

```
┌─────────────────┐         ┌──────────────────┐
│  Android APK    │ ───────▶│  Servidor Flask  │
│  (WebView)      │         │  (Jukebox)       │
│  No celular     │◀─────── │  Raspberry Pi    │
└─────────────────┘         │  ou PC/Linux     │
                            └──────────────────┘
```

O app Android é apenas uma interface - o servidor Flask precisa estar rodando em algum lugar (Raspberry Pi, PC, ou servidor na nuvem).

## 🚀 Passo a Passo Completo

### Passo 1: Clone o Repositório

```bash
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox
```

### Passo 2: Compile o APK

```bash
# Certifique-se de ter Java instalado
java -version

# Execute o script de build
./build-android.sh
```

**Aguarde**: O primeiro build pode demorar 5-10 minutos pois o Gradle vai baixar o Android SDK e dependências.

O APK será gerado em: `android/app/build/outputs/apk/debug/app-debug.apk`

### Passo 3: Transfira o APK para o Celular

**Opção A - Via USB (Recomendado)**
```bash
# Instale ADB
sudo apt install adb

# Conecte o celular via USB
# Habilite "Depuração USB" no celular (Configurações → Opções do desenvolvedor)

# Instale o APK
adb install android/app/build/outputs/apk/debug/app-debug.apk
```

**Opção B - Via Arquivo**
1. Copie o arquivo APK para o celular (via cabo USB, e-mail, WhatsApp, etc.)
2. No celular, abra o gerenciador de arquivos
3. Toque no arquivo APK
4. Permita instalação de fontes desconhecidas (se solicitado)
5. Confirme a instalação

### Passo 4: Configure o Servidor

O app precisa se conectar a um servidor Flask do Jukebox. Você tem 3 opções:

#### Opção A: Servidor no Raspberry Pi (Produção)

1. Configure o Jukebox no Raspberry Pi seguindo [DEPLOY.md](../DEPLOY.md)
2. Inicie o servidor:
   ```bash
   cd Jukebox
   ./start.sh
   ```
3. Descubra o IP do Raspberry Pi:
   ```bash
   hostname -I
   # Exemplo: 192.168.1.100
   ```
4. No app Android, ele tentará conectar em `http://192.168.1.100:5000`

#### Opção B: Servidor no PC/Linux (Desenvolvimento)

1. No seu PC, inicie o servidor:
   ```bash
   cd Jukebox
   ./start-pc.sh
   ```
2. Descubra o IP do PC:
   ```bash
   hostname -I
   # Exemplo: 192.168.1.50
   ```
3. Configure o app para usar esse IP

#### Opção C: Servidor no Próprio Celular (Termux)

1. Instale o [Termux](https://f-droid.org/en/packages/com.termux/) no celular
2. No Termux:
   ```bash
   pkg install python git
   git clone https://github.com/godfathercorleone994-wq/Jukebox.git
   cd Jukebox
   pip install -r requirements.txt
   python src/server/app.py
   ```
3. O app usará `http://localhost:5000` por padrão

### Passo 5: Configure a URL do Servidor no App

**Antes de Compilar** (recomendado):

Edite `android/app/src/main/java/com/jukebox/app/MainActivity.java` linha 13:

```java
private static final String DEFAULT_URL = "http://192.168.1.100:5000";
```

Substitua `192.168.1.100` pelo IP do seu servidor.

**Depois de Compilar**:

Por enquanto, a URL só pode ser alterada antes da compilação. Em futuras versões, haverá uma tela de configuração no app.

### Passo 6: Abra o App e Teste!

1. Abra o app "Jukebox" no seu celular
2. Se tudo estiver configurado corretamente, você verá a interface do Jukebox
3. Teste adicionar uma música à fila

## 🔧 Solução de Problemas

### Problema: "Não foi possível carregar a página"

**Causas possíveis:**
- Servidor Flask não está rodando
- URL do servidor está incorreta
- Celular e servidor não estão na mesma rede Wi-Fi
- Firewall bloqueando conexões

**Soluções:**
1. Verifique se o servidor está rodando:
   ```bash
   curl http://localhost:5000
   ```
2. Verifique se o celular pode alcançar o servidor:
   ```bash
   # No servidor
   ping <IP_DO_CELULAR>
   
   # No celular (Termux)
   pkg install inetutils
   ping <IP_DO_SERVIDOR>
   ```
3. Configure o firewall para permitir conexões na porta 5000:
   ```bash
   # Ubuntu/Debian
   sudo ufw allow 5000
   
   # Raspberry Pi
   sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
   ```

### Problema: "App não instalou"

**Soluções:**
- Habilite "Fontes desconhecidas" nas configurações do Android
- Verifique se há espaço de armazenamento disponível
- Desinstale versões antigas do app primeiro

### Problema: Build falhou

**Erro: "Could not resolve com.android.tools.build:gradle"**

Isso significa que o Gradle não conseguiu baixar dependências. Verifique:
- Conexão com internet está funcionando
- Proxy/firewall não está bloqueando downloads

## 📊 Especificações Técnicas

- **Tamanho do APK**: ~2-5 MB
- **Android mínimo**: 7.0 (Nougat) - API 24
- **Android alvo**: 13 (API 33)
- **Permissões**: Internet, Estado da rede
- **Arquitetura**: WebView simples com configuração JavaScript habilitada

## 🎨 Personalização

### Alterar o Ícone do App

Substitua os arquivos em `android/app/src/main/res/mipmap-*/` com seus próprios ícones.

### Alterar o Nome do App

Edite `android/app/src/main/res/values/strings.xml`:

```xml
<string name="app_name">Meu Jukebox</string>
```

### Alterar as Cores

Edite `android/app/src/main/res/values/colors.xml` e `styles.xml`.

## 🌐 Uso em Produção

Para usar o app em produção:

1. **Configure HTTPS**: Use um certificado SSL no servidor Flask
2. **Use domínio público**: Configure um domínio ou use serviço como ngrok
3. **Assine o APK**: Para distribuir, assine o APK com sua chave
4. **Teste em múltiplos dispositivos**: Teste em diferentes versões do Android

### Assinar o APK

```bash
# Gerar keystore (primeira vez)
keytool -genkey -v -keystore jukebox.keystore \
  -alias jukebox -keyalg RSA -keysize 2048 -validity 10000

# Compile APK Release
cd android
./gradlew assembleRelease

# Assine o APK
jarsigner -verbose -sigalg SHA256withRSA -digestalg SHA-256 \
  -keystore ../jukebox.keystore \
  app/build/outputs/apk/release/app-release-unsigned.apk jukebox

# Alinhe o APK
zipalign -v 4 \
  app/build/outputs/apk/release/app-release-unsigned.apk \
  app/build/outputs/apk/release/jukebox-release.apk
```

## 💡 Dicas Avançadas

### Usar ngrok para Acesso Remoto

Se você quer acessar o Jukebox de qualquer lugar:

```bash
# Instale o ngrok
wget https://bin.equinox.io/c/4VmDzA7iaHb/ngrok-stable-linux-amd64.zip
unzip ngrok-stable-linux-amd64.zip

# Execute o túnel
./ngrok http 5000

# Use a URL gerada no app Android
# Exemplo: https://abc123.ngrok.io
```

### Modo Kiosk no Android

Para transformar o celular em um terminal dedicado:

1. Instale um app de kiosk mode (ex: "Kiosk Browser")
2. Configure para abrir apenas o app Jukebox
3. Desabilite botões de navegação
4. Fixe o app na tela

## 🔐 Segurança

⚠️ **Importante**: Por padrão, o app aceita HTTP não criptografado. Para produção:

1. Use HTTPS no servidor
2. Adicione autenticação no Flask
3. Configure rate limiting
4. Use um token de API
5. Implemente SSL pinning no app

## 📞 Suporte

Problemas? Abra uma issue:
https://github.com/godfathercorleone994-wq/Jukebox/issues

## 🎉 Pronto!

Agora você tem o Jukebox rodando no seu Android! Aproveite para tocar suas músicas favoritas.

---

**Desenvolvido com ❤️ para a comunidade Jukebox**
