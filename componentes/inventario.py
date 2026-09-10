class Inventario:
    def __init__(self):
        self.itens_consolidados = []

    def adicionar_consolidado(self, item):
        self.itens_consolidados.append(item)

    def adicionar_lote(self, lista_itens):
        self.itens_consolidados.extend(lista_itens)

    def remover_ultimo(self):
        if self.itens_consolidados:
            return self.itens_consolidados.pop()
        return None

    def limpar(self):
        self.itens_consolidados.clear()

    def contar_total(self):
        return len(self.itens_consolidados)

    def listar_itens(self):
        return self.itens_consolidados