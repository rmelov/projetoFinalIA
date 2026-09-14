import pygame

COR_CHAO = (160, 160, 160)
COR_RASTRO = (220, 50, 50, 150)

class RenderizadorChao:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, iso_x, iso_y, r, c, eh_rastro, saida_obj):
        larg = self.conversor.largura_tile
        alt = self.conversor.altura_tile

        if eh_rastro:
            cor = COR_RASTRO
        else:
            cor = COR_CHAO

        if len(cor) == 4:
            superficie_temp = pygame.Surface((larg, alt), pygame.SRCALPHA)
            pontos_locais = [(larg // 2, 0), (larg, alt // 2), (larg // 2, alt), (0, alt // 2)]
            pygame.draw.polygon(superficie_temp, cor, pontos_locais)
            pygame.draw.polygon(superficie_temp, (100, 100, 100, 150), pontos_locais, 1)
            self.tela.blit(superficie_temp, (iso_x - larg // 2, iso_y))
        else:
            pontos = [(iso_x, iso_y), (iso_x + larg // 2, iso_y + alt // 2), (iso_x, iso_y + alt), (iso_x - larg // 2, iso_y + alt // 2)]
            pygame.draw.polygon(self.tela, cor, pontos)
            pygame.draw.polygon(self.tela, (100, 100, 100), pontos, 1)