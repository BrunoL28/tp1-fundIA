import itertools
from collections import deque
from typing import Dict, Iterable, List, Sequence, Tuple

from .arc import Arc
from .person import Person
from .state import State

DEFAULT_TIMES = (1, 2, 5, 10)
DEFAULT_CAPACITY = 2


class BridgeProblem:
    """
    Formulação do problema da Ponte e da Tocha como busca em espaço de estados.

    O problema é definido por: um conjunto de estados, um estado inicial, o
    conjunto de ações possíveis em cada estado, uma função de transição, um
    objetivo e um critério de qualidade da solução (aqui, o tempo total de
    travessia).

    Tanto os tempos de travessia quanto a capacidade da ponte são parâmetros, o
    que permite estudar instâncias maiores do que a do enunciado sem alterar
    uma linha dos algoritmos.
    """

    def __init__(
        self,
        times: Sequence[int] = DEFAULT_TIMES,
        capacity: int = DEFAULT_CAPACITY,
        memoize: bool = True,
    ):
        if not times:
            raise ValueError("É preciso ao menos uma pessoa para atravessar a ponte.")
        if capacity < 1:
            raise ValueError("A ponte precisa suportar ao menos uma pessoa por vez.")

        self.times = tuple(times)
        self.capacity = capacity
        self.people = frozenset(self._build_people(self.times))

        # A função sucessora é determinística, então o resultado de cada estado
        # pode ser reaproveitado entre repetições e entre algoritmos. O cache é
        # opcional para permitir medir o custo real de gerá-la.
        self.memoize = memoize
        self._successors: Dict[State, Tuple[Arc, ...]] = {}

    @staticmethod
    def _build_people(times: Sequence[int]) -> List[Person]:
        """
        Cria as pessoas, rotulando-as pelo tempo de travessia. Quando dois
        tempos coincidem, o rótulo ganha um sufixo para que as pessoas
        continuem distinguíveis nos relatórios.
        """
        repeated = {time for time in times if times.count(time) > 1}
        suffixes: Dict[int, int] = {}
        people = []

        for identifier, time in enumerate(times):
            if time in repeated:
                suffix = suffixes.get(time, 0)
                suffixes[time] = suffix + 1
                label = f"{time}{chr(ord('a') + suffix)}"
            else:
                label = str(time)
            people.append(Person(time=time, id=identifier, label=label))

        return people

    def person(self, label_or_time) -> Person:
        """Localiza uma pessoa pelo rótulo ou pelo tempo de travessia."""
        for candidate in sorted(self.people):
            if candidate.label == str(label_or_time) or candidate.time == label_or_time:
                return candidate
        raise KeyError(f"Não há pessoa com rótulo ou tempo {label_or_time!r}.")

    def build_state(self, left: Iterable, torch_is_left: bool = True) -> State:
        """Monta um estado a partir dos rótulos (ou tempos) das pessoas à esquerda."""
        left_people = frozenset(self.person(item) for item in left)
        return State(
            left_side=left_people,
            right_side=self.people - left_people,
            torch_is_left=torch_is_left,
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

    @staticmethod
    def crossing_time(group: Iterable[Person]) -> int:
        """Uma travessia custa o tempo do integrante mais lento do grupo."""
        return max(person.time for person in group)

    def get_successors(self, state: State) -> Tuple[Arc, ...]:
        """
        Função Sucessora: gera todas as transições válidas a partir do estado atual.

        Cada transição é devolvida como um `Arc`, isto é, uma aresta dirigida do
        grafo de espaço de estados rotulada pela ação (quem atravessou) e pelo
        custo (o tempo da pessoa mais lenta do grupo).
        """
        if self.memoize:
            cached = self._successors.get(state)
            if cached is not None:
                return cached

        arcs = self._expand(state)

        if self.memoize:
            self._successors[state] = arcs

        return arcs

    def _expand(self, state: State) -> Tuple[Arc, ...]:
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

            arcs.append(
                Arc(
                    from_node=state,
                    to_node=next_state,
                    action=action,
                    cost=self.crossing_time(action),
                )
            )

        return tuple(arcs)

    def _available_actions(self, side) -> List[Tuple[Person, ...]]:
        """
        Ações válidas: qualquer grupo de 1 até `capacity` pessoas do lado em que
        está a tocha, já que a ponte suporta no máximo `capacity` pessoas por vez
        e toda travessia exige a tocha.
        """
        ordered = sorted(side)
        actions: List[Tuple[Person, ...]] = []
        for size in range(1, min(self.capacity, len(ordered)) + 1):
            actions.extend(itertools.combinations(ordered, size))
        return actions

    def warm_cache(self) -> int:
        """
        Preenche o cache da função sucessora percorrendo todo o espaço de
        estados alcançável. Usado antes de medir tempos, para que todos os
        algoritmos sejam cronometrados nas mesmas condições.
        """
        frontier = deque([self.get_initial_state()])
        seen = {self.get_initial_state()}

        while frontier:
            for arc in self.get_successors(frontier.popleft()):
                if arc.to_node not in seen:
                    seen.add(arc.to_node)
                    frontier.append(arc.to_node)

        return len(seen)
