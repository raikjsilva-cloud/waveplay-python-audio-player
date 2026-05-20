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

from pathlib import Path
from .settings import (
    obter_ultima_pasta,
    salvar_ultima_pasta,
    obter_volume,
    salvar_volume,
    obter_ultima_musica,
    salvar_ultima_musica,
    obter_tempo_reproduzido,
    salvar_tempo_reproduzido,
)

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
    BUSCA_RECT,
)
from .player import MusicPlayer
from .playlist_manager import PlaylistManager
from .ui import UI
from .utils import formatar_tempo

def escolher_pasta(pasta_inicial: str | None = None) -> str:
    """Abre a janela de seleção de pasta e retorna o caminho escolhido."""
    root = tk.Tk()
    root.withdraw()

    if pasta_inicial and Path(pasta_inicial).exists():
        return filedialog.askdirectory(
            title="Selecione a pasta com suas músicas",
            initialdir=pasta_inicial,
        )

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

    texto_busca = ""  # Variável global para armazenar o texto de busca
    busca_ativa = False  # Indica se a busca está ativa ou não

    screen = pygame.display.set_mode((LARGURA, ALTURA))
    pygame.display.set_caption("Player de Música")

    font = pygame.font.SysFont(None, 22)
    font_pequena = pygame.font.SysFont(None, 18)

    pasta = obter_ultima_pasta()
    if not pasta or not Path(pasta).exists():
        pasta = escolher_pasta()
    
    if not pasta:
        raise ValueError("Nenhuma pasta selecionada.")
    playlist_manager = PlaylistManager(EXTENSOES_VALIDAS)
    playlist_manager.carregar_pasta(pasta)
    
    ultima_musica = obter_ultima_musica()
    if ultima_musica and ultima_musica in playlist_manager.playlist:
        playlist_manager.indice = playlist_manager.playlist.index(ultima_musica)

    salvar_ultima_pasta(pasta)
    if playlist_manager.vazia():
        nome_atual = "Nenhuma música encontrada"
    else:
        nome_atual = playlist_manager.nome_atual() if not playlist_manager.vazia() else "Nenhuma música encontrada"

    player = MusicPlayer()
    player.definir_volume(obter_volume())
    ui = UI(screen, font, font_pequena)
    tempo_salvo = obter_tempo_reproduzido()
    player.tocar(playlist_manager.atual(), inicio=tempo_salvo)
    salvar_ultima_musica(playlist_manager.atual())

    clock = pygame.time.Clock()
    rodando = True
    arrastando_barra = False
    arrastando_volume = False

    while rodando:
        ui.desenhar_tela(
            playlist_manager.nome_atual(),
            player,
            BUSCA_RECT,
            texto_busca,
            busca_ativa,
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
                salvar_ultima_musica(playlist_manager.atual())
                salvar_tempo_reproduzido(0)

            elif event.type == pygame.KEYDOWN:
                if busca_ativa:
                    if event.key == pygame.K_BACKSPACE:
                        texto_busca = texto_busca[:-1]
                        playlist_manager.aplicar_busca(texto_busca)
                    elif event.key == pygame.K_ESCAPE:
                        texto_busca = ""
                        busca_ativa = False
                        playlist_manager.aplicar_busca(texto_busca)
                    elif event.key == pygame.K_RETURN:
                        pass
                    elif event.unicode and event.unicode.isprintable():
                        texto_busca += event.unicode
                        playlist_manager.aplicar_busca(texto_busca)
                else:
                    if event.key == pygame.K_ESCAPE:
                        rodando = False
                    elif event.key == pygame.K_p:
                        player.alternar_pause()
                    elif event.key == pygame.K_b:
                        if not playlist_manager.vazia():
                            playlist_manager.anterior()
                            playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                            player.tocar(playlist_manager.atual())
                            salvar_ultima_musica(playlist_manager.atual())
                            salvar_tempo_reproduzido(0)
                    elif event.key == pygame.K_n:
                        if not playlist_manager.vazia():
                            playlist_manager.proxima()
                            playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                            player.tocar(playlist_manager.atual())
                            salvar_ultima_musica(playlist_manager.atual())
                            salvar_tempo_reproduzido(0)
                    elif event.key == pygame.K_o:
                        nova_pasta = escolher_pasta()
                        if nova_pasta:
                            playlist_manager.carregar_pasta(nova_pasta)
                            if not playlist_manager.vazia():
                                salvar_ultima_pasta(nova_pasta)
                                player.tocar(playlist_manager.atual())

            elif event.type == pygame.MOUSEWHEEL:
                playlist_manager.rolar(event.y, ITENS_VISIVEIS)

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                busca_ativa = BUSCA_RECT.collidepoint(event.pos)

                if RECT_ANTERIOR.collidepoint(event.pos):
                    playlist_manager.anterior()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())
                    salvar_ultima_musica(playlist_manager.atual())
                    salvar_tempo_reproduzido(0)

                elif RECT_PLAY.collidepoint(event.pos):
                    player.alternar_pause()

                elif RECT_PROXIMA.collidepoint(event.pos):
                    playlist_manager.proxima()
                    playlist_manager.ajustar_scroll(ITENS_VISIVEIS)
                    player.tocar(playlist_manager.atual())
                    salvar_ultima_musica(playlist_manager.atual())
                    salvar_tempo_reproduzido(0)

                elif RECT_PASTA.collidepoint(event.pos):
                    nova_pasta = escolher_pasta(playlist_manager.pasta)
                    if nova_pasta:
                        playlist_manager.carregar_pasta(nova_pasta)
                        if not playlist_manager.vazia():
                            salvar_ultima_pasta(nova_pasta)
                            player.tocar(playlist_manager.atual())

                elif BARRA_RECT.collidepoint(event.pos):
                    arrastando_barra = True
                    proporcao = (event.pos[0] - BARRA_RECT.x) / BARRA_RECT.width
                    player.definir_posicao(playlist_manager.atual(), proporcao)
                    salvar_tempo_reproduzido(player.tempo_atual())

                elif VOLUME_RECT.collidepoint(event.pos):
                    arrastando_volume = True
                    proporcao = (event.pos[0] - VOLUME_RECT.x) / VOLUME_RECT.width
                    player.definir_volume(proporcao)
                    salvar_volume(player.volume)

                elif clicar_playlist(event.pos, PLAYLIST_RECT, playlist_manager):
                    player.tocar(playlist_manager.atual())
                    salvar_ultima_musica(playlist_manager.atual())

            elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
                if arrastando_volume:
                    salvar_volume(player.volume)
                    
                arrastando_barra = False
                arrastando_volume = False

            elif event.type == pygame.MOUSEMOTION:
                if arrastando_barra:
                    proporcao = (event.pos[0] - BARRA_RECT.x) / BARRA_RECT.width
                    player.definir_posicao(playlist_manager.atual(), proporcao)
                    salvar_tempo_reproduzido(player.tempo_atual())

                if arrastando_volume:
                    proporcao = (event.pos[0] - VOLUME_RECT.x) / VOLUME_RECT.width
                    player.definir_volume(proporcao)
                    salvar_volume(player.volume)
        pygame.display.flip()
        clock.tick(FPS)

    if not playlist_manager.vazia():
        salvar_ultima_musica(playlist_manager.atual())
        salvar_tempo_reproduzido(player.tempo_atual())
        salvar_volume(player.volume)

    pygame.quit()


if __name__ == "__main__":
    main()
