import pygame
from utilidades import config

def criar_fonte(tamanho):
    try:
        return pygame.font.Font(config.FONTE_CAMINHO, tamanho)
    except Exception:
        return pygame.font.SysFont(None, tamanho)