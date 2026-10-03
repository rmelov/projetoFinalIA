"""Resultado padronizado de uma execução de método de busca."""
from dataclasses import dataclass, field
from typing import List, Optional

from dominio.mapa.coordenada import Coordenada


@dataclass(frozen=True)
class ResultadoBusca:
    """encontrado: se existe caminho. rota: origem->destino, inclusive.
    custo: soma de pesos, ou nº de passos quando o método não é ponderado."""

    metodoId: str
    encontrado: bool
    rota: List[Coordenada] = field(default_factory=list)
    custo: Optional[float] = None
    duracaoMs: float = 0.0
    observacao: str = ""

    def rotaComoTexto(self) -> str:
        if not self.rota:
            return "—"
        return " → ".join(str(c) for c in self.rota)
