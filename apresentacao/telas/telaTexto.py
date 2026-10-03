"""Tela de texto genérica: serve tanto o tutorial quanto o 'sobre'. No
projeto original, componentes/menu/sobre.py e tutorial.py existiam mas
estavam completamente vazios — nunca tinham sido implementados."""
import sys

import pygame

TUTORIAL = {
    "titulo": "TUTORIAL",
    "linhas": [
        "Mova-se com W A S D ou as setas do teclado.",
        "Alcance a saída (marcada no labirinto) para vencer a fase.",
        "Fuja do perseguidor e do rastro que ele deixa para trás.",
        "Colete poções de coragem: usando uma (Espaço), você atravessa",
        "o rastro do perseguidor sem ser pego, por um tempo limitado.",
        "O vórtex embaralha o labirinto ao ser tocado — use com cautela.",
        "Pressione 'R' a qualquer momento para reiniciar a fase.",
        "",
        "Experimente também o LABORATÓRIO DE BUSCA, no menu principal,",
        "para comparar lado a lado os 9 métodos de busca do projeto.",
    ],
}

SOBRE = {
    "titulo": "SOBRE",
    "linhas": [
        "Labirinto Isométrico Aleatório — projeto final de Inteligência Artificial.",
        "",
        "Os métodos de busca (amplitude, profundidade, profundidade limitada,",
        "aprofundamento iterativo, bidirecional, custo uniforme, greedy,",
        "A-estrela e AIA-estrela) são implementados com base no código",
        "disponibilizado pelo professor, em algoritmos/busca/.",
        "",
        "Consulte o ReadMe.txt para instruções completas de execução.",
    ],
}


class TelaTexto:
    def __init__(self, contexto, fontes, conteudo):
        self.contexto = contexto
        self.fontePrincipal = fontes.obter(40)
        self.fonteTexto = fontes.obter(20)
        self.conteudo = conteudo

    def executar(self):
        relogio = pygame.time.Clock()
        while True:
            self.contexto.tela.fill((15, 15, 20))
            self._desenhar()
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if evento.type == pygame.KEYDOWN and evento.key in (pygame.K_ESCAPE, pygame.K_RETURN):
                    return
                if evento.type == pygame.MOUSEBUTTONDOWN:
                    return
            pygame.display.flip()
            relogio.tick(30)

    def _desenhar(self):
        largura = self.contexto.largura
        titulo = self.fontePrincipal.render(self.conteudo["titulo"], True, (255, 235, 59))
        self.contexto.tela.blit(titulo, ((largura - titulo.get_width()) // 2, 40))

        y = 130
        for linha in self.conteudo["linhas"]:
            superficie = self.fonteTexto.render(linha, True, (220, 220, 220))
            self.contexto.tela.blit(superficie, (largura // 2 - 380, y))
            y += superficie.get_height() + 10

        rodape = self.fonteTexto.render("Pressione ESC, Enter ou clique para voltar", True, (140, 140, 140))
        self.contexto.tela.blit(rodape, ((largura - rodape.get_width()) // 2, self.contexto.altura - 50))
