"""Gerenciamento da playlist.

Esta classe centraliza o comportamento relacionado à lista de músicas:
- carregar uma pasta
- avançar e voltar
- selecionar uma faixa
- controlar rolagem da playlist na interface
"""

from __future__ import annotations

import os


class PlaylistManager:
    """Representa a playlist atual e o estado de navegação."""

    def __init__(self, extensoes_validas):
        self.extensoes_validas = extensoes_validas
        self.pasta = ""
        self.playlist = []
        self.indice = 0
        self.scroll = 0

    def carregar_pasta(self, pasta: str) -> None:
        """Carrega todas as músicas válidas de uma pasta."""
        self.pasta = pasta
        self.playlist = [
            os.path.join(pasta, arquivo)
            for arquivo in os.listdir(pasta)
            if arquivo.lower().endswith(self.extensoes_validas)
        ]
        self.indice = 0
        self.scroll = 0

    def vazia(self) -> bool:
        """Informa se não há músicas carregadas."""
        return len(self.playlist) == 0

    def atual(self) -> str:
        """Retorna o caminho completo da música atual."""
        return self.playlist[self.indice]

    def nome_atual(self) -> str:
        """Retorna apenas o nome do arquivo atual."""
        return os.path.basename(self.atual())

    def proxima(self) -> None:
        """Avança para a próxima música da playlist."""
        self.indice = (self.indice + 1) % len(self.playlist)

    def anterior(self) -> None:
        """Volta para a música anterior da playlist."""
        self.indice = (self.indice - 1) % len(self.playlist)

    def selecionar(self, novo_indice: int) -> None:
        """Seleciona uma música específica da lista."""
        if 0 <= novo_indice < len(self.playlist):
            self.indice = novo_indice

    def ajustar_scroll(self, itens_visiveis: int) -> None:
        """Mantém a música atual visível dentro da janela da playlist."""
        if self.indice < self.scroll:
            self.scroll = self.indice
        elif self.indice >= self.scroll + itens_visiveis:
            self.scroll = self.indice - itens_visiveis + 1

    def rolar(self, delta: int, itens_visiveis: int) -> None:
        """Controla a rolagem da playlist com a roda do mouse."""
        max_scroll = max(0, len(self.playlist) - itens_visiveis)
        self.scroll -= delta
        self.scroll = max(0, min(self.scroll, max_scroll))
