from utilidades.animadorSprite import AnimadorSprite

class Vortex:
    def __init__(self):
        self.posicao = None
        self.imagem_path = "assets/imgs/CodeManu/13_vortex_spritesheet.png"
        self.ativo = True
        
        self.animador = AnimadorSprite(
            caminho_imagem=self.imagem_path,
            largura_frame=100,
            altura_frame=100,
            colunas_grid=8,
            total_frames=61,
            velocidade_animacao=60,
            tamanho_render=(128, 128)
        )