"""Monta uma Fase pronta para ser jogada."""
from aplicacao.fase import Fase
from dominio.mapa.labirinto import GeradorLabirinto


class PreparadorFase:
    """Gera um labirinto novo com posições iniciais de jogador, perseguidor e saída."""

    @staticmethod
    def montar(linhas: int, colunas: int) -> Fase:
        labirinto, posicaoJogador, posicaoPerseguidor, posicaoSaida = GeradorLabirinto.gerar(linhas, colunas)
        return Fase(
            labirinto=labirinto,
            posicaoJogador=posicaoJogador,
            posicaoPerseguidor=posicaoPerseguidor,
            posicaoSaida=posicaoSaida,
        )
