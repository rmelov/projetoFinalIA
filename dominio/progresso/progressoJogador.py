"""Agrega o progresso consolidado (entre fases) e o da partida em curso."""
from dominio.progresso.mochila import Mochila
from dominio.progresso.placar import Placar


class ProgressoJogador:
    """Mantém placar/mochila geral e os da partida, e sabe consolidar ou
    descartar a partida atual."""

    def __init__(self):
        self.placarGeral = Placar()
        self.placarPartida = Placar()
        self.mochilaGeral = Mochila()
        self.mochilaPartida = Mochila()

    @property
    def totalPontos(self) -> int:
        return self.placarGeral.total + self.placarPartida.total

    @property
    def totalItens(self) -> int:
        return self.mochilaGeral.totalItens + self.mochilaPartida.totalItens

    def consolidarPartida(self):
        """Move os pontos e itens da partida para o progresso geral (ex.: ao avançar de fase)."""
        itensGanhos = self.mochilaPartida.esvaziarDevolvendo()
        self.mochilaGeral.adicionarLote(itensGanhos)
        pontosGanhos = self.placarPartida.total
        self.placarPartida.zerar()
        self.placarGeral.adicionar(pontosGanhos)

    def descartarPartida(self, penalidade: int):
        """Zera os pontos da partida e aplica uma penalidade ao progresso geral (ao perder)."""
        self.placarPartida.zerar()
        self.placarGeral.subtrair(penalidade)

    def zerarPartida(self):
        self.placarPartida.zerar()
        self.mochilaPartida.zerar()
