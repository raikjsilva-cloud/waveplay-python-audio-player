import io
import os
import tkinter as tk
from tkinter import filedialog

import pygame  # type: ignore
from mutagen.mp3 import MP3
from mutagen.id3 import ID3, ID3NoHeaderError

pygame.init()
pygame.mixer.init()

root = tk.Tk()
root.withdraw()

LARGURA = 800
ALTURA = 400
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Player de Música")

font = pygame.font.SysFont(None, 22)
font_pequena = pygame.font.SysFont(None, 18)

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

extensoes_validas = (".mp3", ".wav")

pasta = filedialog.askdirectory(title="Selecione a pasta com suas músicas")
if not pasta:
    raise ValueError("Nenhuma pasta selecionada.")

playlist = [
    os.path.join(pasta, f)
    for f in os.listdir(pasta)
    if f.lower().endswith(extensoes_validas)
]

if not playlist:
    raise ValueError("Nenhuma música encontrada na pasta especificada.")

indice = 0
pausado = False
duracao_total = 0
capa_atual = None
inicio_musica = 0
volume_atual = 0.5

arrastando_barra = False
arrastando_volume = False
scroll_playlist = 0
itens_visiveis = 8
altura_item_playlist = 30

MUSICA_TERMINOU = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSICA_TERMINOU)
pygame.mixer.music.set_volume(volume_atual)

# Layout
capa_rect = pygame.Rect(20, 20, 140, 140)
barra_rect = pygame.Rect(180, 110, 380, 16)
volume_rect = pygame.Rect(180, 150, 160, 10)

rect_anterior = pygame.Rect(180, 185, 54, 54)
rect_play = pygame.Rect(245, 185, 54, 54)
rect_proxima = pygame.Rect(310, 185, 54, 54)
rect_pasta = pygame.Rect(380, 190, 120, 42)

playlist_rect = pygame.Rect(20, 250, 760, 150)


def escolher_pasta():
    global pasta, playlist, indice, scroll_playlist

    nova_pasta = filedialog.askdirectory(title="Selecione a pasta com suas músicas")
    if not nova_pasta:
        return

    nova_playlist = [
        os.path.join(nova_pasta, f)
        for f in os.listdir(nova_pasta)
        if f.lower().endswith(extensoes_validas)
    ]

    if not nova_playlist:
        return

    pasta = nova_pasta
    playlist = nova_playlist
    indice = 0
    scroll_playlist = 0
    tocar(indice)


def formatar_tempo(segundos):
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos:02}:{seg:02}"


def obter_capa(caminho):
    try:
        tags = ID3(caminho)
        apic_list = tags.getall("APIC")
        if apic_list:
            imagem_bytes = apic_list[0].data
            imagem_stream = io.BytesIO(imagem_bytes)
            imagem = pygame.image.load(imagem_stream)
            return pygame.transform.smoothscale(imagem, (140, 140))
    except ID3NoHeaderError:
        pass
    except pygame.error:
        pass
    return None


def tocar(ind, inicio=0):
    global duracao_total, pausado, capa_atual, inicio_musica

    caminho = playlist[ind]

    if caminho.lower().endswith(".mp3"):
        audio = MP3(caminho)
        duracao_total = int(audio.info.length)
    else:
        duracao_total = 0

    capa_atual = obter_capa(caminho)
    inicio_musica = inicio

    pygame.mixer.music.load(caminho)
    if inicio > 0 and caminho.lower().endswith(".mp3"):
        pygame.mixer.music.play(start=inicio)
    else:
        pygame.mixer.music.play()

    pygame.mixer.music.set_volume(volume_atual)
    pausado = False


def proxima_musica():
    global indice
    indice = (indice + 1) % len(playlist)
    tocar(indice)
    ajustar_scroll_playlist()


def musica_anterior():
    global indice
    indice = (indice - 1) % len(playlist)
    tocar(indice)
    ajustar_scroll_playlist()


def alternar_pause():
    global pausado
    pausado = not pausado
    if pausado:
        pygame.mixer.music.pause()
    else:
        pygame.mixer.music.unpause()


def definir_posicao_musica(mouse_x):
    global pausado

    if duracao_total <= 0:
        return

    proporcao = (mouse_x - barra_rect.x) / barra_rect.width
    proporcao = max(0, min(1, proporcao))
    novo_tempo = int(duracao_total * proporcao)

    estava_pausado = pausado
    tocar(indice, inicio=novo_tempo)

    if estava_pausado:
        pygame.mixer.music.pause()
        pausado = True


def definir_volume(mouse_x):
    global volume_atual

    proporcao = (mouse_x - volume_rect.x) / volume_rect.width
    proporcao = max(0, min(1, proporcao))
    volume_atual = proporcao
    pygame.mixer.music.set_volume(volume_atual)


def desenhar_barra(rect, progresso):
    pygame.draw.rect(screen, COR_BARRA, rect, border_radius=8)

    largura_preenchida = int(rect.width * progresso)
    if largura_preenchida > 0:
        pygame.draw.rect(
            screen,
            COR_PROGRESSO,
            (rect.x, rect.y, largura_preenchida, rect.height),
            border_radius=8,
        )

    knob_x = rect.x + int(rect.width * progresso)
    knob_y = rect.y + rect.height // 2
    pygame.draw.circle(screen, COR_KNOB, (knob_x, knob_y), 7)


def desenhar_slider_volume(rect, volume):
    pygame.draw.rect(screen, COR_BARRA, rect, border_radius=6)

    largura_preenchida = int(rect.width * volume)
    if largura_preenchida > 0:
        pygame.draw.rect(
            screen,
            COR_PROGRESSO,
            (rect.x, rect.y, largura_preenchida, rect.height),
            border_radius=6,
        )

    knob_x = rect.x + int(rect.width * volume)
    knob_y = rect.y + rect.height // 2
    pygame.draw.circle(screen, COR_KNOB, (knob_x, knob_y), 8)


def desenhar_botao_base(rect):
    mouse_pos = pygame.mouse.get_pos()
    cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(screen, cor, rect, border_radius=14)


def desenhar_icone_anterior(rect):
    desenhar_botao_base(rect)
    pygame.draw.rect(screen, COR_TEXTO, (rect.x + 14, rect.y + 14, 4, 26), border_radius=2)

    tri1 = [(rect.x + 36, rect.y + 14), (rect.x + 36, rect.y + 40), (rect.x + 18, rect.y + 27)]
    tri2 = [(rect.x + 48, rect.y + 14), (rect.x + 48, rect.y + 40), (rect.x + 30, rect.y + 27)]
    pygame.draw.polygon(screen, COR_TEXTO, tri1)
    pygame.draw.polygon(screen, COR_TEXTO, tri2)


def desenhar_icone_play_pause(rect, pausado):
    desenhar_botao_base(rect)

    if pausado:
        pontos = [(rect.x + 20, rect.y + 14), (rect.x + 20, rect.y + 40), (rect.x + 40, rect.y + 27)]
        pygame.draw.polygon(screen, COR_TEXTO, pontos)
    else:
        barra1 = pygame.Rect(rect.x + 17, rect.y + 14, 7, 26)
        barra2 = pygame.Rect(rect.x + 31, rect.y + 14, 7, 26)
        pygame.draw.rect(screen, COR_TEXTO, barra1, border_radius=2)
        pygame.draw.rect(screen, COR_TEXTO, barra2, border_radius=2)


def desenhar_icone_proxima(rect):
    desenhar_botao_base(rect)
    pygame.draw.rect(screen, COR_TEXTO, (rect.x + 36, rect.y + 14, 4, 26), border_radius=2)

    tri1 = [(rect.x + 18, rect.y + 14), (rect.x + 18, rect.y + 40), (rect.x + 36, rect.y + 27)]
    tri2 = [(rect.x + 6, rect.y + 14), (rect.x + 6, rect.y + 40), (rect.x + 24, rect.y + 27)]
    pygame.draw.polygon(screen, COR_TEXTO, tri1)
    pygame.draw.polygon(screen, COR_TEXTO, tri2)


def desenhar_botao_texto(rect, texto):
    desenhar_botao_base(rect)
    txt = font_pequena.render(texto, True, COR_TEXTO)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)


def ajustar_scroll_playlist():
    global scroll_playlist

    if indice < scroll_playlist:
        scroll_playlist = indice
    elif indice >= scroll_playlist + itens_visiveis:
        scroll_playlist = indice - itens_visiveis + 1


def desenhar_playlist():
    pygame.draw.rect(screen, COR_CARD, playlist_rect, border_radius=16)

    titulo = font.render("Playlist", True, COR_TEXTO)
    screen.blit(titulo, (playlist_rect.x + 12, playlist_rect.y + 10))

    y_base = playlist_rect.y + 40

    for i in range(scroll_playlist, min(len(playlist), scroll_playlist + itens_visiveis)):
        item_y = y_base + (i - scroll_playlist) * altura_item_playlist
        item_rect = pygame.Rect(playlist_rect.x + 10, item_y, playlist_rect.width - 20, 24)

        if i == indice:
            pygame.draw.rect(screen, COR_DESTAQUE, item_rect, border_radius=8)
        elif item_rect.collidepoint(pygame.mouse.get_pos()):
            pygame.draw.rect(screen, COR_CARD_2, item_rect, border_radius=8)

        nome = os.path.basename(playlist[i])
        texto = font_pequena.render(nome[:72], True, COR_TEXTO)
        screen.blit(texto, (item_rect.x + 8, item_rect.y + 4))


def clicar_playlist(pos):
    global indice

    if not playlist_rect.collidepoint(pos):
        return

    y_base = playlist_rect.y + 40
    y_rel = pos[1] - y_base
    if y_rel < 0:
        return

    item = y_rel // altura_item_playlist
    novo_indice = scroll_playlist + item

    if 0 <= novo_indice < len(playlist):
        indice = novo_indice
        tocar(indice)
        ajustar_scroll_playlist()


tocar(indice)

clock = pygame.time.Clock()
rodando = True

while rodando:
    screen.fill(COR_FUNDO)

    pygame.draw.rect(screen, COR_CARD, (10, 10, 780, 230), border_radius=20)

    nome = os.path.basename(playlist[indice])

    tempo_ms = pygame.mixer.music.get_pos()
    if tempo_ms < 0:
        tempo_ms = 0

    tempo_atual = inicio_musica + tempo_ms // 1000
    if duracao_total > 0 and tempo_atual > duracao_total:
        tempo_atual = duracao_total

    tempo_restante = max(0, duracao_total - tempo_atual)
    progresso = tempo_atual / duracao_total if duracao_total > 0 else 0

    if capa_atual:
        screen.blit(capa_atual, capa_rect.topleft)
    else:
        pygame.draw.rect(screen, COR_SEM_CAPA, capa_rect, border_radius=14)
        texto_sem_capa = font_pequena.render("Sem capa", True, COR_TEXTO_SEC)
        rect_sem = texto_sem_capa.get_rect(center=capa_rect.center)
        screen.blit(texto_sem_capa, rect_sem)

    texto_nome = font.render(nome[:38], True, COR_TEXTO)
    screen.blit(texto_nome, (180, 32))

    texto_tempo = font.render(
        f"{formatar_tempo(tempo_atual)} / {formatar_tempo(duracao_total)}",
        True,
        COR_TEXTO,
    )
    screen.blit(texto_tempo, (180, 66))

    texto_restante = font_pequena.render(
        f"Restante: -{formatar_tempo(tempo_restante)}",
        True,
        COR_TEXTO_SEC,
    )
    screen.blit(texto_restante, (180, 88))

    desenhar_barra(barra_rect, progresso)

    texto_volume = font_pequena.render(f"Volume: {int(volume_atual * 100)}%", True, COR_TEXTO)
    screen.blit(texto_volume, (180, 136))
    desenhar_slider_volume(volume_rect, volume_atual)

    desenhar_icone_anterior(rect_anterior)
    desenhar_icone_play_pause(rect_play, pausado)
    desenhar_icone_proxima(rect_proxima)
    desenhar_botao_texto(rect_pasta, "Pasta")

    status = "Pausado" if pausado else "Reproduzindo"
    texto_status = font_pequena.render(f"Status: {status}", True, COR_TEXTO_SEC)
    screen.blit(texto_status, (520, 200))

    

    desenhar_playlist()

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == MUSICA_TERMINOU:
            proxima_musica()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            elif event.key == pygame.K_p:
                alternar_pause()
            elif event.key == pygame.K_b:
                musica_anterior()
            elif event.key == pygame.K_n:
                proxima_musica()
            elif event.key == pygame.K_o:
                escolher_pasta()

        elif event.type == pygame.MOUSEWHEEL:
            max_scroll = max(0, len(playlist) - itens_visiveis)
            scroll_playlist -= event.y
            scroll_playlist = max(0, min(scroll_playlist, max_scroll))

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if rect_anterior.collidepoint(event.pos):
                musica_anterior()
            elif rect_play.collidepoint(event.pos):
                alternar_pause()
            elif rect_proxima.collidepoint(event.pos):
                proxima_musica()
            elif rect_pasta.collidepoint(event.pos):
                escolher_pasta()
            elif barra_rect.collidepoint(event.pos):
                arrastando_barra = True
                definir_posicao_musica(event.pos[0])
            elif volume_rect.collidepoint(event.pos):
                arrastando_volume = True
                definir_volume(event.pos[0])
            elif playlist_rect.collidepoint(event.pos):
                clicar_playlist(event.pos)

        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            arrastando_barra = False
            arrastando_volume = False

        elif event.type == pygame.MOUSEMOTION:
            if arrastando_barra:
                definir_posicao_musica(event.pos[0])
            if arrastando_volume:
                definir_volume(event.pos[0])

    pygame.display.flip()
    clock.tick(30)

pygame.quit()
