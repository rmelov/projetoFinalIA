"""Uma fase montada e pronta para ser jogada."""
from dataclasses import dataclass

from dominio.mapa.coordenada import Coordenada
from dominio.mapa.labirinto import Labirinto


@dataclass(frozen=True)
class Fase:
    labirinto: Labirinto
    posicaoJogador: Coordenada
    posicaoPerseguidor: Coordenada
    posicaoSaida: Coordenada
