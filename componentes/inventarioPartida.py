class InventarioPartida:
    def __init__(self):
        self.itens_temporarios = []

    def adicionar_item(self, item):
        self.itens_temporarios.append(item)

    def remover_ultimo(self):
        if self.itens_temporarios:
            return self.itens_temporarios.pop()
        return None

    def esvaziar(self):
        itens = self.itens_temporarios.copy()
        self.itens_temporarios.clear()
        return itens

    def resgatar_itens(self):
        itens = self.itens_temporarios.copy()
        self.itens_temporarios.clear()
        return itens

    def contar_itens(self):
        return len(self.itens_temporarios)