import sys
import pygame

from componentes.conversorIsometrico import ConversorIsometrico
from renderizacao.renderizadorIsometrico import RenderizadorIsometrico
from utilidades import config
from utilidades.gerenciadorJogo import GerenciadorJogo

pygame.init()
info_display = pygame.display.Info()
config.LARGURA, config.ALTURA = info_display.current_w, info_display.current_h

tela = pygame.display.set_mode((config.LARGURA, config.ALTURA), pygame.FULLSCREEN)
pygame.display.set_caption(config.TITULO)

altura_grid = (config.LINHAS + config.COLUNAS) * (config.ALTURA_TILE / 2)
deslocamento_y = config.ALTURA - altura_grid - 20

conversor = ConversorIsometrico(
    largura_tile=config.LARGURA_TILE, 
    altura_tile=config.ALTURA_TILE, 
    deslocamento_x=config.LARGURA // 2, 
    deslocamento_y=deslocamento_y
)
renderizador = RenderizadorIsometrico(tela, conversor)
gerenciador = GerenciadorJogo(tela, renderizador)

if __name__ == "__main__":
    gerenciador.executar()