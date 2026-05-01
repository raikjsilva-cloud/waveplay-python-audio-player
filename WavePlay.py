from cmath import rect
import io
import tkinter as tk #Biblioteca para criar a interface gráfica do player de música.
from tkinter import filedialog #Para abrir uma janela de diálogo para selecionar a pasta com as músicas.
import pygame # type: ignore #Foi instalado a biblioteca pygame-ce importada como pygame para o exercício 21, para reproduzir um arquivo MP3.
import os 
from mutagen.mp3 import MP3 #Biblioteca mutagen para obter a duração total da música.
from mutagen.id3 import ID3, ID3NoHeaderError #Para ler as tags ID3 das músicas, como título e artista.

pygame.init()


root = tk.Tk()
root.withdraw()  # Oculta a janela principal

# Janela
LARGURA = 970
ALTURA = 340
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Player de Música")

font = pygame.font.SysFont(None, 20)
font_pequena = pygame.font.SysFont(None, 16)

# 📂 Pasta com músicas
pasta = filedialog.askdirectory(title="Selecione a pasta com suas músicas")

if not pasta:
    raise ValueError("Nenhuma pasta selecionada.")
    exit()

# ------- Filtra músicas --------
extesoes_validas = (".mp3", ".wav")

playlist = [os.path.join(pasta, f) for f in os.listdir(pasta) if f.lower().endswith(extesoes_validas)]

if not playlist:
    raise ValueError("Nenhuma música encontrada na pasta especificada.")
    exit()

def escolher_pasta():
    global pasta, playlist, indice
    nova_pasta = filedialog.askdirectory(title="Selecione a pasta com suas músicas")
    if not nova_pasta:
        return
    nova_playlist = [
        os.path.join(nova_pasta, f) 
        for f in os.listdir(nova_pasta)
        if f.lower().endswith(extesoes_validas)
    ]

    if not nova_pasta:
        return
    pasta = nova_pasta
    playlist = nova_playlist
    indice = 0
    tocar(indice)  

# -------- Iniciar pygame.mixer --------
pygame.mixer.init()

indice = 0
pausado = False
duracao_total = 0
capa_atual = None
inicio_musica = 0

#Evento para detectar quando a música termina
MUSICA_TERMINOU = pygame.USEREVENT + 1
pygame.mixer.music.set_endevent(MUSICA_TERMINOU)

COR_FUNDO = (30, 30, 30)
COR_TEXTO = (255, 255, 255)
COR_TEXTO_SEC = (190, 190, 190)
COR_BARRA = (70, 70, 70)
COR_PROGRESSO = (0, 180, 120)
COR_PROGRECAO = (230, 230, 200)
COR_BOTAO = (55, 55, 55)
COR_BOTAO_HOVER = (85, 85, 85)
COR_SEM_CAPA = (60, 60, 60)

react_anterior = pygame.Rect(210, 200, 140, 45)
react_play = pygame.Rect(360, 200, 140, 45)
react_proxima = pygame.Rect(510, 200, 140, 45)
react_pasta = pygame.Rect(660, 200, 140, 45)


#Barras de volume e progresso
barra_rect = pygame.Rect(210, 160, 660, 25)
volume_rect = pygame.Rect(880, 160, 80, 25)

volume_atual = 0.5
arrastando_barra = False
arrastando_volume = False

pygame.mixer.music.set_volume(volume_atual)

#Função para definir a posição da música com base na posição do 
#mouse na barra de progresso, calculando a proporção e convertendo para 
#o tempo correspondente, e mantendo o estado de pausa se estava pausado antes
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

#Função para definir o volume com base na posição do mouse na barra de volume,
# calculando a proporção e definindo o volume do mixer
def definir_volume(mouse_x):
    global volume_atual

    proporcao = (mouse_x - volume_rect.x) / volume_rect.width
    proporcao = max(0, min(1, proporcao))
    volume_atual = proporcao
    pygame.mixer.music.set_volume(volume_atual)

#Função para desenhar o slider de volume, preenchendo a barra de acordo com o volume atual e desenhando um knob para indicar a posição
def desenhar_slider_volume(rect, volume):
    pygame.draw.rect(screen, COR_BARRA, rect, border_radius=6)

    largura_preenchida = int(rect.width * volume)
    if largura_preenchida > 0:
        pygame.draw.rect(
            screen, 
            COR_PROGRESSO, 
            (rect.x, rect.y, largura_preenchida, rect.height), 
            border_radius=6
        )
    
    knob_x = rect.x + int(rect.width * volume)
    knob_y = rect.y + rect.height // 2
    pygame.draw.circle(screen, COR_PROGRECAO, (knob_x, knob_y), 8)

#Função para formatar o tempo em minutos e segundos
def formatar_tempo(segundos):
    min = segundos // 60
    seg = segundos % 60
    return f"{min:02}:{seg:02}"

#Função para obter a capa da música usando as tags ID3
def obter_capa(caminho):
    try:
        tags = ID3(caminho)
        apic_list = tags.getall("APIC")
        if apic_list:
            imagem_bytes = apic_list[0].data
            imagem_stream = io.BytesIO(imagem_bytes)
            imagem = pygame.image.load(imagem_stream)
            return pygame.transform.smoothscale(imagem, (150, 150))
    except ID3NoHeaderError:
        pass
    except pygame.error:
        pass
    return None
#Função para tocar a música atual, carregar a capa e obter a duração total
def tocar(ind, inicio=0):
    global duracao_total, pausado, capa_atual, inicio_musica

    #Obtém o caminho completo da música atual na playlist
    caminho = playlist[ind] 

    #Duração total com o mutagen
    audio = MP3(caminho)
    duracao_total = int(audio.info.length)

    capa_atual = obter_capa(caminho)
    inicio_musica = inicio

    pygame.mixer.music.load(caminho)
    if inicio > 0:
        pygame.mixer.music.play(start=inicio)
    else: 
        pygame.mixer.music.play()
    
    pygame.mixer.music.set_volume(volume_atual)
    pausado = False

#Função para desenhar a barra de progresso da música
def desenhar_barra(rect, progresso):
    pygame.draw.rect(screen, COR_BARRA, rect, border_radius=8)
    
    largura_preenchida = int(rect.width * progresso)
    if largura_preenchida > 0:
        pygame.draw.rect(
            screen, 
            COR_PROGRESSO,
            (rect.x, rect.y, largura_preenchida, rect.height), 
            border_radius=8
        )


#Função para desenhar os botões de controle, mudando a cor quando o mouse estiver sobre eles
def desenhar_botao(rect, texto):
    mouse_pos = pygame.mouse.get_pos()
    cor = COR_BOTAO_HOVER if rect.collidepoint(mouse_pos) else COR_BOTAO
    pygame.draw.rect(screen, cor, rect, border_radius=8)

    txt = font_pequena.render(texto, True, COR_TEXTO)
    txt_rect = txt.get_rect(center=rect.center)
    screen.blit(txt, txt_rect)
#Função para tocar a próxima música da playlist, voltando para a primeira quando chegar no final
def proxima_musica():
    global indice
    indice = (indice + 1) % len(playlist)
    tocar(indice)
#Função para tocar a música anterior da playlist, voltando para a última quando chegar no início
def musica_anterior():
    global indice
    indice = (indice - 1) % len(playlist)
    tocar(indice)
#Função para alternar entre pausar e despausar a música, atualizando o estado de "pausado" e usando as funções de pause e unpause do mixer
def alternar_pause():
    global pausado
    pausado = not pausado
    if pausado:
        pygame.mixer.music.pause()
    else: 
        pygame.mixer.music.unpause()
tocar(indice)

clock = pygame.time.Clock()
rodando = True

while rodando:
    screen.fill(COR_FUNDO)

    # 🎵 Nome da música
    nome = os.path.basename(playlist[indice])

    # ⏱ Tempo atual
    tempo_ms = pygame.mixer.music.get_pos()
    if tempo_ms < 0:
        tempo_ms = 0
    
    tempo_atual = inicio_musica +tempo_ms // 1000
    #evita passar da duração da música
    if tempo_atual > duracao_total:
        tempo_atual = duracao_total

    tempo_restante = max(0, duracao_total - tempo_atual)
    #progresso para barra
    progresso = tempo_atual / duracao_total if duracao_total > 0 else 0

    # Capa da música
    capa_x = 30
    capa_y = 40
    if capa_atual:
        screen.blit(capa_atual, (capa_x, capa_y))
    else:
        pygame.draw.rect(screen, COR_SEM_CAPA, (capa_x, capa_y, 200, 200), border_radius=8)
        texto_sem_capa = font_pequena.render("Sem Capa", True, COR_TEXTO)
        rect_sem_capa = texto_sem_capa.get_rect(center=(capa_x + 100, capa_y + 100))
        screen.blit(texto_sem_capa, rect_sem_capa)

    # Nome da música
    texto_nome = font.render(nome, True, COR_TEXTO)
    screen.blit(texto_nome, (210, 30))

    # Tempos
    texto_tempo = font.render(
        f"{formatar_tempo(tempo_atual)} / {formatar_tempo(duracao_total)}",
        True,
        COR_TEXTO
    )
    screen.blit(texto_tempo, (210, 75))

    texto_restante = font_pequena.render(
        f"Restante: -{formatar_tempo(tempo_restante)}",
        True,
        COR_TEXTO_SEC
    )  
    screen.blit(texto_restante, (210, 120))

    # Barra de progresso
    desenhar_barra(barra_rect, progresso)

    texto_volume = font_pequena.render(
        f"Volume: {int(volume_atual * 100)}%",
        True,
        COR_TEXTO
    )
    screen.blit(texto_volume, (210, 265))
    desenhar_slider_volume(volume_rect, volume_atual)

    # Botões
    desenhar_botao(react_anterior, "Anterior (B)")
    desenhar_botao(react_play, "Pause (P)" if not pausado else "Play (P)")
    desenhar_botao(react_proxima, "Próxima (N)")
    desenhar_botao(react_pasta, "Escolher Pasta (O)")

    #Status
    status = "Pausado" if pausado else "Reproduzindo"
    texto_status = font_pequena.render(f"Status: {status}", True, COR_TEXTO)
    screen.blit(texto_status, (210, 250))


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

        elif event.type == MUSICA_TERMINOU:
            proxima_musica()

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                rodando = False
            # ▶️ Play / Pause (P)
            elif event.key == pygame.K_p:
                alternar_pause()
            elif event.key == pygame.K_b:
                musica_anterior()
            elif event.key == pygame.K_n:
                proxima_musica()
            elif event.key == pygame.K_o:
                escolher_pasta()

        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if react_anterior.collidepoint(event.pos):
                musica_anterior()
            elif react_play.collidepoint(event.pos):
                alternar_pause()
            elif react_proxima.collidepoint(event.pos):
                proxima_musica()
            elif react_pasta.collidepoint(event.pos):
                escolher_pasta()
            elif barra_rect.collidepoint(event.pos):
                arrastando_barra = True
                definir_posicao_musica(event.pos[0])
            elif volume_rect.collidepoint(event.pos):
                arrastando_volume = True
                definir_volume(event.pos[0])
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            arrastando_barra = False
            arrastando_volume = False

        elif event.type == pygame.MOUSEMOTION:
            if arrastando_barra:
                definir_posicao_musica(event.pos[0])
            elif arrastando_volume:
                definir_volume(event.pos[0])   
            
    pygame.display.flip()
    clock.tick(30)

pygame.quit()