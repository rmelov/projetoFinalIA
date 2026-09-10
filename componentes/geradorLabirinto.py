import random
from collections import deque

def gerar_labirinto_base(linhas, colunas):
    """
    Gera um labirinto em grid 0 (caminho) e 9 (parede).
    - Converte números pares para ímpares automaticamente somando 1.
    - Mantém rigorosamente no máximo 2 caminhos alternativos (poucos loops), 
      independente do tamanho do grid.
    """
    if linhas % 2 == 0:
        linhas += 1
    if colunas % 2 == 0:
        colunas += 1

    mapa = [[9 for _ in range(colunas)] for _ in range(linhas)]

    pilha = [(1, 1)]
    mapa[1][1] = 0

    def obter_vizinhos_validos(r, c):
        vizinhos = []
        direcoes = [(-2, 0), (2, 0), (0, -2), (0, 2)]
        for dr, dc in direcoes:
            nr, nc = r + dr, c + dc
            if 0 < nr < linhas - 1 and 0 < nc < colunas - 1:
                if mapa[nr][nc] == 9:
                    vizinhos.append((nr, nc, dr, dc))
        return vizinhos

    while pilha:
        r, c = pilha[-1]
        vizinhos = obter_vizinhos_validos(r, c)
        
        if vizinhos:
            nr, nc, dr, dc = random.choice(vizinhos)
            mapa[r + dr // 2][c + dc // 2] = 0
            mapa[nr][nc] = 0
            pilha.append((nr, nc))
        else:
            pilha.pop()

    pos_jogador = (1, 1)
    pos_perseguidor = (1, colunas - 2 if (colunas - 2) % 2 != 0 else colunas - 3)
    pos_saida = (linhas - 2 if (linhas - 2) % 2 != 0 else linhas - 3, 
                 colunas - 2 if (colunas - 2) % 2 != 0 else colunas - 3)

    mapa[pos_jogador[0]][pos_jogador[1]] = 0
    mapa[pos_perseguidor[0]][pos_perseguidor[1]] = 0
    mapa[pos_saida[0]][pos_saida[1]] = 0

    paredes_removiveis = []
    for r in range(1, linhas - 1):
        for c in range(1, colunas - 1):
            if mapa[r][c] == 9:
                caminhos_h = (mapa[r][c - 1] == 0 and mapa[r][c + 1] == 0)
                caminhos_v = (mapa[r - 1][c] == 0 and mapa[r + 1][c] == 0)
                if caminhos_h or caminhos_v:
                    paredes_removiveis.append((r, c))

    qtd_conexoes_extras = min(2, len(paredes_removiveis))
    if paredes_removiveis and qtd_conexoes_extras > 0:
        for r, c in random.sample(paredes_removiveis, qtd_conexoes_extras):
            mapa[r][c] = 0

    return mapa, pos_jogador, pos_perseguidor, pos_saida