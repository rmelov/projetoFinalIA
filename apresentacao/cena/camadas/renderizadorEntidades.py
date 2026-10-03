import pygame

COR_JOGADOR = (50, 220, 50)
COR_JOGADOR_POCAO = (0, 255, 255)
COR_INIMIGO = (220, 50, 50)


class RenderizadorEntidades:
    """Desenha jogador e inimigo como um marcador com sombra."""

    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor

    def desenhar(self, linha, coluna, tipo, pocaoAtiva):
        centroX, centroY = self.conversor.centroDoTile(linha, coluna)
        raio = 10
        cor = (COR_JOGADOR_POCAO if pocaoAtiva else COR_JOGADOR) if tipo == "jogador" else COR_INIMIGO

        pygame.draw.ellipse(self.tela, (30, 30, 30), (centroX - raio, centroY - 5, raio * 2, 10))
        pygame.draw.circle(self.tela, cor, (centroX, centroY - 8), raio)
        pygame.draw.circle(self.tela, (0, 0, 0), (centroX, centroY - 8), raio, 1)
