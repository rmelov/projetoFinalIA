import pygame

class MiniMapa:
    def __init__(self, largura_tela, altura_tela, tamanho_celula=4, margem=15):
        self.tamanho_celula = tamanho_celula
        self.margem = margem
        self.largura_tela = largura_tela
        self.altura_tela = altura_tela

    def desenhar(self, tela, mapa):
        if not mapa:
            return

        linhas = len(mapa)
        colunas = len(mapa[0]) if linhas > 0 else 0
        if colunas == 0:
            return

        largura_mapa = colunas * self.tamanho_celula
        altura_mapa = linhas * self.tamanho_celula

        x_inicial = self.largura_tela - largura_mapa - self.margem
        y_inicial = self.altura_tela - altura_mapa - self.margem

        superficie_fundo = pygame.Surface((largura_mapa, altura_mapa), pygame.SRCALPHA)
        superficie_fundo.fill((20, 20, 25, 180))
        tela.blit(superficie_fundo, (x_inicial, y_inicial))

        for r in range(linhas):
            for c in range(colunas):
                rx = x_inicial + c * self.tamanho_celula
                ry = y_inicial + r * self.tamanho_celula

                if mapa[r][c] == 9:
                    cor = (70, 70, 85)
                else:
                    cor = (200, 200, 210)

                pygame.draw.rect(tela, cor, (rx, ry, self.tamanho_celula, self.tamanho_celula))

        pygame.draw.rect(tela, (100, 100, 120), (x_inicial, y_inicial, largura_mapa, altura_mapa), 1)