"""Tela de seleção do método de busca do inimigo. A lista vem do catálogo
único (aplicacao/metodosBusca.py) — antes era uma lista hardcoded aqui."""
import sys

import pygame

from aplicacao.metodosBusca import METODOS_DISPONIVEIS
from apresentacao.entrada.mapeadorTeclas import MapeadorTeclas


class TelaModos:
    def __init__(self, contexto, fontes):
        self.contexto = contexto
        self.fontePrincipal = fontes.obter(48)
        self.fonteItem = fontes.obter(28)
        self.fonteHover = fontes.obter(32)
        self.fonteDesc = fontes.obter(18)
        self.indiceSelecionado = 0
        self._opcoes = [{"id": m.id, "nome": m.nome, "desc": m.descricao} for m in METODOS_DISPONIVEIS]
        self._opcoes.append({"id": "voltar", "nome": "VOLTAR", "desc": "Retorna ao menu principal."})

    def executar(self):
        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((20, 20, 25))
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
                            self.indiceSelecionado = indice
                            return self._opcoes[indice]["id"]
            pygame.display.flip()
            relogio.tick(30)

    def _desenhar(self):
        largura, altura = self.contexto.largura, self.contexto.altura
        titulo = self.fontePrincipal.render("SELECIONE O MODO DE BUSCA", True, (0, 191, 255))
        self.contexto.tela.blit(titulo, titulo.get_rect(center=(largura // 2, 70)))

        self._retangulos = []
        y = 160
        mouse_pos = pygame.mouse.get_pos()
        descricaoAtiva = self._opcoes[self.indiceSelecionado]["desc"]

        for indice, opcao in enumerate(self._opcoes):
            yPos = y + indice * 58
            corTexto = (255, 100, 100) if opcao["id"] == "voltar" else (255, 255, 255)

            textoBase = self.fonteItem.render(opcao["nome"], True, corTexto)
            retanguloBase = textoBase.get_rect(center=(largura // 2, yPos))

            if retanguloBase.collidepoint(mouse_pos):
                self.indiceSelecionado = indice
                descricaoAtiva = opcao["desc"]

            if indice == self.indiceSelecionado or retanguloBase.collidepoint(mouse_pos):
                texto = self.fonteHover.render(opcao["nome"], True, (255, 235, 59))
            else:
                texto = textoBase

            retangulo = texto.get_rect(center=(largura // 2, yPos))
            self.contexto.tela.blit(texto, retangulo)
            self._retangulos.append(retangulo)

        if descricaoAtiva:
            descricao = self.fonteDesc.render(descricaoAtiva, True, (200, 200, 200))
            self.contexto.tela.blit(descricao, descricao.get_rect(center=(largura // 2, altura - 80)))
