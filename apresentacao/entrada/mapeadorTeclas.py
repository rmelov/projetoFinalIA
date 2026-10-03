"""Traduz eventos de teclado em intenções (Acao), mantendo o desacoplamento
entre tecla física e significado que já existia no projeto original."""
import pygame

from apresentacao.entrada.acao import Acao


class MapeadorTeclas:
    """Só sabe traduzir eventos — não decide o que fazer com a intenção."""

    @staticmethod
    def acaoDaPartida(evento, partida):
        if evento.type != pygame.KEYDOWN:
            return None
        if evento.key == pygame.K_ESCAPE:
            return Acao.VOLTAR_MENU
        if evento.key == pygame.K_r:
            if partida.vitoria:
                return Acao.PROXIMO_LABIRINTO
            if partida.derrota:
                return Acao.REINICIAR_APOS_DERROTA
            return Acao.REINICIAR_TOTAL
        if evento.key == pygame.K_SPACE:
            return Acao.USAR_POCAO
        return None

    @staticmethod
    def direcaoMovimento():
        teclas = pygame.key.get_pressed()
        if teclas[pygame.K_w] or teclas[pygame.K_UP]:
            return -1, 0
        if teclas[pygame.K_d] or teclas[pygame.K_RIGHT]:
            return 0, 1
        if teclas[pygame.K_s] or teclas[pygame.K_DOWN]:
            return 1, 0
        if teclas[pygame.K_a] or teclas[pygame.K_LEFT]:
            return 0, -1
        return 0, 0

    @staticmethod
    def navegarMenu(evento, indiceAtual, totalOpcoes):
        if evento.type == pygame.KEYDOWN:
            if evento.key in (pygame.K_w, pygame.K_UP):
                return (indiceAtual - 1) % totalOpcoes
            if evento.key in (pygame.K_s, pygame.K_DOWN):
                return (indiceAtual + 1) % totalOpcoes
        return indiceAtual

    @staticmethod
    def confirmarMenu(evento) -> bool:
        return evento.type == pygame.KEYDOWN and evento.key in (pygame.K_RETURN, pygame.K_SPACE)
