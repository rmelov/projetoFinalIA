import pygame
from utilidades import config
from renderizacao.renderizadorFonte import criar_fonte
from renderizacao.renderizadorHud import RenderizadorHud
from renderizacao.renderizadorMiniMapa import RenderizadorMiniMapa
from renderizacao.renderizadorFarejo import RenderizadorFarejo
from renderizacao.subRenderizadores.renderizadorChao import RenderizadorChao
from renderizacao.subRenderizadores.renderizadorParedes import RenderizadorParedes
from renderizacao.subRenderizadores.renderizadorEntidades import RenderizadorEntidades

class RenderizadorIsometrico:
    def __init__(self, tela, conversor):
        self.tela = tela
        self.conversor = conversor
        self.fonte_principal = criar_fonte(config.TAMANHO_FONTE_PRINCIPAL)
        self.fonte_sub = criar_fonte(config.TAMANHO_FONTE_SUB)
        self.hud = RenderizadorHud(tela, self.fonte_principal, self.fonte_sub)
        
        self.largura_tela, self.altura_tela = tela.get_size()
        self.renderizador_minimapa = RenderizadorMiniMapa(self.largura_tela, self.altura_tela)
        self.renderizador_farejo = RenderizadorFarejo(conversor)
        
        self.renderizador_chao = RenderizadorChao(tela, conversor)
        self.renderizador_paredes = RenderizadorParedes(tela, conversor)
        self.renderizador_entidades = RenderizadorEntidades(tela, conversor)

    def desenhar_cena(self, linhas, colunas, mapa, pos_jog, pos_inimigo, saida_obj, rastro, pocao_ativa, renderizador_itens=None, item=None, vortex=None, tempo_atual=0, vitoria=False, gerenciador_textos=None, caminho_inimigo=None, inimigo_obj=None, tempo_congelamento_inimigo=0):
        self.tela.fill((25, 25, 30))
        px, py = pos_jog[0], pos_jog[1]
        elementos = []

        for r in range(linhas):
            for c in range(colunas):
                iso_x, iso_y = self.conversor.cartesiano_para_isometrico(r, c)
                profundidade = self.conversor.calcular_profundidade(r, c)

                # 1. Chão
                elementos.append((profundidade, 0, "chao", r, c, iso_x, iso_y, ((r, c) in rastro, saida_obj)))

                # 2. Itens no chão
                if item and hasattr(item, "posicao") and item.posicao and tuple(item.posicao) == (r, c):
                    elementos.append((profundidade, 1, "item", r, c, iso_x, iso_y, item))

                if vortex and hasattr(vortex, "posicao") and vortex.posicao and tuple(vortex.posicao) == (r, c):
                    elementos.append((profundidade, 1, "item", r, c, iso_x, iso_y, vortex))

                if saida_obj and hasattr(saida_obj, "posicao") and saida_obj.posicao and tuple(saida_obj.posicao) == (r, c):
                    elementos.append((profundidade, 1, "item", r, c, iso_x, iso_y, saida_obj))

                # 3. Paredes
                if mapa[r][c] == 9:
                    dentro_raio = abs(r - px) <= 2 and abs(c - py) <= 2
                    obstrui = (r >= px and c >= py) and (r > px or c > py)
                    elementos.append((profundidade, 2, "parede", r, c, iso_x, iso_y, dentro_raio and obstrui))

                # 4. Jogador e Inimigo
                if [r, c] == list(pos_jog) and not vitoria:
                    elementos.append((profundidade, 3, "jogador", r, c, iso_x, iso_y, pocao_ativa))

                if [r, c] == list(pos_inimigo):
                    elementos.append((profundidade, 3, "inimigo", r, c, iso_x, iso_y, None))

        elementos.sort(key=lambda elem: (elem[0], elem[1]))

        for elem in elementos:
            _, _, tipo, r, c, iso_x, iso_y, dados = elem
            
            if tipo == "chao":
                eh_rastro, s_obj = dados
                self.renderizador_chao.desenhar(iso_x, iso_y, r, c, eh_rastro, s_obj)
            elif tipo == "item" and renderizador_itens:
                renderizador_itens.desenhar_item(dados, tempo_atual)
            elif tipo == "parede":
                self.renderizador_paredes.desenhar(iso_x, iso_y, dados)
            elif tipo in ("jogador", "inimigo"):
                self.renderizador_entidades.desenhar(r, c, tipo, dados)

        caminho_para_desenhar = caminho_inimigo
        if not caminho_para_desenhar and inimigo_obj:
            if hasattr(inimigo_obj, "caminho_atual"):
                caminho_para_desenhar = inimigo_obj.caminho_atual
            elif hasattr(inimigo_obj, "caminho"):
                caminho_para_desenhar = inimigo_obj.caminho

        if caminho_para_desenhar:
            self.renderizador_farejo.desenhar(self.tela, caminho_para_desenhar, tempo_atual, tempo_congelamento_inimigo, mapa, pos_jog)

        if gerenciador_textos:
            gerenciador_textos.atualizar_e_desenhar(self.tela, self.fonte_sub)

        self.renderizador_minimapa.desenhar(self.tela, mapa)

    def desenhar_interface(self, largura_tela, altura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual, frascos, vitoria, derrota, total_itens=0, renderizador_itens=None, item_exemplo=None, pontuacao_total=0, nivel_atual=1, gerenciador_recorde=None, texto_origem="", texto_destino="", campo_ativo=None):
        self.hud.desenhar(
            largura_tela, altura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, 
            tempo_atual, vitoria, derrota, total_itens, renderizador_itens, 
            item_exemplo, pontuacao_total, nivel_atual, gerenciador_recorde,
            texto_origem=texto_origem, texto_destino=texto_destino, campo_ativo=campo_ativo
        )