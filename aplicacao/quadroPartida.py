"""Retrato imutável do que a tela precisa desenhar em um frame. Substitui os
17-18 parâmetros que antes eram passados soltos para desenhar_cena e
desenhar_interface."""
from dataclasses import dataclass


@dataclass(frozen=True)
class QuadroPartida:
    partida: object
    tempoMs: int


def montarQuadro(partida, tempoMs: int) -> QuadroPartida:
    return QuadroPartida(partida=partida, tempoMs=tempoMs)
