"""Carrega fontes com alternativa se o arquivo faltar — em um único lugar.
Antes, esse mesmo try/except estava copiado em 5 pontos diferentes entre
menu.py e modosJogo.py."""
import pygame

CAMINHO_FONTE_PADRAO = "assets/fontes/vhs-vcr-osd.ttf"


class Fontes:
    """Entrega fontes carregadas, com fallback para a fonte do sistema."""

    def __init__(self, caminho=CAMINHO_FONTE_PADRAO):
        self._caminho = caminho
        self._cache = {}

    def obter(self, tamanho: int) -> pygame.font.Font:
        if tamanho not in self._cache:
            try:
                self._cache[tamanho] = pygame.font.Font(self._caminho, tamanho)
            except Exception:
                self._cache[tamanho] = pygame.font.SysFont("arial", tamanho)
        return self._cache[tamanho]
