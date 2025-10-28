# 🚀 Quick Start - Executável Jukebox

Guia rápido para usuários que baixaram o executável standalone do Jukebox.

## 📦 O que você baixou?

Um executável standalone que **não precisa de Python** instalado!
- ✅ Todas as dependências incluídas
- ✅ Pronto para usar
- ✅ Funciona em qualquer Linux ou Windows

## 🐧 Linux

### Passo 1: Tornar executável
```bash
chmod +x jukebox
```

### Passo 2: Criar arquivo de configuração
```bash
# Crie um arquivo .env no mesmo diretório
nano .env
```

Adicione o conteúdo mínimo:
```bash
# Configurações básicas
FLASK_ENV=production
SECRET_KEY=mude-isto-para-algo-secreto-e-aleatorio

# Desabilitar hardware GPIO (para PC)
HARDWARE_ENABLED=false

# YouTube Player (opcional)
YOUTUBE_ENABLED=false

# Pagamentos (opcional)
PAYMENT_PROVIDER=mercadopago
# PAYMENT_API_KEY=sua_chave_aqui
# PAYMENT_ACCESS_TOKEN=seu_token_aqui

# Preços
PRICE_PER_SONG=5.00

# Código de operador (opcional)
ADMIN_ENABLED=false
# ADMIN_CODE=seu_codigo_secreto
# ADMIN_CREDIT_AMOUNT=20.00
```

### Passo 3: Executar
```bash
./jukebox
```

### Passo 4: Acessar
Abra o navegador em:
```
http://localhost:5000
```

## 🪟 Windows

### Passo 1: Criar arquivo de configuração
Crie um arquivo chamado `.env` no mesmo diretório do `jukebox.exe` com o conteúdo:

```
# Configurações básicas
FLASK_ENV=production
SECRET_KEY=mude-isto-para-algo-secreto-e-aleatorio

# Desabilitar hardware GPIO (para PC)
HARDWARE_ENABLED=false

# YouTube Player (opcional)
YOUTUBE_ENABLED=false

# Pagamentos (opcional)
PAYMENT_PROVIDER=mercadopago
# PAYMENT_API_KEY=sua_chave_aqui
# PAYMENT_ACCESS_TOKEN=seu_token_aqui

# Preços
PRICE_PER_SONG=5.00

# Código de operador (opcional)
ADMIN_ENABLED=false
# ADMIN_CODE=seu_codigo_secreto
# ADMIN_CREDIT_AMOUNT=20.00
```

### Passo 2: Executar
Duplo clique em `jukebox.exe` ou execute via linha de comando:
```cmd
jukebox.exe
```

### Passo 3: Acessar
Abra o navegador em:
```
http://localhost:5000
```

## ⌨️ Navegação

A interface suporta navegação completa por teclado:
- **Setas (↑↓←→)**: Navegar
- **Enter**: Selecionar
- **Tab**: Próximo elemento
- **1-9**: Seleção rápida
- **F1 ou ?**: Ajuda de atalhos
- **Esc**: Voltar/Cancelar

## 🎵 Como usar

1. **Selecione método de pagamento**:
   - Dinheiro (simulação para testes)
   - PIX, Débito, Crédito (requer configuração)

2. **Adicione créditos**:
   - Use o endpoint de simulação para testes:
   ```bash
   curl -X POST http://localhost:5000/api/hardware/simulate-cash \
     -H "Content-Type: application/json" \
     -d '{"count":2}'
   ```

3. **Busque e adicione músicas** na interface

4. **Aproveite!** 🎶

## 🔐 Código de Operador (Opcional)

Para adicionar créditos instantaneamente sem pagamento:

1. Configure no `.env`:
   ```bash
   ADMIN_ENABLED=true
   ADMIN_CODE=seu_codigo_secreto
   ADMIN_CREDIT_AMOUNT=20.00
   ```

2. Na interface, pressione **Ctrl+Shift+A**

3. Digite o código secreto

4. Créditos serão adicionados instantaneamente!

## 🛑 Parar o servidor

Pressione **Ctrl+C** no terminal onde o jukebox está rodando.

## 🐛 Problemas?

### Erro: "Address already in use"
Outra aplicação está usando a porta 5000. Você pode:
1. Parar a outra aplicação
2. Ou adicionar no `.env`: `FLASK_PORT=8080` e acessar http://localhost:8080

### Erro: "Failed to execute script"
1. Verifique se o arquivo `.env` existe no mesmo diretório
2. Execute via terminal para ver mensagens de erro detalhadas

### Erro de permissão (Linux)
```bash
chmod +x jukebox
```

### Windows Defender bloqueia
Adicione exceção no Windows Defender para a pasta do jukebox.

## 📖 Documentação completa

Quer saber mais? Veja a documentação completa no GitHub:
- [README.md](https://github.com/godfathercorleone994-wq/Jukebox/blob/main/README.md)
- [BUILD.md](https://github.com/godfathercorleone994-wq/Jukebox/blob/main/BUILD.md)
- [API.md](https://github.com/godfathercorleone994-wq/Jukebox/blob/main/API.md)

## 🌐 Testar online (sem instalar)

Prefere testar no navegador primeiro?
https://godfathercorleone994-wq.github.io/Jukebox/

---

**Desenvolvido com ❤️ para a comunidade**
