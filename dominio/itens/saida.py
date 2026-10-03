"""Saída do labirinto: apenas posição. A silhueta preta do sprite (antes
gerada com pygame.mask dentro do construtor) foi extraída para
apresentacao/recursos/fabricaSprites.py."""

IMAGEM_PADRAO = "assets/imgs/CodeManu/16_sunburn_spritesheet.png"


class Saida:
    """Marca a célula que o jogador precisa alcançar para vencer a fase."""

    def __init__(self):
        self.posicao = None
        self.imagemPath = IMAGEM_PADRAO
