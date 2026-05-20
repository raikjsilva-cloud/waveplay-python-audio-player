"""Camada de interface.

Esta classe desenha todos os elementos visuais do player:
- cartões e fundo
- capa da música
- barra de progresso
- slider de volume
- botões com ícones
- playlist visível
"""

from __future__ import annotations

import os

import pygame

from .config import (
    COR_BARRA,
    COR_BOTAO,
    COR_BOTAO_HOVER,
    COR_CARD,
    COR_CARD_2,
    COR_DESTAQUE,
    COR_FUNDO,
    COR_KNOB,
    COR_PROGRESSO,
    COR_SEM_CAPA,
    COR_TEXTO,
    COR_TEXTO_SEC,
)


class UI:
    """Desenha a interface do aplicativo."""

    def __init__(self, screen, font, font_pequena):
        self.screen = screen
        self.font = font
        self.font_pequena = font_pequena

    def desenhar_fundo_topo(self) -> None:
        pygame.draw.rect(self.screen, COR_CARD, (10, 10, 580, 185), border_radius=20)

    def desenhar_capa(self, capa, rect) -> None:
        if capa:
            self.screen.blit(capa, rect.topleft)
        else:
            pygame.draw.rect(self.screen, COR_SEM_CAPA, rect, border_radius=20)
            texto = self.font_pequena.render("Sem capa", True, COR_TEXTO_SEC)
            rect_texto = texto.get_rect(center=rect.center)
            self.screen.blit(texto, rect_texto)

    def desenhar_barra(self, rect, progresso: float) -> None:
        pygame.draw.rect(self.screen, COR_BARRA, rect, border_radius=8)

        largura = int(rect.width * progresso)
        if largura > 0:
            pygame.draw.rect(
                self.screen,
                COR_PROGRESSO,
                (rect.x, rect.y, largura, rect.height),
                border_radius=8,
            )

        knob_x = rect.x + int(rect.width * progresso)
        knob_y = rect.y + rect.height // 2
        pygame.draw.circle(self.screen, COR_KNOB, (knob_x, knob_y), 7)

    def desenhar_slider_volume(self, rect, volume: float) -> None:
        pygame.draw.rect(self.screen, COR_BARRA, rect, border_radius=6)

        largura = int(rect.width * volume)
        if largura > 0:
            pygame.draw.rect(
                self.screen,
                COR_PROGRESSO,
                (rect.x, rect.y, largura, rect.height),
                border_radius=6,
            )

        knob_x = rect.x + int(rect.width * volume)
        knob_y = rect.y + rect.height // 2
        pygame.draw.circle(self.screen, COR_KNOB, (knob_x, knob_y), 8)

    def desenhar_botao_base(self, rect) -> None:
        mouse_pos = pygame.mouse.get_pos()
        cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else COR_BOTAO
        pygame.draw.rect(self.screen, cor, rect, border_radius=14)

    def desenhar_icone_anterior(self, rect) -> None:
        self.desenhar_botao_base(rect)
        pygame.draw.rect(self.screen, COR_TEXTO, (rect.x + 14, rect.y + 14, 4, 26), border_radius=2)
        tri1 = [(rect.x + 36, rect.y + 14), (rect.x + 36, rect.y + 40), (rect.x + 18, rect.y + 27)]
        tri2 = [(rect.x + 48, rect.y + 14), (rect.x + 48, rect.y + 40), (rect.x + 30, rect.y + 27)]
        pygame.draw.polygon(self.screen, COR_TEXTO, tri1)
        pygame.draw.polygon(self.screen, COR_TEXTO, tri2)

    def desenhar_icone_play_pause(self, rect, pausado: bool) -> None:
        self.desenhar_botao_base(rect)
        if pausado:
            pontos = [(rect.x + 20, rect.y + 14), (rect.x + 20, rect.y + 40), (rect.x + 40, rect.y + 27)]
            pygame.draw.polygon(self.screen, COR_TEXTO, pontos)
        else:
            barra1 = pygame.Rect(rect.x + 17, rect.y + 14, 7, 26)
            barra2 = pygame.Rect(rect.x + 31, rect.y + 14, 7, 26)
            pygame.draw.rect(self.screen, COR_TEXTO, barra1, border_radius=2)
            pygame.draw.rect(self.screen, COR_TEXTO, barra2, border_radius=2)

    def desenhar_icone_proxima(self, rect) -> None:
        self.desenhar_botao_base(rect)
        pygame.draw.rect(self.screen, COR_TEXTO, (rect.x + 36, rect.y + 14, 4, 26), border_radius=2)
        tri1 = [(rect.x + 18, rect.y + 14), (rect.x + 18, rect.y + 40), (rect.x + 36, rect.y + 27)]
        tri2 = [(rect.x + 6, rect.y + 14), (rect.x + 6, rect.y + 40), (rect.x + 24, rect.y + 27)]
        pygame.draw.polygon(self.screen, COR_TEXTO, tri1)
        pygame.draw.polygon(self.screen, COR_TEXTO, tri2)

    def desenhar_busca(self, rect, texto, ativo):
        cor_borda = COR_PROGRESSO if ativo else COR_CARD_2
        pygame.draw.rect(self.screen, COR_CARD_2, rect, border_radius=10)
        pygame.draw.rect(self.screen, cor_borda, rect, 2, border_radius=10)

        placeholder = "Buscar musica..." if not texto else texto
        cor_texto = COR_TEXTO_SEC if not texto else COR_TEXTO
        render = self.font_pequena.render(placeholder, True, cor_texto)
        self.screen.blit(render, (rect.x + 10, rect.y + 6))    

    def desenhar_botao_texto(self, rect, texto: str) -> None:
        self.desenhar_botao_base(rect)
        txt = self.font_pequena.render(texto, True, COR_TEXTO)
        txt_rect = txt.get_rect(center=rect.center)
        self.screen.blit(txt, txt_rect)

    def desenhar_playlist(self, rect, playlist_manager, itens_visiveis: int, altura_item: int) -> None:
        pygame.draw.rect(self.screen, COR_CARD, rect, border_radius=16)

        titulo = self.font.render("Playlist", True, COR_TEXTO)
        self.screen.blit(titulo, (rect.x + 12, rect.y + 10))

        y_base = rect.y + 40
        limite = min(len(playlist_manager.playlist), playlist_manager.scroll + itens_visiveis)

        for i in range(playlist_manager.scroll, limite):
            item_y = y_base + (i - playlist_manager.scroll) * altura_item
            item_rect = pygame.Rect(rect.x + 10, item_y, rect.width - 20, 24)

            if i == playlist_manager.indice:
                pygame.draw.rect(self.screen, COR_DESTAQUE, item_rect, border_radius=8)
            elif item_rect.collidepoint(pygame.mouse.get_pos()):
                pygame.draw.rect(self.screen, COR_CARD_2, item_rect, border_radius=8)

            nome = os.path.basename(playlist_manager.playlist[i])
            texto = self.font_pequena.render(nome[:72], True, COR_TEXTO)
            self.screen.blit(texto, (item_rect.x + 8, item_rect.y + 4))

    def desenhar_tela(
        self,
        nome,
        player,
        busca_rect,
        texto_busca,
        busca_ativa,
        capa_rect,
        barra_rect,
        volume_rect,
        rect_anterior,
        rect_play,
        rect_proxima,
        rect_pasta,
        playlist_rect,
        playlist_manager,
        itens_visiveis,
        altura_item,
        formatar_tempo,
    ) -> None:
        self.screen.fill(COR_FUNDO)
        self.desenhar_fundo_topo()

        tempo_atual = player.tempo_atual()
        if player.duracao_total > 0 and tempo_atual > player.duracao_total:
            tempo_atual = player.duracao_total

        progresso = tempo_atual / player.duracao_total if player.duracao_total > 0 else 0

        self.desenhar_capa(player.capa_atual, capa_rect)

        texto_nome = self.font.render(nome[:38], True, COR_TEXTO)
        self.screen.blit(texto_nome, (180, 32))
        
        texto_tempo = self.font.render(
            f"{formatar_tempo(tempo_atual)}",
            True,
            COR_TEXTO,
        )
        self.screen.blit(texto_tempo, (180, 55))

        texto_tempo_Fim = self.font.render(
            f"{formatar_tempo(player.duracao_total)}",
            True,
            COR_TEXTO,
        )
        self.screen.blit(texto_tempo_Fim, (520, 55))

        self.desenhar_barra(barra_rect, progresso)

        texto_volume = self.font_pequena.render(
            f"Volume: {int(player.volume * 100)}%",
            True,
            COR_TEXTO,
        )
        self.screen.blit(texto_volume, (180, 97))
        self.desenhar_slider_volume(volume_rect, player.volume)
        self.desenhar_icone_anterior(rect_anterior)
        self.desenhar_icone_play_pause(rect_play, player.pausado)
        self.desenhar_icone_proxima(rect_proxima)
        self.desenhar_botao_texto(rect_pasta, "Pasta")
        self.desenhar_playlist(playlist_rect, playlist_manager, itens_visiveis, altura_item)
        self.desenhar_busca(busca_rect, texto_busca, busca_ativa)
