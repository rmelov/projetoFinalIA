"""Tela para digitar (opcionalmente) origem e destino personalizados antes
de iniciar a partida. Extraída de dentro de menu.py, que antes fazia isso
junto com mais cinco outras responsabilidades."""
import sys

import pygame

from dominio.coordenadas.coordenadasTexto import ValidadorCoordenada
from apresentacao.ui.botao import Botao

COR_CAMPO_ATIVO = (255, 235, 59)
COR_CAMPO_INATIVO = (90, 90, 100)


class TelaCoordenadas:
    def __init__(self, contexto, fontes):
        self.contexto = contexto
        self.fontePrincipal = fontes.obter(36)
        self.fonteItem = fontes.obter(22)
        self.fonteSub = fontes.obter(16)

    def executar(self, dimensoes):
        """Devolve (textoOrigem, textoDestino) ou None se o jogador voltar."""
        linhas, colunas = dimensoes
        textoOrigem, textoDestino = "", ""
        campoAtivo = None
        mensagemErro = ""

        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((15, 15, 20))
            retCampoOrigem, retCampoDestino, retBotaoJogar = self._desenhar(
                textoOrigem, textoDestino, campoAtivo, mensagemErro, linhas, colunas
            )

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return None
                    if evento.key == pygame.K_TAB:
                        campoAtivo = "destino" if campoAtivo == "origem" else "origem"
                    elif campoAtivo and evento.key == pygame.K_BACKSPACE:
                        if campoAtivo == "origem":
                            textoOrigem = textoOrigem[:-1]
                        else:
                            textoDestino = textoDestino[:-1]
                    elif campoAtivo and evento.unicode and (evento.unicode.isdigit() or evento.unicode in ",-() "):
                        if campoAtivo == "origem":
                            textoOrigem += evento.unicode
                        else:
                            textoDestino += evento.unicode
                    elif evento.key == pygame.K_RETURN:
                        resultado = self._confirmar(textoOrigem, textoDestino, linhas, colunas)
                        if resultado is not None:
                            return resultado
                        mensagemErro = self._ultimaMensagemErro

                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if retCampoOrigem.collidepoint(evento.pos):
                        campoAtivo = "origem"
                    elif retCampoDestino.collidepoint(evento.pos):
                        campoAtivo = "destino"
                    elif retBotaoJogar.collidepoint(evento.pos):
                        resultado = self._confirmar(textoOrigem, textoDestino, linhas, colunas)
                        if resultado is not None:
                            return resultado
                        mensagemErro = self._ultimaMensagemErro

            pygame.display.flip()
            relogio.tick(30)

    def _confirmar(self, textoOrigem, textoDestino, linhas, colunas):
        resultadoValidacao = ValidadorCoordenada.validarPar(textoOrigem, textoDestino, linhas, colunas)
        if resultadoValidacao.valida:
            return (textoOrigem, textoDestino)
        self._ultimaMensagemErro = resultadoValidacao.mensagemErro
        return None

    def _desenhar(self, textoOrigem, textoDestino, campoAtivo, mensagemErro, linhas, colunas):
        largura = self.contexto.largura
        titulo = self.fontePrincipal.render("ORIGEM E DESTINO (opcional)", True, (255, 235, 59))
        self.contexto.tela.blit(titulo, ((largura - titulo.get_width()) // 2, 60))

        dica = self.fonteSub.render(
            f"Formato: linha,coluna — grid {linhas}x{colunas}. Deixe em branco para aleatório.",
            True, (170, 170, 170),
        )
        self.contexto.tela.blit(dica, ((largura - dica.get_width()) // 2, 110))

        campoLargura, campoAltura = 220, 40
        yOrigem = 170
        retOrigem = self._desenharCampo("Origem", textoOrigem, campoAtivo == "origem",
                                         largura // 2 - campoLargura - 10, yOrigem, campoLargura, campoAltura)
        retDestino = self._desenharCampo("Destino", textoDestino, campoAtivo == "destino",
                                          largura // 2 + 10, yOrigem, campoLargura, campoAltura)

        if mensagemErro:
            erro = self.fonteSub.render(mensagemErro, True, (255, 90, 90))
            self.contexto.tela.blit(erro, ((largura - erro.get_width()) // 2, yOrigem + 70))

        botaoJogar = Botao("JOGAR", (largura // 2, yOrigem + 140), self.fonteItem)
        retJogar = botaoJogar.desenhar(self.contexto.tela)

        rodape = self.fonteSub.render("TAB: trocar campo | Enter: confirmar | ESC: voltar", True, (140, 140, 140))
        self.contexto.tela.blit(rodape, ((largura - rodape.get_width()) // 2, self.contexto.altura - 40))

        return retOrigem, retDestino, retJogar

    def _desenharCampo(self, rotulo, texto, ativo, x, y, largura, altura):
        rotuloSuperficie = self.fonteSub.render(rotulo, True, (200, 200, 200))
        self.contexto.tela.blit(rotuloSuperficie, (x, y - 22))

        retangulo = pygame.Rect(x, y, largura, altura)
        cor = COR_CAMPO_ATIVO if ativo else COR_CAMPO_INATIVO
        pygame.draw.rect(self.contexto.tela, (30, 30, 36), retangulo)
        pygame.draw.rect(self.contexto.tela, cor, retangulo, 2)

        textoSuperficie = self.fonteItem.render(texto or " ", True, (255, 255, 255))
        self.contexto.tela.blit(textoSuperficie, (retangulo.x + 8, retangulo.y + (altura - textoSuperficie.get_height()) // 2))
        return retangulo
