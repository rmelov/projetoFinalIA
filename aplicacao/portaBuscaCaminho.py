"""Contrato que a aplicação e a apresentação usam para pedir uma rota, sem
conhecer qual pacote de busca resolve o pedido (Inversão de Dependência).
A única implementação real está em infraestrutura/busca/adaptadorBusca.py."""
from typing import Protocol

from dominio.mapa.coordenada import Coordenada
from aplicacao.resultadoBusca import ResultadoBusca


class BuscaCaminho(Protocol):
    """Algo capaz de encontrar uma rota entre duas coordenadas de um grid."""

    def encontrarRota(
        self, metodoId: str, origem: Coordenada, destino: Coordenada,
        mapa, linhas: int, colunas: int, limite=None,
    ) -> ResultadoBusca:
        ...
