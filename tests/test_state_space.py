import pytest

from src.models.problem import BridgeProblem
from src.utils.markdown_report import upsert_section
from src.utils.state_space import explore_state_space


@pytest.fixture(scope="module")
def space():
    return explore_state_space(BridgeProblem())


def test_reachable_states_exclude_impossible_torch_configurations(space):
    """
    Das 2^4 x 2 = 32 configurações concebíveis, duas são inalcançáveis: a tocha
    acompanha quem atravessa, então ninguém pode estar todo de um lado com a
    tocha do outro.
    """
    assert space.num_states == 30

    for state in space.states:
        assert not (len(state.left_side) == 4 and not state.torch_is_left)
        assert not (len(state.left_side) == 0 and state.torch_is_left)


def test_graph_size_and_degree(space):
    assert space.num_transitions == 112
    assert space.num_transitions == sum(space.out_degree(s) for s in space.states)
    assert space.min_out_degree == 1
    assert space.max_out_degree == 10
    assert space.average_out_degree == pytest.approx(112 / 30)


def test_graph_is_symmetric(space):
    """Toda travessia pode ser desfeita, o que cria os ciclos do grafo."""
    assert space.is_symmetric
    assert space.num_transitions % 2 == 0


def test_adjacency_list_is_cheaper_than_matrix(space):
    assert space.adjacency_matrix_cells == 900
    assert space.num_transitions < space.adjacency_matrix_cells
    assert space.density == pytest.approx(112 / 900)


def test_single_goal_state(space):
    assert len(space.goals) == 1
    assert space.goals[0].is_goal()


def test_optimal_cost_from_initial_state(space):
    assert space.optimal_costs_to_goal()[space.initial] == 17


def test_labels_are_unique_and_ordered(space):
    labels = [space.label(state) for state in space.states]
    assert labels == sorted(labels)
    assert len(set(labels)) == len(labels)


def test_report_sections_are_idempotent(tmp_path):
    """
    Reexecutar um gerador substitui a sua própria seção e preserva as demais,
    de modo que o relatório nunca acumula conteúdo duplicado.
    """
    report = tmp_path / "resultados.md"

    assert upsert_section(str(report), "metricas", "tabela v1") is False
    assert upsert_section(str(report), "transicoes", "transicoes v1") is False

    first = report.read_text(encoding="utf-8")

    assert upsert_section(str(report), "transicoes", "transicoes v1") is True
    assert report.read_text(encoding="utf-8") == first

    assert upsert_section(str(report), "metricas", "tabela v2") is True
    updated = report.read_text(encoding="utf-8")

    assert "tabela v2" in updated
    assert "tabela v1" not in updated
    assert "transicoes v1" in updated
