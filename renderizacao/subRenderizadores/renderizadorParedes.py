import pygame

COR_PAREDE_TOPO = (120, 120, 140)
COR_PAREDE_ESQ = (80, 80, 100)
COR_PAREDE_DIR = (50, 50, 70)
ALTURA_PAREDE_CHEIA = 28
ALTURA_PAREDE_BAIXA = 6

class RenderizadorParedes:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, iso_x, iso_y, parede_translucida):
        altura_bloco = ALTURA_PAREDE_BAIXA if parede_translucida else ALTURA_PAREDE_CHEIA
        x, y = iso_x, iso_y
        larg = self.conversor.largura_tile
        alt = self.conversor.altura_tile
        w_2, h_2 = larg // 2, alt // 2

        topo = [(x, y - altura_bloco), (x + w_2, y + h_2 - altura_bloco), (x, y + alt - altura_bloco), (x - w_2, y + h_2 - altura_bloco)]
        esquerda = [(x - w_2, y + h_2 - altura_bloco), (x, y + alt - altura_bloco), (x, y + alt), (x - w_2, y + h_2)]
        direita = [(x, y + alt - altura_bloco), (x + w_2, y + h_2 - altura_bloco), (x + w_2, y + h_2), (x, y + alt)]

        pygame.draw.polygon(self.tela, COR_PAREDE_ESQ, esquerda)
        pygame.draw.polygon(self.tela, COR_PAREDE_DIR, direita)
        pygame.draw.polygon(self.tela, COR_PAREDE_TOPO, topo)

        pygame.draw.polygon(self.tela, (20, 20, 20), topo, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), esquerda, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), direita, 1)