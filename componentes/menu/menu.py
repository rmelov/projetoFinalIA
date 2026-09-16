import pygame
import sys
from utilidades import config
from utilidades.controles import Controles
from componentes.menu.modosJogo.modosJogo import MenuModosJogo

class MenuPrincipal:
    """Gerencia o menu principal e a navegação entre as telas (Jogar, Tutorial, Sobre)."""

    def __init__(self, tela, gerenciador_jogo):
        self.tela = tela
        self.gerenciador_jogo = gerenciador_jogo
        self.estado_atual = "principal"
        self.modo_selecionado = "amplitude"  
        self.menu_modos = MenuModosJogo(tela, self)
        
        self.opcoes_principal = ["JOGAR", "TUTORIAL", "SOBRE", "SAIR"]
        self.indice_selecionado = 0
        self.input_origem = ""
        self.input_destino = ""
        self.input_ativo = None
        self.ret_btn_jogar = None

        try:
            self.fonte_titulo = pygame.font.Font(config.FONTE_CAMINHO, config.TAMANHO_FONTE_PRINCIPAL)
            self.fonte_texto = pygame.font.Font(config.FONTE_CAMINHO, config.TAMANHO_FONTE_SUB)
        except Exception:
            self.fonte_titulo = pygame.font.SysFont("arial", config.TAMANHO_FONTE_PRINCIPAL)
            self.fonte_texto = pygame.font.SysFont("arial", config.TAMANHO_FONTE_SUB)

        try:
            self.fonte_hover = pygame.font.Font(config.FONTE_CAMINHO, int(config.TAMANHO_FONTE_SUB * 1.25))
        except Exception:
            self.fonte_hover = pygame.font.SysFont("arial", int(config.TAMANHO_FONTE_SUB * 1.25))

    def executar(self):
        relogio = pygame.time.Clock()
        
        while True:
            self.tela.fill((20, 20, 25))
            
            if self.estado_atual == "principal":
                self._desenhar_menu_principal()
            elif self.estado_atual == "configurar_campos":
                self._desenhar_configurar_campos()
            elif self.estado_atual == "modo_jogo":
                resultado_modo = self.menu_modos.executar()
                if resultado_modo == "voltar":
                    self.estado_atual = "principal"
                elif resultado_modo in ["amplitude", "profundidade", "prof_limitada", "aprofundamento_iterativo", "bidirecional"]:
                    self.modo_selecionado = resultado_modo
                    # Após escolher modo, abrir diálogo para origem/destino antes de iniciar
                    self.estado_atual = "configurar_campos"
                    self.input_origem = ""
                    self.input_destino = ""
                    self.input_ativo = None
                    self.ret_btn_jogar = None
            elif self.estado_atual == "tutorial":
                self._desenhar_tutorial()
            elif self.estado_atual == "sobre":
                self._desenhar_sobre()
            elif self.estado_atual == "jogando":
                self.gerenciador_jogo.executar(modo_jogo=self.modo_selecionado)
                self.estado_atual = "principal"

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_ESCAPE:
                        if self.estado_atual == "principal":
                            pygame.quit()
                            sys.exit()
                        else:
                            self.estado_atual = "principal"
                    elif self.estado_atual == "principal":
                        self.indice_selecionado = Controles.navegar_menu(evento, self.indice_selecionado, len(self.opcoes_principal))
                        if Controles.confirmar_menu(evento):
                            self._executar_opcao_selecionada()
                    elif self.estado_atual in ("tutorial", "sobre"):
                        if Controles.confirmar_menu(evento) or evento.key in (pygame.K_RETURN, pygame.K_SPACE):
                            self.estado_atual = "principal"
                    elif self.estado_atual == "configurar_campos":
                        # Tratamento de digitação nos campos do diálogo
                        if evento.key == pygame.K_RETURN and self.input_ativo is None:
                            # Enter sem campo ativo: tentar iniciar jogo
                            self._iniciar_jogo_com_campos()
                        elif evento.key == pygame.K_ESCAPE:
                            self.estado_atual = "principal"
                        elif evento.key == pygame.K_BACKSPACE:
                            if self.input_ativo == "origem":
                                self.input_origem = self.input_origem[:-1]
                            elif self.input_ativo == "destino":
                                self.input_destino = self.input_destino[:-1]
                        else:
                            tecla_texto = evento.unicode
                            if tecla_texto and tecla_texto in "0123456789,() ":
                                if self.input_ativo == "origem":
                                    self.input_origem += tecla_texto
                                elif self.input_ativo == "destino":
                                    self.input_destino += tecla_texto
                elif evento.type == pygame.MOUSEBUTTONDOWN:
                    if evento.button == 1:
                        # Em tela de configuração, tratar cliques especiais
                        if self.estado_atual == "configurar_campos":
                            self._tratar_clique_config(evento.pos)
                        else:
                            self._tratar_clique(evento.pos)

            pygame.display.flip()
            relogio.tick(30)

    def _desenhar_menu_principal(self):
        txt_titulo = self.fonte_titulo.render(config.TITULO, True, (255, 235, 59))
        rect_titulo = txt_titulo.get_rect(center=(config.LARGURA // 2, config.ALTURA // 4))
        self.tela.blit(txt_titulo, rect_titulo)

        y_inicial = config.ALTURA // 2 - 40
        espacamento = 70
        mouse_pos = pygame.mouse.get_pos()

        self.ret_botoes = []
        for i, texto in enumerate(self.opcoes_principal):
            y_pos = y_inicial + (i * espacamento)
            superficie_base = self.fonte_texto.render(texto, True, (255, 255, 255))
            retangulo_base = superficie_base.get_rect(center=(config.LARGURA // 2, y_pos))

            if retangulo_base.collidepoint(mouse_pos):
                self.indice_selecionado = i

            if i == self.indice_selecionado or retangulo_base.collidepoint(mouse_pos):
                superficie_renderizada = self.fonte_hover.render(texto, True, (255, 235, 59))
            else:
                superficie_renderizada = superficie_base

            retangulo = superficie_renderizada.get_rect(center=(config.LARGURA // 2, y_pos))
            self.tela.blit(superficie_renderizada, retangulo)
            self.ret_botoes.append((retangulo_base, i))

    def _desenhar_tutorial(self):
        txt_titulo = self.fonte_titulo.render("TUTORIAL", True, (0, 255, 127))
        rect_titulo = txt_titulo.get_rect(center=(config.LARGURA // 2, config.ALTURA // 4))
        self.tela.blit(txt_titulo, rect_titulo)

        txt_info = self.fonte_texto.render("Use WASD/Setas para mover. Fuja do Inimigo!", True, (200, 200, 200))
        rect_info = txt_info.get_rect(center=(config.LARGURA // 2, config.ALTURA // 2))
        self.tela.blit(txt_info, rect_info)

        self.ret_voltar = self._desenhar_botao("VOLTAR", config.ALTURA // 2 + 100)

    def _desenhar_sobre(self):
        txt_titulo = self.fonte_titulo.render("SOBRE", True, (255, 105, 180))
        rect_titulo = txt_titulo.get_rect(center=(config.LARGURA // 2, config.ALTURA // 4))
        self.tela.blit(txt_titulo, rect_titulo)

        txt_info = self.fonte_texto.render("Labirinto Isométrico desenvolvido em Python com Pygame.", True, (200, 200, 200))
        rect_info = txt_info.get_rect(center=(config.LARGURA // 2, config.ALTURA // 2))
        self.tela.blit(txt_info, rect_info)

        self.ret_voltar = self._desenhar_botao("VOLTAR", config.ALTURA // 2 + 100)

    def _desenhar_configurar_campos(self):
        # Caixa de diálogo central para inserir origem e destino
        largura = 860
        altura = 320
        x = (config.LARGURA - largura) // 2
        y = (config.ALTURA - altura) // 2

        fundo = pygame.Surface((largura, altura))
        fundo.fill((30, 30, 35))
        pygame.draw.rect(fundo, (200, 200, 200), fundo.get_rect(), 2)

        titulo = self.fonte_texto.render("Configurar Origem e Destino", True, (255, 235, 59))
        fundo.blit(titulo, (20, 12))

        pad_x = 20
        label_largura = 140
        current_y = 70
        linha_altura = self.fonte_texto.get_height()
        altura_campo = 36

        # Origem (label e caixa na mesma linha)
        label_ori = self.fonte_texto.render("Origem:", True, (255, 255, 255))
        fundo.blit(label_ori, (pad_x, current_y + 30 + (altura_campo - linha_altura) // 2))
        origem_rect = pygame.Rect(pad_x + label_largura + 20, current_y + 15, 360, altura_campo)
        cor_o = (100, 100, 100) if getattr(self, 'input_ativo', None) == 'origem' else (60, 60, 60)
        pygame.draw.rect(fundo, cor_o, origem_rect)
        pygame.draw.rect(fundo, (150, 150, 150), origem_rect, 1)
        txt_ori = self.fonte_texto.render(self.input_origem if self.input_origem else "(x,y)", True, (255, 255, 255))
        fundo.blit(txt_ori, (origem_rect.x + 8, origem_rect.y + 13 + (origem_rect.h - txt_ori.get_height()) // 2))

        current_y = origem_rect.y + origem_rect.h + 24

        # Destino (label e caixa na mesma linha)
        label_dest = self.fonte_texto.render("Destino:", True, (255, 255, 255))
        fundo.blit(label_dest, (pad_x, current_y + 30 + (altura_campo - linha_altura) // 2))
        destino_rect = pygame.Rect(pad_x + label_largura + 20, current_y + 15, 360, altura_campo)
        cor_d = (100, 100, 100) if getattr(self, 'input_ativo', None) == 'destino' else (60, 60, 60)
        pygame.draw.rect(fundo, cor_d, destino_rect)
        pygame.draw.rect(fundo, (150, 150, 150), destino_rect, 1)
        txt_dest = self.fonte_texto.render(self.input_destino if self.input_destino else "(x,y)", True, (255, 255, 255))
        fundo.blit(txt_dest, (destino_rect.x + 8, destino_rect.y + 13 + (destino_rect.h - txt_dest.get_height()) // 2))

        mouse_pos = pygame.mouse.get_pos()
        btn_base = self.fonte_titulo.render("JOGAR", True, (255, 255, 255))
        btn_hover = self.fonte_titulo.render("JOGAR", True, (255, 235, 59))
        btn_y = destino_rect.y + destino_rect.h + 90

        btn_rect_tela = btn_base.get_rect(center=(x + largura // 2, y + btn_y))
        if btn_rect_tela.collidepoint(mouse_pos):
            btn_surface = btn_hover
        else:
            btn_surface = btn_base

        btn_rect_local = btn_surface.get_rect(center=(largura // 2, btn_y))
        fundo.blit(btn_surface, btn_rect_local)

        self._config_dialog_rects = {
            'origem': pygame.Rect(x + origem_rect.x, y + origem_rect.y, origem_rect.w, origem_rect.h),
            'destino': pygame.Rect(x + destino_rect.x, y + destino_rect.y, destino_rect.w, destino_rect.h),
            'jogar': pygame.Rect(x + btn_rect_local.x, y + btn_rect_local.y, btn_rect_local.w, btn_rect_local.h)
        }

        self.tela.blit(fundo, (x, y))

    def _tratar_clique_config(self, pos):
        # Checa se clique foi em algum campo ou botão do diálogo
        if not hasattr(self, '_config_dialog_rects'):
            return
        if self._config_dialog_rects['origem'].collidepoint(pos):
            self.input_ativo = 'origem'
        elif self._config_dialog_rects['destino'].collidepoint(pos):
            self.input_ativo = 'destino'
        elif self._config_dialog_rects['jogar'].collidepoint(pos):
            self._iniciar_jogo_com_campos()
        else:
            # clique fora: desativar campo
            self.input_ativo = None

    def _iniciar_jogo_com_campos(self):
        # Transfere os campos para o gerenciador de jogo e inicia
        self.gerenciador_jogo.texto_origem = getattr(self, 'input_origem', '') or ""
        self.gerenciador_jogo.texto_destino = getattr(self, 'input_destino', '') or ""
        self.gerenciador_jogo.campo_ativo = None
        self.gerenciador_jogo.executar(modo_jogo=self.modo_selecionado)
        self.estado_atual = 'principal'
    
    def _desenhar_botao(self, texto, y):
        superficie_base = self.fonte_texto.render(texto, True, (255, 255, 255))
        retangulo_base = superficie_base.get_rect(center=(config.LARGURA // 2, y))

        if retangulo_base.collidepoint(pygame.mouse.get_pos()):
            superficie_renderizada = self.fonte_hover.render(texto, True, (255, 235, 59))
        else:
            superficie_renderizada = superficie_base

        retangulo = superficie_renderizada.get_rect(center=(config.LARGURA // 2, y))
        self.tela.blit(superficie_renderizada, retangulo)
        return retangulo_base

    def _executar_opcao_selecionada(self):
        opcao = self.opcoes_principal[self.indice_selecionado]
        if opcao == "JOGAR":
            self.estado_atual = "modo_jogo"
        elif opcao == "TUTORIAL":
            self.estado_atual = "tutorial"
        elif opcao == "SOBRE":
            self.estado_atual = "sobre"
        elif opcao == "SAIR":
            pygame.quit()
            sys.exit()

    def _tratar_clique(self, pos):
        if self.estado_atual == "principal":
            for rect, indice in self.ret_botoes:
                if rect.collidepoint(pos):
                    self.indice_selecionado = indice
                    self._executar_opcao_selecionada()
                    break
        elif self.estado_atual in ("tutorial", "sobre"):
            if hasattr(self, 'ret_voltar') and self.ret_voltar.collidepoint(pos):
                self.estado_atual = "principal"