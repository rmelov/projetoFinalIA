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
        altura = self.contexto.altura

        panelLargura = 860
        panelAltura = 350
        xPanel = (largura - panelLargura) // 2
        yPanel = (altura - panelAltura) // 2

        painel = pygame.Rect(xPanel, yPanel, panelLargura, panelAltura)
        pygame.draw.rect(self.contexto.tela, (18, 18, 24), painel)
        pygame.draw.rect(self.contexto.tela, (64, 90, 150), painel, 2)

        titulo = self.fontePrincipal.render("ORIGEM E DESTINO", True, (255, 235, 59))
        self.contexto.tela.blit(titulo, titulo.get_rect(center=(largura // 2, yPanel + 52)))

        dica = self.fonteSub.render(
            f"Formato: linha,coluna • Grid {linhas}x{colunas} • Deixe em branco para aleatório",
            True, (170, 170, 180),
        )
        self.contexto.tela.blit(dica, dica.get_rect(center=(largura // 2, yPanel + 88)))

        campoLargura, campoAltura = 290, 56
        yCampos = yPanel + 130
        xOrigem = largura // 2 - campoLargura - 18
        xDestino = largura // 2 + 18

        retOrigem = self._desenharCampo(
            "ORIGEM",
            textoOrigem,
            campoAtivo == "origem",
            xOrigem,
            yCampos,
            campoLargura,
            campoAltura,
        )
        retDestino = self._desenharCampo(
            "DESTINO",
            textoDestino,
            campoAtivo == "destino",
            xDestino,
            yCampos,
            campoLargura,
            campoAltura,
        )

        if mensagemErro:
            erro = self.fonteSub.render(mensagemErro, True, (255, 100, 100))
            self.contexto.tela.blit(erro, erro.get_rect(center=(largura // 2, yPanel + 215)))
            btnY = yPanel + 250
        else:
            btnY = yPanel + 235

        mousePos = pygame.mouse.get_pos()
        botaoTexto = self.fonteItem.render("JOGAR", True, (255, 255, 255))
        botaoRect = botaoTexto.get_rect(center=(largura // 2, btnY))
        larguraBotao = max(170, botaoRect.width + 48)
        alturaBotao = 54
        retBotaoJogar = pygame.Rect(0, 0, larguraBotao, alturaBotao)
        retBotaoJogar.center = (largura // 2, btnY)

        corBotao = (255, 235, 59) if retBotaoJogar.collidepoint(mousePos) else (32, 32, 40)
        corBorda = (255, 235, 59) if retBotaoJogar.collidepoint(mousePos) else (90, 90, 110)
        pygame.draw.rect(self.contexto.tela, corBotao, retBotaoJogar, border_radius=16)
        pygame.draw.rect(self.contexto.tela, corBorda, retBotaoJogar, 2, border_radius=16)

        textoBotao = self.fonteItem.render("JOGAR", True, (255, 255, 255))
        self.contexto.tela.blit(textoBotao, textoBotao.get_rect(center=retBotaoJogar.center))

        rodape = self.fonteSub.render(
            "TAB: trocar campo | Enter: confirmar | ESC: voltar",
            True,
            (140, 140, 145),
        )
        self.contexto.tela.blit(rodape, rodape.get_rect(center=(largura // 2, altura - 44)))

        return retOrigem, retDestino, retBotaoJogar

    def _desenharCampo(self, rotulo, texto, ativo, x, y, largura, altura):
        rotuloSuperficie = self.fonteSub.render(rotulo, True, (211, 220, 240))
        self.contexto.tela.blit(rotuloSuperficie, (x, y - 26))

        retangulo = pygame.Rect(x, y, largura, altura)
        corBorda = COR_CAMPO_ATIVO if ativo else COR_CAMPO_INATIVO
        pygame.draw.rect(self.contexto.tela, (20, 20, 28), retangulo, border_radius=12)
        pygame.draw.rect(self.contexto.tela, corBorda, retangulo, 2, border_radius=12)

        preenchimento = texto or " "
        textoSuperficie = self.fonteItem.render(preenchimento, True, (255, 255, 255))
        self.contexto.tela.blit(
            textoSuperficie,
            (retangulo.x + 14, retangulo.y + (altura - textoSuperficie.get_height()) // 2),
        )
        return retangulo
