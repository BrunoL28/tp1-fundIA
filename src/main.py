import argparse
import sys

from src.algorithms.base_search import DEFAULT_MAX_EXPANSIONS
from src.algorithms.informed import AStarSearch
from src.algorithms.uninformed import (
    BreadthFirstSearch,
    DepthFirstSearch,
    LowestCostFirstSearch,
)
from src.models.problem import BridgeProblem
from src.utils.heuristics import HEURISTICS
from src.utils.metrics_logger import print_metrics_table, save_metrics_to_markdown

DEFAULT_REPETITIONS = 1000


def configure_stdout() -> None:
    """
    Evita que o relatório no terminal quebre em consoles que não usam UTF-8
    (caso do Windows com code page 1252). O arquivo Markdown continua sendo
    gravado sempre em UTF-8.
    """
    try:
        sys.stdout.reconfigure(errors="replace")
    except (AttributeError, ValueError):
        pass


def build_algorithms(max_expansions: int):
    """
    Os quatro métodos pedidos pelo enunciado, mais uma segunda execução da A*
    com a heurística alternativa, para comparar o efeito da informatividade da
    heurística sobre o número de nós expandidos.
    """
    algorithms = [
        BreadthFirstSearch(max_expansions=max_expansions),
        DepthFirstSearch(max_expansions=max_expansions),
        LowestCostFirstSearch(max_expansions=max_expansions),
    ]

    for name, heuristic in HEURISTICS.items():
        algorithms.append(
            AStarSearch(
                heuristic=heuristic,
                max_expansions=max_expansions,
                display_name=f"Busca A* ({name})",
            )
        )

    return algorithms


def parse_args():
    parser = argparse.ArgumentParser(
        description="Resolve o problema da Ponte e da Tocha com quatro estratégias de busca."
    )
    parser.add_argument(
        "-r", "--repeticoes",
        type=int,
        default=DEFAULT_REPETITIONS,
        help=(
            "Número de execuções de cada algoritmo para o cálculo do tempo médio "
            f"e do desvio-padrão (padrão: {DEFAULT_REPETITIONS})."
        ),
    )
    parser.add_argument(
        "-o", "--saida",
        default="resultados.md",
        help="Arquivo Markdown de saída (padrão: resultados.md).",
    )
    parser.add_argument(
        "--max-expansoes",
        type=int,
        default=DEFAULT_MAX_EXPANSIONS,
        help=(
            "Limite de nós expandidos antes de abortar a busca "
            f"(padrão: {DEFAULT_MAX_EXPANSIONS})."
        ),
    )
    return parser.parse_args()


def main():
    configure_stdout()
    args = parse_args()
    problem = BridgeProblem()
    algorithms = build_algorithms(args.max_expansoes)

    print("Iniciando resolução do problema Ponte e Tocha...")
    print(f"Repetições por algoritmo: {args.repeticoes}\n")

    results = []
    for algorithm in algorithms:
        print(f"Executando {algorithm.display_name}...")
        results.append(algorithm.execute(problem, repetitions=args.repeticoes))

    print_metrics_table(results, repetitions=args.repeticoes)
    save_metrics_to_markdown(results, filename=args.saida, repetitions=args.repeticoes)


if __name__ == "__main__":
    main()
