"""Decide qual tela está ativa e os leva de uma para outra. Substitui a
máquina de estados que antes vivia dentro de MenuPrincipal, junto com mais
cinco outras responsabilidades."""
from apresentacao.loopJogo import LoopJogo
from apresentacao.recursos.fontes import Fontes
from apresentacao.telas.telaCoordenadas import TelaCoordenadas
from apresentacao.telas.telaLaboratorioBusca import TelaLaboratorioBusca
from apresentacao.telas.telaMenu import TelaMenu
from apresentacao.telas.telaModos import TelaModos
from apresentacao.telas.telaTexto import SOBRE, TUTORIAL, TelaTexto


class NavegadorTelas:
    """Ponto único de entrada: `executar()` roda até o jogador escolher SAIR."""

    def __init__(self, contexto, conversor, buscador, repositorioRecorde):
        self.contexto = contexto
        fontes = Fontes()

        self.telaMenu = TelaMenu(contexto, fontes)
        self.telaModos = TelaModos(contexto, fontes)
        self.telaCoordenadas = TelaCoordenadas(contexto, fontes)
        self.telaTutorial = TelaTexto(contexto, fontes, TUTORIAL)
        self.telaSobre = TelaTexto(contexto, fontes, SOBRE)
        self.loopJogo = LoopJogo(contexto, conversor, buscador, repositorioRecorde)
        self.telaLaboratorio = TelaLaboratorioBusca(
            contexto, fontes, buscador, obterPartidaAtual=lambda: self.loopJogo.partida
        )

    def executar(self):
        while True:
            opcao = self.telaMenu.executar()

            if opcao == "JOGAR":
                self._fluxoJogar()
            elif opcao == "LABORATÓRIO DE BUSCA":
                self.telaLaboratorio.executar()
            elif opcao == "TUTORIAL":
                self.telaTutorial.executar()
            elif opcao == "SOBRE":
                self.telaSobre.executar()
            elif opcao == "SAIR":
                return

    def _fluxoJogar(self):
        metodoId = self.telaModos.executar()
        if metodoId == "voltar":
            return

        dimensoesProvisorias = (15, 15)  # a Partida define o tamanho real pelo nível
        resultado = self.telaCoordenadas.executar(dimensoesProvisorias)
        if resultado is None:
            return

        textoOrigem, textoDestino = resultado
        self.loopJogo.executar(metodoId=metodoId, textoOrigem=textoOrigem, textoDestino=textoDestino)
