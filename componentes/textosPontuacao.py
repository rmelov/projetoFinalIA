import pygame

class GerenciadorTextosFlutuantes:
    def __init__(self, conversor):
        self.conversor = conversor
        self.textos_flutuantes = []

    def adicionar(self, texto, r, c, cor=(0, 255, 255)):
        iso_x, iso_y = self.conversor.cartesiano_para_isometrico(r, c)
        largura_tile = self.conversor.largura_tile
        altura_tile = self.conversor.altura_tile

        x = iso_x
        y = iso_y + (altura_tile // 2)

        self.textos_flutuantes.append({
            "texto": texto,
            "x": x,
            "y": float(y),
            "cor": cor,
            "opacidade": 255,
            "velocidade_y": 0.5,
            "duracao_max": 60,
            "duracao": 60
        })

    def atualizar_e_desenhar(self, tela, fonte):
        for i in range(len(self.textos_flutuantes) - 1, -1, -1):
            tf = self.textos_flutuantes[i]

            tf["y"] -= tf["velocidade_y"]
            tf["duracao"] -= 1
            tf["opacidade"] = max(0, int(255 * (tf["duracao"] / tf["duracao_max"])))

            if tf["duracao"] <= 0:
                self.textos_flutuantes.pop(i)
                continue

            superficie_texto = fonte.render(tf["texto"], True, tf["cor"])
            
            if tf["opacidade"] < 255:
                superficie_texto = superficie_texto.convert_alpha()
                superficie_texto.set_alpha(tf["opacidade"])

            rect = superficie_texto.get_rect(center=(tf["x"], tf["y"]))
            tela.blit(superficie_texto, rect.topleft)