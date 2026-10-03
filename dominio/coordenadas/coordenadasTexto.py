"""Interpreta e valida coordenadas digitadas pelo jogador ("linha,coluna").
Extraído de dentro de EstadoJogo (era responsabilidade de entrada de UI
misturada com estado de jogo)."""
import re
from typing import NamedTuple, Optional

from dominio.mapa.coordenada import Coordenada


class ParserCoordenada:
    """Converte texto livre em Coordenada, ou None se não for reconhecível."""

    @staticmethod
    def converter(texto: str) -> Optional[Coordenada]:
        texto = str(texto or "").strip()
        if not texto:
            return None
        numeros = re.findall(r"-?\d+", texto)
        if len(numeros) < 2:
            return None
        return Coordenada(int(numeros[0]), int(numeros[1]))


class ResultadoValidacao(NamedTuple):
    valida: bool
    mensagemErro: str


class ValidadorCoordenada:
    """Diz se uma coordenada digitada cabe num grid linhas x colunas e não
    coincide com a outra. Recebe as dimensões, não um Labirinto inteiro —
    validar limites não exige conhecer o conteúdo do grid."""

    @staticmethod
    def validarPar(textoOrigem: str, textoDestino: str, linhas: int, colunas: int) -> ResultadoValidacao:
        origem = ParserCoordenada.converter(textoOrigem)
        destino = ParserCoordenada.converter(textoDestino)

        def dentroDosLimites(coordenada: Coordenada) -> bool:
            return 0 <= coordenada.linha < linhas and 0 <= coordenada.coluna < colunas

        if textoOrigem and textoOrigem.strip() and origem is None:
            return ResultadoValidacao(False, "Origem inválida. Use o formato (linha,coluna).")
        if textoDestino and textoDestino.strip() and destino is None:
            return ResultadoValidacao(False, "Destino inválido. Use o formato (linha,coluna).")

        if origem is not None and not dentroDosLimites(origem):
            return ResultadoValidacao(False, f"Origem fora do grid ({linhas}x{colunas}).")
        if destino is not None and not dentroDosLimites(destino):
            return ResultadoValidacao(False, f"Destino fora do grid ({linhas}x{colunas}).")
        if origem is not None and destino is not None and origem == destino:
            return ResultadoValidacao(False, "Origem e destino não podem ser iguais.")

        return ResultadoValidacao(True, "")
