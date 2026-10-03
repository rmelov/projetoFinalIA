"""As intenções que uma tecla pode expressar durante a partida."""
from enum import Enum, auto


class Acao(Enum):
    VOLTAR_MENU = auto()
    PROXIMO_LABIRINTO = auto()
    REINICIAR_APOS_DERROTA = auto()
    REINICIAR_TOTAL = auto()
    USAR_POCAO = auto()
