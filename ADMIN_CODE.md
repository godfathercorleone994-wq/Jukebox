# Sistema de Código Admin

## 📋 Visão Geral

O sistema de código admin permite que operadores da máquina de Jukebox adicionem créditos artificialmente, sem necessidade de pagamento. Isso é útil quando você deseja:

- Testar o sistema
- Tocar músicas específicas sem inserir dinheiro
- Demonstrar o sistema para clientes
- Dar créditos promocionais
- Evitar ter que ouvir apenas as músicas aleatórias do modo idle

## 🔑 Como Usar

### 1. Ativar o Modal Admin

Na tela principal do Jukebox, pressione a combinação de teclas:

```
Ctrl + Shift + A
```

Isso abrirá um modal discreto solicitando o código de administrador.

### 2. Digitar o Código

Digite o código secreto configurado no arquivo `.env` e pressione **Enter** ou clique em **Confirmar**.

### 3. Créditos Adicionados

Se o código estiver correto:
- Os créditos configurados serão adicionados ao saldo
- Uma mensagem de sucesso será exibida
- O modal será fechado automaticamente
- Você poderá usar os créditos normalmente para adicionar músicas

Se o código estiver incorreto:
- Uma mensagem de erro será exibida
- O campo será limpo para tentar novamente
- Após 3 tentativas incorretas, considere verificar a configuração

## ⚙️ Configuração

### Variáveis de Ambiente

Adicione ou edite as seguintes variáveis no arquivo `.env`:

```bash
# === ADMIN ===
# Habilita funcionalidade de código admin
ADMIN_ENABLED=true

# Código secreto para operadores
# IMPORTANTE: Mantenha este código em segredo!
ADMIN_CODE=1234

# Quantidade de créditos a adicionar (em reais)
ADMIN_CREDIT_AMOUNT=20.00
```

### Recomendações de Segurança

1. **Use um código forte**: Não use códigos óbvios como "1234" ou "0000"
2. **Mantenha o código em segredo**: Compartilhe apenas com operadores autorizados
3. **Rotacione o código periodicamente**: Mude o código regularmente
4. **Monitore os logs**: Verifique os logs para tentativas de uso não autorizado

## 🔒 Segurança

### Validação

- O código é validado no backend (não apenas no frontend)
- Tentativas com código incorreto são registradas nos logs
- A funcionalidade pode ser desabilitada via `ADMIN_ENABLED=false`

### Auditoria

Todas as adições de crédito via código admin são registradas no banco de dados:

- **Tipo de transação**: `admin_*` (identificável pelo prefixo)
- **Método de pagamento**: `cash` (para fins de contabilidade)
- **Status**: `approved`
- **Log**: Registro completo no arquivo de logs

Para verificar transações admin no banco de dados:

```sql
SELECT * FROM transactions WHERE transaction_id LIKE 'admin_%';
```

## 📊 Logs

As ações admin são registradas nos logs do sistema:

```
2024-01-15 10:30:45 - INFO - Créditos admin adicionados: R$ 20.00 - Novo saldo: R$ 25.00
```

Tentativas com código incorreto também são registradas:

```
2024-01-15 10:31:00 - WARNING - Tentativa de uso de código admin inválido
```

## 🛠️ Troubleshooting

### O modal não abre ao pressionar Ctrl+Shift+A

1. Verifique se JavaScript está habilitado no navegador
2. Tente recarregar a página (F5)
3. Verifique o console do navegador para erros
4. Certifique-se de estar na tela principal

### Código correto não funciona

1. Verifique se `ADMIN_ENABLED=true` no `.env`
2. Reinicie o servidor após alterar o `.env`
3. Verifique os logs do servidor para detalhes do erro
4. Confirme que o código no `.env` corresponde ao que está digitando

### Créditos não são adicionados

1. Verifique o saldo antes e depois
2. Consulte os logs do servidor
3. Verifique se há erros no navegador (F12 > Console)
4. Confirme que o servidor está respondendo corretamente

## 🎯 Casos de Uso

### Modo Demonstração

Use o código admin para demonstrar o sistema para clientes potenciais sem precisar inserir dinheiro real:

1. Pressione Ctrl+Shift+A
2. Digite o código
3. Adicione músicas à fila
4. Demonstre todas as funcionalidades

### Testes de Sistema

Durante testes ou desenvolvimento:

1. Use o código admin para adicionar créditos rapidamente
2. Teste diferentes fluxos sem precisar simular pagamentos
3. Valide o comportamento da fila de músicas

### Créditos Promocionais

Para eventos ou promoções:

1. Configure um código temporário
2. Compartilhe com participantes autorizados
3. Monitore o uso via logs
4. Rotacione o código após o evento

## 📝 API Endpoint

### POST /api/admin/add-credits

Adiciona créditos usando código de administrador.

**Request:**

```json
{
  "code": "1234"
}
```

**Response (Sucesso - 200):**

```json
{
  "success": true,
  "message": "Créditos adicionados com sucesso",
  "amount": 20.00,
  "new_balance": 25.00
}
```

**Response (Código Inválido - 401):**

```json
{
  "error": "Código inválido"
}
```

**Response (Funcionalidade Desabilitada - 403):**

```json
{
  "error": "Funcionalidade admin não habilitada"
}
```

## 🔐 Melhores Práticas

1. **Não compartilhe o código publicamente**
2. **Use códigos diferentes para produção e desenvolvimento**
3. **Monitore os logs regularmente**
4. **Desabilite em produção se não for necessário**
5. **Documente internamente quem tem acesso ao código**
6. **Faça backup do arquivo `.env` de forma segura**

## 💡 Dicas

- O código admin respeita o sistema de música idle - adicionar créditos conta como "atividade"
- Você pode adicionar créditos múltiplas vezes
- Os créditos admin funcionam exatamente como créditos pagos
- Use valores maiores em `ADMIN_CREDIT_AMOUNT` para ter que digitar o código menos vezes

## 🚀 Próximos Passos

Após configurar o sistema:

1. Teste o código em ambiente de desenvolvimento
2. Configure um código forte para produção
3. Documente o código para sua equipe
4. Monitore o uso inicial
5. Ajuste `ADMIN_CREDIT_AMOUNT` conforme necessário
