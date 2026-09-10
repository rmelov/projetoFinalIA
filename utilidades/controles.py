import pygame

class Controles:
    @staticmethod
    def verificar_teclas(evento, jogo, tempo_atual):
        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                return "sair"
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
            dy = -1
        elif teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            dx = 1
        elif teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            dy = 1
        elif teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            dx = -1

        return dx, dy