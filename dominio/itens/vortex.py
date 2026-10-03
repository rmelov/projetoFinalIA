"""Vórtex: apenas posição. A animação (sprite) é responsabilidade de
apresentacao/recursos/fabricaSprites.py."""

IMAGEM_PADRAO = "assets/imgs/CodeManu/13_vortex_spritesheet.png"


class Vortex:
    """Item que, ao ser tocado, embaralha o labirinto (regra em aplicacao/partida.py)."""

    def __init__(self):
        self.posicao = None
        self.imagemPath = IMAGEM_PADRAO
