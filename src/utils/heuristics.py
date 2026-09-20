import math
from typing import Callable, Dict, Sequence

from src.models.person import Person
from src.models.state import State


def max_time_heuristic(state: State) -> int:
    """
    h1(n) - tempo da pessoa mais lenta que ainda está na margem esquerda.

    Admissível: toda pessoa que ainda está à esquerda precisa, em algum momento,
    atravessar a ponte. Em particular, a mais lenta delas participará de pelo
    menos uma travessia de ida, e o custo de uma travessia é o tempo do seu
    integrante mais lento. Logo, o tempo restante até o objetivo é no mínimo o
    tempo dessa pessoa, e h1 nunca superestima o custo real.

    Se não houver ninguém na margem esquerda (objetivo alcançado), retorna 0.
    """
    if not state.left_side:
        return 0
    return max(person.time for person in state.left_side)


def pairing_heuristic(state: State, people: Sequence[Person] = ()) -> int:
    """
    h2(n) - limite inferior do emparelhamento das idas somado ao custo mínimo
    dos retornos ainda obrigatórios.

    Construção:

    1. **Idas.** Sejam t_1 >= t_2 >= ... >= t_m os tempos das m pessoas ainda à
       esquerda. Como a ponte leva no máximo duas pessoas por vez, são
       necessárias pelo menos ceil(m/2) travessias de ida, e o custo de cada uma
       é o tempo do seu integrante mais lento. O melhor emparelhamento
       concebível junta a pessoa mais lenta com a segunda mais lenta, a terceira
       com a quarta, e assim por diante; seu custo é t_1 + t_3 + t_5 + ...
       Nenhum agrupamento pode custar menos do que isso.
    2. **Voltas.** Cada travessia de ida, exceto a última, precisa ser seguida
       por alguém trazendo a tocha de volta. São, portanto, pelo menos
       ceil(m/2) - 1 retornos quando a tocha já está à esquerda, e ceil(m/2)
       quando a tocha está à direita (é preciso um retorno antes da primeira
       ida). Cada retorno custa no mínimo o tempo da pessoa mais rápida do
       grupo.

    A soma das duas parcelas é um limite inferior para o tempo restante, logo h2
    é admissível. Como h2(n) >= h1(n) para todo n, h2 domina h1 e tende a
    expandir menos nós.
    """
    remaining = sorted((person.time for person in state.left_side), reverse=True)
    if not remaining:
        return 0

    everyone = people or (state.left_side | state.right_side)
    fastest = min(person.time for person in everyone)

    # Idas: soma dos tempos nas posições ímpares (1a, 3a, 5a... mais lentas).
    crossings_cost = sum(remaining[0::2])

    # Voltas obrigatórias, cobradas pelo menor tempo possível.
    forward_trips = math.ceil(len(remaining) / 2)
    returns = forward_trips - 1 if state.torch_is_left else forward_trips

    return crossings_cost + returns * fastest


HEURISTICS: Dict[str, Callable[[State], int]] = {
    "h1": max_time_heuristic,
    "h2": pairing_heuristic,
}

HEURISTIC_LABELS: Dict[str, str] = {
    "h1": "h₁ = tempo da pessoa mais lenta à esquerda",
    "h2": "h₂ = emparelhamento das idas + retornos mínimos",
}


def get_heuristic(name: str) -> Callable[[State], int]:
    if name not in HEURISTICS:
        raise ValueError(f"Heurística desconhecida: {name!r}. Opções: {sorted(HEURISTICS)}")
    return HEURISTICS[name]
