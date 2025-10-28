# 🎵 Melhorias da Jukebox

## Novas Funcionalidades Implementadas

Este documento descreve as melhorias recentes implementadas na Jukebox.

---

## 1. 💰 Preço Ajustado: R$ 1,00 por Música

### O que mudou?
- O preço padrão por música foi reduzido de **R$ 5,00** para **R$ 1,00**
- Mais acessível para os usuários
- Potencial para maior volume de músicas tocadas

### Como configurar?
Edite o arquivo `.env` e ajuste o valor:

```bash
PRICE_PER_SONG=1.00
```

Você pode definir qualquer valor desejado!

### Observações:
- As taxas dos métodos de pagamento continuam sendo aplicadas:
  - **Dinheiro/PIX**: Sem taxa (R$ 1,00)
  - **Débito**: +1.99% (R$ 1,02)
  - **Crédito**: +3.99% (R$ 1,04)

---

## 2. 📺 Reprodução de Vídeo Opcional

### O que é?
Agora você pode escolher se quer que o vídeo do YouTube seja exibido ou não durante a reprodução das músicas.

### Por que isso é útil?
- **Economia de recursos**: Em Raspberry Pi com poucos recursos, ocultar o vídeo economiza CPU e GPU
- **Economia de energia**: Menos processamento = menor consumo
- **Foco no áudio**: Quando o vídeo não é necessário, apenas o áudio é reproduzido
- **Melhor performance**: Sistema roda mais suave sem renderizar vídeo

### Como configurar?

Edite o arquivo `.env`:

```bash
# Para exibir vídeo E áudio (padrão)
VIDEO_PLAYBACK_ENABLED=true

# Para apenas áudio (vídeo oculto)
VIDEO_PLAYBACK_ENABLED=false
```

### Como funciona?
- Quando `false`, o player de vídeo é ocultado usando JavaScript
- O áudio continua tocando normalmente
- A música flui sem interrupções
- Totalmente transparente para o usuário

---

## 3. 🎶 Sistema de Filas Melhorado

### O que mudou?
O sistema de filas agora fornece feedback mais claro sobre o que está acontecendo com as músicas adicionadas.

### Funcionalidades:

#### ✅ Músicas não interrompem a atual
Quando você adiciona uma música enquanto outra está tocando:
- A música atual **continua tocando** até o fim
- A nova música entra na **fila de reprodução**
- Todas as músicas tocam em ordem

#### ✅ Feedback claro de posição
Ao adicionar uma música, o sistema informa:
- Se a música vai tocar **imediatamente** (fila vazia)
- Ou a **posição na fila** (se houver músicas tocando/na fila)

#### ✅ Informações em tempo real
O endpoint `/api/music/queue` retorna:
```json
{
  "queue": [...],           // Lista completa de músicas
  "queue_size": 3,          // Tamanho da fila (apenas queued)
  "current_song": {...}     // Música atualmente tocando
}
```

### Exemplo de uso:

**Cenário**: Usuário tem R$ 10,00 de crédito

```
1. Adiciona "Música 1" → 🎵 Toca imediatamente!
2. Adiciona "Música 2" → 📋 Fila posição 1
3. Adiciona "Música 3" → 📋 Fila posição 2
4. Adiciona "Música 4" → 📋 Fila posição 3

Todas tocam em ordem, sem interrupções!
```

### Como o sistema funciona?

1. **Música adicionada**: Status `queued` (na fila)
2. **Música tocando**: Status `playing` (tocando agora)
3. **Música finalizada**: Status `played` (já tocou)

### Verificando a fila:

**Na API**:
```bash
curl http://localhost:5000/api/music/queue
```

**Na interface**:
- A tela de busca mostra a fila atual
- Atualiza automaticamente ao adicionar músicas
- Mostra qual está tocando e quais estão na fila

---

## 📊 Comparação: Antes vs Depois

| Aspecto | Antes | Depois |
|---------|-------|--------|
| **Preço por música** | R$ 5,00 | R$ 1,00 |
| **Reprodução de vídeo** | Sempre ligado | Opcional (ligado/desligado) |
| **Feedback da fila** | Básico | Detalhado com posição |
| **Economia de recursos** | Normal | Melhorada (sem vídeo) |

---

## 🚀 Como Começar

### 1. Atualizar configurações

Copie o arquivo de exemplo:
```bash
cp env.example .env
```

Edite `.env` com suas preferências:
```bash
# Preço por música
PRICE_PER_SONG=1.00

# Vídeo opcional
VIDEO_PLAYBACK_ENABLED=true  # ou false
```

### 2. Reiniciar o servidor

```bash
# Raspberry Pi
./start.sh

# PC/Linux
./start-pc.sh
```

### 3. Testar as funcionalidades

```bash
# Executar testes
python3 tests/test_new_features.py
```

---

## ❓ Perguntas Frequentes

### Posso mudar o preço para outro valor?
**Sim!** Basta editar `PRICE_PER_SONG` no arquivo `.env` para qualquer valor desejado.

### Se eu desabilitar o vídeo, perco o áudio?
**Não!** O áudio continua tocando normalmente. Apenas o vídeo é ocultado.

### A fila tem limite?
**Sim**, configurável via `MAX_QUEUE_SIZE` no `.env`. Padrão: 10 músicas.

### Como limpo a fila?
A fila é gerenciada automaticamente. Músicas tocadas são marcadas como `played` e removidas da fila ativa.

### As mudanças afetam o sistema antigo?
**Não!** Todas as mudanças são retrocompatíveis. Se você não alterar o `.env`, o sistema mantém as configurações anteriores.

---

## 🔧 Para Desenvolvedores

### Arquivos Modificados

1. **`src/server/config.py`**
   - `PRICE_PER_SONG = 1.00` (novo padrão)
   - `VIDEO_PLAYBACK_ENABLED` (nova config)

2. **`src/youtube/youtube_player.py`**
   - Método `_hide_video_player()` adicionado
   - `play_video()` atualizado para suportar vídeo opcional

3. **`src/server/app.py`**
   - Endpoint `/api/music/queue` melhorado
   - Endpoint `/api/music/add` retorna mais informações

4. **`src/server/static/app.js`**
   - Função `addMusicToQueue()` mostra posição na fila
   - Auto-refresh da fila após adicionar música

5. **`src/server/static/index.html`**
   - Elemento `#success-message` adicionado
   - Preço atualizado na interface

### Testes

Novos testes em `tests/test_new_features.py`:
- ✅ Configuração de preço
- ✅ Configuração de vídeo
- ✅ Sistema de filas
- ✅ Arquivo env.example

---

## 📞 Suporte

Problemas ou dúvidas? Consulte:
- 📖 [README.md](README.md) - Documentação principal
- 📝 [CHANGES.md](CHANGES.md) - Histórico detalhado de mudanças
- 🐛 [GitHub Issues](https://github.com/godfathercorleone994-wq/Jukebox/issues)

---

**Versão**: 2.2  
**Data**: Outubro 2025  
**Status**: ✅ Testado e Funcionando
