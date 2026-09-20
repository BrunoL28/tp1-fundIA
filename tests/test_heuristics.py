import pytest

from src.models.problem import BridgeProblem
from src.utils.heuristics import HEURISTICS, get_heuristic, max_time_heuristic, pairing_heuristic
from src.utils.state_space import explore_state_space

# Instâncias em que as propriedades são verificadas exaustivamente: a do
# enunciado e variações em número de pessoas e capacidade da ponte. A
# heurística h2 depende da capacidade, e o CLI permite alterá-la.
INSTANCES = [
    pytest.param(((1, 2, 5, 10), 2), id="4p-cap2"),
    pytest.param(((1, 2, 5, 10), 3), id="4p-cap3"),
    pytest.param(((1, 2, 5, 10, 15), 2), id="5p-cap2"),
    pytest.param(((1, 2, 5, 10, 15), 3), id="5p-cap3"),
]


@pytest.fixture(scope="module", params=INSTANCES)
def problem(request):
    times, capacity = request.param
    return BridgeProblem(times=times, capacity=capacity)


@pytest.fixture(scope="module")
def space(problem):
    return explore_state_space(problem)


@pytest.fixture(scope="module")
def optimal(space):
    return space.optimal_costs_to_goal()


def test_max_time_heuristic_values():
    problem = BridgeProblem()
    assert max_time_heuristic(problem.build_state([1, 2, 5, 10])) == 10
    assert max_time_heuristic(problem.build_state([1, 5])) == 5
    assert max_time_heuristic(problem.build_state([], torch_is_left=False)) == 0


def test_pairing_heuristic_values():
    problem = BridgeProblem()
    # Idas: 10 + 2 (emparelhando 10 com 5 e 2 com 1); voltas: 1 retorno x 1 min.
    assert pairing_heuristic(problem.build_state([1, 2, 5, 10])) == 13

    # Com a tocha na direita é preciso um retorno a mais antes da próxima ida.
    assert pairing_heuristic(problem.build_state([5, 10], torch_is_left=False)) == 10 + 1

    assert pairing_heuristic(problem.build_state([], torch_is_left=False)) == 0


def test_pairing_heuristic_respects_capacity():
    """
    Com a ponte para três pessoas, {2, 5, 10} atravessam de uma vez por 10
    minutos: a heurística não pode cobrar duas idas como se a ponte fosse para
    duas pessoas.
    """
    problem = BridgeProblem(capacity=3)
    state = problem.build_state([2, 5, 10])
    assert pairing_heuristic(state, capacity=3) == 10
    # Capacidade 2: idas {10, 5} e {2} (10 + 2) mais um retorno de 1 minuto.
    assert pairing_heuristic(state, capacity=2) == 10 + 2 + 1


def test_pairing_heuristic_uses_the_fastest_person_for_returns():
    """A pessoa mais rápida pode já estar do outro lado e ainda assim voltar."""
    problem = BridgeProblem()
    state = problem.build_state([5, 10], torch_is_left=False)
    assert pairing_heuristic(state, fastest=1) == 11
    assert pairing_heuristic(state, fastest=2) == 12


@pytest.mark.parametrize("name", sorted(HEURISTICS))
def test_heuristic_is_admissible(name, problem, space, optimal):
    """h(n) <= h*(n) para todo estado alcançável: nunca superestima o custo real."""
    heuristic = get_heuristic(name, problem)
    violations = [state for state in space.states if heuristic(state) > optimal[state]]
    assert violations == []


@pytest.mark.parametrize("name", sorted(HEURISTICS))
def test_heuristic_is_consistent(name, problem, space):
    """h(u) <= custo(u, v) + h(v) para toda transição: dispensa reexpansões."""
    heuristic = get_heuristic(name, problem)
    violations = [
        arc for arc in space.all_transitions()
        if heuristic(arc.from_node) > arc.cost + heuristic(arc.to_node)
    ]
    assert violations == []


def test_pairing_heuristic_dominates_max_time(problem, space):
    """h2 >= h1 em todo estado, e é estritamente maior em pelo menos um."""
    h1 = get_heuristic("h1", problem)
    h2 = get_heuristic("h2", problem)
    assert all(h2(s) >= h1(s) for s in space.states)
    assert any(h2(s) > h1(s) for s in space.states)


def test_goal_heuristics_are_zero(problem, space):
    for goal in space.goals:
        for name in HEURISTICS:
            assert get_heuristic(name, problem)(goal) == 0


def test_unknown_heuristic_is_rejected():
    with pytest.raises(ValueError):
        get_heuristic("h99", BridgeProblem())
