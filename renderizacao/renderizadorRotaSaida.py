import pygame
from collections import deque

class RenderizadorRotaSaida:
    """Responsável por calcular e renderizar a rota em azul até a saída quando a poção está ativa."""
    
    def __init__(self, conversor):
        self.conversor = conversor

    def _encontrar_caminho(self, mapa, inicio, fim):
        """Calcula o menor caminho (BFS) do jogador até a saída."""
        if not mapa or not inicio or not fim:
            return []
        
        linhas = len(mapa)
        colunas = len(mapa[0]) if linhas > 0 else 0
        
        if not (0 <= inicio[0] < linhas and 0 <= inicio[1] < colunas):
            return []
        if not (0 <= fim[0] < linhas and 0 <= fim[1] < colunas):
            return []

        fila = deque([[inicio]])
        visitados = {inicio}
        
        while fila:
            caminho = fila.popleft()
            atual = caminho[-1]
            
            if atual == fim:
                return caminho
            
            r, c = atual
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                vr, vc = r + dr, c + dc
                if 0 <= vr < linhas and 0 <= vc < colunas:
                    if mapa[vr][vc] == 0 and (vr, vc) not in visitados:
                        visitados.add((vr, vc))
                        novo_caminho = list(caminho)
                        novo_caminho.append((vr, vc))
                        fila.append(novo_caminho)
        return []

    def desenhar(self, tela, mapa, pos_jogador, pos_saida, ativa=False):
        if not ativa or not pos_jogador or not pos_saida:
            return

        caminho = self._encontrar_caminho(mapa, tuple(pos_jogador), tuple(pos_saida))
        if not caminho or len(caminho) < 2:
            return

        pontos_iso = []
        for pos in caminho:
            r, c = pos[0], pos[1]
            iso_x, iso_y = self.conversor.centro_do_tile(r, c)
            pontos_iso.append((iso_x, iso_y, r, c))

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
                self._desenhar_linha_tracejada(tela, (50, 150, 255), (p1_x, p1_y), (p2_x, p2_y), largura=2)
            else:
                pygame.draw.line(tela, (0, 191, 255), (p1_x, p1_y), (p2_x, p2_y), 3)

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