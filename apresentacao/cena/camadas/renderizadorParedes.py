import pygame

COR_PAREDE_TOPO = (120, 120, 140)
COR_PAREDE_ESQ = (80, 80, 100)
COR_PAREDE_DIR = (50, 50, 70)
ALTURA_PAREDE_CHEIA = 28
ALTURA_PAREDE_BAIXA = 6


class RenderizadorParedes:
    """Desenha um bloco de parede em 3 faces, translúcido quando obstrui a visão."""

    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, isoX, isoY, paredeTranslucida):
        alturaBloco = ALTURA_PAREDE_BAIXA if paredeTranslucida else ALTURA_PAREDE_CHEIA
        larg = self.conversor.larguraTile
        alt = self.conversor.alturaTile
        w2, h2 = larg // 2, alt // 2

        topo = [(isoX, isoY - alturaBloco), (isoX + w2, isoY + h2 - alturaBloco),
                (isoX, isoY + alt - alturaBloco), (isoX - w2, isoY + h2 - alturaBloco)]
        esquerda = [(isoX - w2, isoY + h2 - alturaBloco), (isoX, isoY + alt - alturaBloco),
                    (isoX, isoY + alt), (isoX - w2, isoY + h2)]
        direita = [(isoX, isoY + alt - alturaBloco), (isoX + w2, isoY + h2 - alturaBloco),
                   (isoX + w2, isoY + h2), (isoX, isoY + alt)]

        pygame.draw.polygon(self.tela, COR_PAREDE_ESQ, esquerda)
        pygame.draw.polygon(self.tela, COR_PAREDE_DIR, direita)
        pygame.draw.polygon(self.tela, COR_PAREDE_TOPO, topo)
        pygame.draw.polygon(self.tela, (20, 20, 20), topo, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), esquerda, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), direita, 1)
