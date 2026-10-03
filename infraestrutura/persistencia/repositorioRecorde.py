"""
Substitui GerenciadorRecorde. Antes, RenderizadorRecorde.desenhar() chamava
carregar() a cada frame — 30 leituras de disco por segundo. Aqui o valor é
lido uma vez por modo e mantido em memória; só volta ao disco quando um
novo recorde é salvo.
"""
import os

from aplicacao.metodosBusca import obterMetodo


class RepositorioRecorde:
    """Lê e grava o recorde (pontuação, nível) de cada método de busca, com cache."""

    def __init__(self):
        self._cache = {}

    def _caminhoArquivo(self, metodoId: str) -> str:
        metodo = obterMetodo(metodoId)
        return metodo.arquivoRecorde or obterMetodo("amplitude").arquivoRecorde

    def carregar(self, metodoId: str):
        if metodoId in self._cache:
            return self._cache[metodoId]

        caminho = self._caminhoArquivo(metodoId)
        pontuacao, nivel = 0, 1
        if os.path.exists(caminho):
            try:
                with open(caminho, "r", encoding="utf-8") as arquivo:
                    conteudo = arquivo.read().strip()
                    if conteudo:
                        partes = conteudo.split(",")
                        pontuacao = int(partes[0])
                        nivel = int(partes[1]) if len(partes) > 1 else 1
            except (ValueError, IndexError, OSError):
                pontuacao, nivel = 0, 1

        self._cache[metodoId] = (pontuacao, nivel)
        return self._cache[metodoId]

    def salvarSeMaior(self, metodoId: str, pontuacao: int, nivel: int):
        pontuacaoAtual, nivelAtual = self.carregar(metodoId)
        if pontuacao <= pontuacaoAtual:
            return

        caminho = self._caminhoArquivo(metodoId)
        os.makedirs(os.path.dirname(caminho), exist_ok=True)
        with open(caminho, "w", encoding="utf-8") as arquivo:
            arquivo.write(f"{pontuacao},{nivel}")

        self._cache[metodoId] = (pontuacao, nivel)
