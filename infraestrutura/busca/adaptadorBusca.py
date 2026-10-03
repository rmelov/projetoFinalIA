"""
Único ponto do projeto que importa algoritmos/busca/buscaNP.py e
algoritmos/busca/BuscaP.py. Implementa aplicacao.portaBuscaCaminho.BuscaCaminho.

Uma particularidade do pacote original é tratada aqui, e só aqui:
algoritmos/busca/BuscaP.py importa com `from NodeP import NodeP` (import
"nu", sem prefixo de pacote), porque foi escrito para ser executado a
partir de dentro da própria pasta algoritmos/busca. Para importá-lo como
parte do projeto sem editar essa linha, este módulo acrescenta a pasta
algoritmos/busca ao sys.path antes de importar.
"""
import io
import os
import sys
import time
from contextlib import redirect_stdout

from aplicacao.metodosBusca import obterMetodo
from aplicacao.resultadoBusca import ResultadoBusca
from dominio.mapa.coordenada import coordenadaDeIteravel

from algoritmos.busca.buscaNP import buscaNP

_DIRETORIO_RAIZ = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_DIRETORIO_BUSCA_PONDERADA = os.path.join(_DIRETORIO_RAIZ, "algoritmos", "busca")
if _DIRETORIO_BUSCA_PONDERADA not in sys.path:
    # Necessário só por causa do import "nu" dentro de BuscaP.py (ver docstring acima).
    sys.path.insert(0, _DIRETORIO_BUSCA_PONDERADA)

from BuscaP import buscaP  # noqa: E402  (import tardio, proposital)


class AdaptadorBusca:
    """Traduz um pedido de rota para a chamada correta em buscaNP ou BuscaP."""

    def __init__(self):
        self._buscaNaoPonderada = buscaNP()
        self._buscaPonderada = buscaP()

    def encontrarRota(self, metodoId, origem, destino, mapa, linhas, colunas, limite=None) -> ResultadoBusca:
        metodo = obterMetodo(metodoId)
        instancia = self._buscaPonderada if metodo.ponderado else self._buscaNaoPonderada

        inicioCronometro = time.perf_counter()
        with redirect_stdout(io.StringIO()):
            resultadoBruto = metodo.chamador(instancia, origem, destino, mapa, linhas, colunas, limite)
        duracaoMs = (time.perf_counter() - inicioCronometro) * 1000.0

        rota, custo = self._interpretarResultadoBruto(resultadoBruto, metodo.ponderado)

        if not rota:
            return ResultadoBusca(
                metodoId=metodoId, encontrado=False, rota=[], custo=None,
                duracaoMs=duracaoMs, observacao="Caminho não encontrado.",
            )

        rotaCoordenadas = [coordenadaDeIteravel(passo) for passo in rota]

        if not self._rotaEhContinua(rotaCoordenadas, origem, destino, mapa):
            return ResultadoBusca(
                metodoId=metodoId, encontrado=False, rota=[], custo=None,
                duracaoMs=duracaoMs,
                observacao="O método devolveu uma rota inconsistente e foi descartado.",
            )

        if custo is None:
            custo = len(rotaCoordenadas) - 1

        return ResultadoBusca(
            metodoId=metodoId, encontrado=True, rota=rotaCoordenadas,
            custo=custo, duracaoMs=duracaoMs,
        )

    @staticmethod
    def _interpretarResultadoBruto(resultadoBruto, ponderado):
        if resultadoBruto is None:
            return None, None
        if ponderado:
            rota, custo = resultadoBruto
            return rota, custo
        return resultadoBruto, None

    @staticmethod
    def _rotaEhContinua(rota, origem, destino, mapa):
        origem = tuple(origem)
        destino = tuple(destino)
        if not rota or tuple(rota[0]) != origem or tuple(rota[-1]) != destino:
            return False
        for passo in rota:
            if mapa[passo.linha][passo.coluna] != 0:
                return False
        for anterior, atual in zip(rota, rota[1:]):
            if not anterior.ehAdjacente(atual):
                return False
        return True
