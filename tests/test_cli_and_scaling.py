import pytest

from src.algorithms.base_search import BaseSearch
from src.main import ALGORITHMS, build_algorithms, parse_args
from src.models.problem import BridgeProblem
from src.utils import scaling_experiment as scaling


def test_registry_exposes_every_method():
    assert sorted(ALGORITHMS) == ["astar-h1", "astar-h2", "bfs", "dfs", "lcfs"]


def test_build_algorithms_honours_selection_and_limit():
    algorithms = build_algorithms(["bfs", "astar-h2"], max_expansions=42, problem=BridgeProblem())

    assert [type(a).__name__ for a in algorithms] == ["BreadthFirstSearch", "AStarSearch"]
    assert all(isinstance(a, BaseSearch) for a in algorithms)
    assert all(a.max_expansions == 42 for a in algorithms)
    assert algorithms[1].display_name == "Busca A* (h2)"


def test_cli_defaults_and_overrides(monkeypatch):
    monkeypatch.setattr("sys.argv", ["src.main"])
    defaults = parse_args()
    assert defaults.algoritmos == list(ALGORITHMS)
    assert defaults.tempos == [1, 2, 5, 10]
    assert defaults.capacidade == 2

    monkeypatch.setattr(
        "sys.argv",
        ["src.main", "-a", "dfs", "-r", "5", "-t", "1", "2", "3", "-c", "3"],
    )
    custom = parse_args()
    assert custom.algoritmos == ["dfs"]
    assert custom.repeticoes == 5
    assert custom.tempos == [1, 2, 3]
    assert custom.capacidade == 3


def test_cli_rejects_unknown_algorithm(monkeypatch):
    monkeypatch.setattr("sys.argv", ["src.main", "-a", "guloso"])
    with pytest.raises(SystemExit):
        parse_args()


@pytest.fixture(scope="module")
def instance():
    # Poucas repetições bastam para o teste; o valor original é restaurado ao
    # fim do módulo para não contaminar outros testes.
    original = scaling.REPETITIONS
    scaling.REPETITIONS = 2
    try:
        yield scaling.run_instance(4)
    finally:
        scaling.REPETITIONS = original


def test_scaling_reproduces_the_assignment_instance(instance):
    """Com 4 pessoas, o experimento tem de reencontrar o grafo e o ótimo conhecidos."""
    assert instance.num_states == 30
    assert instance.num_transitions == 112
    assert instance.optimal_cost == 17


def test_informed_search_expands_less_than_blind_search(instance):
    assert instance.expanded["A* (h2)"] < instance.expanded["A* (h1)"]
    assert instance.expanded["A* (h1)"] < instance.expanded["Busca de Custo Mínimo (LCFS)"]


def test_cost_based_methods_stay_optimal_in_the_experiment(instance):
    for name in ("Busca de Custo Mínimo (LCFS)", "A* (h1)", "A* (h2)"):
        assert instance.costs[name] == instance.optimal_cost


def _fake_result(size: int, h1_time: float, h2_time: float) -> scaling.InstanceResult:
    names = ["Busca de Custo Mínimo (LCFS)", "A* (h1)", "A* (h2)"]
    return scaling.InstanceResult(
        size=size, times=(1, 2, 5, 10), num_states=30, num_transitions=112, optimal_cost=17,
        expanded=dict(zip(names, [25, 18, 14])),
        elapsed_us=dict(zip(names, [60.0, h1_time, h2_time])),
        costs={name: 17 for name in names},
    )


@pytest.mark.parametrize(
    "h1_time, h2_time, expected",
    [
        (100.0, 90.0, "cai apenas 10,0%"),
        (100.0, 100.7, "até sobe 0,7%"),
        (100.0, 100.0, "praticamente não muda"),
        (100.0, 100.04, "praticamente não muda"),
    ],
)
def test_scaling_text_matches_the_time_variation(h1_time, h2_time, expected):
    section = scaling.build_section([_fake_result(4, h1_time, h2_time)])
    assert expected in section
