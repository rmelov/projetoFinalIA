from utilidades import config

class Nivel:
    def __init__(self):
        self._fibonacci_cache = [1, 2, 3]

    def _obter_fibonacci(self, n):
        while len(self._fibonacci_cache) <= n:
            prox = self._fibonacci_cache[-1] + self._fibonacci_cache[-2]
            self._fibonacci_cache.append(prox)
        return self._fibonacci_cache[n]

    def obter_valor_nivel(self, indice_nivel):
        if indice_nivel < 0:
            indice_nivel = 0
        return self._obter_fibonacci(indice_nivel)

    def calcular_tamanho_grid(self, indice_nivel):
        """A cada dois níveis, soma +2 no tamanho do grid base."""
        aumento = (indice_nivel // 2) * 2
        tamanho = config.TAMANHO_GRID + aumento
        return min(tamanho, config.TAMANHO_GRID_MAX)