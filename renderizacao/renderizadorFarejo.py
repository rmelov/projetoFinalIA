import pygame

class RenderizadorFarejo:
    """Responsável por renderizar o rastro/caminho que o inimigo faz até o jogador em isométrico."""
    
    def __init__(self, conversor):
        self.conversor = conversor

    def desenhar(self, tela, caminho, tempo_atual=0, tempo_congelamento=0, mapa=None, pos_jogador=None):
        if tempo_atual < tempo_congelamento:
            return

        if not caminho or len(caminho) < 2:
            return

        pontos_iso = []
        for pos in caminho:
            if isinstance(pos, (list, tuple)) and len(pos) >= 2:
                r, c = pos[0], pos[1]
            elif hasattr(pos, 'r') and hasattr(pos, 'c'):
                r, c = pos.r, pos.c
            else:
                continue

            iso_x, iso_y = self.conversor.centro_do_tile(r, c)
            pontos_iso.append((iso_x, iso_y, r, c))

        if len(pontos_iso) >= 2:
            px, py = pos_jogador if pos_jogador else (0, 0)
            
            for i in range(len(pontos_iso) - 1):
                p1_x, p1_y, r1, c1 = pontos_iso[i]
                p2_x, p2_y, r2, c2 = pontos_iso[i+1]

                atras_de_parede = False
                if mapa:
                    linhas_mapa = len(mapa)
                    colunas_mapa = len(mapa[0]) if linhas_mapa > 0 else 0
                    
                    tr_medio_r = (r1 + r2) // 2
                    tr_medio_c = (c1 + c2) // 2
                    
                    for dr in (-1, 0, 1):
                        for dc in (-1, 0, 1):
                            vr, vc = tr_medio_r + dr, tr_medio_c + dc
                            if 0 <= vr < linhas_mapa and 0 <= vc < colunas_mapa:
                                if mapa[vr][vc] == 9:
                                    if vr >= r1 and vc >= c1:
                                        atras_de_parede = True
                                        break
                        if atras_de_parede:
                            break

                if atras_de_parede:
                    self._desenhar_linha_tracejada(tela, (230, 160, 40), (p1_x, p1_y), (p2_x, p2_y), largura=2)
                else:
                    pygame.draw.line(tela, (255, 235, 59), (p1_x, p1_y), (p2_x, p2_y), 3)

    def _desenhar_linha_tracejada(self, tela, cor, p1, p2, largura=2, comprimento_traco=8):
        import math
        x1, y1 = p1
        x2, y2 = p2
        distancia = math.hypot(x2 - x1, y2 - y1)
        if distancia == 0:
            return
        
        dir_x = (x2 - x1) / distancia
        dir_y = (y2 - y1) / distancia
        
        atual = 0.0
        desenhar = True
        while atual < distancia:
            proximo = min(atual + comprimento_traco, distancia)
            px1 = x1 + dir_x * atual
            py1 = y1 + dir_y * atual
            px2 = x1 + dir_x * proximo
            py2 = y1 + dir_y * proximo
            
            if desenhar:
                pygame.draw.line(tela, cor, (int(px1), int(py1)), (int(px2), int(py2)), largura)
            
            atual = proximo
            desenhar = not desenhar