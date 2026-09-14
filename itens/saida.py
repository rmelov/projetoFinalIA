import pygame
from utilidades.animadorSprite import AnimadorSprite

class Saida:
    def __init__(self):
        self.posicao = None
        self.imagem_path = "assets/imgs/CodeManu/16_sunburn_spritesheet.png"
        
        self.animador = AnimadorSprite(
            caminho_imagem=self.imagem_path,
            largura_frame=100,
            altura_frame=100,
            colunas_grid=8,
            total_frames=61,
            velocidade_animacao=60,
            tamanho_render=(156,156)
        )
        
        self._tornar_sprite_preto()

    def _tornar_sprite_preto(self):
        for i, frame in enumerate(self.animador.frames):
            frame_preto = frame.copy()
            frame_preto.fill((0, 0, 0, 255), special_flags=pygame.BLEND_RGBA_MIN)
            base_mask = pygame.mask.from_surface(frame)
            surf_preto = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            surf_preto.fill((0, 0, 0, 255))
            final_frame = pygame.Surface(frame.get_size(), pygame.SRCALPHA)
            final_frame.blit(surf_preto, (0, 0))
            final_frame.blit(frame, (0, 0), special_flags=pygame.BLEND_RGBA_MIN)
            self.animador.frames[i] = final_frame