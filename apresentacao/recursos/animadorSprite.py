"""Recorta uma spritesheet em frames e devolve o frame atual pelo tempo."""
import pygame


class AnimadorSprite:
    """Só recorta e devolve frames — não sabe onde nem quando desenhar."""

    def __init__(self, caminhoImagem, larguraFrame=100, alturaFrame=100, colunasGrid=8,
                 totalFrames=61, velocidadeAnimacao=60, tamanhoRender=(64, 64)):
        self.frames = []
        self.larguraFrame = larguraFrame
        self.alturaFrame = alturaFrame
        self.colunasGrid = colunasGrid
        self.totalFrames = totalFrames
        self.velocidadeAnimacao = velocidadeAnimacao
        self.tamanhoRender = tamanhoRender
        self._carregarSpritesheet(caminhoImagem)

    def _carregarSpritesheet(self, caminho):
        try:
            sheet = pygame.image.load(caminho).convert_alpha()
            sheetLargura, sheetAltura = sheet.get_size()

            for i in range(self.totalFrames):
                col = i % self.colunasGrid
                linha = i // self.colunasGrid
                x = col * self.larguraFrame
                y = linha * self.alturaFrame

                if x + self.larguraFrame <= sheetLargura and y + self.alturaFrame <= sheetAltura:
                    rect = pygame.Rect(x, y, self.larguraFrame, self.alturaFrame)
                    frame = sheet.subsurface(rect)
                    self.frames.append(pygame.transform.scale(frame, self.tamanhoRender))

            if not self.frames:
                raise ValueError("Nenhum frame recortado da spritesheet.")
        except Exception:
            self.frames.append(self._frameReserva())

    def _frameReserva(self):
        superficie = pygame.Surface(self.tamanhoRender, pygame.SRCALPHA)
        raio = self.tamanhoRender[0] // 3
        centro = (self.tamanhoRender[0] // 2, self.tamanhoRender[1] // 2)
        pygame.draw.circle(superficie, (0, 150, 255), centro, raio)
        return superficie

    def obterFrameAtual(self, tempoMs: int):
        if not self.frames:
            return None
        indice = (tempoMs // self.velocidadeAnimacao) % len(self.frames)
        return self.frames[indice]
