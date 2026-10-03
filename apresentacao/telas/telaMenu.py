"""Menu principal. Antes, menu.py acumulava seis responsabilidades (menu,
seleção de modo, campos de coordenadas, tutorial, sobre e a máquina de
estados). Aqui só sobra a navegação do menu; o resto são outras telas."""
import sys

import pygame

from apresentacao.entrada.mapeadorTeclas import MapeadorTeclas
from apresentacao.ui.botao import Botao

OPCOES = ["JOGAR", "TUTORIAL", "SOBRE", "SAIR"]


class TelaMenu:
    def __init__(self, contexto, fontes):
        self.contexto = contexto
        self.fonteTitulo = fontes.obter(52)
        self.fonteItem = fontes.obter(30)
        self.indiceSelecionado = 0

    def executar(self):
        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((12, 12, 16))
            retangulos = self._desenhar()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    self.indiceSelecionado = MapeadorTeclas.navegarMenu(
                        evento, self.indiceSelecionado, len(OPCOES)
                    )
                    if MapeadorTeclas.confirmarMenu(evento):
                        return OPCOES[self.indiceSelecionado]
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    for indice, retangulo in enumerate(retangulos):
                        if retangulo.collidepoint(evento.pos):
                            return OPCOES[indice]

            pygame.display.flip()
            relogio.tick(30)

    def _desenhar(self):
        largura, altura = self.contexto.largura, self.contexto.altura
        titulo = self.fonteTitulo.render("LABIRINTO ISOMÉTRICO", True, (255, 235, 59))
        self.contexto.tela.blit(titulo, ((largura - titulo.get_width()) // 2, altura // 4))

        retangulos = []
        y = altura // 2
        for indice, opcao in enumerate(OPCOES):
            botao = Botao(opcao, (largura // 2, y), self.fonteItem)
            retangulos.append(botao.desenhar(self.contexto.tela, selecionado=(indice == self.indiceSelecionado)))
            y += 90
        return retangulos
