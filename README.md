# Music Player em Python

Player de música desktop feito com `pygame`, `tkinter` e `mutagen`.

## O projeto mostra

- Reprodução de músicas `.mp3` e `.wav`
- Barra de progresso clicável
- Controle de volume com slider
- Botões de anterior, play/pause e próxima
- Exibição de capa embutida no MP3
- Playlist visível e clicável
- Escolha dinâmica de pasta

## Tecnologias

- Python 3
- `pygame-ce`
- `mutagen`
- `tkinter`

## Estrutura

```text
music_player_portfolio/
├─ README.md
├─ requirements.txt
├─ .gitignore
└─ src/
   └─ music_player/
      ├─ __init__.py
      ├─ main.py
      ├─ config.py
      ├─ player.py
      ├─ playlist_manager.py
      ├─ ui.py
      └─ utils.py
```

## O que cada parte faz

### `src/music_player/main.py`
Ponto de entrada do programa. Cria a janela, inicializa os objetos principais e controla o loop de eventos do `pygame`.

### `src/music_player/config.py`
Centraliza tamanhos, cores, posições dos elementos e constantes visuais. Isso evita números soltos pelo projeto.

### `src/music_player/player.py`
Contém a lógica de reprodução: tocar, pausar, controlar volume, obter tempo atual e avançar a música.

### `src/music_player/playlist_manager.py`
Cuida da playlist: carregar arquivos de uma pasta, trocar música atual, controlar índice e rolagem da lista.

### `src/music_player/ui.py`
Responsável por desenhar a interface: capa, barra de progresso, volume, botões e playlist.

### `src/music_player/utils.py`
Funções auxiliares reutilizáveis, como formatação de tempo e leitura da capa da música.

## Como rodar

1. Crie e ative um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute:

```bash
python -m src.music_player.main
```

## Ideias de evolução

- Salvar última pasta aberta
- Salvar volume em arquivo `.json`
- Botão de embaralhar e repetir
- Busca dentro da playlist
- Melhorar suporte a `.wav`

## Aprendizados demonstrados

- Organização modular em Python
- Separação entre lógica e interface
- Manipulação de eventos no `pygame`
- Leitura de metadados de áudio com `mutagen`
- Estruturação de projeto para portfólio
