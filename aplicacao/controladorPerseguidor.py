"""Decide QUANDO o perseguidor recalcula a rota e dá um passo — a cadência,
não a lógica de perseguição em si (que é do Perseguidor)."""


class ControladorPerseguidor:
    """Controla a cadência de movimento do perseguidor a partir do relógio do jogo."""

    def __init__(self):
        self.ultimoMovimentoMs = 0
        self.congeladoAteMs = 0

    def sincronizarRelogio(self, tempoMs: int):
        self.ultimoMovimentoMs = tempoMs

    def congelarAte(self, tempoMs: int):
        self.congeladoAteMs = tempoMs

    def atualizar(self, perseguidor, posicaoJogador, labirinto, tempoMs: int) -> bool:
        """Recalcula e move o perseguidor se a cadência permitir. Devolve True se ele se moveu."""
        if tempoMs < self.congeladoAteMs:
            return False
        if tempoMs - self.ultimoMovimentoMs <= perseguidor.tempoMovimentoIa:
            return False

        perseguidor.atualizarCaminho(posicaoJogador, labirinto)
        perseguidor.mover()
        self.ultimoMovimentoMs = tempoMs
        return True
