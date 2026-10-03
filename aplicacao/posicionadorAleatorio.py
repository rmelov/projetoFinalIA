"""Sorteia uma célula livre de um labirinto, excluindo posições ocupadas.
Uma única implementação para todos os itens — antes, a mesma lógica estava
duplicada entre PocaoCoragem.nascer e EstadoJogo.posicionar_vortex."""
import random

from dominio.mapa.labirinto import Labirinto


class PosicionadorAleatorio:
    """Sorteia uma célula livre do labirinto, fora de um conjunto de exclusões."""

    def __init__(self, gerador=random):
        self._gerador = gerador

    def sortearCelulaLivre(self, labirinto: Labirinto, excluindo=frozenset()):
        candidatas = labirinto.celulasLivres(excluindo=excluindo)
        if not candidatas:
            return None
        return self._gerador.choice(candidatas)
