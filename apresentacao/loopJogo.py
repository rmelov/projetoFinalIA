"""Laço principal de uma partida: lê entrada, atualiza a Partida, desenha."""
import sys

import pygame

from aplicacao.partida import Partida
from dominio.regras.regrasTempo import TEMPO_PASSO_JOGADOR, TEMPO_PASSO_JOGADOR_COM_POCAO

from apresentacao.cena.renderizadorCena import RenderizadorCena
from apresentacao.cena.renderizadorItens import RenderizadorItens
from apresentacao.cena.renderizadorRotaSaida import RenderizadorRotaSaida
from apresentacao.configVisual import ALTURA_TILE, TAMANHO_FONTE_PRINCIPAL, TAMANHO_FONTE_SUB
from apresentacao.entrada.acao import Acao
from apresentacao.entrada.mapeadorTeclas import MapeadorTeclas
from apresentacao.hud.hud import Hud
from apresentacao.recursos.fabricaSprites import FabricaSprites
from apresentacao.recursos.fontes import Fontes


class LoopJogo:
    """Orquestra uma partida do início ao fim; devolve o controle ao sair (ESC)."""

    def __init__(self, contextoVisual, conversor, buscador, repositorioRecorde):
        self.contexto = contextoVisual
        self.conversor = conversor
        self.buscador = buscador
        self.repositorioRecorde = repositorioRecorde

        fontes = Fontes()
        self.fontePrincipal = fontes.obter(TAMANHO_FONTE_PRINCIPAL)
        self.fonteSub = fontes.obter(TAMANHO_FONTE_SUB)

        fabricaSprites = FabricaSprites()
        self.renderizadorItens = RenderizadorItens(contextoVisual.tela, conversor, fabricaSprites)
        self.renderizadorCena = RenderizadorCena(contextoVisual.tela, conversor, fabricaSprites)
        self.renderizadorRotaSaida = RenderizadorRotaSaida(conversor, buscador)
        self.hud = Hud(contextoVisual.tela, self.fontePrincipal, self.fonteSub)

        self.partida = None
        self.textoOrigem = ""
        self.textoDestino = ""

    def executar(self, metodoId=None, textoOrigem="", textoDestino=""):
        if metodoId is not None:
            self.partida = Partida(self.buscador, self.repositorioRecorde, metodoId=metodoId)
            self.textoOrigem = textoOrigem
            self.textoDestino = textoDestino

        self.partida.definirCoordenadasPersonalizadas(self.textoOrigem, self.textoDestino)
        self.partida.reiniciar()
        self._centralizarCamera()

        relogio = pygame.time.Clock()
        while True:
            tempoMs = pygame.time.get_ticks()
            resultado = self._processarEventos()
            if resultado == "voltar":
                return
            self._atualizarLogica(tempoMs)
            self._renderizar(tempoMs)
            relogio.tick(30)

    def _centralizarCamera(self):
        linhas, colunas = self.partida.dimensoesAtuais()
        alturaGrid = linhas * (ALTURA_TILE / 2)
        self.conversor.deslocamentoX = self.contexto.largura // 2
        self.conversor.deslocamentoY = (self.contexto.altura - alturaGrid) // 2 - (ALTURA_TILE * linhas // 4)

    def _processarEventos(self):
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            acao = MapeadorTeclas.acaoDaPartida(evento, self.partida)
            if acao == Acao.VOLTAR_MENU:
                return "voltar"
            elif acao == Acao.PROXIMO_LABIRINTO:
                self.partida.avancarProximoLabirinto()
                self._centralizarCamera()
            elif acao in (Acao.REINICIAR_TOTAL, Acao.REINICIAR_APOS_DERROTA):
                self.partida.reiniciar()
                self._centralizarCamera()
            elif acao == Acao.USAR_POCAO:
                self.partida.usarPocao(pygame.time.get_ticks())
        return None

    def _atualizarLogica(self, tempoMs):
        partida = self.partida
        if not partida.vitoria and not partida.derrota:
            tempoPasso = TEMPO_PASSO_JOGADOR_COM_POCAO if partida.pocao.ativa else TEMPO_PASSO_JOGADOR
            if tempoMs - partida.ultimoPassoJogadorMs > tempoPasso:
                deltaLinha, deltaColuna = MapeadorTeclas.direcaoMovimento()
                partida.processarMovimento(deltaLinha, deltaColuna, tempoMs)

        partida.atualizar(tempoMs)
        self._drenarNotificacoes()

    def _drenarNotificacoes(self):
        for texto, coordenada, cor in self.partida.notificacoesPendentes:
            self.renderizadorCena.textosFlutuantes.adicionar(texto, coordenada, cor)
        self.partida.notificacoesPendentes.clear()

    def _renderizar(self, tempoMs):
        self.renderizadorCena.desenhar(self.partida, tempoMs, self.fonteSub)
        self.renderizadorRotaSaida.desenhar(
            self.contexto.tela, self.partida.labirinto.comoGrade(),
            self.partida.jogador.posicao, self.partida.saida.posicao, self.partida.pocao.ativa,
        )
        self.hud.desenhar(
            self.contexto.largura, self.contexto.altura, self.partida, tempoMs,
            self.renderizadorItens, self.repositorioRecorde,
        )
        pygame.display.flip()
