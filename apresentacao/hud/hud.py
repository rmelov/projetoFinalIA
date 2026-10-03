"""
Interface de status (HUD). Substitui RenderizadorHud, removendo:
- `calcular_posicoes_campos`, um método morto (recalculava um layout que
  nenhum consumidor usava);
- os parâmetros `texto_origem`, `texto_destino`, `campo_ativo`, que
  atravessavam duas camadas sem nenhum efeito.
"""
from apresentacao.hud.painelRecorde import PainelRecorde

PADDING_X = 15
PADDING_Y = 12
ESPACAMENTO_VERTICAL = 8


class Hud:
    def __init__(self, tela, fontePrincipal, fonteSub):
        self.tela = tela
        self.fontePrincipal = fontePrincipal
        self.fonteSub = fonteSub
        self.painelRecorde = PainelRecorde(fonteSub)

    def desenhar(self, largura, altura, partida, tempoMs, renderizadorItens, repositorioRecorde):
        if partida.vitoria or partida.derrota:
            self._desenharTelaFim(largura, partida)
            self.painelRecorde.desenhar(self.tela, repositorioRecorde, partida.metodoId, altura)
            return

        status = self._textoStatus(partida, tempoMs)
        dica = self.fonteSub.render(f"Controles: WASD/Setas | {status} | R: Reiniciar", True, (200, 200, 200))
        yDica = PADDING_Y + self.fonteSub.get_height() + 6
        self.tela.blit(dica, (PADDING_X, yDica))

        nivel = self.fonteSub.render(f"Nível: {partida.nivelAtual}", True, (255, 200, 100))
        self.tela.blit(nivel, ((largura - nivel.get_width()) // 2, PADDING_Y))

        pontos = self.fonteSub.render(f"Pontos: {partida.obterPontuacaoTotal()}", True, (255, 215, 0))
        yPontos = yDica + dica.get_height() + 12
        self.tela.blit(pontos, (PADDING_X, yPontos))

        ySlot = yPontos + pontos.get_height() + ESPACAMENTO_VERTICAL
        self._desenharSlotItem(renderizadorItens, partida.pocao, partida.contarTotalItens(), PADDING_X, ySlot)

        self.painelRecorde.desenhar(self.tela, repositorioRecorde, partida.metodoId, altura)

    def _textoStatus(self, partida, tempoMs):
        if not partida.jogoIniciado:
            return "Movimente-se para iniciar..."
        if partida.pocao.ativa:
            tempoRestanteS = max(0, (partida.pocao.tempoFim - tempoMs) // 1000 + 1)
            return f"POÇÃO ATIVA ({tempoRestanteS}s)"
        return "Espaço para usar a poção"

    def _desenharSlotItem(self, renderizadorItens, item, quantidade, x, y):
        if not (renderizadorItens and item):
            return
        imagem = renderizadorItens.imagemDoItem(item)
        alturaSlot = max(28, self.fonteSub.get_height())
        self.tela.blit(imagem, (x, y + (alturaSlot - imagem.get_height()) // 2))
        texto = self.fonteSub.render(f"x{quantidade}", True, (255, 255, 255))
        self.tela.blit(texto, (x + 34, y + (alturaSlot - texto.get_height()) // 2))

    def _desenharTelaFim(self, largura, partida):
        textoStr = "VOCÊ VENCEU!" if partida.vitoria else "VOCÊ PERDEU!"
        cor = (100, 255, 100) if partida.vitoria else (255, 100, 100)

        texto = self.fontePrincipal.render(textoStr, True, cor)
        subPontos = self.fonteSub.render(f"Pontuação Total: {partida.obterPontuacaoTotal()}", True, (255, 255, 255))
        subDica = self.fonteSub.render("Pressione 'R' para reiniciar", True, (200, 200, 200))

        centroX = largura // 2
        self.tela.blit(texto, (centroX - texto.get_width() // 2, 30))
        self.tela.blit(subPontos, (centroX - subPontos.get_width() // 2, 30 + texto.get_height() + 10))
        self.tela.blit(subDica, (centroX - subDica.get_width() // 2, 30 + texto.get_height() + subPontos.get_height() + 20))
