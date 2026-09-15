from algoritmos.busca.BuscaNP import BuscaNP
from utilidades import config

class Perseguidor:
    def __init__(self, pos_inicial):
        self.posicao = list(pos_inicial)
        self.buscador = BuscaNP()
        self.caminho_atual = []
        self.tempo_movimento_ia = config.TEMPO_MOVIMENTO_IA

    def ajustar_velocidade(self, nivel_index):
        """A cada nível ganho diminui 20ms, a cada perdido aumenta 20ms. Limites: 30 a 300."""
        novo_tempo = config.TEMPO_MOVIMENTO_IA - (nivel_index * 20)
        self.tempo_movimento_ia = max(config.TEMPO_MOVIMENTO_IA_MAX, min(config.TEMPO_MOVIMENTO_IA, novo_tempo))

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

    @property
    def caminho(self):
        """Propriedade de compatibilidade para expor o caminho atual."""
        return self.caminho_atual