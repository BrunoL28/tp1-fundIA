from dataclasses import dataclass, field
from typing import Optional
from .state import State

@dataclass
class Node:
    """
    Representa um nó na árvore de busca.
    """
    state: State
    parent: Optional['Node'] = None
    action: Optional[tuple] = None  # Ex: (1, 2) representando quem atravessou
    path_cost: int = 0              # Custo g(n): tempo acumulado até aqui
    heuristic: int = 0              # Custo h(n): heurística estimada até o objetivo

    @property
    def total_cost(self) -> int:
        """
        Custo f(n) = g(n) + h(n). Usado pelo algoritmo A*.
        """
        return self.path_cost + self.heuristic

    def __lt__(self, other: 'Node') -> bool:
        """
        Sobrescrita do operador '<' (Less Than).
        Crucial para que a fila de prioridade (heapq) consiga ordenar os nós
        na Busca de Custo Uniforme e no A*.
        """
        return self.total_cost < other.total_cost