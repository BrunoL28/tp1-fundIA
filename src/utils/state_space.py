import heapq
from collections import deque
from dataclasses import dataclass
from typing import Dict, List, Optional, Tuple

from src.models.arc import Arc
from src.models.problem import BridgeProblem
from src.models.state import State


@dataclass(frozen=True)
class StateSpace:
    """
    Enumeração completa do grafo de espaço de estados alcançável a partir do
    estado inicial, mantida em uma lista de adjacências.

    Esta classe centraliza a varredura do domínio.
    """
    initial: State
    states: Tuple[State, ...]
    adjacency: Dict[State, Tuple[Arc, ...]]
    labels: Dict[State, str]

    # ------------------------------------------------------------------
    # Propriedades do grafo
    # ------------------------------------------------------------------
    @property
    def num_states(self) -> int:
        """Cardinalidade do conjunto de vértices, |V|."""
        return len(self.states)

    @property
    def num_transitions(self) -> int:
        """Cardinalidade do conjunto de arestas dirigidas, |E|."""
        return sum(len(arcs) for arcs in self.adjacency.values())

    @property
    def average_out_degree(self) -> float:
        """Grau de saída médio: |E| / |V|."""
        return self.num_transitions / self.num_states

    @property
    def min_out_degree(self) -> int:
        return min(len(arcs) for arcs in self.adjacency.values())

    @property
    def max_out_degree(self) -> int:
        return max(len(arcs) for arcs in self.adjacency.values())

    @property
    def adjacency_matrix_cells(self) -> int:
        """Número de posições que uma matriz de adjacências |V| x |V| ocuparia."""
        return self.num_states ** 2

    @property
    def density(self) -> float:
        """Fração das posições da matriz de adjacências que seriam não nulas."""
        return self.num_transitions / self.adjacency_matrix_cells

    @property
    def is_symmetric(self) -> bool:
        """
        True se toda aresta (u, v) tem a aresta inversa (v, u) com o mesmo custo.
        Vale para este problema porque qualquer travessia pode ser desfeita
        refazendo o mesmo trajeto com o mesmo grupo de pessoas.
        """
        pairs = {(arc.from_node, arc.to_node, arc.cost) for arc in self.all_transitions()}
        return all((v, u, cost) in pairs for u, v, cost in pairs)

    @property
    def goals(self) -> Tuple[State, ...]:
        return tuple(state for state in self.states if state.is_goal())

    # ------------------------------------------------------------------
    # Acesso
    # ------------------------------------------------------------------
    def label(self, state: State) -> str:
        return self.labels[state]

    def successors(self, state: State) -> Tuple[Arc, ...]:
        return self.adjacency[state]

    def out_degree(self, state: State) -> int:
        return len(self.adjacency[state])

    def all_transitions(self) -> List[Arc]:
        return [arc for state in self.states for arc in self.adjacency[state]]

    def optimal_costs_to_goal(self) -> Dict[State, float]:
        """
        Custo real h*(n) do caminho de custo mínimo de cada estado até o
        objetivo, obtido por uma busca de custo mínimo sobre o grafo invertido.

        Serve de referência para verificar, de forma exaustiva, se uma
        heurística é admissível (h(n) <= h*(n) para todo n).
        """
        reverse: Dict[State, List[Tuple[State, int]]] = {state: [] for state in self.states}
        for arc in self.all_transitions():
            reverse[arc.to_node].append((arc.from_node, arc.cost))

        distances: Dict[State, float] = {}
        seq = 0
        queue: List[Tuple[float, int, State]] = []

        for goal in self.goals:
            distances[goal] = 0
            queue.append((0, seq, goal))
            seq += 1
        heapq.heapify(queue)

        while queue:
            cost, _, state = heapq.heappop(queue)
            if cost > distances.get(state, float("inf")):
                continue

            for previous, arc_cost in reverse[state]:
                candidate = cost + arc_cost
                if candidate < distances.get(previous, float("inf")):
                    distances[previous] = candidate
                    seq += 1
                    heapq.heappush(queue, (candidate, seq, previous))

        return distances


def explore_state_space(problem: Optional[BridgeProblem] = None) -> StateSpace:
    """
    Percorre em largura todo o espaço de estados alcançável e devolve o grafo
    correspondente como lista de adjacências.

    Observação: o percurso não é podado no estado objetivo. O grafo modela o
    domínio do problema, e não a árvore de busca; do estado objetivo também
    partem travessias de volta, que existem no grafo ainda que nenhuma busca
    precise explorá-las.
    """
    problem = problem or BridgeProblem()
    initial = problem.get_initial_state()

    adjacency: Dict[State, Tuple[Arc, ...]] = {}
    frontier = deque([initial])
    discovered = {initial}

    while frontier:
        state = frontier.popleft()
        arcs = list(problem.get_successors(state))

        for arc in arcs:
            if arc.to_node not in discovered:
                discovered.add(arc.to_node)
                frontier.append(arc.to_node)

        # Ordem determinística dentro de cada estado: primeiro o mais barato.
        arcs.sort(key=lambda item: (item.cost, item.action))
        adjacency[state] = tuple(arcs)

    states = tuple(sorted(discovered, key=State.sort_key))
    labels = {state: f"E{index:02d}" for index, state in enumerate(states)}

    return StateSpace(initial=initial, states=states, adjacency=adjacency, labels=labels)
