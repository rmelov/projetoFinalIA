"""Substitui as antigas Pontuacao e PontuacaoPartida, que tinham corpos
quase idênticos com nomes de método diferentes. Comando/consulta separados:
`total` só lê, `adicionar`/`subtrair`/`zerar` só alteram — nenhum método
devolve e zera ao mesmo tempo (o antigo `resgatar_pontos()` fazia isso)."""


class Placar:
    """Acumula pontos. Uma única implementação para o placar geral e o da partida."""

    def __init__(self, valorInicial=0):
        self._valor = valorInicial

    @property
    def total(self) -> int:
        return self._valor

    def adicionar(self, quantidade: int):
        self._valor += quantidade

    def subtrair(self, quantidade: int):
        self._valor -= quantidade

    def zerar(self):
        self._valor = 0
