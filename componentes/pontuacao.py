class Pontuacao:
    def __init__(self, pontuacao_inicial=0):
        self.valor = pontuacao_inicial

    def adicionar(self, quantidade):
        self.valor += quantidade

    def subtrair(self, quantidade):
        self.valor -= quantidade

    def resetar(self):
        self.valor = 0