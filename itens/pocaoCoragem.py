import random

class PocaoCoragem:
    def __init__(self, quantidade_inicial=0):
        self.quantidade_inicial = quantidade_inicial
        self.frascos = self.quantidade_inicial
        self.ativa = False
        self.tempo_fim = 0
        self.duracao_ms = 10000
        self.posicao = None
        self.imagem_path = "assets/imgs/DailyDoodles/glass02blue.png"

    def nascer(self, mapa, linhas, colunas, pos_jogador, pos_saida, pos_inimigo):
        caminhos_livres = []
        for r in range(linhas):
            for c in range(colunas):
                coord = (r, c)
                if mapa[r][c] == 0 and coord != tuple(pos_jogador) and coord != tuple(pos_saida) and coord != tuple(pos_inimigo):
                    caminhos_livres.append(coord)

        if caminhos_livres:
            self.posicao = random.choice(caminhos_livres)
        else:
            self.posicao = None

    def usar(self, tempo_atual):
        if self.frascos > 0 and not self.ativa:
            self.frascos -= 1
            self.ativa = True
            self.tempo_fim = tempo_atual + self.duracao_ms
            return True
        return False

    def atualizar(self, tempo_atual):
        if self.ativa and tempo_atual > self.tempo_fim:
            self.ativa = False

    def coletar(self):
        self.frascos += 1