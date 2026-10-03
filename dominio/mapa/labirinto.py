"""Grid do labirinto. Único arquivo que conhece os valores 9 (parede) e 0
(livre) usados pelos algoritmos de busca — o resto do projeto usa esta
classe em vez de ler o grid diretamente."""
import random

from dominio.mapa.coordenada import Coordenada

PAREDE = 9
LIVRE = 0


class Labirinto:
    """Responde o que há em cada célula do grid e permite abrir passagens."""

    def __init__(self, grade):
        self._grade = grade

    @property
    def linhas(self) -> int:
        return len(self._grade)

    @property
    def colunas(self) -> int:
        return len(self._grade[0]) if self._grade else 0

    def ehParede(self, coordenada: Coordenada) -> bool:
        return self._grade[coordenada.linha][coordenada.coluna] == PAREDE

    def ehLivre(self, coordenada: Coordenada) -> bool:
        return self._grade[coordenada.linha][coordenada.coluna] == LIVRE

    def dentroDosLimites(self, coordenada: Coordenada) -> bool:
        return 0 <= coordenada.linha < self.linhas and 0 <= coordenada.coluna < self.colunas

    def abrirCelula(self, coordenada: Coordenada) -> None:
        """Garante que a célula seja livre (usado ao aplicar origem/destino customizados)."""
        self._grade[coordenada.linha][coordenada.coluna] = LIVRE

    def celulasLivres(self, excluindo=frozenset()):
        """Lista todas as células livres, exceto as informadas em `excluindo`."""
        excluidas = {tuple(c) for c in excluindo}
        return [
            Coordenada(l, c)
            for l in range(self.linhas)
            for c in range(self.colunas)
            if self._grade[l][c] == LIVRE and (l, c) not in excluidas
        ]

    def comoGrade(self):
        """Devolve o grid cru (lista de listas de 0/9), para os algoritmos de busca."""
        return self._grade

    def copiar(self) -> "Labirinto":
        return Labirinto([linha[:] for linha in self._grade])


class GeradorLabirinto:
    """Gera um Labirinto aleatório e posições iniciais de jogador, perseguidor e saída."""

    @staticmethod
    def gerar(linhas: int, colunas: int):
        """Devolve (Labirinto, posicaoJogador, posicaoPerseguidor, posicaoSaida)."""
        if linhas % 2 == 0:
            linhas += 1
        if colunas % 2 == 0:
            colunas += 1

        grade = [[PAREDE for _ in range(colunas)] for _ in range(linhas)]

        pilha = [(1, 1)]
        grade[1][1] = LIVRE

        def vizinhosValidos(l, c):
            vizinhos = []
            for dl, dc in ((-2, 0), (2, 0), (0, -2), (0, 2)):
                nl, nc = l + dl, c + dc
                if 0 < nl < linhas - 1 and 0 < nc < colunas - 1 and grade[nl][nc] == PAREDE:
                    vizinhos.append((nl, nc, dl, dc))
            return vizinhos

        while pilha:
            l, c = pilha[-1]
            vizinhos = vizinhosValidos(l, c)
            if vizinhos:
                nl, nc, dl, dc = random.choice(vizinhos)
                grade[l + dl // 2][c + dc // 2] = LIVRE
                grade[nl][nc] = LIVRE
                pilha.append((nl, nc))
            else:
                pilha.pop()

        posicaoJogador = Coordenada(1, 1)
        colunaPerseguidor = colunas - 2 if (colunas - 2) % 2 != 0 else colunas - 3
        posicaoPerseguidor = Coordenada(1, colunaPerseguidor)
        linhaSaida = linhas - 2 if (linhas - 2) % 2 != 0 else linhas - 3
        colunaSaida = colunas - 2 if (colunas - 2) % 2 != 0 else colunas - 3
        posicaoSaida = Coordenada(linhaSaida, colunaSaida)

        grade[posicaoJogador.linha][posicaoJogador.coluna] = LIVRE
        grade[posicaoPerseguidor.linha][posicaoPerseguidor.coluna] = LIVRE
        grade[posicaoSaida.linha][posicaoSaida.coluna] = LIVRE

        paredesRemoviveis = []
        for l in range(1, linhas - 1):
            for c in range(1, colunas - 1):
                if grade[l][c] == PAREDE:
                    caminhoHorizontal = grade[l][c - 1] == LIVRE and grade[l][c + 1] == LIVRE
                    caminhoVertical = grade[l - 1][c] == LIVRE and grade[l + 1][c] == LIVRE
                    if caminhoHorizontal or caminhoVertical:
                        paredesRemoviveis.append((l, c))

        qtdConexoesExtras = min(2, len(paredesRemoviveis))
        if paredesRemoviveis and qtdConexoesExtras > 0:
            for l, c in random.sample(paredesRemoviveis, qtdConexoesExtras):
                grade[l][c] = LIVRE

        return Labirinto(grade), posicaoJogador, posicaoPerseguidor, posicaoSaida
