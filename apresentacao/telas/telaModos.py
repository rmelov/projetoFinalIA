"""Tela de seleção do método de busca do inimigo. A lista vem do catálogo
único (aplicacao/metodosBusca.py) — antes era uma lista hardcoded aqui."""
import sys

import pygame

from aplicacao.metodosBusca import METODOS_DISPONIVEIS
from apresentacao.entrada.mapeadorTeclas import MapeadorTeclas
from apresentacao.ui.botao import Botao


class TelaModos:
    def __init__(self, contexto, fontes):
        self.contexto = contexto
        self.fontePrincipal = fontes.obter(48)
        self.fonteItem = fontes.obter(28)
        self.fonteDesc = fontes.obter(18)
        self.indiceSelecionado = 0
        self._opcoes = [{"id": m.id, "nome": m.nome, "desc": m.descricao} for m in METODOS_DISPONIVEIS]
        self._opcoes.append({"id": "voltar", "nome": "VOLTAR", "desc": "Retorna ao menu principal."})

    def executar(self):
        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((15, 15, 20))
            self._desenhar()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN:
                    self.indiceSelecionado = MapeadorTeclas.navegarMenu(
                        evento, self.indiceSelecionado, len(self._opcoes)
                    )
                    if MapeadorTeclas.confirmarMenu(evento):
                        return self._opcoes[self.indiceSelecionado]["id"]
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    for indice, retangulo in enumerate(self._retangulos):
                        if retangulo.collidepoint(evento.pos):
                            return self._opcoes[indice]["id"]
            pygame.display.flip()
            relogio.tick(30)

    def _desenhar(self):
        largura, altura = self.contexto.largura, self.contexto.altura
        titulo = self.fontePrincipal.render("ESCOLHA O MÉTODO", True, (255, 235, 59))
        self.contexto.tela.blit(titulo, ((largura - titulo.get_width()) // 2, 40))

        self._retangulos = []
        y = 150
        for indice, opcao in enumerate(self._opcoes):
            selecionado = indice == self.indiceSelecionado
            botao = Botao(opcao["nome"], (largura // 2, y), self.fonteItem)
            retangulo = botao.desenhar(self.contexto.tela, selecionado=selecionado)
            self._retangulos.append(retangulo)
            if opcao["desc"]:
                desc = self.fonteDesc.render(opcao["desc"], True, (170, 170, 170))
                self.contexto.tela.blit(desc, ((largura - desc.get_width()) // 2, y + 22))
            y += 100
