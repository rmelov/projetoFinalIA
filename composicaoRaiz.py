"""
Composition root: o único lugar do projeto que decide QUEM implementa
cada peça (qual buscador, qual repositório de recorde) e conecta tudo.
Nenhuma outra classe do projeto instancia suas próprias dependências —
todas recebem por injeção a partir daqui.
"""
import pygame

from apresentacao.cena.conversorIsometrico import ConversorIsometrico
from apresentacao.configVisual import ALTURA_TILE, LARGURA_TILE, TITULO
from apresentacao.contextoVisual import ContextoVisual
from apresentacao.telas.navegadorTelas import NavegadorTelas
from infraestrutura.busca.adaptadorBusca import AdaptadorBusca
from infraestrutura.persistencia.repositorioRecorde import RepositorioRecorde


def montarAplicacao() -> NavegadorTelas:
    pygame.init()
    pygame.font.init()

    info = pygame.display.Info()
    largura, altura = info.current_w, info.current_h
    tela = pygame.display.set_mode((largura, altura), pygame.FULLSCREEN)
    pygame.display.set_caption(TITULO)

    contexto = ContextoVisual(tela=tela, largura=largura, altura=altura)
    conversor = ConversorIsometrico(LARGURA_TILE, ALTURA_TILE, largura // 2, altura // 2)

    buscador = AdaptadorBusca()
    repositorioRecorde = RepositorioRecorde()

    return NavegadorTelas(contexto, conversor, buscador, repositorioRecorde)
