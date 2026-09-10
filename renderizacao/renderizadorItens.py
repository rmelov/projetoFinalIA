import os
import pygame

class RenderizadorItens:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor
        self._cache_imagens = {}

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

    def desenhar_item(self, item):
        """Método genérico para renderizar qualquer item que possua posicao e imagem_path."""
        if hasattr(item, "posicao") and item.posicao:
            r, c = item.posicao

            sx, sy = self.conversor.centro_do_tile(r, c)
            
            caminho_img = getattr(item, "imagem_path", "")
            img = self._carregar_imagem(caminho_img)
            
            rect = img.get_rect(center=(sx, sy - 6))
            self.tela.blit(img, rect)

    def desenhar_pocao(self, pocao):
        """Método específico para a Poção de Coragem (mantido por compatibilidade)."""
        self.desenhar_item(pocao)