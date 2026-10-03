import pygame

COR_CHAO = (160, 160, 160)
COR_RASTRO = (220, 50, 50, 150)


class RenderizadorChao:
    """Desenha o losango de uma célula de chão, normal ou marcada como rastro."""

    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, isoX, isoY, ehRastro):
        larg = self.conversor.larguraTile
        alt = self.conversor.alturaTile
        cor = COR_RASTRO if ehRastro else COR_CHAO

        if len(cor) == 4:
            superficieTemp = pygame.Surface((larg, alt), pygame.SRCALPHA)
            pontosLocais = [(larg // 2, 0), (larg, alt // 2), (larg // 2, alt), (0, alt // 2)]
            pygame.draw.polygon(superficieTemp, cor, pontosLocais)
            pygame.draw.polygon(superficieTemp, (100, 100, 100, 150), pontosLocais, 1)
            self.tela.blit(superficieTemp, (isoX - larg // 2, isoY))
        else:
            pontos = [(isoX, isoY), (isoX + larg // 2, isoY + alt // 2),
                      (isoX, isoY + alt), (isoX - larg // 2, isoY + alt // 2)]
            pygame.draw.polygon(self.tela, cor, pontos)
            pygame.draw.polygon(self.tela, (100, 100, 100), pontos, 1)
