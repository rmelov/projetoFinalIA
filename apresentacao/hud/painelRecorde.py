"""Mostra o recorde salvo no canto inferior esquerdo. Lê de
RepositorioRecorde, que já cacheia em memória — antes, este painel abria e
lia o arquivo de recorde a cada frame (~30 vezes por segundo)."""


class PainelRecorde:
    def __init__(self, fonte):
        self.fonte = fonte

    def desenhar(self, tela, repositorioRecorde, metodoId, alturaTela):
        if not repositorioRecorde:
            return
        pontuacaoMaxima, nivelMaximo = repositorioRecorde.carregar(metodoId)
        texto = f"recorde: nível {nivelMaximo} | {pontuacaoMaxima}pts"
        superficie = self.fonte.render(texto, True, (150, 150, 150))
        tela.blit(superficie, (15, alturaTela - superficie.get_height() - 15))
