"""Decide o desfecho da partida a cada instante, sem aplicar consequências
(quem aplica pontuação/recorde é a Partida)."""
from enum import Enum, auto


class DesfechoPartida(Enum):
    EM_ANDAMENTO = auto()
    VITORIA = auto()
    DERROTA = auto()


class ArbitroPartida:
    """Compara jogador, saída, inimigo e rastro para decidir o desfecho."""

    @staticmethod
    def avaliar(posicaoJogador, posicaoSaida, posicaoPerseguidor, rastroPerseguidor, pocaoAtiva) -> DesfechoPartida:
        if posicaoJogador == posicaoSaida:
            return DesfechoPartida.VITORIA

        if posicaoJogador == posicaoPerseguidor:
            return DesfechoPartida.DERROTA
        if posicaoJogador in rastroPerseguidor and not pocaoAtiva:
            return DesfechoPartida.DERROTA

        return DesfechoPartida.EM_ANDAMENTO
