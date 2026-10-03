"""Conversor entre coordenadas do mapa matricial e coordenadas isométricas de tela."""


class ConversorIsometrico:
    def __init__(self, larguraTile, alturaTile, deslocamentoX=500, deslocamentoY=100):
        self.larguraTile = larguraTile
        self.alturaTile = alturaTile
        self.deslocamentoX = deslocamentoX
        self.deslocamentoY = deslocamentoY

    def cartesianoParaIsometrico(self, linha, coluna):
        """Vértice superior da célula isométrica."""
        isoX = (coluna - linha) * (self.larguraTile // 2) + self.deslocamentoX
        isoY = (coluna + linha) * (self.alturaTile // 2) + self.deslocamentoY
        return isoX, isoY

    def centroDoTile(self, linha, coluna):
        isoX, isoY = self.cartesianoParaIsometrico(linha, coluna)
        return isoX, isoY + (self.alturaTile // 2)

    def calcularProfundidade(self, linha, coluna):
        """Ordem de renderização (painter's algorithm)."""
        return linha + coluna
