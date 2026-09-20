"""
Experimento de escalabilidade.

Com quatro pessoas, o espaço de estados tem apenas 30 estados e os quatro
métodos terminam em microssegundos, o que esconde as diferenças entre eles.
Aumentando o número de pessoas, o espaço cresce como 2^n x 2 e as diferenças
aparecem: a busca cega precisa varrer quase tudo, enquanto a A* com uma
heurística informativa continua expandindo uma fração do grafo.
"""

from dataclasses import dataclass
from typing import Dict, List, Sequence

from src.algorithms.base_search import BaseSearch
from src.algorithms.informed import AStarSearch
from src.algorithms.uninformed import (
    BreadthFirstSearch,
    DepthFirstSearch,
    LowestCostFirstSearch,
)
from src.models.problem import BridgeProblem
from src.utils.heuristics import get_heuristic
from src.utils.markdown_report import upsert_section
from src.utils.state_space import explore_state_space

SECTION_ID = "escalabilidade"

# Instância do enunciado, estendida com pessoas progressivamente mais lentas.
TIME_POOL = (1, 2, 5, 10, 15, 20, 25, 30)
SIZES = (4, 5, 6, 7, 8)
REPETITIONS = 200
MAX_EXPANSIONS = 200000


def build_algorithms() -> List[BaseSearch]:
    return [
        BreadthFirstSearch(max_expansions=MAX_EXPANSIONS),
        DepthFirstSearch(max_expansions=MAX_EXPANSIONS),
        LowestCostFirstSearch(max_expansions=MAX_EXPANSIONS),
        AStarSearch(heuristic=get_heuristic("h1"), max_expansions=MAX_EXPANSIONS,
                    display_name="A* (h1)"),
        AStarSearch(heuristic=get_heuristic("h2"), max_expansions=MAX_EXPANSIONS,
                    display_name="A* (h2)"),
    ]


@dataclass
class InstanceResult:
    size: int
    times: Sequence[int]
    num_states: int
    num_transitions: int
    optimal_cost: float
    expanded: Dict[str, int]
    elapsed_us: Dict[str, float]
    costs: Dict[str, float]


def run_instance(size: int) -> InstanceResult:
    times = TIME_POOL[:size]
    problem = BridgeProblem(times=times)
    space = explore_state_space(problem)
    problem.warm_cache()

    expanded, elapsed, costs = {}, {}, {}
    for algorithm in build_algorithms():
        result = algorithm.execute(problem, repetitions=REPETITIONS)
        expanded[algorithm.display_name] = result.nodes_expanded
        elapsed[algorithm.display_name] = result.mean_time_us
        costs[algorithm.display_name] = result.cost

    return InstanceResult(
        size=size,
        times=times,
        num_states=space.num_states,
        num_transitions=space.num_transitions,
        optimal_cost=space.optimal_costs_to_goal()[space.initial],
        expanded=expanded,
        elapsed_us=elapsed,
        costs=costs,
    )


def _decimal(value: float, places: int = 1) -> str:
    return f"{value:.{places}f}".replace(".", ",")


def build_section(results: List[InstanceResult]) -> str:
    names = list(results[0].expanded)

    lines = [
        "## Escalabilidade: crescimento com o número de pessoas",
        "",
        "A instância do enunciado (quatro pessoas) é pequena demais para separar os métodos.",
        "Aumentando o grupo - mantendo a ponte com capacidade para duas pessoas e acrescentando",
        f"travessias progressivamente mais lentas a partir de {list(TIME_POOL[:4])} -, o espaço de",
        "estados cresce como 2^n x 2 e as diferenças ficam evidentes.",
        "",
        "### Tamanho do grafo e solução ótima",
        "",
        r"| Pessoas | Tempos | Estados (\|V\|) | Transições (\|E\|) | Custo ótimo |",
        "|--:|:--|--:|--:|--:|",
    ]

    for result in results:
        lines.append(
            f"| {result.size} | {', '.join(map(str, result.times))} | {result.num_states} | "
            f"{result.num_transitions} | {result.optimal_cost:.0f} |"
        )

    lines.extend([
        "",
        "### Nós expandidos",
        "",
        "| Pessoas | " + " | ".join(names) + " |",
        "|--:|" + "|".join(["--:"] * len(names)) + "|",
    ])

    for result in results:
        lines.append(
            f"| {result.size} | " + " | ".join(str(result.expanded[name]) for name in names) + " |"
        )

    lines.extend([
        "",
        "### Tempo médio de processamento (µs)",
        "",
        "| Pessoas | " + " | ".join(names) + " |",
        "|--:|" + "|".join(["--:"] * len(names)) + "|",
    ])

    for result in results:
        lines.append(
            f"| {result.size} | "
            + " | ".join(_decimal(result.elapsed_us[name]) for name in names) + " |"
        )

    largest = results[-1]
    blind = largest.expanded["Busca de Custo Mínimo (LCFS)"]
    informed = largest.expanded["A* (h2)"]

    # Só afirmamos subotimalidade para quem falhou em todas as instâncias.
    suboptimal = [
        name for name in names
        if all(result.costs[name] > result.optimal_cost for result in results)
    ]

    lines.extend([
        "",
        f"Com {largest.size} pessoas, a Busca de Custo Mínimo expande {blind} dos "
        f"{largest.num_states} estados do grafo, enquanto a A* com h₂ expande {informed} "
        f"({_decimal(100 * informed / blind)}% do total da busca cega) e chega ao mesmo custo",
        "ótimo. É esse o ganho que a heurística traz e que a instância de quatro pessoas não",
        "deixa enxergar.",
        "",
    ])

    if suboptimal:
        lines.extend([
            "Em todas as instâncias testadas, " + " e ".join(suboptimal) + " devolveram soluções",
            "subótimas. O DFS é o caso mais eloquente: é de longe quem menos expande e, ainda",
            "assim, nunca encontra a melhor solução - expandir pouco não é sinal de qualidade,",
            "apenas de parar no primeiro ramo que alcança o objetivo.",
            "",
        ])

    h1_time = largest.elapsed_us["A* (h1)"]
    h2_time = largest.elapsed_us["A* (h2)"]
    node_drop = 100 * (1 - largest.expanded["A* (h2)"] / largest.expanded["A* (h1)"])
    time_drop = 100 * (1 - h2_time / h1_time)

    if node_drop > time_drop:
        lines.extend([
            "Um detalhe que a tabela de tempos revela: de h₁ para h₂ os nós expandidos caem",
            f"{_decimal(node_drop)}%, mas o tempo cai apenas {_decimal(time_drop)}%. A heurística mais",
            "informativa poda mais, porém custa mais caro por nó avaliado - ela ordena os tempos",
            "da margem esquerda a cada chamada, enquanto h₁ apenas toma um máximo. O ganho em nós",
            "expandidos não se converte integralmente em ganho de tempo.",
            "",
        ])

    return "\n".join(lines)


def generate_and_save_scaling(filename: str = "resultados.md") -> List[InstanceResult]:
    results = []
    for size in SIZES:
        print(f"Instância com {size} pessoas...")
        results.append(run_instance(size))

    replaced = upsert_section(filename, SECTION_ID, build_section(results))

    for result in results:
        resumo = ", ".join(f"{k}={v}" for k, v in result.expanded.items())
        print(f"  n={result.size}: |V|={result.num_states}, otimo={result.optimal_cost:.0f}, {resumo}")

    action = "atualizada" if replaced else "criada"
    print(f"Seção de escalabilidade {action} em '{filename}'.")
    return results


if __name__ == "__main__":
    generate_and_save_scaling()
