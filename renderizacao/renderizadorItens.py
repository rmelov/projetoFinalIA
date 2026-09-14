import os
import pygame
from utilidades.animadorSprite import AnimadorSprite

class RenderizadorItens:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor
        self._cache_imagens = {}
        self._cache_animadores = {}

    def _carregar_imagem(self, caminho):
        if caminho not in self._cache_imagens:
            if os.path.exists(caminho):
                img = pygame.image.load(caminho).convert_alpha()
                self._cache_imagens[caminho] = pygame.transform.scale(img, (28, 28))
            else:
                surf = pygame.Surface((28, 28), pygame.SRCALPHA)
                pygame.draw.circle(surf, (0, 150, 255), (14, 14), 10)
                self._cache_imagens[caminho] = surf
        return self._cache_imagens[caminho]

    def _obter_animador(self, caminho):
        if caminho not in self._cache_animadores:
            self._cache_animadores[caminho] = AnimadorSprite(caminho)
        return self._cache_animadores[caminho]

    def desenhar_item(self, item, tempo_atual=0):
        if hasattr(item, "posicao") and item.posicao:
            r, c = item.posicao
            sx, sy = self.conversor.centro_do_tile(r, c)
            caminho_img = getattr(item, "imagem_path", "")

            if hasattr(item, "animador") or "spritesheet" in caminho_img:
                animador = getattr(item, "animador", None)
                if not animador:
                    animador = self._obter_animador(caminho_img)
                
                img = animador.obter_frame_atual(tempo_atual)
                if img:
                    rect = img.get_rect(center=(sx, sy - 14))
                    self.tela.blit(img, rect)
            else:
                img = self._carregar_imagem(caminho_img)
                rect = img.get_rect(center=(sx, sy - 6))
                self.tela.blit(img, rect)