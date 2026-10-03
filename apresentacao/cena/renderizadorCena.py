"""Monta e desenha a cena isométrica de uma Partida: chão, itens, paredes,
entidades, rastro do perseguidor, mini-mapa e textos flutuantes."""
from dominio.mapa.coordenada import Coordenada

from apresentacao.cena.camadas.renderizadorChao import RenderizadorChao
from apresentacao.cena.camadas.renderizadorEntidades import RenderizadorEntidades
from apresentacao.cena.camadas.renderizadorParedes import RenderizadorParedes
from apresentacao.cena.miniMapa import MiniMapa
from apresentacao.cena.ordenadorDesenho import ElementoCena, ordenarEDesenhar
from apresentacao.cena.renderizadorItens import RenderizadorItens
from apresentacao.cena.renderizadorRastroPerseguidor import RenderizadorRastroPerseguidor
from apresentacao.cena.textosFlutuantes import GerenciadorTextosFlutuantes
from apresentacao.recursos.fabricaSprites import FabricaSprites

COR_FUNDO = (25, 25, 30)


class RenderizadorCena:
    """Orquestra as camadas — cada uma sabe desenhar só a si mesma."""

    def __init__(self, tela, conversor, fabricaSprites: FabricaSprites = None):
        self.tela = tela
        self.conversor = conversor
        self.renderizadorChao = RenderizadorChao(tela, conversor)
        self.renderizadorParedes = RenderizadorParedes(tela, conversor)
        self.renderizadorEntidades = RenderizadorEntidades(tela, conversor)
        self.renderizadorItens = RenderizadorItens(tela, conversor, fabricaSprites)
        self.renderizadorRastro = RenderizadorRastroPerseguidor(conversor)
        self.miniMapa = MiniMapa(*tela.get_size())
        self.textosFlutuantes = GerenciadorTextosFlutuantes(conversor)

    def desenhar(self, partida, tempoMs, fonteTextos):
        self.tela.fill(COR_FUNDO)
        labirinto = partida.labirinto
        mapa = labirinto.comoGrade()
        posJogador = partida.jogador.posicao

        elementos = self._montarElementos(partida, mapa, posJogador, tempoMs)
        ordenarEDesenhar(elementos)

        self.renderizadorRastro.desenhar(
            self.tela, partida.perseguidor.caminhoAtual, tempoMs,
            partida.controladorPerseguidor.congeladoAteMs, mapa,
        )
        self.textosFlutuantes.atualizarEDesenhar(self.tela, fonteTextos)
        self.miniMapa.desenhar(self.tela, mapa)

    def _montarElementos(self, partida, mapa, posJogador, tempoMs):
        elementos = []
        itensNoChao = (partida.pocao, partida.vortex, partida.saida)

        for linha in range(partida.labirinto.linhas):
            for coluna in range(partida.labirinto.colunas):
                coordenada = Coordenada(linha, coluna)
                isoX, isoY = self.conversor.cartesianoParaIsometrico(linha, coluna)
                profundidade = self.conversor.calcularProfundidade(linha, coluna)

                ehRastro = coordenada in partida.rastroPerseguidor
                elementos.append(ElementoCena(
                    profundidade, 0,
                    lambda x=isoX, y=isoY, r=ehRastro: self.renderizadorChao.desenhar(x, y, r),
                ))

                for item in itensNoChao:
                    if item.posicao == coordenada:
                        elementos.append(ElementoCena(
                            profundidade, 1,
                            lambda i=item: self.renderizadorItens.desenharItem(i, tempoMs),
                        ))

                if mapa[linha][coluna] == 9:
                    translucida = self._paredeObstrui(linha, coluna, posJogador)
                    elementos.append(ElementoCena(
                        profundidade, 2,
                        lambda x=isoX, y=isoY, t=translucida: self.renderizadorParedes.desenhar(x, y, t),
                    ))

                if coordenada == posJogador and not partida.vitoria:
                    elementos.append(ElementoCena(
                        profundidade, 3,
                        lambda l=linha, c=coluna: self.renderizadorEntidades.desenhar(l, c, "jogador", partida.pocao.ativa),
                    ))
                if coordenada == partida.perseguidor.posicao:
                    elementos.append(ElementoCena(
                        profundidade, 3,
                        lambda l=linha, c=coluna: self.renderizadorEntidades.desenhar(l, c, "inimigo", None),
                    ))
        return elementos

    @staticmethod
    def _paredeObstrui(linha, coluna, posJogador) -> bool:
        dentroDoRaio = abs(linha - posJogador.linha) <= 2 and abs(coluna - posJogador.coluna) <= 2
        naDirecao = (linha >= posJogador.linha and coluna >= posJogador.coluna) and (
            linha > posJogador.linha or coluna > posJogador.coluna
        )
        return dentroDoRaio and naDirecao
