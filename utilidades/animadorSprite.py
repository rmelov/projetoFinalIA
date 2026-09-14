import pygame

class AnimadorSprite:
    def __init__(self, caminho_imagem, largura_frame=100, altura_frame=100, colunas_grid=8, total_frames=61, velocidade_animacao=60, tamanho_render=(64, 64)):
        self.frames = []
        self.largura_frame = largura_frame
        self.altura_frame = altura_frame
        self.colunas_grid = colunas_grid
        self.total_frames = total_frames
        self.velocidade_animacao = velocidade_animacao
        self.tamanho_render = tamanho_render
        
        self._carregar_spritesheet(caminho_imagem)

    def _carregar_spritesheet(self, caminho):
        try:
            sheet = pygame.image.load(caminho).convert_alpha()
            sheet_largura, sheet_altura = sheet.get_size()
            
            for i in range(self.total_frames):
                col = i % self.colunas_grid
                row = i // self.colunas_grid
                
                x = col * self.largura_frame
                y = row * self.altura_frame
                
                if x + self.largura_frame <= sheet_largura and y + self.altura_frame <= sheet_altura:
                    rect = pygame.Rect(x, y, self.largura_frame, self.altura_frame)
                    frame = sheet.subsurface(rect)
                    frame_redimensionado = pygame.transform.scale(frame, self.tamanho_render)
                    self.frames.append(frame_redimensionado)
            
            if not self.frames:
                raise ValueError("Nenhum frame recortado da spritesheet.")

        except Exception:
            surf = pygame.Surface(self.tamanho_render, pygame.SRCALPHA)
            raio = self.tamanho_render[0] // 3
            pygame.draw.circle(surf, (0, 150, 255), (self.tamanho_render[0] // 2, self.tamanho_render[1] // 2), raio)
            self.frames.append(surf)

    def obter_frame_atual(self, tempo_atual):
        if not self.frames:
            return None
        indice = (tempo_atual // self.velocidade_animacao) % len(self.frames)
        return self.frames[indice]