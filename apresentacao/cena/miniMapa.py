"""
Mapa em miniatura no canto da tela. Substitui MiniMapa + RenderizadorMiniMapa
— este último era um wrapper que só repassava a chamada para o primeiro,
sem acrescentar nada (código morto).
"""
import pygame


class MiniMapa:
    def __init__(self, larguraTela, alturaTela, tamanhoCelula=4, margem=15):
        self.tamanhoCelula = tamanhoCelula
        self.margem = margem
        self.larguraTela = larguraTela
        self.alturaTela = alturaTela

    def desenhar(self, tela, mapa):
        if not mapa:
            return
        linhas = len(mapa)
        colunas = len(mapa[0]) if linhas > 0 else 0
        if colunas == 0:
            return

        larguraMapa = colunas * self.tamanhoCelula
        alturaMapa = linhas * self.tamanhoCelula
        xInicial = self.larguraTela - larguraMapa - self.margem
        yInicial = self.alturaTela - alturaMapa - self.margem

        fundo = pygame.Surface((larguraMapa, alturaMapa), pygame.SRCALPHA)
        fundo.fill((20, 20, 25, 180))
        tela.blit(fundo, (xInicial, yInicial))

        for l in range(linhas):
            for c in range(colunas):
                cor = (70, 70, 85) if mapa[l][c] == 9 else (200, 200, 210)
                pygame.draw.rect(
                    tela, cor,
                    (xInicial + c * self.tamanhoCelula, yInicial + l * self.tamanhoCelula,
                     self.tamanhoCelula, self.tamanhoCelula),
                )

        pygame.draw.rect(tela, (100, 100, 120), (xInicial, yInicial, larguraMapa, alturaMapa), 1)
