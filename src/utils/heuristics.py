import math
from typing import Callable, Dict, Optional

from src.models.problem import BridgeProblem
from src.models.state import State

Heuristic = Callable[[State], int]


def max_time_heuristic(state: State) -> int:
    """
    h1(n) - tempo da pessoa mais lenta que ainda está na margem esquerda.

    Admissível: toda pessoa que ainda está à esquerda precisa, em algum momento,
    atravessar a ponte. Em particular, a mais lenta delas participará de pelo
    menos uma travessia de ida, e o custo de uma travessia é o tempo do seu
    integrante mais lento. Logo, o tempo restante até o objetivo é no mínimo o
    tempo dessa pessoa, e h1 nunca superestima o custo real.

    Não depende da capacidade da ponte. Se não houver ninguém na margem
    esquerda (objetivo alcançado), retorna 0.
    """
    if not state.left_side:
        return 0
    return max(person.time for person in state.left_side)


def pairing_heuristic(state: State, capacity: int = 2, fastest: Optional[int] = None) -> int:
    """
    h2(n) - limite inferior do agrupamento das idas somado ao custo mínimo dos
    retornos ainda obrigatórios, para uma ponte que leva até `capacity`
    pessoas por vez.

    Construção:

    1. **Idas.** Sejam t_1 >= t_2 >= ... >= t_m os tempos das m pessoas ainda à
       esquerda. Considere, para cada uma, a sua *última* travessia de ida:
       isso particiona as m pessoas em grupos de no máximo `capacity`, um por
       travessia, de modo que são necessárias pelo menos ceil(m / capacity)
       idas. Cada ida custa pelo menos o tempo do integrante mais lento do seu
       grupo. Os `i` grupos mais caros cobrem no máximo i x capacity pessoas,
       logo o i-ésimo maior custo de ida é >= t_{(i-1) x capacity + 1}. A soma
       t_1 + t_{c+1} + t_{2c+1} + ... é, portanto, um limite inferior para o
       custo das idas. Com capacidade 2 isso é o emparelhamento
       (10 com 5, 2 com 1) e vale t_1 + t_3 + ...
    2. **Voltas.** Entre duas idas consecutivas alguém precisa trazer a tocha de
       volta. São, portanto, pelo menos ceil(m / capacity) - 1 retornos quando a
       tocha já está à esquerda, e ceil(m / capacity) quando a tocha está à
       direita (é preciso um retorno antes da primeira ida). Cada retorno custa
       no mínimo o tempo da pessoa mais rápida do problema (`fastest`), que
       pode estar em qualquer margem.

    A soma das duas parcelas é um limite inferior para o tempo restante, logo h2
    é admissível. Como h2(n) >= h1(n) para todo n, h2 domina h1 e tende a
    expandir menos nós.

    Se `fastest` não for informado, é tomado o mínimo entre todas as pessoas
    presentes no estado. Use `get_heuristic("h2", problem)` para obter uma
    versão já amarrada à capacidade e aos tempos do problema.
    """
    remaining = sorted((person.time for person in state.left_side), reverse=True)
    if not remaining:
        return 0

    if fastest is None:
        fastest = min(person.time for person in state.left_side | state.right_side)

    # Idas: o mais lento de cada grupo de `capacity` pessoas, do mais lento ao
    # mais rápido (posições 1, c+1, 2c+1, ...).
    crossings_cost = sum(remaining[0::capacity])

    # Voltas obrigatórias, cobradas pelo menor tempo possível.
    forward_trips = math.ceil(len(remaining) / capacity)
    returns = forward_trips - 1 if state.torch_is_left else forward_trips

    return crossings_cost + returns * fastest


def _bind_max_time(problem: BridgeProblem) -> Heuristic:
    return max_time_heuristic


def _bind_pairing(problem: BridgeProblem) -> Heuristic:
    capacity = problem.capacity
    fastest = min(problem.times)

    def bound_pairing_heuristic(state: State) -> int:
        return pairing_heuristic(state, capacity=capacity, fastest=fastest)

    return bound_pairing_heuristic


# Registro das heurísticas. Cada entrada é uma fábrica que recebe o problema e
# devolve h(n): assim h2 conhece a capacidade da ponte e o tempo da pessoa mais
# rápida sem que os algoritmos precisem saber disso.
HEURISTICS: Dict[str, Callable[[BridgeProblem], Heuristic]] = {
    "h1": _bind_max_time,
    "h2": _bind_pairing,
}

HEURISTIC_LABELS: Dict[str, str] = {
    "h1": "h₁ = tempo da pessoa mais lenta à esquerda",
    "h2": "h₂ = agrupamento das idas + retornos mínimos",
}


def get_heuristic(name: str, problem: BridgeProblem) -> Heuristic:
    """Devolve a heurística `name` amarrada aos parâmetros de `problem`."""
    if name not in HEURISTICS:
        raise ValueError(f"Heurística desconhecida: {name!r}. Opções: {sorted(HEURISTICS)}")
    return HEURISTICS[name](problem)
