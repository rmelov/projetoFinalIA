"""
Desenha a rota até a saída quando a poção está ativa. Antes, esta classe
tinha sua PRÓPRIA implementação de BFS (`_encontrar_caminho`), duplicando
`amplitude_grid`. Agora ela recebe o mesmo buscador (BuscaCaminho) usado
pelo perseguidor e pelo Laboratório de Busca — o projeto deixa de ter duas
implementações de busca em largura.
"""
from apresentacao.cena.caminho.desenhadorCaminho import DesenhadorCaminho
from apresentacao.cena.caminho.detectorOclusao import DetectorOclusao

COR_ROTA_VISIVEL = (0, 191, 255)
COR_ROTA_ATRAS_PAREDE = (50, 150, 255)


class RenderizadorRotaSaida:
    """Traça a rota mais curta até a saída, tracejada quando atrás de parede."""

    def __init__(self, conversor, buscador):
        self.conversor = conversor
        self._buscador = buscador

    def desenhar(self, tela, mapa, posicaoJogador, posicaoSaida, ativa=False):
        if not ativa or posicaoJogador is None or posicaoSaida is None:
            return

        resultado = self._buscador.encontrarRota(
            "amplitude", posicaoJogador, posicaoSaida, mapa, len(mapa), len(mapa[0]) if mapa else 0,
        )
        if not resultado.encontrado or len(resultado.rota) < 2:
            return

        pontos = [(self.conversor.centroDoTile(p.linha, p.coluna), p) for p in resultado.rota]

        for (p1, c1), (p2, c2) in zip(pontos, pontos[1:]):
            oclusao = DetectorOclusao.estaAtrasDeParede(mapa, c1.linha, c1.coluna, c2.linha, c2.coluna)
            if oclusao:
                DesenhadorCaminho.linhaTracejada(tela, COR_ROTA_ATRAS_PAREDE, p1, p2, largura=2)
            else:
                DesenhadorCaminho.linhaSolida(tela, COR_ROTA_VISIVEL, p1, p2, largura=3)
