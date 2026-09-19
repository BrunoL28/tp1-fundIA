import pytest

from src.models.problem import BridgeProblem
from src.models.state import State
from src.utils.heuristics import HEURISTICS, get_heuristic, max_time_heuristic, pairing_heuristic
from src.utils.state_space import explore_state_space


@pytest.fixture(scope="module")
def space():
    return explore_state_space(BridgeProblem())


@pytest.fixture(scope="module")
def optimal(space):
    return space.optimal_costs_to_goal()


def test_max_time_heuristic_values():
    state1 = State(frozenset([1, 2, 5, 10]), frozenset(), torch_is_left=True)
    assert max_time_heuristic(state1) == 10

    state2 = State(frozenset([1, 5]), frozenset([2, 10]), torch_is_left=True)
    assert max_time_heuristic(state2) == 5

    goal = State(frozenset(), frozenset([1, 2, 5, 10]), torch_is_left=False)
    assert max_time_heuristic(goal) == 0


def test_pairing_heuristic_values():
    # Idas: 10 + 2 (emparelhando 10 com 5 e 2 com 1); voltas: 1 retorno x 1 min.
    state = State(frozenset([1, 2, 5, 10]), frozenset(), torch_is_left=True)
    assert pairing_heuristic(state) == 13

    # Com a tocha na direita é preciso um retorno a mais antes da próxima ida.
    state_torch_right = State(frozenset([5, 10]), frozenset([1, 2]), torch_is_left=False)
    assert pairing_heuristic(state_torch_right) == 10 + 1

    goal = State(frozenset(), frozenset([1, 2, 5, 10]), torch_is_left=False)
    assert pairing_heuristic(goal) == 0


@pytest.mark.parametrize("name", sorted(HEURISTICS))
def test_heuristic_is_admissible(name, space, optimal):
    """h(n) <= h*(n) para todo estado alcançável: nunca superestima o custo real."""
    heuristic = get_heuristic(name)
    violations = [state for state in space.states if heuristic(state) > optimal[state]]
    assert violations == []


@pytest.mark.parametrize("name", sorted(HEURISTICS))
def test_heuristic_is_consistent(name, space):
    """h(u) <= custo(u, v) + h(v) para toda transição: dispensa reexpansões."""
    heuristic = get_heuristic(name)
    violations = [
        arc for arc in space.all_transitions()
        if heuristic(arc.from_node) > arc.cost + heuristic(arc.to_node)
    ]
    assert violations == []


def test_pairing_heuristic_dominates_max_time(space):
    """h2 >= h1 em todo estado, e é estritamente maior em pelo menos um."""
    assert all(pairing_heuristic(s) >= max_time_heuristic(s) for s in space.states)
    assert any(pairing_heuristic(s) > max_time_heuristic(s) for s in space.states)


def test_goal_heuristics_are_zero(space):
    for goal in space.goals:
        for heuristic in HEURISTICS.values():
            assert heuristic(goal) == 0


def test_unknown_heuristic_is_rejected():
    with pytest.raises(ValueError):
        get_heuristic("h99")
