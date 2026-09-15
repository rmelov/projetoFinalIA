import os

class GerenciadorRecorde:
    def __init__(self, modo_jogo="amplitude"):
        caminhos_recordes = {
            "amplitude": "componentes/menu/modosJogo/recordes/recordeAmplitude.txt",
            "aprofundamento_iterativo": "componentes/menu/modosJogo/recordes/recordeAprofundamentoIterativo.txt",
            "bidirecional": "componentes/menu/modosJogo/recordes/recordeBidirecional.txt",
            "profundidade": "componentes/menu/modosJogo/recordes/recordeProfundidade.txt",
            "prof_limitada": "componentes/menu/modosJogo/recordes/recordeProfundidadeLimitada.txt"
        }
        
        self.caminho = caminhos_recordes.get(modo_jogo, caminhos_recordes["amplitude"])

    def carregar(self):
        if not os.path.exists(self.caminho):
            return 0, 1
        try:
            with open(self.caminho, "r") as f:
                linhas = f.readlines()
                pontuacao = int(linhas[0].strip()) if len(linhas) > 0 else 0
                nivel = int(linhas[1].strip()) if len(linhas) > 1 else 1
                return pontuacao, nivel
        except (ValueError, IndexError):
            return 0, 1

    def salvar_se_maior(self, pontuacao_atual, nivel_atual):
        pontuacao_salva, _ = self.carregar()
        if pontuacao_atual > pontuacao_salva:
            pasta = os.path.dirname(self.caminho)
            if pasta and not os.path.exists(pasta):
                os.makedirs(pasta, exist_ok=True)
            with open(self.caminho, "w") as f:
                f.write(f"{pontuacao_atual}\n{nivel_atual}\n")
            return True
        return False