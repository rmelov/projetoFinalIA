import sys
import pygame
from utilidades import config
from utilidades.estadoJogo import EstadoJogo
from utilidades.controles import Controles
from renderizacao.renderizadorItens import RenderizadorItens
from renderizacao.renderizadorRotaSaida import RenderizadorRotaSaida

class GerenciadorJogo:
    def __init__(self, tela, renderizador):
        self.tela = tela
        self.renderizador = renderizador
        self.renderizador_itens = RenderizadorItens(tela, renderizador.conversor)
        self.renderizador_rota_saida = RenderizadorRotaSaida(renderizador.conversor)
        self.jogo = EstadoJogo(renderizador.conversor)
        self.relogio = pygame.time.Clock()

    def executar(self):
        self.jogo.reiniciar()
        self._atualizar_centralizacao_isometrica()
        rodando = True

        while rodando:
            tempo_atual = pygame.time.get_ticks()
            rodando = self._processar_eventos(tempo_atual)

            self._atualizar_logica(tempo_atual)
            self._renderizar_quadro(tempo_atual)

            self.relogio.tick(30)

        pygame.quit()
        sys.exit()

    def _atualizar_centralizacao_isometrica(self):
        linhas, colunas = self.jogo._obter_dimensoes_atuais()
        largura_grid = colunas * (config.LARGURA_TILE / 2)
        altura_grid = linhas * (config.ALTURA_TILE / 2)
        
        self.renderizador.conversor.deslocamento_x = config.LARGURA // 2
        self.renderizador.conversor.deslocamento_y = (config.ALTURA - altura_grid) // 2 - (config.ALTURA_TILE * linhas // 4)

    def _processar_eventos(self, tempo_atual):
        for evento in pygame.event.get():
            acao = Controles.verificar_teclas(evento, self.jogo, tempo_atual)
            
            if acao == "sair":
                return False
            elif acao == "proximo_labirinto":
                self.jogo.avancar_proximo_labirinto()
                self._atualizar_centralizacao_isometrica()
            elif acao in ("reiniciar_total", "reiniciar_apos_derrota"):
                self.jogo.reiniciar()
                self._atualizar_centralizacao_isometrica()
            elif acao == "usar_pocao":
                self.jogo.usar_pocao(tempo_atual)
        return True

    def _atualizar_logica(self, tempo_atual):
        if not self.jogo.vitoria and not self.jogo.derrota:
            tempo_passo_atual = (
                config.TEMPO_PASSO_JOGADOR_POCAO 
                if self.jogo.pocao.ativa 
                else config.TEMPO_PASSO_JOGADOR
            )
            
            if tempo_atual - self.jogo.ultimo_passo_jogador > tempo_passo_atual:
                dx, dy = Controles.processar_movimento()
                self.jogo.processar_movimento(dx, dy, tempo_atual)

        self.jogo.atualizar(tempo_atual)

    def _renderizar_quadro(self, tempo_atual):
        linhas_atuais, colunas_atuais = self.jogo._obter_dimensoes_atuais()

        self.tela.fill((20, 20, 25))
        self.renderizador.desenhar_cena(
            linhas=linhas_atuais,
            colunas=colunas_atuais,
            mapa=self.jogo.mapa,
            pos_jog=self.jogo.pos_jogador,
            pos_inimigo=self.jogo.inimigo.posicao,
            saida_obj=self.jogo.saida_obj,
            rastro=self.jogo.rastro_inimigo,
            pocao_ativa=self.jogo.pocao.ativa,
            renderizador_itens=self.renderizador_itens,
            item=self.jogo.pocao,
            vortex=self.jogo.vortex,
            tempo_atual=tempo_atual,
            vitoria=self.jogo.vitoria,
            gerenciador_textos=self.jogo.gerenciador_textos,
            inimigo_obj=self.jogo.inimigo,
            tempo_congelamento_inimigo=self.jogo.tempo_congelamento_inimigo
        )

        self.renderizador_rota_saida.desenhar(
            self.tela, 
            self.jogo.mapa, 
            self.jogo.pos_jogador, 
            self.jogo.pos_saida, 
            self.jogo.pocao.ativa
        )

        self.renderizador.desenhar_interface(
            largura_tela=config.LARGURA,
            altura_tela=config.ALTURA,
            jogo_iniciado=self.jogo.jogo_iniciado,
            pocao_ativa=self.jogo.pocao.ativa, 
            tempo_pocao_fim=self.jogo.pocao.tempo_fim,
            tempo_atual=tempo_atual,
            frascos=self.jogo.pocao.frascos,
            vitoria=self.jogo.vitoria,
            derrota=self.jogo.derrota,
            total_itens=self.jogo.contar_total_itens(),
            renderizador_itens=self.renderizador_itens,
            item_exemplo=self.jogo.pocao,
            pontuacao_total=self.jogo.obter_pontuacao_total(),
            nivel_atual=self.jogo.nivel_atual,
            gerenciador_recorde=self.jogo.gerenciador_recorde
        )
        pygame.display.flip()