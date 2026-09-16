import pygame
from renderizacao.renderizadorRecorde import RenderizadorRecorde

class RenderizadorHud:
    """Responsável por desenhar elementos de interface (HUD, status e telas de fim de jogo)."""
    
    _PADDING_X = 15
    _PADDING_Y = 12
    _ESPAÇAMENTO_VERTICAL = 8

    def __init__(self, tela, fonte_principal, fonte_sub):
        self.tela = tela
        self.fonte_principal = fonte_principal
        self.fonte_sub = fonte_sub
        self.renderizador_recorde = RenderizadorRecorde(fonte_sub)

    def calcular_posicoes_campos(self, largura_tela, altura_tela, fonte_sub, padding_x, padding_y, espacamento_vertical):
        """Calcula e retorna as posições dos retângulos dos campos de entrada."""
        # Simular o cálculo do método desenhar para obter as posições
        y_slot = 0  # Vamos calcular step by step
        
        # Simulação das posições do HUD
        y_dica = padding_y + fonte_sub.get_height() + 6
        texto_nivel = fonte_sub.render(f"Nível: 1", True, (255, 200, 100))
        y_pontos = y_dica + texto_nivel.get_height() + 4
        texto_pontos = fonte_sub.render(f"Pontos: 0", True, (255, 215, 0))
        y_slot = y_pontos + texto_pontos.get_height() + espacamento_vertical
        
        y_origem = y_slot + 28 + espacamento_vertical
        texto_origem = fonte_sub.render("Célula de Origem:", True, (255, 255, 255))
        
        origem_rect = pygame.Rect(padding_x + texto_origem.get_width() + 10, y_origem + 4, 100, 28)
        
        y_destino = y_origem + texto_origem.get_height() + espacamento_vertical
        texto_destino = fonte_sub.render("Célula de Destino:", True, (255, 255, 255))
        
        destino_rect = pygame.Rect(padding_x + texto_destino.get_width() + 10, y_destino + 4, 100, 28)
        
        return {
            "origem": origem_rect,
            "destino": destino_rect
        }

    def desenhar_item_slot(self, renderizador_itens, item, quantidade, x, y):
        """Renderiza o ícone do item e o contador em formato limpo, sem fundo quadriculado."""
        if not (renderizador_itens and item):
            return

        img = renderizador_itens._carregar_imagem(getattr(item, "imagem_path", ""))
        altura_fonte = self.fonte_sub.get_height()
        
        altura_slot = max(28, altura_fonte)
        
        self.tela.blit(img, (x, y + (altura_slot - img.get_height()) // 2))
        
        texto_qtd = self.fonte_sub.render(f"x{quantidade}", True, (255, 255, 255))
        self.tela.blit(texto_qtd, (x + 34, y + (altura_slot - texto_qtd.get_height()) // 2))

    def desenhar_telas_fim(self, largura_tela, vitoria, derrota, pontuacao_total):
        """Desenha centralizada a tela de vitória ou derrota respeitando a largura da tela."""
        if not vitoria and not derrota:
            return

        texto_str = "VOCÊ VENCEU!" if vitoria else "VOCÊ PERDEU!"
        cor_txt = (100, 255, 100) if vitoria else (255, 100, 100)

        texto = self.fonte_principal.render(texto_str, True, cor_txt)
        subtexto_pontos = self.fonte_sub.render(f"Pontuação Total: {pontuacao_total}", True, (255, 255, 255))
        subtexto = self.fonte_sub.render("Pressione 'R' para reiniciar", True, (200, 200, 200))

        centro_x = largura_tela // 2
        self.tela.blit(texto, (centro_x - texto.get_width() // 2, 30))
        self.tela.blit(subtexto_pontos, (centro_x - subtexto_pontos.get_width() // 2, 30 + texto.get_height() + 10))
        self.tela.blit(subtexto, (centro_x - subtexto.get_width() // 2, 30 + texto.get_height() + subtexto_pontos.get_height() + 20))

    def _obter_texto_status(self, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual):
        """Retorna a string de status atual formatada de acordo com o estado do jogo."""
        if not jogo_iniciado:
            return "Movimente-se para iniciar..."
        if pocao_ativa:
            tempo_restante = max(0, (tempo_pocao_fim - tempo_atual) // 1000 + 1)
            return f"POÇÃO ATIVA ({tempo_restante}s)"
        return "Espaço para usar a poção"

    def desenhar(self, largura_tela, altura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual, vitoria, derrota, total_itens=0, renderizador_itens=None, item_exemplo=None, pontuacao_total=0, nivel_atual=1, gerenciador_recorde=None, texto_origem="", texto_destino="", campo_ativo=None):
        """Orquestra a renderização completa da interface de usuário em fluxo vertical dinâmico."""
        if vitoria or derrota:
            self.desenhar_telas_fim(largura_tela, vitoria, derrota, pontuacao_total)
            self.renderizador_recorde.desenhar(self.tela, gerenciador_recorde, altura_tela)
            return

        status = self._obter_texto_status(jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual)
        dica_texto = f"Controles: WASD/Setas | {status} | R: Reiniciar"
        dica = self.fonte_sub.render(dica_texto, True, (200, 200, 200))
        
        y_dica = self._PADDING_Y + self.fonte_sub.get_height() + 6
        self.tela.blit(dica, (self._PADDING_X, y_dica))

        texto_nivel = self.fonte_sub.render(f"Nível: {nivel_atual}", True, (255, 200, 100))
        self.tela.blit(texto_nivel, ((largura_tela - texto_nivel.get_width()) // 2, self._PADDING_Y))

        texto_pontos = self.fonte_sub.render(f"Pontos: {pontuacao_total}", True, (255, 215, 0))
        y_pontos = y_dica + dica.get_height() + 12
        self.tela.blit(texto_pontos, (self._PADDING_X, y_pontos))

        y_slot = y_pontos + texto_pontos.get_height() + self._ESPAÇAMENTO_VERTICAL
        self.desenhar_item_slot(renderizador_itens, item_exemplo, total_itens, self._PADDING_X, y_slot)
        self.renderizador_recorde.desenhar(self.tela, gerenciador_recorde, altura_tela)