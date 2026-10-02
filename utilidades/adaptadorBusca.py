import importlib.util
import os
import sys

BUSCA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'algoritmos', 'busca'))
if BUSCA_DIR not in sys.path:
    sys.path.insert(0, BUSCA_DIR)

spec = importlib.util.spec_from_file_location(
    "BuscaP_modulo",
    os.path.join(BUSCA_DIR, "BuscaP.py")
)
if spec is None or spec.loader is None:
    raise ImportError("Não foi possível carregar BuscaP.py")

BuscaP_modulo = importlib.util.module_from_spec(spec)
spec.loader.exec_module(BuscaP_modulo)

from algoritmos.busca.buscaNP import buscaNP
buscaP = BuscaP_modulo.buscaP


class AdaptadorBusca:
    """Adaptador para chamar os algoritmos de busca do professor sem alterar BuscaP.py."""

    def __init__(self):
        self.buscador_np = buscaNP()
        self.buscador_p = buscaP()

    def _executar_pesado(self, metodo_id, origem, destino, grade, linhas, colunas):
        try:
            if metodo_id == "custo_uniforme":
                return self.buscador_p.custo_uniforme_grid(origem, destino, grade, linhas, colunas)
            if metodo_id == "greedy":
                return self.buscador_p.greedy_grid(origem, destino, grade, linhas, colunas)
            if metodo_id == "a_estrela":
                return self.buscador_p.a_estrela_grid(origem, destino, grade, linhas, colunas)
            if metodo_id == "aia_estrela":
                return self.buscador_p.aia_estrela_grid(origem, destino, grade, linhas, colunas)
        except Exception:
            return self.buscador_np.amplitude_grid(origem, destino, linhas, colunas, grade)

        return self.buscador_np.amplitude_grid(origem, destino, linhas, colunas, grade)

    def _mapear_metodo(self, metodo_id):
        if metodo_id == "profundidade":
            return lambda origem, destino, grade, linhas, colunas: self.buscador_np.profundidade_grid(origem, destino, linhas, colunas, grade)
        if metodo_id == "prof_limitada":
            return lambda origem, destino, grade, linhas, colunas: self.buscador_np.prof_limitada_grid(origem, destino, linhas, colunas, grade, lim=50)
        if metodo_id == "aprofundamento_iterativo":
            return lambda origem, destino, grade, linhas, colunas: self.buscador_np.aprof_iterativo_grid(origem, destino, linhas, colunas, grade, lim_max=max(linhas, colunas) * 2)
        if metodo_id == "amplitude":
            return lambda origem, destino, grade, linhas, colunas: self.buscador_np.amplitude_grid(origem, destino, linhas, colunas, grade)
        if metodo_id == "bidirecional":
            return lambda origem, destino, grade, linhas, colunas: self.buscador_np.bidirecional_grid(origem, destino, linhas, colunas, grade)

        if metodo_id in {"custo_uniforme", "greedy", "a_estrela", "aia_estrela"}:
            return lambda origem, destino, grade, linhas, colunas: self._executar_pesado(metodo_id, origem, destino, grade, linhas, colunas)

        return lambda origem, destino, grade, linhas, colunas: self.buscador_np.amplitude_grid(origem, destino, linhas, colunas, grade)

    def encontrar_rota(self, metodo_id, origem, destino, grade, linhas, colunas):
        metodo = self._mapear_metodo(metodo_id)
        return metodo(origem, destino, grade, linhas, colunas)
