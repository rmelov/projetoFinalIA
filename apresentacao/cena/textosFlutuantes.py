"""Mostra e anima os textos "+N"/"-N" que sobem e desaparecem."""


class GerenciadorTextosFlutuantes:
    def __init__(self, conversor):
        self.conversor = conversor
        self._textos = []

    def adicionar(self, texto, coordenada, cor=(0, 255, 255)):
        isoX, isoY = self.conversor.cartesianoParaIsometrico(coordenada.linha, coordenada.coluna)
        y = isoY + (self.conversor.alturaTile // 2)
        self._textos.append({
            "texto": texto, "x": isoX, "y": float(y), "cor": cor,
            "opacidade": 255, "velocidadeY": 0.5, "duracaoMax": 60, "duracao": 60,
        })

    def atualizarEDesenhar(self, tela, fonte):
        for i in range(len(self._textos) - 1, -1, -1):
            tf = self._textos[i]
            tf["y"] -= tf["velocidadeY"]
            tf["duracao"] -= 1
            tf["opacidade"] = max(0, int(255 * (tf["duracao"] / tf["duracaoMax"])))

            if tf["duracao"] <= 0:
                self._textos.pop(i)
                continue

            superficie = fonte.render(tf["texto"], True, tf["cor"])
            if tf["opacidade"] < 255:
                superficie = superficie.convert_alpha()
                superficie.set_alpha(tf["opacidade"])

            rect = superficie.get_rect(center=(tf["x"], tf["y"]))
            tela.blit(superficie, rect.topleft)
