import sys
import pygame
from utilidades import config
from utilidades.estadoJogo import EstadoJogo
from utilidades.controles import Controles
from renderizacao.renderizadorItens import RenderizadorItens

class GerenciadorJogo:
    def __init__(self, tela, renderizador):
        self.tela = tela
        self.renderizador = renderizador
        self.renderizador_itens = RenderizadorItens(tela, renderizador.conversor)
        self.jogo = EstadoJogo()
        self.relogio = pygame.time.Clock()

    def executar(self):
        self.jogo.reiniciar()
        rodando = True

        while rodando:
            tempo_atual = pygame.time.get_ticks()
            rodando = self._processar_eventos(tempo_atual)

            self._atualizar_logica(tempo_atual)
            self._renderizar_quadro(tempo_atual)

            self.relogio.tick(30)

        pygame.quit()
        sys.exit()

    def _processar_eventos(self, tempo_atual):
        for evento in pygame.event.get():
            acao = Controles.verificar_teclas(evento, self.jogo, tempo_atual)
            
            if acao == "sair":
                return False
            elif acao == "proximo_labirinto":
                self.jogo.avancar_proximo_labirinto()
            elif acao in ("reiniciar_total", "reiniciar_apos_derrota"):
                self.jogo.reiniciar()
            elif acao == "usar_pocao":
                self.jogo.usar_pocao(tempo_atual)
        return True

    def _atualizar_logica(self, tempo_atual):
        if not self.jogo.vitoria and not self.jogo.derrota:
            if tempo_atual - self.jogo.ultimo_passo_jogador > config.TEMPO_PASSO_JOGADOR:
                dx, dy = Controles.processar_movimento()
                self.jogo.processar_movimento(dx, dy, tempo_atual)

        self.jogo.atualizar(tempo_atual)

    def _renderizar_quadro(self, tempo_atual):
        self.tela.fill((20, 20, 25))
        self.renderizador.desenhar_cena(
            config.LINHAS, config.COLUNAS, self.jogo.mapa, self.jogo.pos_jogador, 
            self.jogo.inimigo.posicao, self.jogo.pos_saida, self.jogo.rastro_inimigo, self.jogo.pocao.ativa,
            renderizador_itens=self.renderizador_itens, item=self.jogo.pocao
        )

        self.renderizador.desenhar_interface(
            config.LARGURA, self.jogo.jogo_iniciado, self.jogo.pocao.ativa, 
            self.jogo.pocao.tempo_fim, tempo_atual, self.jogo.pocao.frascos, self.jogo.vitoria, self.jogo.derrota,
            total_itens=self.jogo.contar_total_itens(),
            renderizador_itens=self.renderizador_itens,
            item_exemplo=self.jogo.pocao
        )
        pygame.display.flip()