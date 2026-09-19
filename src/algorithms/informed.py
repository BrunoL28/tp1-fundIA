"""
Estratégia de busca informada (heurística).

A busca A* acelera a procura pelo caminho de custo mínimo priorizando os
caminhos que parecem mais promissores, segundo uma função heurística h(n) que
estima o custo restante de n até o objetivo.
"""

import heapq
from typing import Callable, Optional

from src.algorithms.base_search import BaseSearch, DEFAULT_MAX_EXPANSIONS
from src.models.path import Path
from src.models.problem import BridgeProblem
from src.utils.heuristics import max_time_heuristic


class AStarSearch(BaseSearch):
    """
    Busca A*.

    Combina o critério da Busca pelo Primeiro Caminho de Custo Mínimo com a
    informação da heurística: para um caminho p = <n_0, ..., n>, a fronteira é
    ordenada pela estimativa do custo total

        f(p) = cost(p) + h(n)

    em que cost(p) é o custo já percorrido (g) e h(n) estima o que falta. Com
    uma heurística admissível, f nunca superestima o custo total do melhor
    caminho que passa por p, e o primeiro caminho-solução selecionado é ótimo.
    """

    display_name = "Busca A*"

    def __init__(
        self,
        heuristic: Callable = max_time_heuristic,
        max_expansions: int = DEFAULT_MAX_EXPANSIONS,
        display_name: Optional[str] = None,
    ):
        super().__init__(max_expansions=max_expansions)
        self.heuristic = heuristic
        if display_name is not None:
            self.display_name = display_name

    def solve(self, problem: BridgeProblem) -> Optional[Path]:
        initial = Path(problem.get_initial_state())

        seq = 0
        frontier = [(initial.cost + self.heuristic(initial.end()), seq, initial)]
        self.observe_frontier(len(frontier))

        explored = {}

        while frontier:
            if self.expansion_limit_reached():
                return None

            _, _, path = heapq.heappop(frontier)
            node = path.end()

            if node in explored and explored[node] <= path.cost:
                continue

            explored[node] = path.cost

            if node.is_goal():
                return path

            self.count_expansion()

            for arc in problem.get_successors(node):
                self.count_generated()
                new_cost = path.cost + arc.cost

                if arc.to_node not in explored or new_cost < explored[arc.to_node]:
                    seq += 1
                    priority = new_cost + self.heuristic(arc.to_node)
                    heapq.heappush(frontier, (priority, seq, path.extend(arc)))
                    self.observe_frontier(len(frontier))

        return None
