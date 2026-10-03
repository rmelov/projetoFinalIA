"""Poção de coragem: controla duração e disponibilidade do efeito. O sorteio
de posição foi extraído para aplicacao/posicionadorAleatorio.py (evita
duplicar a mesma lógica de "sortear célula livre" que também é usada pelo
vórtex) e a aparência (sprite) foi extraída para
apresentacao/recursos/fabricaSprites.py — item de domínio não sabe desenhar."""
from dominio.regras.regrasTempo import DURACAO_POCAO_MS

IMAGEM_PADRAO = "assets/imgs/DailyDoodles/glass02blue.png"


class PocaoCoragem:
    """Controla quantos frascos existem e se o efeito está ativo agora."""

    def __init__(self, quantidadeInicial=0):
        self.frascos = quantidadeInicial
        self.ativa = False
        self.tempoFim = 0
        self.duracaoMs = DURACAO_POCAO_MS
        self.posicao = None
        self.imagemPath = IMAGEM_PADRAO

    def usar(self, tempoMs: int) -> bool:
        if self.frascos > 0 and not self.ativa:
            self.frascos -= 1
            self.ativa = True
            self.tempoFim = tempoMs + self.duracaoMs
            return True
        return False

    def atualizar(self, tempoMs: int):
        if self.ativa and tempoMs > self.tempoFim:
            self.ativa = False

    def coletar(self):
        self.frascos += 1

    def encerrarEfeito(self):
        self.ativa = False
        self.tempoFim = 0
