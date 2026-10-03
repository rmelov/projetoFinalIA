"""Rótulo clicável com destaque ao passar o mouse. Antes, este padrão
(renderiza base, testa collidepoint, re-renderiza em amarelo) estava
duplicado entre MenuPrincipal e MenuModosJogo."""
import pygame

COR_NORMAL = (255, 255, 255)
COR_DESTAQUE = (255, 235, 59)


class Botao:
    def __init__(self, texto, centro, fonteNormal, fonteDestaque=None):
        self.texto = texto
        self.centro = centro
        self.fonteNormal = fonteNormal
        self.fonteDestaque = fonteDestaque or fonteNormal
        self._retangulo = None

    def estaSobMouse(self, posicaoMouse=None) -> bool:
        posicaoMouse = posicaoMouse or pygame.mouse.get_pos()
        base = self.fonteNormal.render(self.texto, True, COR_NORMAL)
        retanguloBase = base.get_rect(center=self.centro)
        return retanguloBase.collidepoint(posicaoMouse)

    def desenhar(self, tela, selecionado=False):
        emDestaque = selecionado or self.estaSobMouse()
        fonte = self.fonteDestaque if emDestaque else self.fonteNormal
        cor = COR_DESTAQUE if emDestaque else COR_NORMAL
        superficie = fonte.render(self.texto, True, cor)
        self._retangulo = superficie.get_rect(center=self.centro)
        tela.blit(superficie, self._retangulo)
        return self._retangulo
