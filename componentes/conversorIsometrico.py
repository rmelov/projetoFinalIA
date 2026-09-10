class ConversorIsometrico:
    """
    Conversor entre coordenadas do mapa matricial e coordenadas isométricas de tela.
    """

    def __init__(
        self,
        largura_tile,
        altura_tile,
        deslocamento_x=500,
        deslocamento_y=100
    ):
        self.largura_tile = largura_tile
        self.altura_tile = altura_tile
        self.deslocamento_x = deslocamento_x
        self.deslocamento_y = deslocamento_y

    def cartesiano_para_isometrico(self, x, y):
        """Retorna o topo superior (vértice superior) da célula isométrica."""
        iso_x = (x - y) * (self.largura_tile // 2) + self.deslocamento_x
        iso_y = (x + y) * (self.altura_tile // 2) + self.deslocamento_y
        return iso_x, iso_y

    def centro_do_tile(self, x, y):
        """Retorna o ponto central da tile (onde entidades devem ser posicionadas)."""
        iso_x, iso_y = self.cartesiano_para_isometrico(x, y)
        return iso_x, iso_y + (self.altura_tile // 2)

    def calcular_profundidade(self, x, y):
        """Calcula a ordem de renderização (painter's algorithm)."""
        return x + y