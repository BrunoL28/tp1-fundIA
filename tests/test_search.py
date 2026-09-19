import pytest

from src.algorithms.informed import AStarSearch
from src.algorithms.uninformed import (
    BreadthFirstSearch,
    DepthFirstSearch,
    LowestCostFirstSearch,
)
from src.models.path import Path
from src.models.problem import BridgeProblem

OPTIMAL_COST = 17


@pytest.fixture
def problem():
    return BridgeProblem()


def all_algorithms():
    return [
        BreadthFirstSearch(),
        DepthFirstSearch(),
        LowestCostFirstSearch(),
        AStarSearch(),
    ]


def replay(problem: BridgeProblem, actions) -> tuple:
    """
    Reexecuta as ações a partir do estado inicial, validando cada travessia.
    Devolve o estado final e o custo acumulado.
    """
    state = problem.get_initial_state()
    cost = 0

    for action in actions:
        arc = next(
            (a for a in problem.get_successors(state) if a.action == action),
            None,
        )
        assert arc is not None, f"Ação inválida {action} a partir de {state}"
        state = arc.to_node
        cost += arc.cost

    return state, cost


@pytest.mark.parametrize("algorithm", all_algorithms(), ids=lambda a: a.__class__.__name__)
def test_every_algorithm_finds_a_valid_solution(problem, algorithm):
    solution = algorithm.solve(problem)

    assert solution is not None
    assert solution.end().is_goal()

    final_state, cost = replay(problem, solution.actions())
    assert final_state.is_goal()
    assert cost == solution.cost


@pytest.mark.parametrize(
    "algorithm",
    [LowestCostFirstSearch(), AStarSearch()],
    ids=lambda a: a.__class__.__name__,
)
def test_cost_based_algorithms_are_optimal(problem, algorithm):
    """Custo Mínimo e A* garantem a solução de menor tempo."""
    assert algorithm.solve(problem).cost == OPTIMAL_COST


@pytest.mark.parametrize(
    "algorithm",
    [BreadthFirstSearch(), DepthFirstSearch()],
    ids=lambda a: a.__class__.__name__,
)
def test_blind_algorithms_are_not_guaranteed_optimal(problem, algorithm):
    """
    BFS minimiza o número de travessias, não o tempo; DFS não oferece garantia
    alguma. Ambos encontram solução válida, mas não necessariamente a de menor
    custo - e é exatamente o que ocorre neste problema.
    """
    solution = algorithm.solve(problem)
    assert solution.cost >= OPTIMAL_COST


def test_bfs_minimises_number_of_crossings(problem):
    """A BFS devolve um caminho com o menor número possível de arestas."""
    bfs = BreadthFirstSearch().solve(problem)
    optimal = AStarSearch().solve(problem)
    assert len(bfs) <= len(optimal)


def test_metrics_follow_a_single_convention(problem):
    """
    O nó objetivo é removido da fronteira mas não chega a ser expandido, então
    nenhum algoritmo deve contá-lo entre os expandidos. Todo nó expandido gera
    pelo menos um sucessor, e a fronteira nunca fica vazia antes do fim.
    """
    for algorithm in all_algorithms():
        metrics = algorithm.run_once(problem)

        assert metrics.solved
        assert metrics.nodes_expanded > 0
        assert metrics.nodes_generated >= metrics.nodes_expanded
        assert metrics.max_frontier_size > 0
        assert metrics.elapsed_us > 0
        assert not metrics.cutoff


def test_expansion_limit_stops_the_search(problem):
    """O corte de segurança interrompe a busca e sinaliza que houve corte."""
    metrics = DepthFirstSearch(max_expansions=2).run_once(problem)

    assert metrics.cutoff
    assert not metrics.solved
    assert metrics.nodes_expanded == 2


def test_execute_aggregates_repetitions(problem):
    result = LowestCostFirstSearch().execute(problem, repetitions=5)

    assert result.repetitions == 5
    assert result.cost == OPTIMAL_COST
    assert result.mean_time_us > 0
    assert result.min_time_us <= result.mean_time_us


def test_execute_rejects_invalid_repetitions(problem):
    with pytest.raises(ValueError):
        BreadthFirstSearch().execute(problem, repetitions=0)


def test_path_is_built_by_extension(problem):
    """Um caminho é um nó inicial ou um caminho seguido de um arco."""
    initial = Path(problem.get_initial_state())
    assert len(initial) == 0
    assert initial.cost == 0
    assert initial.end() == problem.get_initial_state()

    arc = problem.get_successors(initial.end())[0]
    extended = initial.extend(arc)

    assert len(extended) == 1
    assert extended.cost == arc.cost
    assert extended.end() == arc.to_node
    assert extended.nodes() == [initial.end(), arc.to_node]
    # O caminho original permanece intacto: a extensão não o modifica.
    assert len(initial) == 0
