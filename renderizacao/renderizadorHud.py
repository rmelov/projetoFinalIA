import pygame

class RenderizadorHud:
    def __init__(self, tela, fonte_principal, fonte_sub):
        self.tela = tela
        self.fonte_principal = fonte_principal
        self.fonte_sub = fonte_sub

    def desenhar_item_slot(self, renderizador_itens, item, quantidade, x, y):
        if renderizador_itens and item:
            img = renderizador_itens._carregar_imagem(getattr(item, "imagem_path", ""))
            rect_bg = pygame.Rect(x, y - 2, 60, 32)
            pygame.draw.rect(self.tela, (40, 40, 50), rect_bg, border_radius=4)
            pygame.draw.rect(self.tela, (80, 80, 100), rect_bg, 1, border_radius=4)
            
            self.tela.blit(img, (x + 4, y + 2))
            texto_qtd = self.fonte_sub.render(f"x{quantidade}", True, (255, 255, 255))
            self.tela.blit(texto_qtd, (x + 36, y + 6))

    def desenhar_telas_fim(self, largura_tela, vitoria, derrota):
        if not vitoria and not derrota:
            return

        texto_str = "VOCÊ VENCEU!" if vitoria else "VOCÊ PERDEU!"
        cor_txt = (100, 255, 100) if vitoria else (255, 100, 100)

        texto = self.fonte_principal.render(texto_str, True, cor_txt)
        subtexto = self.fonte_sub.render("Pressione 'R' para reiniciar", True, (200, 200, 200))

        self.tela.blit(texto, (largura_tela // 2 - texto.get_width() // 2, 30))
        self.tela.blit(subtexto, (largura_tela // 2 - subtexto.get_width() // 2, 80))

    def desenhar(self, largura_tela, jogo_iniciado, pocao_ativa, tempo_pocao_fim, tempo_atual, vitoria, derrota, total_itens=0, renderizador_itens=None, item_exemplo=None):
        if vitoria or derrota:
            self.desenhar_telas_fim(largura_tela, vitoria, derrota)
        else:
            if not jogo_iniciado:
                status = "Movimente-se para iniciar..."
            elif pocao_ativa:
                tempo_restante = max(0, (tempo_pocao_fim - tempo_atual) // 1000 + 1)
                status = f"POÇÃO ATIVA ({tempo_restante}s)"
            else:
                status = "Espaço para usar"

            dica_texto = f"Controles: WASD/Setas | {status} | R: Reiniciar"
            dica = self.fonte_sub.render(dica_texto, True, (200, 200, 200))
            self.tela.blit(dica, (15, 12))

            self.desenhar_item_slot(renderizador_itens, item_exemplo, total_itens, 15, 40)