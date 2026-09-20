import pytest

from src.models.person import Person
from src.models.problem import BridgeProblem


@pytest.fixture
def problem():
    return BridgeProblem()


@pytest.fixture
def initial_state(problem):
    return problem.get_initial_state()


def arc_for(arcs, group):
    """Localiza o arco cuja ação corresponde ao conjunto de rótulos informado."""
    return next(arc for arc in arcs if {str(p) for p in arc.action} == group)


def test_initial_state_configuration(initial_state):
    assert len(initial_state.left_side) == 4
    assert len(initial_state.right_side) == 0
    assert initial_state.torch_is_left is True
    assert not initial_state.is_goal()


def test_goal_state_recognition(problem):
    goal_state = problem.build_state([], torch_is_left=False)
    assert goal_state.is_goal() is True


def test_state_diagram_is_the_single_formatter(problem, initial_state):
    assert initial_state.diagram() == "*[1, 2, 5, 10] ~~~ [-]"
    assert str(initial_state) == initial_state.diagram()
    assert initial_state.diagram(multiline=True) == "*[1, 2, 5, 10]\n~~~\n[-]"

    crossed = problem.build_state([5, 10], torch_is_left=False)
    assert crossed.diagram() == "[5, 10] ~~~ [1, 2]*"


def test_successor_generates_correct_number_of_actions(problem, initial_state):
    successors = problem.get_successors(initial_state)
    # 4 pessoas = 4 ações individuais + 6 combinações de pares = 10 sucessores
    assert len(successors) == 10


def test_successor_torch_alternation_and_movement(problem, initial_state):
    arc = arc_for(problem.get_successors(initial_state), {"1", "2"})

    # A tocha deve ir para a direita
    assert arc.to_node.torch_is_left is False
    assert arc.is_forward is True

    # 1 e 2 devem sair da esquerda e ir para a direita
    assert {str(p) for p in arc.to_node.left_side} == {"5", "10"}
    assert {str(p) for p in arc.to_node.right_side} == {"1", "2"}


def test_successor_calculates_correct_cost(problem, initial_state):
    successors = problem.get_successors(initial_state)

    # O custo de um grupo é o tempo do seu integrante mais lento
    assert arc_for(successors, {"5", "10"}).cost == 10
    assert arc_for(successors, {"2"}).cost == 2


def test_successors_from_right_to_left(problem):
    # Força um estado onde a tocha está na direita com as pessoas 1 e 2
    state = problem.build_state([5, 10], torch_is_left=False)
    successors = problem.get_successors(state)

    # Do lado direito (1, 2), podemos ter: (1), (2), ou (1, 2). Total = 3 movimentos
    assert len(successors) == 3

    # Se o 2 voltar, a tocha vem para a esquerda, 2 entra na esquerda, e o custo é 2
    arc = arc_for(successors, {"2"})
    assert arc.to_node.torch_is_left is True
    assert arc.is_forward is False
    assert {str(p) for p in arc.to_node.left_side} == {"2", "5", "10"}
    assert arc.cost == 2


def test_successor_function_is_deterministic(problem, initial_state):
    """A ordem dos sucessores precisa ser estável para que o DFS seja reprodutível."""
    first = [arc.action for arc in problem.get_successors(initial_state)]
    second = [arc.action for arc in problem.get_successors(initial_state)]
    assert first == second


def test_capacity_limits_group_size():
    """Nenhuma ação pode mover mais pessoas do que a ponte suporta."""
    problem = BridgeProblem(times=(1, 2, 5, 10, 20), capacity=2)
    arcs = problem.get_successors(problem.get_initial_state())
    assert max(len(arc.action) for arc in arcs) == 2
    # 5 individuais + 10 pares
    assert len(arcs) == 15


def test_larger_capacity_allows_larger_groups():
    problem = BridgeProblem(times=(1, 2, 5, 10), capacity=3)
    arcs = problem.get_successors(problem.get_initial_state())
    # 4 individuais + 6 pares + 4 trios
    assert len(arcs) == 14
    assert max(len(arc.action) for arc in arcs) == 3


def test_people_with_equal_times_remain_distinct():
    """
    A identidade da pessoa não é o seu tempo: duas pessoas de 5 minutos são
    duas pessoas, e não uma só.
    """
    problem = BridgeProblem(times=(1, 2, 5, 5))

    assert len(problem.people) == 4
    assert sorted(str(p) for p in problem.people) == ["1", "2", "5a", "5b"]

    # Ambas precisam atravessar, então o estado inicial tem as duas à esquerda.
    initial = problem.get_initial_state()
    assert len(initial.left_side) == 4
    assert initial.diagram() == "*[1, 2, 5a, 5b] ~~~ [-]"


def test_person_identity_is_independent_of_time():
    assert Person(time=5, id=0) != Person(time=5, id=1)
    assert len({Person(time=5, id=0), Person(time=5, id=1)}) == 2
    # A ordenação é por tempo e, no empate, por identificador.
    assert min(Person(time=5, id=1), Person(time=2, id=9)).time == 2


def test_invalid_configurations_are_rejected():
    with pytest.raises(ValueError):
        BridgeProblem(times=())
    with pytest.raises(ValueError):
        BridgeProblem(capacity=0)


def test_state_immutability(problem):
    state = problem.build_state([1, 2])

    # Tentar modificar o set diretamente deve gerar AttributeError (frozenset não tem .add ou .remove)
    with pytest.raises(AttributeError):
        state.left_side.add(problem.person(5))


def test_memoized_successors_are_reused(problem, initial_state):
    first = problem.get_successors(initial_state)
    second = problem.get_successors(initial_state)
    assert first is second


def test_memoization_can_be_disabled():
    problem = BridgeProblem(memoize=False)
    initial = problem.get_initial_state()
    assert problem.get_successors(initial) is not problem.get_successors(initial)
    assert problem.get_successors(initial) == problem.get_successors(initial)
