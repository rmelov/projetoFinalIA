"""Cada elemento da cena sabe sua profundidade e como desenhar a si mesmo;
ordenar por profundidade é o painter's algorithm da cena isométrica."""
from dataclasses import dataclass
from typing import Callable


@dataclass
class ElementoCena:
    profundidade: int
    camada: int
    desenhar: Callable[[], None]


def ordenarEDesenhar(elementos):
    for elemento in sorted(elementos, key=lambda e: (e.profundidade, e.camada)):
        elemento.desenhar()
