import pygame
from utilidades import config
from renderizacao.renderizadorFonte import criar_fonte
from renderizacao.renderizadorHud import RenderizadorHud

COR_CHAO = (160, 160, 160)
COR_PAREDE_TOPO = (120, 120, 140)
COR_PAREDE_ESQ = (80, 80, 100)
COR_PAREDE_DIR = (50, 50, 70)
COR_RASTRO = (220, 50, 50, 150)
COR_JOGADOR = (50, 220, 50)
COR_JOGADOR_POCAO = (0, 255, 255)
COR_INIMIGO = (220, 50, 50)
COR_SAIDA = (255, 215, 0)

ALTURA_PAREDE_CHEIA = 28
ALTURA_PAREDE_BAIXA = 6


class RenderizadorIsometrico:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor
        self.fonte_principal = criar_fonte(config.TAMANHO_FONTE_PRINCIPAL)
        self.fonte_sub = criar_fonte(config.TAMANHO_FONTE_SUB)
        self.hud = RenderizadorHud(tela, self.fonte_principal, self.fonte_sub)

    def desenhar_chao(self, iso_x, iso_y, cor=COR_CHAO):
        larg = self.conversor.largura_tile
        alt = self.conversor.altura_tile

        if len(cor) == 4:
            superficie_temp = pygame.Surface((larg, alt), pygame.SRCALPHA)
            pontos_locais = [(larg // 2, 0), (larg, alt // 2), (larg // 2, alt), (0, alt // 2)]
            pygame.draw.polygon(superficie_temp, cor, pontos_locais)
            pygame.draw.polygon(superficie_temp, (100, 100, 100, 150), pontos_locais, 1)
            self.tela.blit(superficie_temp, (iso_x - larg // 2, iso_y))
        else:
            pontos = [(iso_x, iso_y), (iso_x + larg // 2, iso_y + alt // 2), (iso_x, iso_y + alt), (iso_x - larg // 2, iso_y + alt // 2)]
            pygame.draw.polygon(self.tela, cor, pontos)
            pygame.draw.polygon(self.tela, (100, 100, 100), pontos, 1)

    def desenhar_parede(self, iso_x, iso_y, altura_bloco):
        x, y = iso_x, iso_y
        larg = self.conversor.largura_tile
        alt = self.conversor.altura_tile
        w_2, h_2 = larg // 2, alt // 2

        topo = [(x, y - altura_bloco), (x + w_2, y + h_2 - altura_bloco), (x, y + alt - altura_bloco), (x - w_2, y + h_2 - altura_bloco)]
        esquerda = [(x - w_2, y + h_2 - altura_bloco), (x, y + alt - altura_bloco), (x, y + alt), (x - w_2, y + h_2)]
        direita = [(x, y + alt - altura_bloco), (x + w_2, y + h_2 - altura_bloco), (x + w_2, y + h_2), (x, y + alt)]

        pygame.draw.polygon(self.tela, COR_PAREDE_ESQ, esquerda)
        pygame.draw.polygon(self.tela, COR_PAREDE_DIR, direita)
        pygame.draw.polygon(self.tela, COR_PAREDE_TOPO, topo)

        pygame.draw.polygon(self.tela, (20, 20, 20), topo, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), esquerda, 1)
        pygame.draw.polygon(self.tela, (20, 20, 20), direita, 1)

    def desenhar_entidade(self, centro_x, centro_y, cor):
        raio = 10
        pygame.draw.ellipse(self.tela, (30, 30, 30), (centro_x - raio, centro_y - 5, raio * 2, 10))
        pygame.draw.circle(self.tela, cor, (centro_x, centro_y - 8), raio)
        pygame.draw.circle(self.tela, (0, 0, 0), (centro_x, centro_y - 8), raio, 1)

    def desenhar_cena(self, linhas, colunas, mapa, pos_jog, pos_inimigo, pos_saida, rastro, pocao_ativa, renderizador_itens=None, item=None):
        self.tela.fill((25, 25, 30))
        px, py = pos_jog[0], pos_jog[1]
        elementos = []

        for r in range(linhas):
            for c in range(colunas):
                iso_x, iso_y = self.conversor.cartesiano_para_isometrico(r, c)
                profundidade = self.conversor.calcular_profundidade(r, c)

                if (r, c) == tuple(pos_saida):
                    cor_chao = COR_SAIDA
                elif (r, c) in rastro:
                    cor_chao = COR_RASTRO
                else:
                    cor_chao = COR_CHAO

                elementos.append((profundidade, 0, "chao", r, c, iso_x, iso_y, cor_chao))

                if item and hasattr(item, "posicao") and item.posicao and tuple(item.posicao) == (r, c):
                    elementos.append((profundidade, 1, "item", r, c, iso_x, iso_y, item))

                if mapa[r][c] == 9:
                    dentro_raio = abs(r - px) <= 2 and abs(c - py) <= 2
                    obstrui = (r >= px and c >= py) and (r > px or c > py)
                    altura = ALTURA_PAREDE_BAIXA if (dentro_raio and obstrui) else ALTURA_PAREDE_CHEIA
                    elementos.append((profundidade, 2, "parede", r, c, iso_x, iso_y, altura))

                if [r, c] == list(pos_jog):
                    cor = COR_JOGADOR_POCAO if pocao_ativa else COR_JOGADOR
                    elementos.append((profundidade, 3, "jogador", r, c, iso_x, iso_y, cor))

                if [r, c] == list(pos_inimigo):
                    elementos.append((profundidade, 3, "inimigo", r, c, iso_x, iso_y, COR_INIMIGO))

        elementos.sort(key=lambda item: (item[0], item[1]))

        for elem in elementos:
            _, _, tipo, r, c, iso_x, iso_y, dados = elem
            cx, cy = self.conversor.centro_do_tile(r, c)

            if tipo == "chao":
                self.desenhar_chao(iso_x, iso_y, dados)
            elif tipo == "item" and renderizador_itens:
                renderizador_itens.desenhar_item(dados)
            elif tipo == "parede":
                self.desenhar_parede(iso_x, iso_y, dados)
            elif tipo == "jogador":
                self.desenhar_entidade(cx, cy, dados)
            elif tipo == "inimigo":
                self.desenhar_entidade(cx, cy, dados)

    def desenhar_interface(self, largura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual, frascos, vitoria, derrota, total_itens=0, renderizador_itens=None, item_exemplo=None):
        self.hud.desenhar(largura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual, vitoria, derrota, total_itens, renderizador_itens, item_exemplo)