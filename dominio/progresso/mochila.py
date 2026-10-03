"""Substitui as antigas Inventario e InventarioPartida. `esvaziar()` e
`resgatar_itens()` tinham corpos idênticos no código original — viram um
só método aqui."""


class Mochila:
    """Guarda itens coletados. Uma única implementação para geral e partida."""

    def __init__(self):
        self._itens = []

    @property
    def totalItens(self) -> int:
        return len(self._itens)

    @property
    def itens(self):
        return list(self._itens)

    def adicionar(self, item):
        self._itens.append(item)

    def adicionarLote(self, itens):
        self._itens.extend(itens)

    def removerUltimo(self):
        if self._itens:
            return self._itens.pop()
        return None

    def zerar(self):
        self._itens.clear()

    def esvaziarDevolvendo(self):
        """Zera a mochila e devolve os itens que ela continha (usado ao
        consolidar os itens da partida na mochila geral)."""
        itens = list(self._itens)
        self._itens.clear()
        return itens
