"""
Produz a aparência visual de um item de domínio a partir do seu
`imagemPath`. Antes desta extração, Saida processava a própria imagem
(silhueta preta com pygame.mask) dentro do construtor de domínio — um item
de jogo não deveria saber manipular superfícies.
"""
import pygame

from apresentacao.recursos.animadorSprite import AnimadorSprite
from apresentacao.recursos.cacheImagens import CacheImagens
from dominio.itens.saida import IMAGEM_PADRAO as IMAGEM_SAIDA
from dominio.itens.vortex import IMAGEM_PADRAO as IMAGEM_VORTEX


class FabricaSprites:
    """Cacheia e devolve o frame atual (animado) ou a imagem estática de um item."""

    def __init__(self):
        self._cacheImagens = CacheImagens()
        self._animadores = {}

    def obterVisual(self, imagemPath: str, tempoMs: int):
        """Devolve a Surface a desenhar para este item neste instante."""
        if imagemPath == IMAGEM_VORTEX:
            return self._animadorVortex().obterFrameAtual(tempoMs)
        if imagemPath == IMAGEM_SAIDA:
            return self._animadorSaida().obterFrameAtual(tempoMs)
        return self._cacheImagens.obter(imagemPath)

    def _animadorVortex(self) -> AnimadorSprite:
        if "vortex" not in self._animadores:
            self._animadores["vortex"] = AnimadorSprite(
                IMAGEM_VORTEX, larguraFrame=100, alturaFrame=100, colunasGrid=8,
                totalFrames=61, velocidadeAnimacao=60, tamanhoRender=(128, 128),
            )
        return self._animadores["vortex"]

    def _animadorSaida(self) -> AnimadorSprite:
        if "saida" not in self._animadores:
            animador = AnimadorSprite(
                IMAGEM_SAIDA, larguraFrame=100, alturaFrame=100, colunasGrid=8,
                totalFrames=61, velocidadeAnimacao=60, tamanhoRender=(156, 156),
            )
            self._tornarSilhuetaPreta(animador)
            self._animadores["saida"] = animador
        return self._animadores["saida"]

    @staticmethod
    def _tornarSilhuetaPreta(animador: AnimadorSprite):
        """Recolore cada frame para uma silhueta preta, preservando o alfa original."""
        for indice, frame in enumerate(animador.frames):
            superficiePreta = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            superficiePreta.fill((0, 0, 0, 255))
            frameFinal = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            frameFinal.blit(superficiePreta, (0, 0))
            frameFinal.blit(frame, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            animador.frames[indice] = frameFinal
