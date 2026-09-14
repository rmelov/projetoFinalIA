import pygame

COR_JOGADOR = (50, 220, 50)
COR_JOGADOR_POCAO = (0, 255, 255)
COR_INIMIGO = (220, 50, 50)

class RenderizadorEntidades:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, r, c, tipo, pocao_ativa):
        centro_x, centro_y = self.conversor.centro_do_tile(r, c)
        raio = 10

        if tipo == "jogador":
            cor = COR_JOGADOR_POCAO if pocao_ativa else COR_JOGADOR
        else:
            cor = COR_INIMIGO

        pygame.draw.ellipse(self.tela, (30, 30, 30), (centro_x - raio, centro_y - 5, raio * 2, 10))
        pygame.draw.circle(self.tela, cor, (centro_x, centro_y - 8), raio)
        pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y - 8), raio, 1)