# 🌐 Testando o Jukebox no Navegador via GitHub Pages

Este documento explica como testar o código do Jukebox diretamente no navegador através do GitHub Pages.

## 📋 O que é este recurso?

Um workflow do GitHub Actions que automaticamente implanta uma versão de demonstração do frontend do Jukebox no GitHub Pages. Isso permite:

- ✅ Testar a interface sem instalar nada localmente
- ✅ Visualizar mudanças em pull requests
- ✅ Demonstrar funcionalidades para colaboradores
- ✅ Testar o player do YouTube diretamente no navegador

## 🚀 Como funciona?

### Implantação Automática

O workflow `.github/workflows/deploy-pages.yml` é executado automaticamente quando:

1. **Push para branch main/master**: Qualquer commit na branch principal dispara a implantação
2. **Execução manual**: Você pode executar manualmente via GitHub Actions tab

### O que é implantado?

- **Página inicial**: Lista de demos disponíveis
- **YouTube Player Demo**: Interface de teste do player de YouTube com IFrame API
- **Arquivos estáticos**: JavaScript necessário para funcionamento

## 📝 Configuração Inicial

### 1. Habilitar GitHub Pages

1. Vá para o repositório no GitHub
2. Clique em **Settings** (Configurações)
3. No menu lateral, clique em **Pages**
4. Em **Source** (Origem), selecione **GitHub Actions**
5. Salve as configurações

### 2. Executar o Workflow

#### Opção A: Push para branch main/master
```bash
git add .
git commit -m "Adicionar workflow de GitHub Pages"
git push origin main
```

#### Opção B: Execução Manual
1. Vá para a aba **Actions** no repositório
2. Clique no workflow **Deploy to GitHub Pages**
3. Clique no botão **Run workflow**
4. Selecione a branch e clique em **Run workflow**

### 3. Acessar o Site

Após a conclusão do workflow (geralmente leva 1-2 minutos):

1. Vá para **Settings** > **Pages**
2. Você verá a URL do site: `https://<seu-usuario>.github.io/<nome-repo>/`
3. Ou verifique o link na aba **Actions** > clique no workflow executado > veja a URL no job "deploy"

## 🎯 Funcionalidades Disponíveis

### YouTube Player Demo

Acesse `https://<seu-usuario>.github.io/<nome-repo>/demo.html` para testar:

- ✅ Reproduzir vídeos do YouTube usando apenas o ID ou URL completa
- ✅ Controles de Play, Pause e Stop
- ✅ Reprodução apenas de áudio (sem vídeo visível)
- ✅ Interface moderna e responsiva

### Exemplos de URLs aceitas:
- URL completa: `https://www.youtube.com/watch?v=dQw4w9WgXcQ`
- URL curta: `https://youtu.be/dQw4w9WgXcQ`
- Apenas ID: `dQw4w9WgXcQ`

## 🔧 Estrutura do Workflow

```yaml
.github/workflows/deploy-pages.yml
├── build job
│   ├── Checkout código
│   ├── Setup GitHub Pages
│   ├── Preparar arquivos (_site/)
│   └── Upload artifact
└── deploy job
    └── Deploy para GitHub Pages
```

### Arquivos Implantados:
```
_site/
├── index.html              # Página principal com lista de demos
├── demo.html               # Demo do YouTube Player
└── static/
    └── js/
        └── youtube-player.js  # Módulo do player
```

## 🛠️ Customização

### Adicionar Novas Demos

Para adicionar uma nova demo ao GitHub Pages:

1. Edite o workflow `.github/workflows/deploy-pages.yml`
2. Na seção "Preparar arquivos para GitHub Pages", adicione:
   ```bash
   # Copiar sua nova demo
   cp caminho/para/sua-demo.html _site/minha-demo.html
   ```
3. Adicione um link na página principal editando o `_site/index.html`

### Modificar a Página Principal

A página inicial é gerada dinamicamente no workflow. Para modificá-la:

1. Edite o conteúdo dentro do `cat > _site/index.html << 'EOF'` no workflow
2. Faça commit e push
3. O workflow será executado automaticamente

## 🐛 Troubleshooting

### O workflow falha com "Permission denied"

**Solução**: Verifique se as permissões do workflow estão corretas:
1. Vá em **Settings** > **Actions** > **General**
2. Em "Workflow permissions", selecione "Read and write permissions"
3. Salve e execute o workflow novamente

### GitHub Pages não está disponível

**Solução**: 
1. Verifique se o repositório é público (GitHub Pages Free requer repo público)
2. Ou se tem GitHub Pro/Enterprise para repos privados com Pages

### A página não atualiza

**Solução**:
1. Limpe o cache do navegador (Ctrl+F5 ou Cmd+Shift+R)
2. Aguarde alguns minutos para propagação do DNS
3. Verifique se o workflow foi executado com sucesso em **Actions**

### Arquivos não encontrados (404)

**Solução**:
1. Verifique os logs do workflow na aba **Actions**
2. Confirme que os arquivos foram copiados corretamente
3. Verifique os caminhos relativos no código HTML/JS

## 📚 Recursos Adicionais

- [Documentação oficial do GitHub Pages](https://docs.github.com/pages)
- [Documentação do GitHub Actions](https://docs.github.com/actions)
- [Guia completo do Jukebox](../README.md)

## ❓ Perguntas Frequentes

**P: Preciso pagar para usar GitHub Pages?**
R: Não, GitHub Pages é gratuito para repositórios públicos.

**P: Posso usar domínio customizado?**
R: Sim, você pode configurar um domínio customizado nas configurações do GitHub Pages.

**P: O backend Flask também é implantado?**
R: Não, apenas o frontend estático. Para o sistema completo, veja [DEPLOY.md](../DEPLOY.md).

**P: Quanto tempo leva para atualizar?**
R: Geralmente 1-2 minutos após o workflow completar.

## 🤝 Contribuindo

Se você adicionar novas demos ou melhorias, considere:

1. Documentar a nova funcionalidade aqui
2. Adicionar exemplos de uso
3. Atualizar a página principal com o novo link

---

**Desenvolvido com ❤️ para facilitar testes e demonstrações do Jukebox**
