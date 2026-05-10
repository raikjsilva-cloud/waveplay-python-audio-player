"""Funções auxiliares do projeto.

Aqui ficam utilidades pequenas e reutilizáveis que não pertencem
diretamente nem à interface nem à lógica principal do player.
"""

import io

import pygame
from mutagen.id3 import ID3, ID3NoHeaderError


def formatar_tempo(segundos: int) -> str:
    """Converte segundos para o formato MM:SS."""
    minutos = segundos // 60
    seg = segundos % 60
    return f"{minutos:02}:{seg:02}"


def obter_capa(caminho: str, tamanho=(140, 140)):
    """Tenta extrair a capa embutida do arquivo MP3.

    Retorna uma Surface do pygame redimensionada quando encontra a capa.
    Caso o arquivo não tenha imagem, retorna None.
    """
    try:
        tags = ID3(caminho)
        apic_list = tags.getall("APIC")
        if apic_list:
            imagem_bytes = apic_list[0].data
            imagem_stream = io.BytesIO(imagem_bytes)
            imagem = pygame.image.load(imagem_stream)
            return pygame.transform.smoothscale(imagem, tamanho)
    except (ID3NoHeaderError, pygame.error):
        return None
    return None
