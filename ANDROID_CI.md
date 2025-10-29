# 🤖 GitHub Actions CI para Android APK

## 📋 Visão Geral

Este documento explica o workflow de CI/CD configurado para gerar automaticamente o APK do Jukebox Android.

## 🎯 O que faz?

O workflow **"Build Android APK"** compila automaticamente o aplicativo Android e disponibiliza o APK como artefato para download.

## 🚀 Quando é executado?

O workflow é acionado automaticamente nos seguintes casos:

1. **Push para main/master** - Quando há alterações em:
   - Qualquer arquivo no diretório `android/`
   - O próprio arquivo do workflow

2. **Pull Requests** - Para branches que vão ser mesclados em main/master

3. **Manual** - Via botão "Run workflow" na aba Actions do GitHub

## 📦 Como baixar o APK gerado?

### Passo a Passo:

1. Acesse: https://github.com/godfathercorleone994-wq/Jukebox/actions/workflows/build-android-apk.yml

2. Clique na execução mais recente com ✅ (sucesso)

3. Role até o final da página até a seção **"Artifacts"**

4. Clique em **"jukebox-android-apk"** para baixar (arquivo ZIP)

5. Extraia o APK do arquivo ZIP

6. Transfira para seu celular Android e instale

### Via URL Direta:

```
https://github.com/godfathercorleone994-wq/Jukebox/actions/workflows/build-android-apk.yml
```

## 🔧 Tecnologias Utilizadas

- **GitHub Actions** - Plataforma de CI/CD
- **Ubuntu Latest** - Sistema operacional do runner
- **Java 11 (Temurin)** - JDK para compilação
- **Gradle 8.2** - Sistema de build Android
- **Android SDK 33** - API target do aplicativo

## 📊 Etapas do Workflow

1. **Checkout** - Clona o repositório
2. **Setup JDK** - Instala Java 11 com cache do Gradle
3. **Build APK** - Compila o APK release usando Gradle
4. **Rename APK** - Renomeia para `jukebox-app-release.apk`
5. **Upload Artifact** - Disponibiliza APK para download (retenção: 30 dias)
6. **Build Summary** - Mostra resumo com instruções de download

## 🔐 Assinatura do APK (Opcional)

O workflow inclui suporte para assinatura de APK, mas está desabilitado por padrão.

### Para habilitar a assinatura:

1. **Gerar keystore:**
   ```bash
   keytool -genkey -v -keystore jukebox.keystore \
     -alias jukebox -keyalg RSA -keysize 2048 -validity 10000
   ```

2. **Converter keystore para base64:**
   ```bash
   base64 jukebox.keystore > keystore.base64
   ```

3. **Adicionar secrets no GitHub:**
   - `KEYSTORE_FILE` - Conteúdo do arquivo keystore.base64
   - `KEYSTORE_PASSWORD` - Senha do keystore
   - `KEY_ALIAS` - Alias da chave (jukebox)
   - `KEY_PASSWORD` - Senha da chave

4. **Editar workflow:**
   - Mudar `if: false` para `if: true` na etapa "Sign APK"

## 📱 Informações do APK

- **Nome:** jukebox-app-release.apk
- **Tipo:** Release build (unsigned por padrão)
- **Tamanho:** ~2-3 MB (varia)
- **Min SDK:** Android 7.0 (API 24)
- **Target SDK:** Android 13 (API 33)
- **Retenção:** 30 dias após build

## 🐛 Troubleshooting

### Problema: Workflow não executou

**Solução:** Verifique se houve mudanças no diretório `android/` ou execute manualmente via "workflow_dispatch"

### Problema: Build falhou

**Soluções:**
1. Verifique os logs do workflow no GitHub Actions
2. Teste localmente: `./build-android.sh`
3. Verifique se o código Java/Gradle está correto
4. Confirme que não há erros de compilação

### Problema: Não consigo baixar o artefato

**Soluções:**
1. Certifique-se de que o workflow completou com sucesso (✅)
2. Artefatos expiram após 30 dias - execute novamente se necessário
3. Você precisa estar autenticado no GitHub para baixar artefatos

## 🔄 Executar Manualmente

1. Acesse: https://github.com/godfathercorleone994-wq/Jukebox/actions/workflows/build-android-apk.yml
2. Clique em **"Run workflow"**
3. Selecione a branch (geralmente main)
4. Clique em **"Run workflow"** verde
5. Aguarde a conclusão (~3-5 minutos)
6. Baixe o APK dos artefatos

## 📖 Documentação Relacionada

- [README.md](../README.md) - Documentação principal
- [android/README.md](../android/README.md) - Guia do app Android
- [ANDROID_QUICKSTART.md](../ANDROID_QUICKSTART.md) - Guia rápido Android
- [build-android.sh](../build-android.sh) - Script de build local

## 💡 Dicas

- ✅ O APK gerado é **unsigned** - funciona normalmente mas mostra aviso na instalação
- ✅ Para distribuição em produção, considere assinar o APK
- ✅ Para publicar na Google Play Store, é obrigatório assinar
- ✅ Artefatos são mantidos por 30 dias - baixe logo após o build
- ✅ Cada push/PR gera um novo artefato

## 🆘 Suporte

- 🐛 Issues: https://github.com/godfathercorleone994-wq/Jukebox/issues
- 📧 Email: godfathercorleone994@gmail.com
- 📖 Docs: https://github.com/godfathercorleone994-wq/Jukebox

---

**Desenvolvido com ❤️ para automatizar builds Android**
