"""Constantes visuais e de layout do projeto.

Este arquivo concentra tamanhos, cores e posições da interface.
Assim, o restante do código fica mais legível e fácil de ajustar.
"""

import pygame

LARGURA = 800
ALTURA = 400
FPS = 30

COR_FUNDO = (18, 18, 24)
COR_CARD = (32, 32, 40)
COR_CARD_2 = (44, 44, 54)
COR_TEXTO = (245, 245, 245)
COR_TEXTO_SEC = (180, 180, 190)
COR_BARRA = (70, 70, 85)
COR_PROGRESSO = (0, 190, 140)
COR_KNOB = (240, 240, 240)
COR_BOTAO = (55, 55, 68)
COR_BOTAO_HOVER = (80, 80, 98)
COR_DESTAQUE = (0, 150, 115)
COR_SEM_CAPA = (55, 55, 65)

CAPA_RECT = pygame.Rect(20, 20, 140, 140)
BARRA_RECT = pygame.Rect(180, 72, 380, 16)
VOLUME_RECT = pygame.Rect(180, 110, 160, 10)

RECT_ANTERIOR = pygame.Rect(180, 135, 54, 54)
RECT_PLAY = pygame.Rect(245, 135, 54, 54)
RECT_PROXIMA = pygame.Rect(310, 135, 54, 54)
RECT_PASTA = pygame.Rect(380, 140, 120, 42)

PLAYLIST_RECT = pygame.Rect(10, 205, 780, 185)
ALTURA_ITEM_PLAYLIST = 30
ITENS_VISIVEIS = 5

EXTENSOES_VALIDAS = (".mp3", ".wav")
