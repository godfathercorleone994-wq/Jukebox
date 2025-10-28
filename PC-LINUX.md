# 🖥️ Guia de Uso em PC/Linux

Este guia explica como executar o Jukebox em um PC comum com Linux, sem necessidade de Raspberry Pi ou hardware específico.

## 📋 Requisitos

### Sistema Operacional
- Qualquer distribuição Linux (Ubuntu, Debian, Fedora, Arch, etc.)
- Windows com WSL2 (Windows Subsystem for Linux)
- macOS (com algumas adaptações)

### Software
- Python 3.9 ou superior
- pip (gerenciador de pacotes Python)
- Navegador web moderno (Chrome, Firefox, Edge)

### Hardware
- **Não requer** Raspberry Pi
- **Não requer** aceitador de notas ou hardware GPIO
- **Não requer** touchscreen (funciona com teclado e mouse)
- Conexão à Internet (opcional, para alguns recursos)

## 🚀 Instalação Rápida

### 1. Clone o Repositório

```bash
git clone https://github.com/godfathercorleone994-wq/Jukebox.git
cd Jukebox
```

### 2. Execute o Script de Inicialização para PC

```bash
./start-pc.sh
```

O script automaticamente:
- ✅ Detecta que você está em um PC (não Raspberry Pi)
- ✅ Cria ambiente virtual Python
- ✅ Instala apenas as dependências necessárias (sem RPi.GPIO)
- ✅ Configura o sistema para modo de desenvolvimento
- ✅ Desabilita hardware GPIO automaticamente
- ✅ Inicia o servidor web

### 3. Acesse a Interface

Abra seu navegador em: **http://localhost:5000**

## ⌨️ Navegação por Teclado

O Jukebox possui suporte completo para navegação por teclado, ideal para sistemas sem touchscreen.

### Atalhos Disponíveis

| Tecla | Função |
|-------|--------|
| **F1** ou **?** | Mostrar/ocultar ajuda de atalhos |
| **↑↓←→** | Navegar entre elementos |
| **Enter** | Selecionar/ativar elemento |
| **Espaço** | Ativar elemento focado |
| **Tab** | Próximo elemento |
| **Shift+Tab** | Elemento anterior |
| **1-9** | Seleção rápida (ex: tecla "1" seleciona primeira opção) |
| **H** | Voltar para tela inicial (Home) |
| **R** | Atualizar status |
| **Esc** | Voltar/Cancelar ação atual |
| **F5** | Recarregar página |

### Como Usar

1. **Na tela inicial**: Use as setas ou números (1-4) para selecionar método de pagamento
2. **Na busca de música**: Digite o nome da música e pressione Enter
3. **Navegando resultados**: Use setas para mover entre resultados, Enter para adicionar à fila
4. **Em qualquer tela**: Pressione **H** para voltar ao início, **Esc** para cancelar

### Indicadores Visuais

- Elementos com foco têm **borda dourada brilhante**
- Números aparecem nos cantos dos botões para seleção rápida
- O elemento focado é automaticamente rolado para ficar visível

## 🎯 Funcionalidades Disponíveis em Modo PC

### ✅ Funcionam Completamente

- ✅ Interface web responsiva
- ✅ Navegação por teclado completa
- ✅ Navegação por mouse/touchpad
- ✅ Sistema de créditos e saldo
- ✅ Fila de músicas
- ✅ API REST completa
- ✅ Banco de dados SQLite
- ✅ Simulação de pagamentos para testes
- ✅ Todos os endpoints da API

### ⚠️ Desabilitados por Padrão (mas podem ser habilitados)

- ⚠️ Hardware GPIO (aceitador de notas)
  - Não disponível em PC
  - Use simulação de pagamento para testes
  
- ⚠️ YouTube Player (requer display)
  - Pode ser habilitado se você tiver display conectado
  - Configure `YOUTUBE_ENABLED=true` no `.env`

## 🧪 Modo de Desenvolvimento

O modo PC inicia automaticamente em modo de desenvolvimento, que inclui:

- 🔓 Endpoint de simulação de pagamento desbloqueado
- 📝 Logs detalhados no console
- 🔄 Auto-reload ao modificar código (opcional)
- 🐛 Mensagens de debug mais verbosas

### Simular Inserção de Dinheiro

```bash
# Simular R$ 4,00 (2 pulsos de R$ 2,00)
curl -X POST http://localhost:5000/api/hardware/simulate-cash \
  -H "Content-Type: application/json" \
  -d '{"count":2}'
```

Ou use a interface web para adicionar créditos via métodos digitais (PIX, cartão).

## 🔧 Configuração Avançada

### Habilitar YouTube Player em PC

Se você tem um display conectado e quer testar o YouTube player:

1. Instale o Chrome/Chromium:
   ```bash
   # Ubuntu/Debian
   sudo apt install chromium-browser chromium-chromedriver
   
   # Fedora
   sudo dnf install chromium chromedriver
   ```

2. Edite o `.env`:
   ```bash
   YOUTUBE_ENABLED=true
   CHROME_DRIVER_PATH=/usr/bin/chromedriver
   ```

3. Reinicie o servidor

### Configurar Porta e Host

Edite o `.env`:

```bash
FLASK_HOST=0.0.0.0    # Permite acesso de outros PCs na rede
FLASK_PORT=8080       # Mude a porta se 5000 estiver ocupada
```

### Habilitar Pagamentos Reais

Para testar com gateway de pagamento real:

1. Obtenha credenciais do Mercado Pago
2. Configure no `.env`:
   ```bash
   PAYMENT_DIGITAL_ENABLED=true
   PAYMENT_PROVIDER=mercadopago
   PAYMENT_API_KEY=sua_api_key
   PAYMENT_ACCESS_TOKEN=seu_token
   ```

## 🎮 Exemplo de Uso Completo

### Fluxo com Teclado

1. **Inicie o servidor**: `./start-pc.sh`
2. **Abra o navegador**: `http://localhost:5000`
3. **Pressione F1**: Veja os atalhos disponíveis
4. **Pressione 1**: Seleciona "Dinheiro" (primeira opção)
5. **Sistema vai para tela de busca** (em ambiente de teste, já tem crédito)
6. **Digite**: "Queen Bohemian Rhapsody"
7. **Pressione Enter**: Busca a música
8. **Pressione Enter novamente**: Adiciona música à fila
9. **Pressione H**: Volta ao início

### Fluxo com Mouse

1. Abra `http://localhost:5000`
2. Clique em qualquer método de pagamento
3. Digite nome da música
4. Clique em "Buscar"
5. Clique em "Adicionar" no resultado
6. Música adicionada à fila!

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'RPi'"

✅ **Solução**: Use o script `start-pc.sh` em vez de `start.sh`. O script PC detecta automaticamente que não é Raspberry Pi e não tenta instalar RPi.GPIO.

### "Address already in use" (porta 5000 ocupada)

✅ **Solução**: Mude a porta no `.env`:
```bash
FLASK_PORT=8080
```

### Interface não responde ao teclado

✅ **Solução**: 
- Certifique-se de que não está com foco em um campo de texto
- Pressione Esc para sair de campos de texto
- Recarregue a página (F5)
- Pressione F1 para ver ajuda de teclado

### Não consigo adicionar música (saldo insuficiente)

✅ **Solução**: Use a simulação de pagamento:
```bash
curl -X POST http://localhost:5000/api/hardware/simulate-cash \
  -H "Content-Type: application/json" \
  -d '{"count":3}'
```

## 📊 Comparação PC vs Raspberry Pi

| Funcionalidade | PC/Linux | Raspberry Pi |
|----------------|----------|--------------|
| Interface Web | ✅ Completo | ✅ Completo |
| Teclado | ✅ Completo | ⚠️ Opcional |
| Mouse/Touch | ✅ Completo | ✅ Completo |
| API REST | ✅ Completo | ✅ Completo |
| Banco de Dados | ✅ Completo | ✅ Completo |
| Hardware GPIO | ❌ N/A | ✅ Completo |
| YouTube Player | ⚠️ Opcional | ✅ Completo |
| Modo Kiosk | ⚠️ Manual | ✅ Automático |

## 🎓 Casos de Uso

### Desenvolvimento

- ✅ Desenvolver e testar novas funcionalidades
- ✅ Testar integrações de pagamento
- ✅ Desenvolver interface sem hardware
- ✅ Criar e testar APIs

### Demonstração

- ✅ Demonstrar o sistema em apresentações
- ✅ Fazer testes de usabilidade
- ✅ Treinar operadores
- ✅ Validar fluxos de trabalho

### Produção Alternativa

- ✅ Usar como fallback se Raspberry Pi falhar
- ✅ Rodar em servidor dedicado
- ✅ Deploy em cloud (Heroku, AWS, etc.)

## 🔐 Segurança

### Modo Desenvolvimento

- ⚠️ Não exponha na Internet pública
- ⚠️ Use apenas em redes confiáveis
- ⚠️ Endpoint de simulação está habilitado

### Modo Produção

Para usar em produção (não recomendado, use Raspberry Pi):

1. Mude para produção no `.env`:
   ```bash
   FLASK_ENV=production
   ```

2. Configure tokens fortes:
   ```bash
   SECRET_KEY=$(openssl rand -hex 32)
   HARDWARE_TOKEN=$(openssl rand -hex 32)
   ```

3. Configure firewall apropriadamente
4. Use HTTPS (configure proxy reverso nginx/apache)

## 📚 Recursos Adicionais

- [README Principal](README.md) - Visão geral do projeto
- [API.md](API.md) - Documentação da API REST
- [DEPLOY.md](DEPLOY.md) - Deploy em Raspberry Pi
- [GitHub Issues](https://github.com/godfathercorleone994-wq/Jukebox/issues) - Reporte bugs

## 💡 Dicas

1. **Use o navegador em tela cheia** (F11) para experiência tipo kiosk
2. **Configure atalhos de teclado personalizados** editando `app.js`
3. **Teste a navegação por teclado** antes de usar em produção
4. **Use `start-pc.sh --test`** para rodar testes antes de iniciar
5. **Monitore logs** em `logs/jukebox.log` para debugging

## 🤝 Contribuindo

Encontrou um bug ou tem sugestão de melhoria para o modo PC? 

1. Abra uma [Issue](https://github.com/godfathercorleone994-wq/Jukebox/issues)
2. Faça um Fork e envie Pull Request
3. Entre em contato: godfathercorleone994@gmail.com

---

**Desenvolvido com ❤️ para funcionar em qualquer Linux!**
