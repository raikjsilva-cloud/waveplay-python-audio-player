"""Ponto de entrada do projeto.

Este arquivo conecta tudo:
- abre a pasta inicial
- cria os objetos principais
- processa eventos do teclado e do mouse
- manda a UI desenhar a tela a cada frame
"""

from __future__ import annotations

import tkinter as tk
from tkinter import filedialog

import pygame

from .config import (
    ALTURA,
    ALTURA_ITEM_PLAYLIST,
    BARRA_RECT,
    CAPA_RECT,
    EXTENSOES_VALIDAS,
    FPS,
    ITENS_VISIVEIS,
    LARGURA,
    PLAYLIST_RECT,
    RECT_ANTERIOR,
    RECT_PASTA,
    RECT_PLAY,
    RECT_PROXIMA,
    VOLUME_RECT,
)
from .player import MusicPlayer
from .playlist_manager import PlaylistManager
from .ui import UI
from .utils import formatar_tempo


def escolher_pasta() -> str:
    """Abre a janela de seleção de pasta e retorna o caminho escolhido."""
    root = tk.Tk()
    root.withdraw()
    return filedialog.askdirectory(title="Selecione a pasta com suas músicas")


def clicar_playlist(pos, playlist_rect, playlist_manager) -> bool:
    """Converte um clique na área da playlist em seleção de faixa."""
    if not playlist_rect.collidepoint(pos):
        return False

    y_base = playlist_rect.y + 40
    y_rel = pos[1] - y_base
    if y_rel < 0:
        return False

    item = y_rel // ALTURA_ITEM_PLAYLIST
    novo_indice = playlist_manager.scroll + item

    if 0 <= novo_indice < len(playlist_manager.playlist):
        playlist_manager.selecionar(novo_indice)
        playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
        return True

    return False


def main() -> None:
    """Inicializa o app e executa o loop principal."""
    pygame.init()

    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Player de Música")

    font = pygame.font.SysFont(None, 22)
    font_pequena = pygame.font.SysFont(None, 18)

    pasta = escolher_pasta()
    if not pasta:
        raise ValueError("Nenhuma pasta selecionada.")

    playlist_manager = PlaylistManager(EXTENSOES_VALIDAS)
    playlist_manager.carregar_pasta(pasta)
    if playlist_manager.vazia():
        raise ValueError("Nenhuma música encontrada na pasta especificada.")

    player = MusicPlayer()
    ui = UI(screen, font, font_pequena)
    player.tocar(playlist_manager.atual())

    clock = pygame.time.Clock()
    rodando = True
    arrastando_barra = False
    arrastando_volume = False

    while rodando:
        ui.desenhar_tela(
            playlist_manager.nome_atual(),
            player,
            CAPA_RECT,
            BARRA_RECT,
            VOLUME_RECT,
            RECT_ANTERIOR,
            RECT_PLAY,
            RECT_PROXIMA,
            RECT_PASTA,
            PLAYLIST_RECT,
            playlist_manager,
            ITENS_VISIVEIS,
            ALTURA_ITEM_PLAYLIST,
            formatar_tempo,
        )

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                rodando = False

            elif event.type == player.evento_fim:
                playlist_manager.proxima()
                playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                player.tocar(playlist_manager.atual())

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    rodando = False
                elif event.key == pygame.K_p:
                    player.alternar_pause()
                elif event.key == pygame.K_b:
                    playlist_manager.anterior()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())
                elif event.key == pygame.K_n:
                    playlist_manager.proxima()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())
                elif event.key == pygame.K_o:
                    nova_pasta = escolher_pasta()
                    if nova_pasta:
                        playlist_manager.carregar_pasta(nova_pasta)
                        if not playlist_manager.vazia():
                            player.tocar(playlist_manager.atual())

            elif event.type == pygame.MOUSEWHEEL:
                playlist_manager.rolar(event.y, ITENS_VISIVEIS)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                if RECT_ANTERIOR.collidepoint(event.pos):
                    playlist_manager.anterior()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())

                elif RECT_PLAY.collidepoint(event.pos):
                    player.alternar_pause()

                elif RECT_PROXIMA.collidepoint(event.pos):
                    playlist_manager.proxima()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())

                elif RECT_PASTA.collidepoint(event.pos):
                    nova_pasta = escolher_pasta()
                    if nova_pasta:
                        playlist_manager.carregar_pasta(nova_pasta)
                        if not playlist_manager.vazia():
                            player.tocar(playlist_manager.atual())

                elif BARRA_RECT.collidepoint(event.pos):
                    arrastando_barra = True
                    proporcao = (event.pos[0] - BARRA_RECT.x) / BARRA_RECT.width
                    player.definir_posicao(playlist_manager.atual(), proporcao)

                elif VOLUME_RECT.collidepoint(event.pos):
                    arrastando_volume = True
                    proporcao = (event.pos[0] - VOLUME_RECT.x) / VOLUME_RECT.width
                    player.definir_volume(proporcao)

                elif clicar_playlist(event.pos, PLAYLIST_RECT, playlist_manager):
                    player.tocar(playlist_manager.atual())

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                arrastando_barra = False
                arrastando_volume = False

            elif event.type == pygame.MOUSEMOTION:
                if arrastando_barra:
                    proporcao = (event.pos[0] - BARRA_RECT.x) / BARRA_RECT.width
                    player.definir_posicao(playlist_manager.atual(), proporcao)

                if arrastando_volume:
                    proporcao = (event.pos[0] - VOLUME_RECT.x) / VOLUME_RECT.width
                    player.definir_volume(proporcao)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
