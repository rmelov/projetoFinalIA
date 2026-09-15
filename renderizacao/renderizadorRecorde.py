class RenderizadorRecorde:
    """Responsável por renderizar o recorde salvo no canto inferior esquerdo da tela."""
    
    def __init__(self, fonte):
        self.fonte = fonte

    def desenhar(self, tela, gerenciador_recorde, altura_tela):
        if not gerenciador_recorde:
            return
            
        pontuacao_max, nivel_max = gerenciador_recorde.carregar()
        texto_recorde = f"recorde: nível {nivel_max} | {pontuacao_max}pts"
        
        superficie_texto = self.fonte.render(texto_recorde, True, (150, 150, 150))
        
        x = 15
        y = altura_tela - superficie_texto.get_height() - 15
        
        tela.blit(superficie_texto, (x, y))