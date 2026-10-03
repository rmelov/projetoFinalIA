"""Objeto de valor imutável que representa uma célula do grid."""
from typing import NamedTuple


class Coordenada(NamedTuple):
    """Uma posição no grid, identificada por linha e coluna."""

    linha: int
    coluna: int

    def paraLista(self):
        """Devolve [linha, coluna] — formato aceito pelos algoritmos de busca."""
        return [self.linha, self.coluna]

    def ehAdjacente(self, outra: "Coordenada") -> bool:
        """Verdadeiro se `outra` está a exatamente um passo ortogonal daqui."""
        distancia = abs(self.linha - outra.linha) + abs(self.coluna - outra.coluna)
        return distancia == 1

    def __str__(self):
        return f"({self.linha},{self.coluna})"


def coordenadaDeIteravel(valores) -> Coordenada:
    """Converte [linha, coluna] ou (linha, coluna) em Coordenada."""
    return Coordenada(int(valores[0]), int(valores[1]))
