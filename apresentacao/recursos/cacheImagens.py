"""Carrega e cacheia imagens simples (ícones de item), com um círculo de
reserva quando o arquivo não existe."""
import os
import pygame


class CacheImagens:
    """Carrega uma imagem uma vez e reaproveita nas chamadas seguintes."""

    def __init__(self, tamanho=(28, 28)):
        self._tamanho = tamanho
        self._cache = {}

    def obter(self, caminho: str) -> pygame.Surface:
        if caminho not in self._cache:
            if caminho and os.path.exists(caminho):
                imagem = pygame.image.load(caminho).convert_alpha()
                self._cache[caminho] = pygame.transform.scale(imagem, self._tamanho)
            else:
                self._cache[caminho] = self._imagemReserva()
        return self._cache[caminho]

    def _imagemReserva(self) -> pygame.Surface:
        superficie = pygame.Surface(self._tamanho, pygame.SRCALPHA)
        centro = (self._tamanho[0] // 2, self._tamanho[1] // 2)
        pygame.draw.circle(superficie, (0, 150, 255), centro, self._tamanho[0] // 3)
        return superficie
