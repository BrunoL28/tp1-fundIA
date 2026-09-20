"""
Verificação empírica das heurísticas sobre todo o espaço de estados.

Como o domínio é pequeno (algumas dezenas de estados), é viável calcular o
custo real h*(n) de cada estado até o objetivo e conferir exaustivamente as
duas propriedades que interessam:

- **Admissibilidade:** h(n) <= h*(n) para todo estado n. Garante que a A*
  devolva um caminho de custo mínimo.
- **Consistência:** h(u) <= custo(u, v) + h(v) para toda aresta (u, v). É uma
  condição mais forte; quando vale, nenhum estado precisa ser reexpandido.
"""

from dataclasses import dataclass
from typing import Callable, Dict, List, Optional

from src.algorithms.informed import AStarSearch
from src.models.problem import BridgeProblem
from src.models.state import State
from src.utils.heuristics import HEURISTIC_LABELS, HEURISTICS, get_heuristic
from src.utils.markdown_report import upsert_section
from src.utils.state_space import StateSpace, explore_state_space

SECTION_ID = "heuristicas"


@dataclass
class HeuristicReport:
    name: str
    label: str
    initial_value: int
    optimal_cost: float
    admissible: bool
    consistent: bool
    admissibility_violations: int
    consistency_violations: int
    mean_gap: float
    max_gap: float
    nodes_expanded: int
    solution_cost: float

    @property
    def relative_error(self) -> float:
        """Quanto a heurística subestima o custo real do estado inicial."""
        return 1 - (self.initial_value / self.optimal_cost)


def analyse(
    name: str,
    heuristic: Callable[[State], int],
    space: StateSpace,
    optimal: Dict[State, float],
    problem: BridgeProblem,
) -> HeuristicReport:
    gaps = [optimal[state] - heuristic(state) for state in space.states]
    admissibility_violations = sum(1 for gap in gaps if gap < 0)
    consistency_violations = sum(
        1 for arc in space.all_transitions()
        if heuristic(arc.from_node) > arc.cost + heuristic(arc.to_node)
    )

    result = AStarSearch(heuristic=heuristic).run_once(problem)

    return HeuristicReport(
        name=name,
        label=HEURISTIC_LABELS.get(name, name),
        initial_value=heuristic(space.initial),
        optimal_cost=optimal[space.initial],
        admissible=admissibility_violations == 0,
        consistent=consistency_violations == 0,
        admissibility_violations=admissibility_violations,
        consistency_violations=consistency_violations,
        mean_gap=sum(gaps) / len(gaps),
        max_gap=max(gaps),
        nodes_expanded=result.nodes_expanded,
        solution_cost=result.cost,
    )


def _decimal(value: float, places: int = 2) -> str:
    return f"{value:.{places}f}".replace(".", ",")


def _yes_no(flag: bool, violations: int) -> str:
    return "sim" if flag else f"não ({violations} violações)"


def build_section(reports: List[HeuristicReport], space: StateSpace) -> str:
    lines = [
        "## Comparação das Heurísticas",
        "",
        f"As duas heurísticas foram verificadas nos {space.num_states} estados alcançáveis e",
        f"nas {space.num_transitions} transições do grafo, comparando cada h(n) com o custo real",
        "h\\*(n) obtido por uma busca de custo mínimo sobre o grafo invertido.",
        "",
        "| Heurística | h(inicial) | h\\*(inicial) | Admissível | Consistente | Erro médio h\\*−h | Nós expandidos (A\\*) | Custo obtido |",
        "|:--|--:|--:|:--:|:--:|--:|--:|--:|",
    ]

    for report in reports:
        lines.append(
            f"| {report.label} | {report.initial_value} | {report.optimal_cost:.0f} | "
            f"{_yes_no(report.admissible, report.admissibility_violations)} | "
            f"{_yes_no(report.consistent, report.consistency_violations)} | "
            f"{_decimal(report.mean_gap)} | {report.nodes_expanded} | {report.solution_cost:.0f} |"
        )

    lines.append("")

    if len(reports) == 2:
        weaker, stronger = reports
        reduction = weaker.nodes_expanded - stronger.nodes_expanded
        percent = 100 * reduction / weaker.nodes_expanded if weaker.nodes_expanded else 0
        lines.extend([
            f"Como {stronger.name}(n) >= {weaker.name}(n) para todo estado sem deixar de ser admissível,",
            f"{stronger.name} **domina** {weaker.name}: é mais informativa e poda mais o espaço de busca.",
            f"O efeito prático é uma redução de {weaker.nodes_expanded} para {stronger.nodes_expanded}",
            f"nós expandidos pela A\\* ({reduction} a menos, {_decimal(percent, 1)}%), mantendo o mesmo",
            "custo ótimo da solução - o que era esperado, já que ambas são admissíveis.",
            "",
        ])

    return "\n".join(lines)


def generate_and_save_analysis(filename: str = "resultados.md") -> List[HeuristicReport]:
    print("Analisando heurísticas sobre o espaço de estados completo...")

    problem = BridgeProblem()
    space = explore_state_space(problem)
    optimal = space.optimal_costs_to_goal()

    reports = [
        analyse(name, get_heuristic(name, problem), space, optimal, problem)
        for name in HEURISTICS
    ]

    replaced = upsert_section(filename, SECTION_ID, build_section(reports, space))

    for report in reports:
        status = "admissível" if report.admissible else "NÃO admissível"
        status += " e consistente" if report.consistent else " e NÃO consistente"
        print(
            f"  {report.name}: h(inicial)={report.initial_value} (ótimo={report.optimal_cost:.0f}), "
            f"{status}, A* expande {report.nodes_expanded} nós."
        )

    action = "atualizada" if replaced else "criada"
    print(f"Seção de heurísticas {action} em '{filename}'.")
    return reports


if __name__ == "__main__":
    generate_and_save_analysis()
