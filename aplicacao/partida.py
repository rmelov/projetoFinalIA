"""
Substitui a antiga EstadoJogo (351 linhas, sete responsabilidades). Aqui só
sobra a orquestração: guardar o estado corrente e encaminhar cada evento ao
colaborador certo. Parsing/validação de coordenadas, sorteio de posição,
regras de pontuação, decisão de vitória/derrota e cadência do perseguidor
foram todos extraídos para classes próprias.
"""
from dominio.coordenadas.coordenadasTexto import ParserCoordenada, ValidadorCoordenada
from dominio.entidades.jogador import Jogador
from dominio.entidades.perseguidor import Perseguidor
from dominio.itens.pocaoCoragem import PocaoCoragem
from dominio.itens.saida import Saida
from dominio.itens.vortex import Vortex
from dominio.mapa.coordenada import Coordenada
from dominio.progresso.progressoJogador import ProgressoJogador
from dominio.regras.nivel import Nivel
from dominio.regras.regrasPontuacao import (
    PONTOS_ACIONAR_VORTEX,
    PONTOS_COLETAR_POCAO,
    PONTOS_LIMPAR_RASTRO_COM_POCAO,
)
from dominio.regras.regrasTempo import CONGELAMENTO_APOS_VORTEX_MS

from aplicacao.arbitroPartida import ArbitroPartida, DesfechoPartida
from aplicacao.controladorPerseguidor import ControladorPerseguidor
from aplicacao.posicionadorAleatorio import PosicionadorAleatorio
from aplicacao.preparadorFase import PreparadorFase

COR_NOTIFICACAO_POCAO = (0, 255, 0)
COR_NOTIFICACAO_VORTEX = (255, 215, 0)
COR_NOTIFICACAO_RASTRO_LIMPO = (0, 255, 255)
COR_NOTIFICACAO_PENALIDADE = (255, 50, 50)


class Partida:
    """Orquestra uma partida: mantém o estado corrente e delega regras aos colaboradores."""

    def __init__(self, buscador, repositorioRecorde, metodoId="amplitude", posicionador=None):
        self.buscador = buscador
        self.repositorioRecorde = repositorioRecorde
        self.metodoId = metodoId
        self._posicionador = posicionador or PosicionadorAleatorio()
        self._sistemaNivel = Nivel()
        self.controladorPerseguidor = ControladorPerseguidor()

        self.progresso = ProgressoJogador()
        self.indiceNivel = 0

        self.labirinto = None
        self.jogador = None
        self.perseguidor = None
        self.rastroPerseguidor = set()
        self.saida = Saida()
        self.pocao = PocaoCoragem()
        self.vortex = Vortex()

        self.jogoIniciado = False
        self.vitoria = False
        self.derrota = False
        self.ultimoPassoJogadorMs = 0

        self.textoOrigemCustomizada = ""
        self.textoDestinoCustomizada = ""
        self._posicaoOrigemCustomizada = None
        self._posicaoDestinoCustomizada = None

        self.notificacoesPendentes = []  # [(texto, coordenada, cor)] — a apresentação drena isto

        self.pontuacaoMaxima, self.nivelMaximo = self.repositorioRecorde.carregar(metodoId)

    # ------------------------------------------------------------------
    # Consultas
    # ------------------------------------------------------------------
    @property
    def nivelAtual(self) -> int:
        return self._sistemaNivel.obterValorNivel(self.indiceNivel)

    def dimensoesAtuais(self):
        tamanho = self._sistemaNivel.calcularTamanhoGrid(self.indiceNivel)
        return tamanho, tamanho

    def contarTotalItens(self) -> int:
        return self.progresso.totalItens

    def obterPontuacaoTotal(self) -> int:
        return self.progresso.totalPontos

    # ------------------------------------------------------------------
    # Coordenadas customizadas (entrada do jogador no menu)
    # ------------------------------------------------------------------
    def definirCoordenadasPersonalizadas(self, textoOrigem="", textoDestino=""):
        self.textoOrigemCustomizada = str(textoOrigem or "")
        self.textoDestinoCustomizada = str(textoDestino or "")
        self._posicaoOrigemCustomizada = ParserCoordenada.converter(self.textoOrigemCustomizada)
        self._posicaoDestinoCustomizada = ParserCoordenada.converter(self.textoDestinoCustomizada)

    def validarCoordenadasPersonalizadas(self, textoOrigem="", textoDestino=""):
        linhas, colunas = self.dimensoesAtuais()
        return ValidadorCoordenada.validarPar(textoOrigem, textoDestino, linhas, colunas)

    # ------------------------------------------------------------------
    # Ciclo de vida da partida
    # ------------------------------------------------------------------
    def reiniciar(self):
        self.progresso.zerarPartida()
        self.pocao.encerrarEfeito()
        self._prepararFaseCompleta()

    def avancarProximoLabirinto(self):
        self.progresso.consolidarPartida()
        self.indiceNivel += 1
        self._prepararFaseCompleta()

    def usarPocao(self, tempoMs: int) -> bool:
        if not self.pocao.usar(tempoMs):
            return False
        if self.progresso.mochilaPartida.totalItens > 0:
            self.progresso.mochilaPartida.removerUltimo()
        elif self.progresso.mochilaGeral.totalItens > 0:
            self.progresso.mochilaGeral.removerUltimo()
        self.pocao.frascos = self.contarTotalItens()
        return True

    # ------------------------------------------------------------------
    # Preparação de fase
    # ------------------------------------------------------------------
    def _prepararFaseCompleta(self):
        """Gera um labirinto totalmente novo (nova fase ou reinício)."""
        linhas, colunas = self.dimensoesAtuais()
        fase = PreparadorFase.montar(linhas, colunas)
        self.labirinto = fase.labirinto
        self.jogador = Jogador(fase.posicaoJogador)
        self.perseguidor = Perseguidor(self.buscador, fase.posicaoPerseguidor, metodoId=self.metodoId)
        self.perseguidor.ajustarVelocidade(self.indiceNivel)
        self.rastroPerseguidor = {self.perseguidor.posicao}
        self.jogoIniciado = False
        self.controladorPerseguidor.congelarAte(0)

        self._aplicarCoordenadasPersonalizadas(linhas, colunas)
        self._reposicionarItensColetaveis(frascosPreservados=0, pocaoAtivaPreservada=False, tempoFimPreservado=0)

    def _remontarPreservandoEntidades(self):
        """Regenera o labirinto mantendo jogador e perseguidor no lugar (usado ao acionar o vórtex)."""
        linhas, colunas = self.dimensoesAtuais()
        frascosAtuais = self.pocao.frascos
        pocaoAtivaAnterior = self.pocao.ativa
        tempoFimAnterior = self.pocao.tempoFim

        posicaoJogadorAnterior = self.jogador.posicao
        posicaoPerseguidorAnterior = self.perseguidor.posicao

        fase = PreparadorFase.montar(linhas, colunas)
        self.labirinto = fase.labirinto

        self.jogador.posicao = self._clamp(posicaoJogadorAnterior, linhas, colunas, padrao=Coordenada(1, 1))
        self.labirinto.abrirCelula(self.jogador.posicao)

        self.perseguidor.posicao = self._clamp(posicaoPerseguidorAnterior, linhas, colunas, padrao=Coordenada(1, 2))
        self.labirinto.abrirCelula(self.perseguidor.posicao)

        self.saida.posicao = fase.posicaoSaida
        self.labirinto.abrirCelula(self.saida.posicao)

        self._reposicionarItensColetaveis(frascosAtuais, pocaoAtivaAnterior, tempoFimAnterior)

    @staticmethod
    def _clamp(coordenada: Coordenada, linhas: int, colunas: int, padrao: Coordenada) -> Coordenada:
        if 0 <= coordenada.linha < linhas and 0 <= coordenada.coluna < colunas:
            return coordenada
        return padrao

    def _aplicarCoordenadasPersonalizadas(self, linhas, colunas):
        origem = self._posicaoOrigemCustomizada
        destino = self._posicaoDestinoCustomizada

        if origem is not None and not (0 <= origem.linha < linhas and 0 <= origem.coluna < colunas):
            origem = None
        if destino is not None and not (0 <= destino.linha < linhas and 0 <= destino.coluna < colunas):
            destino = None
        if origem is not None and destino is not None and origem == destino:
            destino = None

        if origem is not None:
            self.labirinto.abrirCelula(origem)
            self.jogador.posicao = origem

        if destino is not None:
            self.labirinto.abrirCelula(destino)
            self.saida.posicao = destino
        else:
            self.saida.posicao = Coordenada(linhas - 2, colunas - 2)

        if self.jogador.posicao == self.saida.posicao:
            alternativa = self._posicionador.sortearCelulaLivre(self.labirinto, excluindo={self.jogador.posicao})
            if alternativa is not None:
                self.saida.posicao = alternativa

        self.labirinto.abrirCelula(self.saida.posicao)

    def _reposicionarItensColetaveis(self, frascosPreservados, pocaoAtivaPreservada, tempoFimPreservado):
        self.pocao = PocaoCoragem()
        self.pocao.frascos = frascosPreservados
        self.pocao.ativa = pocaoAtivaPreservada
        self.pocao.tempoFim = tempoFimPreservado
        ocupadas = {self.jogador.posicao, self.saida.posicao, self.perseguidor.posicao}
        self.pocao.posicao = self._posicionador.sortearCelulaLivre(self.labirinto, excluindo=ocupadas)

        self.vortex = Vortex()
        ocupadas = {self.jogador.posicao, self.saida.posicao, self.perseguidor.posicao}
        if self.pocao.posicao:
            ocupadas.add(self.pocao.posicao)
        self.vortex.posicao = self._posicionador.sortearCelulaLivre(self.labirinto, excluindo=ocupadas)

        self.vitoria = False
        self.derrota = False

    # ------------------------------------------------------------------
    # Movimento e regras durante a partida
    # ------------------------------------------------------------------
    def processarMovimento(self, deltaLinha: int, deltaColuna: int, tempoMs: int):
        if deltaLinha == 0 and deltaColuna == 0:
            return

        novaPosicao = Coordenada(self.jogador.posicao.linha + deltaLinha, self.jogador.posicao.coluna + deltaColuna)
        if not (self.labirinto.dentroDosLimites(novaPosicao) and self.labirinto.ehLivre(novaPosicao)):
            return

        self.jogador.mover(novaPosicao)
        self.ultimoPassoJogadorMs = tempoMs

        if not self.jogoIniciado:
            self.jogoIniciado = True
            self.controladorPerseguidor.sincronizarRelogio(tempoMs)

        if novaPosicao in self.rastroPerseguidor and self.pocao.ativa:
            self.progresso.placarPartida.adicionar(PONTOS_LIMPAR_RASTRO_COM_POCAO)
            self.notificacoesPendentes.append(
                (f"+{PONTOS_LIMPAR_RASTRO_COM_POCAO}", novaPosicao, COR_NOTIFICACAO_RASTRO_LIMPO)
            )
            self.rastroPerseguidor.discard(novaPosicao)

        if self.pocao.posicao and novaPosicao == self.pocao.posicao:
            self.pocao.coletar()
            self.progresso.mochilaPartida.adicionar(self.pocao)
            self.pocao.frascos = self.contarTotalItens()
            self.progresso.placarPartida.adicionar(PONTOS_COLETAR_POCAO)
            self.notificacoesPendentes.append((f"+{PONTOS_COLETAR_POCAO}", novaPosicao, COR_NOTIFICACAO_POCAO))
            self.pocao.posicao = None

        if self.vortex.posicao and novaPosicao == self.vortex.posicao:
            self._reagirAoVortex(tempoMs, jogadorAcionou=True)

    def _reagirAoVortex(self, tempoMs: int, jogadorAcionou: bool):
        """Reação ao vórtice, seja o jogador ou o perseguidor quem o tocou —
        antes esta lógica estava duplicada nos dois pontos de chamada."""
        if jogadorAcionou:
            self.progresso.placarPartida.adicionar(PONTOS_ACIONAR_VORTEX)
            self.notificacoesPendentes.append(
                (f"+{PONTOS_ACIONAR_VORTEX}", self.jogador.posicao, COR_NOTIFICACAO_VORTEX)
            )
        self._remontarPreservandoEntidades()
        self.controladorPerseguidor.congelarAte(tempoMs + CONGELAMENTO_APOS_VORTEX_MS)
        self.rastroPerseguidor = {self.perseguidor.posicao}

    # ------------------------------------------------------------------
    # Atualização por frame
    # ------------------------------------------------------------------
    def atualizar(self, tempoMs: int):
        self.pocao.atualizar(tempoMs)
        self._atualizarPerseguidor(tempoMs)
        self._avaliarDesfecho()

    def _atualizarPerseguidor(self, tempoMs: int):
        if not (self.jogoIniciado and not self.vitoria and not self.derrota):
            return

        moveu = self.controladorPerseguidor.atualizar(self.perseguidor, self.jogador.posicao, self.labirinto, tempoMs)
        if not moveu:
            return

        if self.vortex.posicao and self.perseguidor.posicao == self.vortex.posicao:
            self._reagirAoVortex(tempoMs, jogadorAcionou=False)
            return

        self.rastroPerseguidor.add(self.perseguidor.posicao)

    def _avaliarDesfecho(self):
        desfecho = ArbitroPartida.avaliar(
            self.jogador.posicao, self.saida.posicao, self.perseguidor.posicao,
            self.rastroPerseguidor, self.pocao.ativa,
        )

        if desfecho == DesfechoPartida.VITORIA and not self.vitoria:
            self.vitoria = True
            self.pocao.encerrarEfeito()
            self.progresso.placarPartida.adicionar(self.nivelAtual)
            self.progresso.consolidarPartida()
            self.repositorioRecorde.salvarSeMaior(self.metodoId, self.obterPontuacaoTotal(), self.nivelAtual)

        elif desfecho == DesfechoPartida.DERROTA and not self.derrota:
            self.derrota = True
            self.pocao.encerrarEfeito()
            penalidade = self.nivelAtual
            self.progresso.descartarPartida(penalidade)
            self.indiceNivel = max(0, self.indiceNivel - 1)
            self.notificacoesPendentes.append((f"-{penalidade}", self.jogador.posicao, COR_NOTIFICACAO_PENALIDADE))
