from typing import Iterator, List, Optional, Tuple, Union

from .arc import Arc
from .state import State


class Path:
    """
    Um caminho <n_0, n_1, ..., n_k> no grafo de espaço de estados.

    Fronteira: um *conjunto de caminhos*: a busca remove
    um caminho <n_0, ..., n_k> da fronteira e, se n_k não é objetivo, devolve à
    fronteira os caminhos <n_0, ..., n_k, n> para cada vizinho n de n_k. Esta
    classe implementa exatamente essa noção.

    A definição é recursiva: um caminho é ou um nó isolado, ou um caminho
    seguido de um arco. Com isso, estender um caminho custa O(1) e caminhos que
    compartilham um prefixo compartilham a mesma estrutura em memória, sem que
    seja necessário copiar a sequência de nós a cada expansão.
    """

    __slots__ = ("initial", "arc", "cost", "length")

    def __init__(self, initial: Union[State, "Path"], arc: Optional[Arc] = None):
        self.initial = initial
        self.arc = arc

        if arc is None:
            # Caminho de custo zero, formado apenas pelo nó inicial.
            self.cost = 0
            self.length = 0
        else:
            self.cost = initial.cost + arc.cost
            self.length = initial.length + 1

    def end(self) -> State:
        """O último nó do caminho, n_k."""
        return self.initial if self.arc is None else self.arc.to_node

    def extend(self, arc: Arc) -> "Path":
        """Devolve o caminho <n_0, ..., n_k, n> obtido ao percorrer `arc`."""
        return Path(self, arc)

    def arcs(self) -> List[Arc]:
        """Arcos do caminho, em ordem cronológica."""
        arcs: List[Arc] = []
        current: Path = self
        while current.arc is not None:
            arcs.append(current.arc)
            current = current.initial
        arcs.reverse()
        return arcs

    def actions(self) -> List[Tuple[int, ...]]:
        """Ações tomadas ao longo do caminho, em ordem cronológica."""
        return [arc.action for arc in self.arcs()]

    def nodes(self) -> List[State]:
        """Sequência de nós <n_0, ..., n_k>, em ordem cronológica."""
        arcs = self.arcs()
        if not arcs:
            return [self.end()]
        return [arcs[0].from_node] + [arc.to_node for arc in arcs]

    def __iter__(self) -> Iterator[State]:
        return iter(self.nodes())

    def __len__(self) -> int:
        """Número de arestas do caminho."""
        return self.length

    def __str__(self) -> str:
        steps = " ".join(str(arc) for arc in self.arcs())
        return f"<{steps}>_{self.cost}" if steps else f"<>_{self.cost}"

    def __repr__(self) -> str:
        return f"Path(len={self.length}, cost={self.cost}, end={self.end()})"
