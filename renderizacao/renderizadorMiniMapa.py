from componentes.miniMapa import MiniMapa
from utilidades import config

class RenderizadorMiniMapa:
    def __init__(self, largura_tela, altura_tela):
        self.mini_mapa = MiniMapa(largura_tela, altura_tela)

    def desenhar(self, tela, mapa):
        self.mini_mapa.desenhar(tela, mapa)