import itertools
from typing import List, Sequence, Tuple

from .arc import Arc
from .state import State

DEFAULT_PEOPLE = (1, 2, 5, 10)
DEFAULT_CAPACITY = 2


class BridgeProblem:
    """
    Formulação do problema da Ponte e da Tocha como busca em espaço de estados.

    O problema é definido por: um conjunto de estados, um estado inicial, o
    conjunto de ações possíveis em cada estado, uma função de transição, um
    objetivo e um critério de qualidade da solução (aqui, o tempo total de
    travessia).
    """

    def __init__(self, people: Sequence[int] = DEFAULT_PEOPLE, capacity: int = DEFAULT_CAPACITY):
        # Representamos as pessoas diretamente pelo tempo que levam para atravessar.
        # Isso simplifica o cálculo do custo, já que o ID da pessoa é o próprio tempo.
        self.people = frozenset(people)
        self.capacity = capacity

        if len(self.people) != len(people):
            raise ValueError(
                "Cada pessoa é identificada pelo seu tempo de travessia, "
                "portanto os tempos informados precisam ser distintos."
            )

    def get_initial_state(self) -> State:
        """
        Retorna o estado inicial: todos no lado esquerdo com a tocha.
        """
        return State(
            left_side=self.people,
            right_side=frozenset(),
            torch_is_left=True
        )

    def is_goal(self, state: State) -> bool:
        """Todas as pessoas (e a tocha) na margem direita."""
        return state.is_goal()

    def get_successors(self, state: State) -> List[Arc]:
        """
        Função Sucessora: gera todas as transições válidas a partir do estado atual.

        Cada transição é devolvida como um `Arc`, isto é, uma aresta dirigida do
        grafo de espaço de estados rotulada pela ação (quem atravessou) e pelo
        custo (o tempo da pessoa mais lenta do grupo).
        """
        # Identifica de qual lado o movimento vai partir
        current_side = state.left_side if state.torch_is_left else state.right_side

        # A tocha sempre muda de lado após uma transição
        next_is_left = not state.torch_is_left

        arcs: List[Arc] = []

        for action in self._available_actions(current_side):
            action_set = frozenset(action)

            if state.torch_is_left:
                # Movimento da Esquerda -> Direita
                new_left = state.left_side - action_set
                new_right = state.right_side | action_set
            else:
                # Movimento da Direita -> Esquerda
                new_left = state.left_side | action_set
                new_right = state.right_side - action_set

            next_state = State(
                left_side=new_left,
                right_side=new_right,
                torch_is_left=next_is_left
            )

            # O custo da travessia é a velocidade da pessoa mais lenta do grupo
            arcs.append(Arc(from_node=state, to_node=next_state, action=action, cost=max(action)))

        return arcs

    def _available_actions(self, side: frozenset) -> List[Tuple[int, ...]]:
        """
        Ações válidas: qualquer grupo de 1 até `capacity` pessoas do lado em que
        está a tocha, já que a ponte suporta no máximo `capacity` pessoas por vez
        e toda travessia exige a tocha.
        """
        actions: List[Tuple[int, ...]] = []
        for size in range(1, self.capacity + 1):
            actions.extend(itertools.combinations(sorted(side), size))
        return actions
