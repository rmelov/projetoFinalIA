"""Desenha um item (poção, vórtex ou saída) na posição isométrica correta."""
from apresentacao.recursos.fabricaSprites import FabricaSprites


class RenderizadorItens:
    """Só desenha — a aparência (animada ou estática) vem da FabricaSprites."""

    def __init__(self, tela, conversor, fabricaSprites: FabricaSprites = None):
        self.tela = tela
        self.conversor = conversor
        self._fabricaSprites = fabricaSprites or FabricaSprites()

    def desenharItem(self, item, tempoMs=0):
        if not getattr(item, "posicao", None):
            return
        linha, coluna = item.posicao
        centroX, centroY = self.conversor.centroDoTile(linha, coluna)
        imagem = self._fabricaSprites.obterVisual(getattr(item, "imagemPath", ""), tempoMs)
        if imagem:
            rect = imagem.get_rect(center=(centroX, centroY - 10))
            self.tela.blit(imagem, rect)

    def imagemDoItem(self, item):
        """Ícone estático de um item, para desenhar em painéis de HUD."""
        return self._fabricaSprites.obterVisual(getattr(item, "imagemPath", ""), tempoMs=0)
