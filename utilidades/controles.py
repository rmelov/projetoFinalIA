import pygame

class Controles:
    @staticmethod
    def verificar_teclas(evento, jogo, tempo_atual):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "voltar_menu"
            elif evento.key == pygame.K_r:
                if jogo.vitoria:
                    return "proximo_labirinto"
                elif jogo.derrota:
                    return "reiniciar_apos_derrota"
                else:
                    return "reiniciar_total"
            elif evento.key == pygame.K_SPACE:
                return "usar_pocao"
        return None

    @staticmethod
    def processar_movimento():
        teclas = pygame.key.get_pressed()
        dx, dy = 0, 0

        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            dx = -1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dy = 1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dx = 1
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dy = -1

        return dx, dy

    @staticmethod
    def navegar_menu(evento, indice_atual, total_opcoes):
        """Gerencia a navegação vertical por teclado (W/S ou Setas Cima/Baixo) em menus."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_w, pygame.K_UP):
                return (indice_atual - 1) % total_opcoes
            elif evento.key in (pygame.K_s, pygame.K_DOWN):
                return (indice_atual + 1) % total_opcoes
        return indice_atual

    @staticmethod
    def confirmar_menu(evento):
        """Verifica se a tecla de confirmação (Enter ou Espaço) foi pressionada."""
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                return True
        return False