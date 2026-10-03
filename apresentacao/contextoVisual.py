"""Substitui a antiga escrita em config.LARGURA/config.ALTURA feita por
main.py em tempo de import — agora é um objeto criado pela composição raiz
e passado a quem precisa, em vez de estado global mutável."""
from dataclasses import dataclass


@dataclass
class ContextoVisual:
    tela: object
    largura: int
    altura: int
