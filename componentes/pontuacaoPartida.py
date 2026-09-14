class PontuacaoPartida:
    def __init__(self):
        self.pontos = 0

    def adicionar(self, quantidade):
        self.pontos += quantidade

    def esvaziar(self):
        self.pontos = 0

    def resgatar_pontos(self):
        total = self.pontos
        self.esvaziar()
        return total