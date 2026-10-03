"""Diz se um segmento de rota está atrás de uma parede (para desenhá-lo
tracejado). Antes, este mesmo bloco de laços estava duplicado em
RenderizadorFarejo e RenderizadorRotaSaida."""


class DetectorOclusao:
    @staticmethod
    def estaAtrasDeParede(mapa, linha1, coluna1, linha2, coluna2) -> bool:
        linhasMapa = len(mapa)
        colunasMapa = len(mapa[0]) if linhasMapa > 0 else 0
        medioLinha = (linha1 + linha2) // 2
        medioColuna = (coluna1 + coluna2) // 2

        for deltaLinha in (-1, 0, 1):
            for deltaColuna in (-1, 0, 1):
                vl, vc = medioLinha + deltaLinha, medioColuna + deltaColuna
                if 0 <= vl < linhasMapa and 0 <= vc < colunasMapa and mapa[vl][vc] == 9:
                    if vl >= linha1 and vc >= coluna1:
                        return True
        return False
