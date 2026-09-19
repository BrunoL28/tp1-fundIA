from dataclasses import dataclass
from typing import Tuple

from .state import State


@dataclass(frozen=True)
class Arc:
    """
    Aresta dirigida do grafo de espaço de estados.

    Em um grafo de espaço de estados os nós são os
    estados, e existe uma aresta (n_i, n_j) quando alguma ação executada sobre
    n_i leva o agente a n_j. Aqui a aresta carrega também o rótulo da ação (quem
    atravessou) e o seu custo (o tempo da travessia).
    """
    from_node: State
    to_node: State
    action: Tuple[int, ...]
    cost: int

    @property
    def is_forward(self) -> bool:
        """True se a travessia é de ida (margem esquerda -> margem direita)."""
        return self.from_node.torch_is_left

    @property
    def label(self) -> str:
        """Rótulo da aresta: o grupo que atravessou. Ex.: `{1, 2}`."""
        return "{" + ", ".join(map(str, sorted(self.action))) + "}"

    def __str__(self) -> str:
        direction = "->" if self.is_forward else "<-"
        return f"{direction} {self.label} (t:{self.cost})"
