"""
Desenha segmentos sólidos ou tracejados entre pontos de tela. Antes, o
método de linha tracejada estava copiado, linha por linha (inclusive o
`import math` dentro da função), em RenderizadorFarejo e
RenderizadorRotaSaida.
"""
import math

import pygame


class DesenhadorCaminho:
    """Só desenha linhas — não decide onde é oclusão nem de onde vem a rota."""

    @staticmethod
    def linhaSolida(tela, cor, p1, p2, largura=3):
        pygame.draw.line(tela, cor, p1, p2, largura)

    @staticmethod
    def linhaTracejada(tela, cor, p1, p2, largura=2, comprimentoTraco=8):
        x1, y1 = p1
        x2, y2 = p2
        distancia = math.hypot(x2 - x1, y2 - y1)
        if distancia == 0:
            return

        direcaoX = (x2 - x1) / distancia
        direcaoY = (y2 - y1) / distancia

        atual = 0.0
        desenhar = True
        while atual < distancia:
            proximo = min(atual + comprimentoTraco, distancia)
            if desenhar:
                px1 = x1 + direcaoX * atual
                py1 = y1 + direcaoY * atual
                px2 = x1 + direcaoX * proximo
                py2 = y1 + direcaoY * proximo
                pygame.draw.line(tela, cor, (int(px1), int(py1)), (int(px2), int(py2)), largura)
            atual = proximo
            desenhar = not desenhar
