# 🚀 Guia Rápido - Sistema de Código Admin

## O que foi implementado?

Um sistema secreto que permite operadores da máquina adicionarem créditos sem pagamento, ideal para:
- 🎵 Tocar músicas específicas sem inserir dinheiro
- 🧪 Testar o sistema
- 🎁 Dar créditos promocionais
- 🎤 Demonstrações para clientes

## Como usar AGORA MESMO

### 1️⃣ Configure o código (arquivo `.env`)

Crie ou edite o arquivo `.env` na raiz do projeto:

```bash
# Sistema de código admin
ADMIN_ENABLED=true
ADMIN_CODE=seu_codigo_secreto
ADMIN_CREDIT_AMOUNT=20.00
```

**DICA**: Use um código forte, não óbvio como "1234"!

### 2️⃣ Inicie o servidor

```bash
cd /home/runner/work/Jukebox/Jukebox
python3 src/server/app.py
```

Ou use o script de inicialização:
```bash
./start.sh
```

### 3️⃣ Abra o Jukebox no navegador

```
http://localhost:5000
```

### 4️⃣ Use o código admin

1. **Pressione**: `Ctrl + Shift + A` (no teclado)
2. **Digite**: seu código secreto
3. **Pressione**: `Enter` ou clique em "Confirmar"
4. **Pronto**: R$ 20,00 adicionados ao saldo! 💰

### 5️⃣ Adicione músicas

Agora você tem créditos! Use-os para adicionar músicas:
1. Clique em "Buscar Música"
2. Digite o nome da música
3. Adicione à fila
4. Aproveite! 🎶

## 🎯 Exemplo Prático

```bash
# 1. Abrir Jukebox no navegador
firefox http://localhost:5000

# 2. No Jukebox:
#    - Pressione: Ctrl+Shift+A
#    - Digite: 1234 (ou seu código)
#    - Enter

# 3. Agora você tem R$ 20,00!
#    - Busque: "Bohemian Rhapsody"
#    - Adicione à fila
#    - Música tocando! 🎵
```

## ⚠️ IMPORTANTE

### Segurança
- ⛔ **NÃO compartilhe** o código publicamente
- 🔒 **Mantenha** o código em segredo
- 👥 **Apenas operadores** devem conhecer
- 📝 **Monitore** os logs regularmente

### Auditoria
Todas as transações admin são registradas:
- No banco de dados com prefixo `admin_`
- Nos logs do sistema
- Podem ser auditadas a qualquer momento

## 🐛 Resolução de Problemas

### Modal não abre (Ctrl+Shift+A não funciona)
```bash
# Solução: Recarregue a página
# Pressione F5 no navegador
```

### Código não funciona
```bash
# Verifique o arquivo .env:
cat .env | grep ADMIN

# Deve mostrar:
# ADMIN_ENABLED=true
# ADMIN_CODE=seu_codigo
# ADMIN_CREDIT_AMOUNT=20.00
```

### Servidor não inicia
```bash
# Instale dependências:
pip3 install flask flask-cors python-dotenv

# Inicie novamente:
python3 src/server/app.py
```

## 📚 Documentação Completa

Para mais detalhes, consulte:
- **ADMIN_CODE.md** - Documentação completa
- **README.md** - Visão geral do sistema
- **API.md** - Detalhes da API

## 🎉 Pronto!

Você agora tem:
- ✅ Sistema de código admin funcionando
- ✅ Créditos sob demanda
- ✅ Músicas sem pagamento
- ✅ Sistema totalmente testado
- ✅ Documentação completa

**Aproveite o seu Jukebox! 🎵🎸🎹**

---

💡 **Dica Pro**: Configure `ADMIN_CREDIT_AMOUNT=50.00` para ter mais créditos por uso!
