"""Lógica principal de reprodução.

Esta classe conversa com o pygame mixer para:
- tocar músicas
- pausar e despausar
- alterar volume
- controlar posição da música
- manter informações de duração e capa atual
"""

from __future__ import annotations

import pygame
from mutagen.mp3 import MP3

from .utils import obter_capa


class MusicPlayer:
    """Encapsula a lógica de áudio do player."""

    def __init__(self):
        pygame.mixer.init()
        self.pausado = False
        self.duracao_total = 0
        self.inicio_musica = 0
        self.volume = 0.5
        self.capa_atual = None

        self.evento_fim = pygame.USEREVENT + 1
        pygame.mixer.music.set_endevent(self.evento_fim)
        pygame.mixer.music.set_volume(self.volume)

    def tocar(self, caminho: str, inicio: int = 0) -> None:
        """Carrega e toca uma música a partir de um ponto opcional."""
        if caminho.lower().endswith(".mp3"):
            self.duracao_total = int(MP3(caminho).info.length)
        else:
            self.duracao_total = 0

        self.capa_atual = obter_capa(caminho)
        self.inicio_musica = inicio

        pygame.mixer.music.load(caminho)
        if inicio > 0 and caminho.lower().endswith(".mp3"):
            pygame.mixer.music.play(start=inicio)
        else:
            pygame.mixer.music.play()

        pygame.mixer.music.set_volume(self.volume)
        self.pausado = False

    def alternar_pause(self) -> None:
        """Alterna entre pausar e despausar a música atual."""
        self.pausado = not self.pausado
        if self.pausado:
            pygame.mixer.music.pause()
        else:
            pygame.mixer.music.unpause()

    def definir_volume(self, volume: float) -> None:
        """Define o volume entre 0 e 1."""
        self.volume = max(0, min(1, volume))
        pygame.mixer.music.set_volume(self.volume)

    def tempo_atual(self) -> int:
        """Retorna o tempo atual real da música em segundos."""
        tempo_ms = pygame.mixer.music.get_pos()
        if tempo_ms < 0:
            tempo_ms = 0
        return self.inicio_musica + tempo_ms // 1000

    def definir_posicao(self, caminho: str, proporcao: float) -> None:
        """Move a reprodução para um ponto da música com base em uma proporção."""
        if self.duracao_total <= 0:
            return

        proporcao = max(0, min(1, proporcao))
        novo_tempo = int(self.duracao_total * proporcao)

        estava_pausado = self.pausado
        self.tocar(caminho, inicio=novo_tempo)

        if estava_pausado:
            pygame.mixer.music.pause()
            self.pausado = True
