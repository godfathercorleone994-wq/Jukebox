# 🚀 Guia Rápido: Como Habilitar o Teste no Navegador

## 📝 Resumo

Este guia mostra como configurar o GitHub Pages para testar o Jukebox diretamente no navegador, sem instalar nada.

## ✅ Passo a Passo

### 1️⃣ Aceitar este Pull Request

Primeiro, aceite e faça merge deste Pull Request para a branch `main` ou `master`.

### 2️⃣ Habilitar GitHub Pages

1. Vá para o seu repositório no GitHub
2. Clique em **Settings** (⚙️ Configurações)
3. No menu lateral esquerdo, role até encontrar **Pages**
4. Em **Source** (Origem), selecione **GitHub Actions**
5. A página será salva automaticamente

### 3️⃣ Executar o Workflow

Existem duas formas:

#### Opção A - Automática (Recomendada)
O workflow será executado automaticamente após o merge para `main`/`master`.

#### Opção B - Manual
1. Vá para a aba **Actions** no repositório
2. Clique no workflow **"Deploy to GitHub Pages"**
3. Clique no botão **Run workflow** (lado direito)
4. Selecione a branch `main` ou `master`
5. Clique em **Run workflow** (botão verde)

### 4️⃣ Aguardar a Conclusão

O workflow leva aproximadamente 1-2 minutos. Você pode acompanhar o progresso na aba **Actions**.

### 5️⃣ Acessar o Site

Após a conclusão:

1. Volte para **Settings** > **Pages**
2. Você verá uma mensagem: **"Your site is live at..."**
3. A URL será algo como: `https://godfathercorleone994-wq.github.io/Jukebox/`
4. Clique no link ou copie e cole no navegador

## 🎵 O que você pode fazer?

No site publicado, você poderá:

✅ Testar o **YouTube Player** interativo  
✅ Reproduzir músicas usando apenas URL ou ID do YouTube  
✅ Ver a interface funcionando em tempo real  
✅ Compartilhar o link para outras pessoas testarem  

## 🔍 URLs Úteis

- **Página principal**: `https://[seu-usuario].github.io/Jukebox/`
- **Demo do Player**: `https://[seu-usuario].github.io/Jukebox/demo.html`

## ⚠️ Importante

- O repositório deve ser **público** para usar GitHub Pages gratuitamente
- Ou você pode ter GitHub Pro/Enterprise para repos privados
- Apenas o **frontend** é publicado (sem backend Flask)
- Para o sistema completo, veja [DEPLOY.md](DEPLOY.md)

## 🐛 Problemas?

Se algo não funcionar:

1. Verifique se o workflow foi executado com sucesso em **Actions**
2. Aguarde alguns minutos para propagação
3. Limpe o cache do navegador (Ctrl+F5)
4. Consulte [GITHUB_PAGES.md](GITHUB_PAGES.md) para troubleshooting detalhado

## 📚 Documentação Completa

Para mais detalhes, consulte: [GITHUB_PAGES.md](GITHUB_PAGES.md)

---

**Pronto! 🎉 Em poucos minutos você terá uma demo online do Jukebox!**
