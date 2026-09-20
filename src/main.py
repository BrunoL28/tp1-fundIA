import argparse
import sys
from typing import Callable, Dict, List

from src.algorithms.base_search import BaseSearch, DEFAULT_MAX_EXPANSIONS
from src.algorithms.informed import AStarSearch
from src.algorithms.uninformed import (
    BreadthFirstSearch,
    DepthFirstSearch,
    LowestCostFirstSearch,
)
from src.models.problem import BridgeProblem, DEFAULT_CAPACITY, DEFAULT_TIMES
from src.utils.heuristics import get_heuristic
from src.utils.metrics_logger import print_metrics_table, save_metrics_to_markdown

DEFAULT_REPETITIONS = 1000

# Registro dos métodos disponíveis: a chave é o nome usado na linha de comando
# e o valor é a fábrica que constrói o algoritmo com o limite de expansões e o
# problema (de que as heurísticas dependem: h2 usa a capacidade da ponte).
ALGORITHMS: Dict[str, Callable[[int, BridgeProblem], BaseSearch]] = {
    "bfs": lambda limit, problem: BreadthFirstSearch(max_expansions=limit),
    "dfs": lambda limit, problem: DepthFirstSearch(max_expansions=limit),
    "lcfs": lambda limit, problem: LowestCostFirstSearch(max_expansions=limit),
    "astar-h1": lambda limit, problem: AStarSearch(
        heuristic=get_heuristic("h1", problem), max_expansions=limit, display_name="Busca A* (h1)"
    ),
    "astar-h2": lambda limit, problem: AStarSearch(
        heuristic=get_heuristic("h2", problem), max_expansions=limit, display_name="Busca A* (h2)"
    ),
}


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


def build_algorithms(
    names: List[str], max_expansions: int, problem: BridgeProblem
) -> List[BaseSearch]:
    return [ALGORITHMS[name](max_expansions, problem) for name in names]


def parse_args():
    parser = argparse.ArgumentParser(
        description="Resolve o problema da Ponte e da Tocha com quatro estratégias de busca."
    )
    parser.add_argument(
        "-a", "--algoritmos",
        nargs="+",
        choices=sorted(ALGORITHMS),
        default=list(ALGORITHMS),
        metavar="NOME",
        help=f"Métodos a executar (padrão: todos). Opções: {', '.join(sorted(ALGORITHMS))}.",
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
        "-t", "--tempos",
        nargs="+",
        type=int,
        default=list(DEFAULT_TIMES),
        metavar="MIN",
        help=f"Tempos de travessia das pessoas (padrão: {' '.join(map(str, DEFAULT_TIMES))}).",
    )
    parser.add_argument(
        "-c", "--capacidade",
        type=int,
        default=DEFAULT_CAPACITY,
        help=f"Quantas pessoas a ponte suporta por vez (padrão: {DEFAULT_CAPACITY}).",
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
    parser.add_argument(
        "--sem-cache",
        action="store_true",
        help="Desliga a memoização da função sucessora, medindo o custo de regerá-la.",
    )
    return parser.parse_args()


def main():
    configure_stdout()
    args = parse_args()

    problem = BridgeProblem(
        times=args.tempos,
        capacity=args.capacidade,
        memoize=not args.sem_cache,
    )
    algorithms = build_algorithms(args.algoritmos, args.max_expansoes, problem)

    print("Iniciando resolução do problema Ponte e Tocha...")
    print(f"Tempos: {list(args.tempos)} | capacidade: {args.capacidade}")
    print(f"Repetições por algoritmo: {args.repeticoes}")

    if problem.memoize:
        # Aquece o cache antes de cronometrar, para que todos os algoritmos
        # sejam medidos nas mesmas condições e a ordem de execução não influa.
        print(f"Cache da função sucessora aquecido: {problem.warm_cache()} estados\n")
    else:
        print()

    results = []
    for algorithm in algorithms:
        print(f"Executando {algorithm.display_name}...")
        results.append(algorithm.execute(problem, repetitions=args.repeticoes))

    print_metrics_table(results, repetitions=args.repeticoes)
    save_metrics_to_markdown(results, filename=args.saida, repetitions=args.repeticoes)


if __name__ == "__main__":
    main()
