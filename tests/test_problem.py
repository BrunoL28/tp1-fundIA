import pytest
from src.models.problem import BridgeProblem
from src.models.state import State
from src.utils.heuristics import max_time_heuristic

@pytest.fixture
def problem():
    return BridgeProblem()

@pytest.fixture
def initial_state(problem):
    return problem.get_initial_state()

def test_initial_state_configuration(initial_state):
    assert len(initial_state.left_side) == 4
    assert len(initial_state.right_side) == 0
    assert initial_state.torch_is_left is True
    assert not initial_state.is_goal()

def test_goal_state_recognition():
    goal_state = State(
        left_side=frozenset(),
        right_side=frozenset([1, 2, 5, 10]),
        torch_is_left=False
    )
    assert goal_state.is_goal() is True

def test_successor_generates_correct_number_of_actions(problem, initial_state):
    successors = problem.get_successors(initial_state)
    # 4 pessoas = 4 ações individuais + 6 combinações de pares = 10 sucessores
    assert len(successors) == 10

def test_successor_torch_alternation_and_movement(problem, initial_state):
    successors = problem.get_successors(initial_state)
    action, next_state, cost = next(s for s in successors if set(s[0]) == {1, 2})
    
    # A tocha deve ir para a direita
    assert next_state.torch_is_left is False
    
    # 1 e 2 devem sair da esquerda e ir para a direita
    assert 1 not in next_state.left_side
    assert 2 not in next_state.left_side
    assert 1 in next_state.right_side
    assert 2 in next_state.right_side

def test_successor_calculates_correct_cost(problem, initial_state):
    successors = problem.get_successors(initial_state)
    
    # Testa dupla (5, 10)
    _, _, cost_pair = next(s for s in successors if set(s[0]) == {5, 10})
    assert cost_pair == 10
    
    # Testa individual (2)
    _, _, cost_single = next(s for s in successors if set(s[0]) == {2})
    assert cost_single == 2

def test_successors_from_right_to_left(problem):
    # Força um estado onde a tocha está na direita com as pessoas 1 e 2
    state = State(
        left_side=frozenset([5, 10]),
        right_side=frozenset([1, 2]),
        torch_is_left=False
    )
    successors = problem.get_successors(state)
    
    # Do lado direito (1, 2), podemos ter: (1), (2), ou (1, 2). Total = 3 movimentos
    assert len(successors) == 3
    
    # Se o 2 voltar, a tocha vem para a esquerda, 2 entra na esquerda, e o custo é 2
    action, next_state, cost = next(s for s in successors if set(s[0]) == {2})
    assert next_state.torch_is_left is True
    assert 2 in next_state.left_side
    assert 2 not in next_state.right_side
    assert cost == 2

def test_heuristic_is_admissible_and_correct():
    # Estado inicial: mais lento é 10
    state1 = State(left_side=frozenset([1, 2, 5, 10]), right_side=frozenset(), torch_is_left=True)
    assert max_time_heuristic(state1) == 10
    
    # Estado intermediário: mais lento é 5
    state2 = State(left_side=frozenset([1, 5]), right_side=frozenset([2, 10]), torch_is_left=True)
    assert max_time_heuristic(state2) == 5
    
    # Estado objetivo: vazio
    state3 = State(left_side=frozenset(), right_side=frozenset([1, 2, 5, 10]), torch_is_left=False)
    assert max_time_heuristic(state3) == 0

def test_state_immutability():
    state = State(left_side=frozenset([1, 2]), right_side=frozenset([5, 10]), torch_is_left=True)
    
    # Tentar modificar o set diretamente deve gerar AttributeError (frozenset não tem .add ou .remove)
    with pytest.raises(AttributeError):
        state.left_side.add(3)