# WavePlay

Player de música desktop desenvolvido em Python com foco em organização modular, interface gráfica e persistência de configurações.

## Visão geral

O WavePlay é um player para arquivos MP3 construído com `pygame`, `tkinter` e `mutagen`. O projeto foi organizado em módulos para separar interface, reprodução, playlist, configurações e utilitários, deixando o código mais limpo e mais fácil de manter.

## Funcionalidades

- Reprodução de arquivos `.mp3`
- Botões de anterior, play/pause e próxima
- Barra de progresso clicável
- Controle de volume com slider
- Exibição da capa da música quando disponível
- Playlist visível e clicável
- Campo de busca na playlist
- Escolha dinâmica da pasta de músicas
- Salvamento da última pasta aberta
- Salvamento do volume
- Salvamento da última música tocada
- Salvamento do tempo de reprodução

## Tecnologias utilizadas

- Python 3
- `pygame-ce`
- `mutagen`
- `tkinter`
- `json`

## Estrutura do projeto

```text
WavePlay/
├─ src/
│  └─ music_player/
│     ├─ __init__.py
│     ├─ main.py
│     ├─ config.py
│     ├─ player.py
│     ├─ playlist_manager.py
│     ├─ settings.py
│     ├─ ui.py
│     └─ utils.py
├─ requirements.txt
└─ README.md
```

## O que cada arquivo faz

### `main.py`
É o ponto de entrada do projeto. Inicializa a janela, cria os objetos principais, trata os eventos do teclado e do mouse e mantém o loop principal em execução.

### `config.py`
Centraliza tamanhos, cores, posições e constantes visuais da interface. Isso evita números soltos espalhados pelo código.

### `player.py`
Cuida da lógica de reprodução de áudio. É onde ficam ações como tocar, pausar, trocar o volume, mover a posição da música e consultar o tempo atual.

### `playlist_manager.py`
Gerencia a playlist. Carrega músicas da pasta escolhida, troca o índice atual, aplica busca e controla a rolagem da lista.

### `settings.py`
Lê e salva configurações em JSON. É responsável por persistir a última pasta aberta, o volume, a última música tocada e o tempo salvo.

### `ui.py`
Desenha toda a interface do aplicativo: fundo, capa, barra de progresso, slider de volume, botões com ícones, campo de busca e playlist.

### `utils.py`
Agrupa funções auxiliares reutilizáveis, como formatação de tempo e leitura da capa da música.

## Persistência de dados

O projeto utiliza um arquivo `settings.json` para salvar informações entre execuções.

Exemplo:

```json
{
  "ultima_pasta": "C:\\Musicas",
  "ultima_musica": "C:\\Musicas\\album\\faixa01.mp3",
  "volume": 0.65,
  "tempo_reproduzido": 42
}
```

Esses dados permitem que o aplicativo reabra com mais continuidade de uso.

## Como executar

1. Crie e ative um ambiente virtual.
2. Instale as dependências:

```bash
pip install -r requirements.txt
```

3. Execute o projeto a partir da pasta raiz:

```bash
python -m src.music_player.main
```

## Decisões de projeto

- O formato principal suportado é `MP3`
- A interface foi ajustada para uma janela compacta de `800x400`
- Os controles principais usam ícones em vez de texto para deixar o layout mais limpo
- A playlist fica sempre visível para facilitar a navegação
- As configurações foram separadas em um arquivo próprio para facilitar manutenção

## Aprendizados demonstrados

- Organização modular em Python
- Separação entre lógica e interface
- Manipulação de eventos com `pygame`
- Uso de arquivos JSON para persistência
- Leitura de metadados com `mutagen`
- Estruturação de projeto com foco em portfólio

## Próximos passos possíveis

- Salvar estado de pausa
- Mostrar artista e álbum
- Adicionar embaralhar e repetir
- Melhorar a experiência da busca
- Criar instalador ou versão executável
