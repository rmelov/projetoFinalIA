"""
A interface gráfica exigida na atividade: seletor de método (entre os 9
disponíveis), definição de estado inicial e objetivo, botão de execução,
área de exibição do caminho e custo, e a imagem do problema com o caminho
desenhado.

Reaproveita o labirinto da partida em andamento (LoopJogo.partida) quando
existe uma; caso o jogador ainda não tenha jogado nesta sessão, gera um
labirinto de exemplo com o mesmo PreparadorFase usado pelo jogo — não há
uma segunda lógica de geração de labirinto.
"""
import sys

import pygame

from aplicacao.metodosBusca import METODOS_DISPONIVEIS
from aplicacao.preparadorFase import PreparadorFase
from apresentacao.entrada.mapeadorTeclas import MapeadorTeclas
from apresentacao.ui.botao import Botao

COR_PAINEL = (28, 28, 34)
COR_PAREDE = (40, 40, 46)
COR_LIVRE = (230, 228, 220)
COR_GRADE = (70, 70, 78)
COR_ORIGEM = (60, 200, 100)
COR_DESTINO = (220, 60, 60)
COR_AVISO = (255, 200, 90)

TAMANHO_GRID_EXEMPLO = 15


class TelaLaboratorioBusca:
    def __init__(self, contexto, fontes, buscador, obterPartidaAtual=None):
        self.contexto = contexto
        self.buscador = buscador
        self._obterPartidaAtual = obterPartidaAtual

        self.fonteTitulo = fontes.obter(20)
        self.fonteItem = fontes.obter(15)
        self.fonteRodape = fontes.obter(13)

        self.indiceSelecionado = 0
        self.resultadoAtual = None
        self.mensagemAviso = ""
        self._retItensMetodo = []

        self._calcularLayout()

    def _calcularLayout(self):
        largura, altura = self.contexto.largura, self.contexto.altura
        margem, largSeletor, largPainel, topo, rodape = 20, 260, 300, 70, 90

        self.areaSeletor = pygame.Rect(margem, topo, largSeletor, altura - topo - rodape)
        self.areaPainel = pygame.Rect(largura - largPainel - margem, topo, largPainel, altura - topo - rodape)
        largGrade = largura - largSeletor - largPainel - margem * 3
        self.areaGrade = pygame.Rect(margem * 2 + largSeletor, topo, largGrade, altura - topo - rodape)

        y = altura - rodape + 20
        self.botaoExecutar = pygame.Rect(margem, y, 160, 40)
        self.botaoSincronizar = pygame.Rect(margem + 180, y, 260, 40)

    def _sincronizarComPartida(self):
        partida = self._obterPartidaAtual() if self._obterPartidaAtual else None
        if partida is not None and partida.labirinto is not None:
            self.labirinto = partida.labirinto
            self.origem = partida.jogador.posicao
            self.destino = partida.saida.posicao
            self.origemDados = "partida em andamento"
        else:
            fase = PreparadorFase.montar(TAMANHO_GRID_EXEMPLO, TAMANHO_GRID_EXEMPLO)
            self.labirinto = fase.labirinto
            self.origem = fase.posicaoJogador
            self.destino = fase.posicaoSaida
            self.origemDados = "labirinto de exemplo (nenhuma partida em andamento)"
        self.resultadoAtual = None
        self.mensagemAviso = ""

    def executar(self):
        self._sincronizarComPartida()
        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((18, 18, 22))
            self._desenhar()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return
                    elif evento.key in (pygame.K_w, pygame.K_UP, pygame.K_s, pygame.K_DOWN):
                        self.indiceSelecionado = MapeadorTeclas.navegarMenu(
                            evento, self.indiceSelecionado, len(METODOS_DISPONIVEIS)
                        )
                    elif MapeadorTeclas.confirmarMenu(evento):
                        self._executarBusca()
                    elif evento.key == pygame.K_n:
                        self._sincronizarComPartida()
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    self._tratarClique(evento.pos, evento.button)

            pygame.display.flip()
            relogio.tick(30)

    def _tratarClique(self, posicao, botao):
        if self.botaoExecutar.collidepoint(posicao):
            self._executarBusca()
            return
        if self.botaoSincronizar.collidepoint(posicao):
            self._sincronizarComPartida()
            return
        for indice, retangulo in enumerate(self._retItensMetodo):
            if retangulo.collidepoint(posicao):
                self.indiceSelecionado = indice
                return

        celula = self._celulaNaPosicao(posicao)
        if celula is None:
            return
        linha, coluna = celula
        if self.labirinto.comoGrade()[linha][coluna] != 0:
            self.mensagemAviso = "Essa célula é parede: escolha uma célula livre."
            return

        self.mensagemAviso = ""
        from dominio.mapa.coordenada import Coordenada
        if botao == 1:
            self.origem = Coordenada(linha, coluna)
        elif botao == 3:
            self.destino = Coordenada(linha, coluna)
        self.resultadoAtual = None

    def _executarBusca(self):
        metodo = METODOS_DISPONIVEIS[self.indiceSelecionado]
        self.resultadoAtual = self.buscador.encontrarRota(
            metodo.id, self.origem, self.destino,
            self.labirinto.comoGrade(), self.labirinto.linhas, self.labirinto.colunas,
        )

    # ------------------------------------------------------------------
    # Geometria da grade (compartilhada entre desenho e clique)
    # ------------------------------------------------------------------
    def _geometriaGrade(self):
        linhas, colunas = self.labirinto.linhas, self.labirinto.colunas
        tamanhoCelula = max(4, min(self.areaGrade.width // colunas, self.areaGrade.height // linhas))
        largGrid, altGrid = tamanhoCelula * colunas, tamanhoCelula * linhas
        origemX = self.areaGrade.x + (self.areaGrade.width - largGrid) // 2
        origemY = self.areaGrade.y + (self.areaGrade.height - altGrid) // 2
        return origemX, origemY, tamanhoCelula

    def _celulaNaPosicao(self, posicaoMouse):
        if not self.areaGrade.collidepoint(posicaoMouse):
            return None
        origemX, origemY, tamanhoCelula = self._geometriaGrade()
        mx, my = posicaoMouse
        coluna = (mx - origemX) // tamanhoCelula
        linha = (my - origemY) // tamanhoCelula
        if 0 <= linha < self.labirinto.linhas and 0 <= coluna < self.labirinto.colunas:
            return int(linha), int(coluna)
        return None

    # ------------------------------------------------------------------
    # Desenho
    # ------------------------------------------------------------------
    def _desenhar(self):
        titulo = self.fonteTitulo.render(
            "LABORATÓRIO DE BUSCA — selecione o método, defina origem/destino e execute",
            True, (255, 235, 59),
        )
        self.contexto.tela.blit(titulo, (20, 20))
        fonteOrigemDados = self.fonteRodape.render(f"Labirinto: {self.origemDados}", True, (140, 200, 140))
        self.contexto.tela.blit(fonteOrigemDados, (20, 46))

        pygame.draw.rect(self.contexto.tela, COR_PAINEL, self.areaSeletor)
        self._desenharSeletorMetodo()

        pygame.draw.rect(self.contexto.tela, COR_PAINEL, self.areaGrade)
        self._desenharGrade()

        pygame.draw.rect(self.contexto.tela, COR_PAINEL, self.areaPainel)
        self._desenharPainelResultado()

        self._desenharBotao(self.botaoExecutar, "EXECUTAR")
        self._desenharBotao(self.botaoSincronizar, "USAR LABIRINTO ATUAL (N)")

        rodape = (
            "Clique esquerdo: origem (verde) | Clique direito: destino (vermelho) | "
            "W/S: método | Enter: executar | ESC: voltar"
        )
        self.contexto.tela.blit(self.fonteRodape.render(rodape, True, (170, 170, 170)),
                                 (20, self.contexto.altura - 26))
        if self.mensagemAviso:
            self.contexto.tela.blit(self.fonteRodape.render(self.mensagemAviso, True, COR_AVISO),
                                     (20, self.contexto.altura - 48))

    def _desenharSeletorMetodo(self):
        self._retItensMetodo = []
        alturaLinha = self.fonteItem.get_height() + 10
        for indice, metodo in enumerate(METODOS_DISPONIVEIS):
            y = self.areaSeletor.y + indice * alturaLinha
            retangulo = pygame.Rect(self.areaSeletor.x, y, self.areaSeletor.width, alturaLinha)
            self._retItensMetodo.append(retangulo)

            selecionado = indice == self.indiceSelecionado
            if selecionado:
                pygame.draw.rect(self.contexto.tela, (55, 55, 40), retangulo)
            cor = (255, 235, 59) if selecionado else (225, 225, 225)
            prefixo = "▶ " if selecionado else "  "
            sufixo = " (ponderado)" if metodo.ponderado else ""
            texto = self.fonteItem.render(prefixo + metodo.nome + sufixo, True, cor)
            self.contexto.tela.blit(texto, (retangulo.x + 6, retangulo.y + 5))

    def _desenharGrade(self):
        mapa = self.labirinto.comoGrade()
        origemX, origemY, tamanhoCelula = self._geometriaGrade()

        for l in range(self.labirinto.linhas):
            for c in range(self.labirinto.colunas):
                cor = COR_PAREDE if mapa[l][c] == 9 else COR_LIVRE
                retangulo = pygame.Rect(origemX + c * tamanhoCelula, origemY + l * tamanhoCelula,
                                         tamanhoCelula, tamanhoCelula)
                pygame.draw.rect(self.contexto.tela, cor, retangulo)
                pygame.draw.rect(self.contexto.tela, COR_GRADE, retangulo, 1)

        resultado = self.resultadoAtual
        if resultado and resultado.encontrado:
            corRota = METODOS_DISPONIVEIS[self.indiceSelecionado].corRota
            pontos = [self._centroCelula(origemX, origemY, tamanhoCelula, p.linha, p.coluna) for p in resultado.rota]
            if len(pontos) > 1:
                pygame.draw.lines(self.contexto.tela, corRota, False, pontos, max(2, tamanhoCelula // 6))
            for ponto in pontos:
                pygame.draw.circle(self.contexto.tela, corRota, ponto, max(2, tamanhoCelula // 7))

        self._desenharMarcador(origemX, origemY, tamanhoCelula, self.origem, COR_ORIGEM)
        self._desenharMarcador(origemX, origemY, tamanhoCelula, self.destino, COR_DESTINO)

    @staticmethod
    def _centroCelula(origemX, origemY, tamanhoCelula, linha, coluna):
        return (origemX + coluna * tamanhoCelula + tamanhoCelula // 2,
                origemY + linha * tamanhoCelula + tamanhoCelula // 2)

    def _desenharMarcador(self, origemX, origemY, tamanhoCelula, coordenada, cor):
        centro = self._centroCelula(origemX, origemY, tamanhoCelula, *coordenada)
        pygame.draw.circle(self.contexto.tela, cor, centro, max(3, tamanhoCelula // 3))
        pygame.draw.circle(self.contexto.tela, (20, 20, 20), centro, max(3, tamanhoCelula // 3), 1)

    def _desenharPainelResultado(self):
        x, y = self.areaPainel.x, self.areaPainel.y
        self.contexto.tela.blit(self.fonteTitulo.render("RESULTADO", True, (255, 235, 59)), (x, y))
        y += self.fonteTitulo.get_height() + 10

        resultado = self.resultadoAtual
        if resultado is None:
            texto = self.fonteItem.render("Escolha um método e clique em Executar.", True, (220, 220, 220))
            self.contexto.tela.blit(texto, (x, y))
            return

        if not resultado.encontrado:
            texto = self.fonteItem.render(resultado.observacao or "Caminho não encontrado.", True, (255, 110, 110))
            self.contexto.tela.blit(texto, (x, y))
            y += texto.get_height() + 8
            self.contexto.tela.blit(
                self.fonteItem.render(f"Tempo de execução: {resultado.duracaoMs:.3f} ms", True, (220, 220, 220)), (x, y)
            )
            return

        linhas = [
            (f"Custo do caminho: {resultado.custo}", (140, 230, 160)),
            (f"Passos: {len(resultado.rota) - 1}", (220, 220, 220)),
            (f"Tempo de execução: {resultado.duracaoMs:.3f} ms", (220, 220, 220)),
        ]
        for texto, cor in linhas:
            self.contexto.tela.blit(self.fonteItem.render(texto, True, cor), (x, y))
            y += self.fonteItem.get_height() + 6
        y += 6
        self._desenharTextoComQuebra(x, y, "Caminho: " + resultado.rotaComoTexto())

    def _desenharTextoComQuebra(self, x, y, texto):
        largMax = self.areaPainel.width
        palavras = texto.split(" ")
        linhaAtual = ""
        for palavra in palavras:
            candidata = (linhaAtual + " " + palavra).strip()
            if self.fonteItem.size(candidata)[0] > largMax and linhaAtual:
                self.contexto.tela.blit(self.fonteItem.render(linhaAtual, True, (220, 220, 220)), (x, y))
                y += self.fonteItem.get_height() + 2
                linhaAtual = palavra
            else:
                linhaAtual = candidata
        if linhaAtual:
            self.contexto.tela.blit(self.fonteItem.render(linhaAtual, True, (220, 220, 220)), (x, y))

    def _desenharBotao(self, retangulo, texto):
        cor = (90, 90, 105) if retangulo.collidepoint(pygame.mouse.get_pos()) else (60, 60, 70)
        pygame.draw.rect(self.contexto.tela, cor, retangulo, border_radius=6)
        pygame.draw.rect(self.contexto.tela, (150, 150, 150), retangulo, 1, border_radius=6)
        superficie = self.fonteItem.render(texto, True, (255, 255, 255))
        self.contexto.tela.blit(superficie, superficie.get_rect(center=retangulo.center))
