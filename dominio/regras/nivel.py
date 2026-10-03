"""Progressão de nível: quanto vale e qual o tamanho do grid em cada um."""

TAMANHO_GRID_BASE = 15
TAMANHO_GRID_MAXIMO = 25


class Nivel:
    """Calcula o valor (pontos) e o tamanho do grid de cada nível."""

    def __init__(self):
        self._cacheFibonacci = [1, 2, 3]

    def _obterFibonacci(self, n: int) -> int:
        while len(self._cacheFibonacci) <= n:
            proximo = self._cacheFibonacci[-1] + self._cacheFibonacci[-2]
            self._cacheFibonacci.append(proximo)
        return self._cacheFibonacci[n]

    def obterValorNivel(self, indiceNivel: int) -> int:
        return self._obterFibonacci(max(0, indiceNivel))

    def calcularTamanhoGrid(self, indiceNivel: int) -> int:
        """A cada dois níveis, soma +2 no tamanho do grid base."""
        aumento = (indiceNivel // 2) * 2
        tamanho = TAMANHO_GRID_BASE + aumento
        return min(tamanho, TAMANHO_GRID_MAXIMO)
