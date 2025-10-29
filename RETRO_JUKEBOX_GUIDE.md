# 🎵 Retro Jukebox Frontend - Guia de Recursos

## 🎨 Design Retrô Profissional

O frontend foi completamente redesenhado para parecer uma jukebox retrô clássica dos anos 50-60, inspirada em modelos icônicos como Wurlitzer e Rock-Ola.

### Características Visuais

#### 1. **Moldura Dourada Estilo Vintage**
- Borda dourada brilhante com efeito de gradiente
- Sombras internas e externas para profundidade
- Efeito de brilho animado que gira continuamente

#### 2. **Título em Neon Rosa e Dourado**
- Texto "Jukebox" com efeito de néon pulsante
- Animação de brilho que simula luz néon vintage
- Fontes especiais: Audiowide, Bebas Neue, Righteous

#### 3. **Métodos de Pagamento como Discos de Vinil**
- Cada opção de pagamento é um disco de vinil circular
- Efeito de rotação ao passar o mouse
- Centro do disco com gradiente escuro
- Linhas radiais simulando sulcos do vinil
- Borda dourada brilhante

#### 4. **Busca Estilo Console Retrô**
- Campo de busca com fundo escuro e texto verde fosforescente
- Borda dourada com efeito de pulsação ao focar
- Estilo de terminal de computador vintage

#### 5. **Resultados de Busca Estilo Jukebox**
- Cartões com gradiente escuro avermelhado
- Barra lateral colorida animada (gradiente arco-íris)
- Efeito de deslizamento suave ao passar o mouse
- Indicadores visuais de origem (💾 Local / 🌐 YouTube)

#### 6. **Botões Estilo Arcade**
- Botões grandes e coloridos com bordas grossas
- Efeitos de sombra 3D
- Animação de brilho ao passar o mouse
- Cores vibrantes: verde (primário), cinza (secundário), vermelho (perigo)

## 🎵 Sistema de Música Local (HD)

### Visão Geral

O sistema agora suporta armazenamento local de músicas no disco rígido, permitindo reprodução mesmo sem conexão com a internet.

### Estrutura de Armazenamento

```
data/
└── local_music/
    ├── metadata.json          # Banco de dados de músicas
    ├── song1.mp3             # Arquivos de áudio
    ├── song2.mp3
    └── ...
```

### Formato do metadata.json

```json
{
  "songs": {
    "local_001": {
      "title": "Nome da Música",
      "artist": "Nome do Artista",
      "duration": 225,           // duração em segundos
      "file_path": "song.mp3",   // caminho relativo
      "plays": 0                 // contador de reproduções
    }
  }
}
```

### Como Adicionar Músicas Locais

1. **Copie os arquivos MP3** para `/data/local_music/`
2. **Edite o metadata.json** e adicione as informações da música:

```json
{
  "songs": {
    "local_001": {
      "title": "Minha Música",
      "artist": "Meu Artista",
      "duration": 180,
      "file_path": "minha_musica.mp3",
      "plays": 0
    }
  }
}
```

3. **Reinicie o servidor** para carregar as novas músicas

### API Endpoints para Música Local

#### Listar todas as músicas locais
```
GET /api/local/songs
```

Resposta:
```json
{
  "songs": [...],
  "total": 3,
  "storage_info": {
    "total_songs": 3,
    "storage_path": "/path/to/local_music",
    "is_available": true
  }
}
```

#### Obter informações de uma música
```
GET /api/local/songs/{song_id}
```

#### Reproduzir arquivo de música local
```
GET /api/local/songs/{song_id}/file
```

## 🌐 Integração com YouTube

### YouTube Data API v3

O sistema agora usa a API oficial do YouTube para buscar músicas reais.

### Configuração

1. **Obtenha uma API Key** no [Google Cloud Console](https://console.cloud.google.com/)
2. **Habilite a YouTube Data API v3**
3. **Configure a variável de ambiente**:

```bash
export YOUTUBE_API_KEY="sua-api-key-aqui"
```

Ou adicione ao arquivo `.env`:
```
YOUTUBE_API_KEY=sua-api-key-aqui
```

### Busca de Músicas

A busca funciona com três modos:

1. **Auto (padrão)**: Busca primeiro no armazenamento local, depois no YouTube
2. **Local**: Busca apenas no armazenamento local
3. **YouTube**: Busca apenas no YouTube

Exemplo de requisição:
```json
POST /api/music/search
{
  "query": "nome da música",
  "source": "auto"  // "auto", "local", ou "youtube"
}
```

## 🔄 Sistema de Fallback Automático

### Como Funciona

1. **Conexão com Internet Disponível**:
   - Busca primeiro no armazenamento local
   - Se não encontrar, busca no YouTube
   - Reproduz usando YouTube IFrame Player

2. **Sem Conexão com Internet**:
   - Busca apenas no armazenamento local
   - Reproduz arquivos locais diretamente
   - Mostra indicador visual 💾

### Indicadores Visuais

- **💾 Música Local**: Arquivo armazenado no HD
- **🌐 YouTube**: Streaming do YouTube

## 🎨 Personalização do Design

### Cores Principais

- **Dourado**: `#d4af37`, `#ffd700` (bordas, títulos)
- **Rosa Néon**: `#ff00ff` (título principal)
- **Verde Fosforescente**: `#00ff00` (saldo, preços)
- **Vermelho Escuro**: `#4d0000`, `#1a0000` (fundo)

### Fontes

- **Audiowide**: Títulos neon e preços
- **Bebas Neue**: Nomes de botões e métodos
- **Righteous**: Textos gerais
- **Courier New**: Campo de busca (estilo terminal)

### Animações

1. **neonGlow**: Pulsação de néon (2s)
2. **vinylSpin**: Rotação de discos (2s linear infinito)
3. **shine**: Brilho da moldura (20s)
4. **colorFlow**: Fluxo de cores (3s)
5. **borderFlow**: Fluxo na borda do player (4s)

## 📱 Funcionalidades Existentes Mantidas

- ✅ Navegação por teclado completa
- ✅ Suporte a múltiplos métodos de pagamento
- ✅ Sistema de fila de músicas
- ✅ Código de operador para créditos
- ✅ Design responsivo
- ✅ Animações suaves
- ✅ Player YouTube IFrame API

## 🚀 Como Usar

### Iniciar o Servidor

```bash
cd /path/to/Jukebox
export YOUTUBE_ENABLED=false  # Não precisa do Selenium
export YOUTUBE_API_KEY=sua-api-key  # Opcional para busca real no YouTube
python3 -m src.server.app
```

### Acessar Interface

Abra o navegador em: `http://localhost:5000`

### Testar Música Local

1. Clique em "Dinheiro" (ou qualquer método de pagamento)
2. Digite "jazz" no campo de busca
3. Clique em "Buscar"
4. Você verá "Jazz Café Instrumental 💾 Música Local"

### Testar YouTube

1. Configure a API key do YouTube
2. Busque por qualquer música popular
3. Você verá resultados do YouTube com 🌐

## 🎯 Próximos Passos Sugeridos

1. **Adicionar mais músicas locais** para ter uma biblioteca offline robusta
2. **Implementar player HTML5** para músicas locais (atualmente só busca)
3. **Criar interface de administração** para gerenciar músicas locais
4. **Adicionar thumbnails** para as músicas
5. **Implementar cache de músicas** do YouTube para reprodução offline

## 📝 Notas Técnicas

- O sistema é totalmente compatível com a versão anterior
- As músicas locais são armazenadas em `data/local_music/`
- O metadata é gerenciado pelo módulo `LocalMusicStorage`
- A busca usa fallback automático em caso de erro de rede
- O design é 100% CSS, sem imagens externas
