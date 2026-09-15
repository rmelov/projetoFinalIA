import pygame
import sys
from utilidades import config
from utilidades.controles import Controles

class MenuModosJogo:
    """Gerencia a tela de seleção de modos de jogo baseados nos algoritmos de busca (Do mais fácil ao mais difícil)."""

    def __init__(self, tela, menu_principal):
        self.tela = tela
        self.menu_principal = menu_principal
        self.indice_selecionado = 0

        try:
            self.fonte_titulo = pygame.font.Font(config.FONTE_CAMINHO, int(config.TAMANHO_FONTE_PRINCIPAL * 0.8))
            self.fonte_item = pygame.font.Font(config.FONTE_CAMINHO, int(config.TAMANHO_FONTE_SUB * 0.9))
            self.fonte_descricao = pygame.font.Font(config.FONTE_CAMINHO, int(config.TAMANHO_FONTE_SUB * 0.7))
        except Exception:
            self.fonte_titulo = pygame.font.SysFont("arial", int(config.TAMANHO_FONTE_PRINCIPAL * 0.8))
            self.fonte_item = pygame.font.SysFont("arial", int(config.TAMANHO_FONTE_SUB * 0.9))
            self.fonte_descricao = pygame.font.SysFont("arial", int(config.TAMANHO_FONTE_SUB * 0.7))

        try:
            self.fonte_hover = pygame.font.Font(config.FONTE_CAMINHO, int(config.TAMANHO_FONTE_SUB * 1.1))
        except Exception:
            self.fonte_hover = pygame.font.SysFont("arial", int(config.TAMANHO_FONTE_SUB * 1.1))

        self.modos = [
            {
                "id": "profundidade",
                "nome": "Profundidade",
                "desc": "Avança fundo antes de voltar. Fácil de enganar e se perde em rotas longas."
            },
            {
                "id": "prof_limitada",
                "nome": "Profundidade Limitada",
                "desc": "Restrito a um limite de passos. Se o jogador estiver longe, o perseguidor se perde."
            },
            {
                "id": "aprofundamento_iterativo",
                "nome": "Aprofundamento Iterativo",
                "desc": "Combina profundidade e limites crescentes. Uma ameaça equilibrada."
            },
            {
                "id": "amplitude",
                "nome": "Amplitude",
                "desc": "Explora em camadas e sempre encontra o menor caminho exato até você."
            },
            {
                "id": "bidirecional",
                "nome": "Bidirecional",
                "desc": "Busca simultânea a partir da origem e do destino. Quase impossível escapar!"
            },
            {
                "id": "voltar",
                "nome": "VOLTAR",
                "desc": "Retorna ao menu principal."
            }
        ]

    def executar(self):
        relogio = pygame.time.Clock()
        
        while True:
            self.tela.fill((20, 20, 25))
            self._desenhar()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        return "voltar"
                    else:
                        self.indice_selecionado = Controles.navegar_menu(evento, self.indice_selecionado, len(self.modos))
                        if Controles.confirmar_menu(evento):
                            return self.modos[self.indice_selecionado]["id"]
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        resultado = self._tratar_clique(evento.pos)
                        if resultado:
                            return resultado

            pygame.display.flip()
            relogio.tick(30)

    def _desenhar(self):
        txt_titulo = self.fonte_titulo.render("SELECIONE O MODO DE BUSCA", True, (0, 191, 255))
        rect_titulo = txt_titulo.get_rect(center=(config.LARGURA // 2, 70))
        self.tela.blit(txt_titulo, rect_titulo)

        self.ret_itens = []
        y_inicial = 160
        espacamento = 50
        mouse_pos = pygame.mouse.get_pos()
        
        descricao_ativa = self.modos[self.indice_selecionado]["desc"]

        for i, modo in enumerate(self.modos):
            y_pos = y_inicial + (i * espacamento)
            cor_texto = (255, 100, 100) if modo["id"] == "voltar" else (255, 255, 255)
            base_sup = self.fonte_item.render(modo["nome"], True, cor_texto)
            base_rect = base_sup.get_rect(center=(config.LARGURA // 2, y_pos))

            if base_rect.collidepoint(mouse_pos):
                self.indice_selecionado = i
                descricao_ativa = modo["desc"]

            if i == self.indice_selecionado or base_rect.collidepoint(mouse_pos):
                render_sup = self.fonte_hover.render(modo["nome"], True, (255, 235, 59))
            else:
                render_sup = base_sup

            rect = render_sup.get_rect(center=(config.LARGURA // 2, y_pos))
            self.tela.blit(render_sup, rect)
            self.ret_itens.append((base_rect, modo["id"]))

        if descricao_ativa:
            txt_desc = self.fonte_descricao.render(descricao_ativa, True, (200, 200, 200))
            rect_desc = txt_desc.get_rect(center=(config.LARGURA // 2, config.ALTURA - 80))
            self.tela.blit(txt_desc, rect_desc)

    def _tratar_clique(self, pos):
        for i, (rect, modo_id) in enumerate(self.ret_itens):
            if rect.collidepoint(pos):
                self.indice_selecionado = i
                return modo_id
        return None