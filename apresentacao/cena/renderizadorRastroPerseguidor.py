"""Desenha o rastro que o perseguidor deixa até o jogador."""
from apresentacao.cena.caminho.desenhadorCaminho import DesenhadorCaminho
from apresentacao.cena.caminho.detectorOclusao import DetectorOclusao

COR_RASTRO_VISIVEL = (255, 235, 59)
COR_RASTRO_ATRAS_PAREDE = (230, 160, 40)


class RenderizadorRastroPerseguidor:
    """Traça o caminho percorrido pelo perseguidor, tracejado quando atrás de parede."""

    def __init__(self, conversor):
        self.conversor = conversor

    def desenhar(self, tela, caminho, tempoMs, tempoCongelamentoMs, mapa):
        if tempoMs < tempoCongelamentoMs or not caminho or len(caminho) < 2:
            return

        pontos = [(self.conversor.centroDoTile(p.linha, p.coluna), p) for p in caminho]

        for (p1, c1), (p2, c2) in zip(pontos, pontos[1:]):
            oclusao = DetectorOclusao.estaAtrasDeParede(mapa, c1.linha, c1.coluna, c2.linha, c2.coluna)
            if oclusao:
                DesenhadorCaminho.linhaTracejada(tela, COR_RASTRO_ATRAS_PAREDE, p1, p2, largura=2)
            else:
                DesenhadorCaminho.linhaSolida(tela, COR_RASTRO_VISIVEL, p1, p2, largura=3)
