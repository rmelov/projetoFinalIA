from algoritmos.busca.BuscaNP import BuscaNP

class Perseguidor:
    def __init__(self, pos_inicial):
        self.posicao = list(pos_inicial)
        self.buscador = BuscaNP()
        self.caminho_atual = []

    def atualizar_caminho(self, posicao_jogador, nx, ny, mapa):
        """Recalcula a rota até o jogador usando Busca em Amplitude no Grid."""
        resultado = self.buscador.amplitude_grid(
            self.posicao, 
            posicao_jogador, 
            nx, 
            ny, 
            mapa
        )
        if resultado and len(resultado) > 1:
            self.caminho_atual = resultado[1:]

    def mover(self):
        """Avança um passo ao longo do caminho calculado."""
        if self.caminho_atual:
            self.posicao = list(self.caminho_atual.pop(0))