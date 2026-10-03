"""O jogador: guarda apenas sua posição no grid."""
from dominio.mapa.coordenada import Coordenada


class Jogador:
    """Mantém e move a posição do jogador."""

    def __init__(self, posicaoInicial: Coordenada):
        self.posicao = posicaoInicial

    def mover(self, novaPosicao: Coordenada):
        self.posicao = novaPosicao
