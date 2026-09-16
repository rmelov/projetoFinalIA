import random
import re
from componentes.geradorLabirinto import gerar_labirinto_base
from componentes.entidades.oponentes.perseguidor import Perseguidor
from componentes.inventario import Inventario
from componentes.inventarioPartida import InventarioPartida
from componentes.pontuacao import Pontuacao
from componentes.pontuacaoPartida import PontuacaoPartida
from componentes.textosPontuacao import GerenciadorTextosFlutuantes
from componentes.niveis import Nivel
from componentes.recorde import GerenciadorRecorde
from itens.pocaoCoragem import PocaoCoragem
from itens.vortex import Vortex
from itens.saida import Saida
from utilidades import config

class EstadoJogo:
    def __init__(self, conversor=None, modo_jogo="amplitude"):
        self.mapa = []
        self.pos_jogador = []
        self.pos_saida = ()
        self.inimigo = None
        self.rastro_inimigo = set()
        self.posicao_origem_customizada = None
        self.posicao_destino_customizada = None
        self.texto_origem_customizada = ""
        self.texto_destino_customizada = ""
        
        self.inventario_geral = Inventario()
        self.inventario_partida = InventarioPartida()

        self.gerenciador_textos = GerenciadorTextosFlutuantes(conversor) if conversor else None
        
        self.pontuacao_geral = Pontuacao(0)
        self.pontuacao_partida = PontuacaoPartida()
        
        self.sistema_nivel = Nivel()
        self.indice_nivel = 0
        
        self.pocao = PocaoCoragem(quantidade_inicial=0)
        self.vortex = Vortex()
        self.saida_obj = Saida()
        
        self.jogo_iniciado = False
        self.vitoria = False
        self.derrota = False
        self.ultimo_movimento_ia = 0
        self.ultimo_passo_jogador = 0
        self.tempo_congelamento_inimigo = 0

        self.gerenciador_recorde = GerenciadorRecorde(modo_jogo=modo_jogo)
        self.pontuacao_maxima, self.nivel_maximo = self.gerenciador_recorde.carregar()

    @property
    def nivel_atual(self):
        return self.sistema_nivel.obter_valor_nivel(self.indice_nivel)

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
        self.pontuacao_partida.esvaziar()
        self.pocao.ativa = False
        self.pocao.tempo_fim = 0
        self._preparar_novo_labirinto(resetar_total=True)

    @staticmethod
    def _parse_coordenada(texto):
        texto = str(texto or "").strip()
        if not texto:
            return None
        numeros = re.findall(r"-?\d+", texto)
        if len(numeros) < 2:
            return None
        return (int(numeros[0]), int(numeros[1]))

    def definir_coordenadas_personalizadas(self, texto_origem="", texto_destino=""):
        self.texto_origem_customizada = str(texto_origem or "")
        self.texto_destino_customizada = str(texto_destino or "")
        self.posicao_origem_customizada = self._parse_coordenada(self.texto_origem_customizada)
        self.posicao_destino_customizada = self._parse_coordenada(self.texto_destino_customizada)

    def _aplicar_coordenadas_personalizadas(self, linhas, colunas):
        origem = self.posicao_origem_customizada
        destino = self.posicao_destino_customizada

        if origem is not None:
            if not (0 <= origem[0] < linhas and 0 <= origem[1] < colunas):
                origem = None
        if destino is not None:
            if not (0 <= destino[0] < linhas and 0 <= destino[1] < colunas):
                destino = None

        if origem is not None and destino is not None and origem == destino:
            destino = None

        if origem is not None:
            self.mapa[origem[0]][origem[1]] = 0
            self.pos_jogador = [origem[0], origem[1]]
        else:
            self.pos_jogador = [1, 1]

        if destino is not None:
            self.mapa[destino[0]][destino[1]] = 0
            self.pos_saida = (destino[0], destino[1])
        else:
            self.pos_saida = (linhas - 2, colunas - 2)

        if tuple(self.pos_jogador) == self.pos_saida:
            for r in range(linhas):
                for c in range(colunas):
                    if (r, c) != tuple(self.pos_jogador) and self.mapa[r][c] == 0:
                        self.pos_saida = (r, c)
                        break
                if tuple(self.pos_jogador) != self.pos_saida:
                    break

        self.mapa[self.pos_saida[0]][self.pos_saida[1]] = 0
        self.saida_obj.posicao = self.pos_saida

    def avancar_proximo_labirinto(self):
        itens_ganhos = self.inventario_partida.resgatar_itens()
        self.inventario_geral.adicionar_lote(itens_ganhos)
        
        pontos_ganhos = self.pontuacao_partida.resgatar_pontos()
        self.pontuacao_geral.adicionar(pontos_ganhos)
        
        self.indice_nivel += 1
        self._preparar_novo_labirinto(resetar_total=True)

    def _obter_dimensoes_atuais(self):
        tamanho = self.sistema_nivel.calcular_tamanho_grid(self.indice_nivel)
        return tamanho, tamanho

    def _preparar_novo_labirinto(self, resetar_total=True):
        linhas_atuais, colunas_atuais = self._obter_dimensoes_atuais()
        pocao_ativa_anterior = self.pocao.ativa
        tempo_fim_anterior = self.pocao.tempo_fim
        frascos_atuais = self.pocao.frascos

        if resetar_total or not self.pos_jogador or not self.inimigo:
            self.mapa, pos_jog_tup, pos_inim_tup, self.pos_saida = gerar_labirinto_base(linhas_atuais, colunas_atuais)
            self.pos_jogador = list(pos_jog_tup)
            self.inimigo = Perseguidor(pos_inicial=pos_inim_tup)
            self.inimigo.ajustar_velocidade(self.indice_nivel)
            self.rastro_inimigo = {tuple(pos_inim_tup)}
            self.jogo_iniciado = False
            import pygame
            self.ultimo_movimento_ia = pygame.time.get_ticks()
            self.ultimo_passo_jogador = pygame.time.get_ticks()
        else:
            pos_jog_atual = tuple(self.pos_jogador)
            pos_inim_atual = tuple(self.inimigo.posicao)
            
            self.mapa, _, _, self.pos_saida = gerar_labirinto_base(linhas_atuais, colunas_atuais)
            
            if pos_jog_atual[0] < linhas_atuais and pos_jog_atual[1] < colunas_atuais:
                self.mapa[pos_jog_atual[0]][pos_jog_atual[1]] = 0
                self.pos_jogador = list(pos_jog_atual)
            else:
                self.pos_jogador = [1, 1]

            if pos_inim_atual[0] < linhas_atuais and pos_inim_atual[1] < colunas_atuais:
                self.mapa[pos_inim_atual[0]][pos_inim_atual[1]] = 0
                self.inimigo.posicao = list(pos_inim_atual)
            else:
                self.inimigo.posicao = [1, 2]

            self.mapa[self.pos_saida[0]][self.pos_saida[1]] = 0
            self.rastro_inimigo = {tuple(self.inimigo.posicao)}

        self._aplicar_coordenadas_personalizadas(linhas_atuais, colunas_atuais)
        self.inimigo.ajustar_velocidade(self.indice_nivel)
        self.saida_obj.posicao = self.pos_saida
        self.pocao = PocaoCoragem(quantidade_inicial=0)
        self.pocao.frascos = frascos_atuais
        self.pocao.ativa = pocao_ativa_anterior
        self.pocao.tempo_fim = tempo_fim_anterior

        self.pocao.nascer(self.mapa, linhas_atuais, colunas_atuais, self.pos_jogador, self.pos_saida, self.inimigo.posicao)

        self.vortex = Vortex()
        self.posicionar_vortex(linhas_atuais, colunas_atuais)

        self.vitoria = False
        self.derrota = False
        self.tempo_congelamento_inimigo = 0

    def posicionar_vortex(self, linhas, colunas):
        celulas_livres = [
            (r, c) for r in range(linhas) for c in range(colunas) 
            if self.mapa[r][c] == 0 
            and (r, c) != tuple(self.pos_saida)
            and (r, c) != tuple(self.pos_jogador)
            and (r, c) != tuple(self.inimigo.posicao)
        ]
        if celulas_livres:
            self.vortex.posicao = random.choice(celulas_livres)

    def _acionar_vortex(self, tempo_atual):
        ganho = 7
        self.pontuacao_partida.adicionar(ganho)
        if self.gerenciador_textos:
            self.gerenciador_textos.adicionar(f"+{ganho}", self.pos_jogador[0], self.pos_jogador[1], (255, 215, 0))
        
        self._preparar_novo_labirinto(resetar_total=False)
        self.tempo_congelamento_inimigo = tempo_atual + 2000
        self.rastro_inimigo.clear()
        self.rastro_inimigo.add(tuple(self.inimigo.posicao))

    def processar_movimento(self, dx, dy, tempo_atual):
        if dx == 0 and dy == 0:
            return

        linhas_atuais, colunas_atuais = self._obter_dimensoes_atuais()
        nx, ny = self.pos_jogador[0] + dx, self.pos_jogador[1] + dy
        if not (0 <= nx < linhas_atuais and 0 <= ny < colunas_atuais and self.mapa[nx][ny] == 0):
            return

        self.pos_jogador = [nx, ny]
        self.ultimo_passo_jogador = tempo_atual

        if not self.jogo_iniciado:
            self.jogo_iniciado = True
            import pygame
            self.ultimo_movimento_ia = tempo_atual

        pos_tupla = tuple(self.pos_jogador)
        
        if pos_tupla in self.rastro_inimigo and self.pocao.ativa:
            ganho = 2
            self.pontuacao_partida.adicionar(ganho)
            if self.gerenciador_textos:
                self.gerenciador_textos.adicionar(f"+{ganho}", self.pos_jogador[0], self.pos_jogador[1], (0, 255, 255))
            self.rastro_inimigo.remove(pos_tupla)

        if self.pocao.posicao and pos_tupla == self.pocao.posicao:
            self.pocao.coletar()
            self.inventario_partida.adicionar_item(self.pocao)
            self.sincronizar_frascos()
            ganho = 3
            self.pontuacao_partida.adicionar(ganho)
            if self.gerenciador_textos:
                self.gerenciador_textos.adicionar(f"+{ganho}", self.pos_jogador[0], self.pos_jogador[1], (0, 255, 0))
            self.pocao.posicao = None

        if self.vortex.posicao and pos_tupla == self.vortex.posicao:
            self._acionar_vortex(tempo_atual)
            return

        if self.pocao.ativa and pos_tupla in self.rastro_inimigo:
            self.rastro_inimigo.remove(pos_tupla)

    def atualizar(self, tempo_atual):
        self.pocao.atualizar(tempo_atual)
        self._atualizar_ia(tempo_atual)
        self._verificar_condicoes_fim_jogo()

    def _atualizar_ia(self, tempo_atual):
        if self.jogo_iniciado and not self.vitoria and not self.derrota:
            if tempo_atual < self.tempo_congelamento_inimigo:
                return

            if tempo_atual - self.ultimo_movimento_ia > self.inimigo.tempo_movimento_ia:
                linhas_atuais, colunas_atuais = self._obter_dimensoes_atuais()
                self.inimigo.atualizar_caminho(self.pos_jogador, linhas_atuais, colunas_atuais, self.mapa)
                self.inimigo.mover()
                
                pos_inimigo_tup = tuple(self.inimigo.posicao)
                
                if self.vortex.posicao and pos_inimigo_tup == self.vortex.posicao:
                    self._preparar_novo_labirinto(resetar_total=False)
                    self.tempo_congelamento_inimigo = tempo_atual + 2000
                    self.rastro_inimigo.clear()
                    self.rastro_inimigo.add(tuple(self.inimigo.posicao))
                    return

                self.rastro_inimigo.add(pos_inimigo_tup)
                self.ultimo_movimento_ia = tempo_atual

    def _verificar_condicoes_fim_jogo(self):
        if tuple(self.pos_jogador) == self.pos_saida and not self.vitoria:
            self.vitoria = True
            self.pocao.ativa = False
            self.pocao.tempo_fim = 0
            
            self.pontuacao_partida.adicionar(self.nivel_atual)
            pontos_ganhos = self.pontuacao_partida.resgatar_pontos()
            self.pontuacao_geral.adicionar(pontos_ganhos)
            self.gerenciador_recorde.salvar_se_maior(self.obter_pontuacao_total(), self.nivel_atual)

        perdeu = False
        if self.pos_jogador == self.inimigo.posicao:
            perdeu = True

        if tuple(self.pos_jogador) in self.rastro_inimigo and not self.pocao.ativa:
            perdeu = True

        if perdeu and not self.derrota:
            self.derrota = True
            self.pocao.ativa = False
            self.pocao.tempo_fim = 0
            
            self.pontuacao_partida.esvaziar()
            penalidade = self.nivel_atual
            self.pontuacao_geral.subtrair(penalidade)
            
            self.indice_nivel = max(0, self.indice_nivel - 1)
            
            if self.gerenciador_textos:
                self.gerenciador_textos.adicionar(f"-{penalidade}", self.pos_jogador[0], self.pos_jogador[1], (255, 50, 50))

    def contar_total_itens(self):
        return self.inventario_geral.contar_total() + self.inventario_partida.contar_itens()

    def obter_pontuacao_total(self):
        return self.pontuacao_geral.valor + self.pontuacao_partida.pontos