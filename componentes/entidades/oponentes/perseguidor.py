from algoritmos.busca.buscaNP import buscaNP
from utilidades.adaptadorBusca import AdaptadorBusca
from utilidades import config

class Perseguidor:
    def __init__(self, pos_inicial, modo="amplitude"):
        self.posicao = list(pos_inicial)
        self.buscador = buscaNP()
        self.adaptador = AdaptadorBusca()
        self.caminho_atual = []
        self.tempo_movimento_ia = config.TEMPO_MOVIMENTO_IA
        self.modo = modo

    def ajustar_velocidade(self, nivel_index):
        """A cada nível ganho diminui 20ms, a cada perdido aumenta 20ms. Limites: 30 a 300."""
        novo_tempo = config.TEMPO_MOVIMENTO_IA - (nivel_index * 20)
        self.tempo_movimento_ia = max(config.TEMPO_MOVIMENTO_IA_MAX, min(config.TEMPO_MOVIMENTO_IA, novo_tempo))

    def atualizar_caminho(self, posicao_jogador, nx, ny, mapa):
        """Recalcula a rota até o jogador usando o algoritmo correspondente ao modo escolhido."""
        origem = list(self.posicao)
        destino = list(posicao_jogador)

        resultado = None
        try:
            resultado = self.adaptador.encontrar_rota(self.modo, origem, destino, mapa, nx, ny)
        except Exception:
            resultado = None

        if resultado is None:
            resultado = self.buscador.amplitude_grid(origem, destino, nx, ny, mapa)

        if isinstance(resultado, tuple):
            rota = resultado[0] if resultado and resultado[0] else []
        else:
            rota = resultado or []

        if len(rota) <= 1:
            rota = self.buscador.amplitude_grid(origem, destino, nx, ny, mapa) or []

        if isinstance(rota, tuple):
            rota = rota[0] if rota else []

        if len(rota) > 1:
            self.caminho_atual = rota[1:]
        else:
            self.caminho_atual = []

    def mover(self):
        """Avança um passo ao longo do caminho calculado."""
        if self.caminho_atual:
            self.posicao = list(self.caminho_atual.pop(0))

    @property
    def caminho(self):
        """Propriedade de compatibilidade para expor o caminho atual."""
        return self.caminho_atual