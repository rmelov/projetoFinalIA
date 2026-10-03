"""
O inimigo que persegue o jogador. Depende apenas de um objeto `buscador`
injetado no construtor (Princípio da Inversão de Dependência) — não conhece
buscaNP, BuscaP nem o catálogo de métodos. Isso permite testar o
Perseguidor com um buscador falso, sem pygame e sem os pacotes de busca.

O `buscador` precisa apenas de um método:
    encontrarRota(metodoId, origem, destino, mapa, linhas, colunas, limite=None)
        -> objeto com `.encontrado`, `.rota`, `.custo`
(ver aplicacao/portaBuscaCaminho.py e infraestrutura/busca/adaptadorBusca.py)
"""
from dominio.mapa.coordenada import Coordenada
from dominio.regras.regrasTempo import (
    LIMITE_PROFUNDIDADE_LIMITADA_JOGO,
    TEMPO_MOVIMENTO_IA_INICIAL,
    TEMPO_MOVIMENTO_IA_MINIMO,
)


class Perseguidor:
    """Persegue o jogador usando o método de busca escolhido no menu."""

    def __init__(self, buscador, posicaoInicial: Coordenada, metodoId="amplitude"):
        self.posicao = posicaoInicial
        self._buscador = buscador
        self.metodoId = metodoId
        self.caminhoAtual = []
        self.tempoMovimentoIa = TEMPO_MOVIMENTO_IA_INICIAL

    def ajustarVelocidade(self, indiceNivel: int):
        """A cada nível ganho diminui 20ms, a cada perdido aumenta 20ms."""
        novoTempo = TEMPO_MOVIMENTO_IA_INICIAL - (indiceNivel * 20)
        self.tempoMovimentoIa = max(TEMPO_MOVIMENTO_IA_MINIMO, min(TEMPO_MOVIMENTO_IA_INICIAL, novoTempo))

    def atualizarCaminho(self, posicaoJogador: Coordenada, labirinto):
        """Recalcula a rota até o jogador com o método de busca escolhido."""
        # Só "profLimitada" precisa de um limite ajustado ao jogo: os demais
        # métodos ignoram este argumento, e "aprofIterativo" usa o próprio
        # limite generoso do catálogo (calculado a partir do mapa), o que
        # continua garantindo sucesso em labirintos grandes.
        limite = LIMITE_PROFUNDIDADE_LIMITADA_JOGO if self.metodoId == "profLimitada" else None
        resultado = self._buscador.encontrarRota(
            self.metodoId, self.posicao, posicaoJogador,
            labirinto.comoGrade(), labirinto.linhas, labirinto.colunas, limite=limite,
        )
        if resultado.encontrado and len(resultado.rota) > 1:
            self.caminhoAtual = list(resultado.rota[1:])

    def mover(self):
        """Avança um passo ao longo do caminho calculado."""
        if self.caminhoAtual:
            self.posicao = self.caminhoAtual.pop(0)
