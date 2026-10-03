"""
Catálogo único dos métodos de busca do projeto.

Este é o ÚNICO arquivo que conhece os nomes reais dos métodos dentro de
algoritmos/busca/buscaNP.py e algoritmos/busca/BuscaP.py — arquivos que não
são alterados por este projeto. Todo o resto do sistema (o inimigo do jogo,
a tela de seleção de modo, o repositório de recordes e o Laboratório de
Busca) consulta este catálogo em vez de conhecer os pacotes de busca
diretamente. Para acrescentar um método novo no futuro, basta implementá-lo
em algoritmos/busca e acrescentar uma entrada em METODOS_DISPONIVEIS —
nenhum outro arquivo do projeto precisa mudar (Aberto/Fechado).

Os cinco primeiros métodos (não ponderados) são os usados pelo inimigo do
jogo e têm arquivo de recorde associado. Os quatro últimos (ponderados) usam
o custo de movimento de algoritmos/busca/BuscaP.py e aparecem só no
Laboratório de Busca.
"""
from dataclasses import dataclass
from typing import Callable, Optional, Tuple


@dataclass(frozen=True)
class MetodoBusca:
    """Descreve um método de busca: identificação, aparência e como chamá-lo."""

    id: str
    nome: str
    descricao: str
    ponderado: bool
    corRota: Tuple[int, int, int]
    chamador: Callable
    arquivoRecorde: Optional[str] = None


def _chamarBuscaNpSemLimite(nomeMetodo: str) -> Callable:
    """Chamador de um método de buscaNP que não usa limite de profundidade."""

    def chamador(instancia, origem, destino, mapa, nx, ny, limite=None):
        metodoReal = getattr(instancia, nomeMetodo)
        return metodoReal(list(origem), list(destino), nx, ny, mapa)

    return chamador


def _chamarBuscaNpComLimite(nomeMetodo: str, limitePadraoFn: Callable) -> Callable:
    """Chamador de um método de buscaNP que exige um limite de profundidade.
    `limitePadraoFn(mapa, nx, ny)` é usado quando o chamador não recebe um
    `limite` explícito — cada consumidor (jogo ou Laboratório) pode passar
    o seu próprio valor."""

    def chamador(instancia, origem, destino, mapa, nx, ny, limite=None):
        metodoReal = getattr(instancia, nomeMetodo)
        limiteUsado = limite if limite is not None else limitePadraoFn(mapa, nx, ny)
        return metodoReal(list(origem), list(destino), nx, ny, mapa, limiteUsado)

    return chamador


def _chamarBuscaP(nomeMetodo: str) -> Callable:
    """
    Chamador de um método ponderado de BuscaP.py (custo uniforme, greedy,
    A-estrela, AIA-estrela).

    IMPORTANTE: ao contrário de buscaNP, os métodos de BuscaP comparam
    `atual.estado == fim` sem converter `fim` para tupla internamente. Se
    destino for passado como lista, a comparação nunca é verdadeira e o
    método devolve "não encontrado" mesmo quando existe caminho (chegando a
    causar ZeroDivisionError em aia_estrela_grid). O script de referência do
    professor sempre passa origem/destino como tupla — por isso convertemos.
    """

    def chamador(instancia, origem, destino, mapa, nx, ny, limite=None):
        metodoReal = getattr(instancia, nomeMetodo)
        return metodoReal(tuple(origem), tuple(destino), mapa, nx, ny)

    return chamador


def _contarCelulasLivres(mapa, nx, ny) -> int:
    """Cota segura para o limite de profundidade: nenhum caminho sem repetição
    de estado passa por mais células livres do que o mapa possui."""
    return sum(linha.count(0) for linha in mapa)


METODOS_DISPONIVEIS = [
    MetodoBusca(
        id="profundidade", nome="Profundidade",
        descricao="Avança fundo antes de voltar. Fácil de enganar e se perde em rotas longas.",
        ponderado=False, corRota=(255, 140, 80),
        chamador=_chamarBuscaNpSemLimite("profundidade_grid"),
        arquivoRecorde="assets/recordes/recordeProfundidade.txt",
    ),
    MetodoBusca(
        id="profLimitada", nome="Profundidade Limitada",
        descricao="Restrito a um limite de passos. Se o jogador estiver longe, o perseguidor se perde.",
        ponderado=False, corRota=(255, 205, 60),
        chamador=_chamarBuscaNpComLimite(
            "prof_limitada_grid", lambda mapa, nx, ny: 50  # sobrescrito pelo jogo/laboratório
        ),
        arquivoRecorde="assets/recordes/recordeProfundidadeLimitada.txt",
    ),
    MetodoBusca(
        id="aprofIterativo", nome="Aprofundamento Iterativo",
        descricao="Combina profundidade e limites crescentes. Uma ameaça equilibrada.",
        ponderado=False, corRota=(195, 120, 255),
        chamador=_chamarBuscaNpComLimite("aprof_iterativo_grid", _contarCelulasLivres),
        arquivoRecorde="assets/recordes/recordeAprofundamentoIterativo.txt",
    ),
    MetodoBusca(
        id="amplitude", nome="Amplitude",
        descricao="Explora em camadas e sempre encontra o menor caminho exato até você.",
        ponderado=False, corRota=(80, 180, 255),
        chamador=_chamarBuscaNpSemLimite("amplitude_grid"),
        arquivoRecorde="assets/recordes/recordeAmplitude.txt",
    ),
    MetodoBusca(
        id="bidirecional", nome="Bidirecional",
        descricao="Busca simultânea a partir da origem e do destino. Quase impossível escapar!",
        ponderado=False, corRota=(100, 220, 150),
        chamador=_chamarBuscaNpSemLimite("bidirecional_grid"),
        arquivoRecorde="assets/recordes/recordeBidirecional.txt",
    ),
    MetodoBusca(
        id="custoUniforme", nome="Custo Uniforme",
        descricao="Expande sempre o nó de menor custo acumulado; garante o caminho de menor custo.",
        ponderado=True, corRota=(255, 90, 90),
        chamador=_chamarBuscaP("custo_uniforme_grid"),
        arquivoRecorde="assets/recordes/recordeCustoUniforme.txt",
    ),
    MetodoBusca(
        id="greedy", nome="Greedy",
        descricao="Guia-se só pela distância estimada até o destino; rápido, mas pode errar o custo.",
        ponderado=True, corRota=(255, 215, 0),
        chamador=_chamarBuscaP("greedy_grid"),
        arquivoRecorde="assets/recordes/recordeGreedy.txt",
    ),
    MetodoBusca(
        id="aEstrela", nome="A-estrela",
        descricao="Combina custo acumulado e distância estimada; costuma achar o caminho ótimo mais rápido.",
        ponderado=True, corRota=(0, 210, 210),
        chamador=_chamarBuscaP("a_estrela_grid"),
        arquivoRecorde="assets/recordes/recordeAEstrela.txt",
    ),
    MetodoBusca(
        id="aiaEstrela", nome="AIA-estrela",
        descricao="A-estrela em rodadas com limite de custo crescente.",
        ponderado=True, corRota=(255, 120, 200),
        chamador=_chamarBuscaP("aia_estrela_grid"),
        arquivoRecorde="assets/recordes/recordeAiaEstrela.txt",
    ),
]

_METODOS_POR_ID = {metodo.id: metodo for metodo in METODOS_DISPONIVEIS}


def obterMetodo(idMetodo: str) -> MetodoBusca:
    """Devolve o MetodoBusca correspondente ao id informado."""
    if idMetodo not in _METODOS_POR_ID:
        raise ValueError(f"Método de busca desconhecido: {idMetodo!r}")
    return _METODOS_POR_ID[idMetodo]


def metodosNaoPonderados():
    """Métodos usados pelo inimigo do jogo (os que não dependem de peso)."""
    return [m for m in METODOS_DISPONIVEIS if not m.ponderado]
