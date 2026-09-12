import pygame
from componentes.geradorLabirinto import gerar_labirinto_base
from componentes.perseguidor import Perseguidor
from componentes.inventario import Inventario
from componentes.inventarioPartida import InventarioPartida
from itens.pocaoCoragem import PocaoCoragem
from utilidades import config

class EstadoJogo:
    def __init__(self):
        self.mapa = []
        self.pos_jogador = []
        self.pos_saida = ()
        self.inimigo = None
        self.rastro_inimigo = set()
        
        self.inventario_geral = Inventario()
        self.inventario_partida = InventarioPartida()
        
        self.pocao = PocaoCoragem(quantidade_inicial=0)
        self.jogo_iniciado = False
        self.vitoria = False
        self.derrota = False
        self.ultimo_movimento_ia = 0
        self.ultimo_passo_jogador = 0

    def sincronizar_frascos(self):
        self.pocao.frascos = self.contar_total_itens()

    def usar_pocao(self, tempo_atual):
        if self.pocao.usar(tempo_atual):
            if self.inventario_partida.contar_itens() > 0:
                self.inventario_partida.remover_ultimo()
            elif self.inventario_geral.contar_total() > 0:
                self.inventario_geral.remover_ultimo()
            self.sincronizar_frascos()
            return True
        return False

    def reiniciar(self):
        self.inventario_partida.esvaziar()
        self._preparar_novo_labirinto()

    def avancar_proximo_labirinto(self):
        itens_ganhos = self.inventario_partida.resgatar_itens()
        self.inventario_geral.adicionar_lote(itens_ganhos)
        self._preparar_novo_labirinto()

    def _preparar_novo_labirinto(self):
        self.mapa, pos_jog_tup, pos_inim_tup, self.pos_saida = gerar_labirinto_base(config.LINHAS, config.COLUNAS)
        self.pos_jogador = list(pos_jog_tup)
        self.inimigo = Perseguidor(pos_inicial=pos_inim_tup)
        self.rastro_inimigo = {tuple(pos_inim_tup)}

        self.pocao = PocaoCoragem(quantidade_inicial=0)
        self.sincronizar_frascos()
        self.pocao.nascer(self.mapa, config.LINHAS, config.COLUNAS, self.pos_jogador, self.pos_saida, self.inimigo.posicao)

        self.jogo_iniciado = False
        self.vitoria = False
        self.derrota = False
        self.ultimo_movimento_ia = pygame.time.get_ticks()
        self.ultimo_passo_jogador = pygame.time.get_ticks()

    def processar_movimento(self, dx, dy, tempo_atual):
        if dx == 0 and dy == 0:
            return

        nx, ny = self.pos_jogador[0] + dx, self.pos_jogador[1] + dy
        if not (0 <= nx < config.LINHAS and 0 <= ny < config.COLUNAS and self.mapa[nx][ny] == 0):
            return

        self.pos_jogador = [nx, ny]
        self.ultimo_passo_jogador = tempo_atual

        if not self.jogo_iniciado:
            self.jogo_iniciado = True
            self.ultimo_movimento_ia = tempo_atual

        pos_tupla = tuple(self.pos_jogador)
        
        if self.pocao.posicao and pos_tupla == self.pocao.posicao:
            self.pocao.coletar()
            self.inventario_partida.adicionar_item(self.pocao)
            self.sincronizar_frascos()
            self.pocao.posicao = None

        if self.pocao.ativa and pos_tupla in self.rastro_inimigo:
            self.rastro_inimigo.remove(pos_tupla)

    def atualizar(self, tempo_atual):
        self.pocao.atualizar(tempo_atual)
        self._atualizar_ia(tempo_atual)
        self._verificar_condicoes_fim_jogo()

    def _atualizar_ia(self, tempo_atual):
        if self.jogo_iniciado and not self.vitoria and not self.derrota:
            if tempo_atual - self.ultimo_movimento_ia > config.TEMPO_MOVIMENTO_IA:
                self.inimigo.atualizar_caminho(self.pos_jogador, config.LINHAS, config.COLUNAS, self.mapa)
                self.inimigo.mover()
                self.rastro_inimigo.add(tuple(self.inimigo.posicao))
                self.ultimo_movimento_ia = tempo_atual

    def _verificar_condicoes_fim_jogo(self):
        if tuple(self.pos_jogador) == self.pos_saida and not self.vitoria:
            self.vitoria = True
            # Removido self.avancar_proximo_labirinto() daqui para esperar o 'R'

        if self.pos_jogador == self.inimigo.posicao:
            self.derrota = True

        if tuple(self.pos_jogador) in self.rastro_inimigo and not self.pocao.ativa:
            self.derrota = True

    def contar_total_itens(self):
        return self.inventario_geral.contar_total() + self.inventario_partida.contar_itens()