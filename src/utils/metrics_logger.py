from typing import Any, Dict, List

from src.utils.markdown_report import upsert_section

SECTION_ID = "metricas"

COLUMNS = [
    ("Algoritmo", "<", lambda r: r.display_name),
    ("Custo (min)", ">", lambda r: _cost(r)),
    ("Travessias", ">", lambda r: str(r.solution_length)),
    ("Nós expandidos", ">", lambda r: str(r.nodes_expanded)),
    ("Nós gerados", ">", lambda r: str(r.nodes_generated)),
    ("Fronteira máx.", ">", lambda r: str(r.max_frontier_size)),
    ("Tempo médio (µs)", ">", lambda r: _decimal(r.mean_time_us)),
    ("Desvio (µs)", ">", lambda r: _decimal(r.stdev_time_us)),
    ("Tempo mín. (µs)", ">", lambda r: _decimal(r.min_time_us)),
]


def _decimal(value: float, places: int = 2) -> str:
    """Formata número no padrão brasileiro (vírgula decimal)."""
    return f"{value:.{places}f}".replace(".", ",")


def _cost(result) -> str:
    if result.cutoff:
        return "limite atingido"
    if not result.solved:
        return "sem solução"
    return str(result.cost)


def build_table(results: List[Any]) -> List[str]:
    """
    Monta a tabela comparativa em Markdown.

    A mesma função alimenta a impressão no terminal e a gravação do relatório,
    evitando que os dois formatos saiam do lugar um do outro.
    """
    rows = [[render(result) for _, _, render in COLUMNS] for result in results]
    widths = [
        max(len(title), *(len(row[index]) for row in rows)) if rows else len(title)
        for index, (title, _, _) in enumerate(COLUMNS)
    ]

    header = "| " + " | ".join(
        title.ljust(widths[index]) for index, (title, _, _) in enumerate(COLUMNS)
    ) + " |"
    divider = "|" + "|".join(
        (":" + "-" * (widths[index] + 1)) if align == "<" else ("-" * (widths[index] + 1) + ":")
        for index, (_, align, _) in enumerate(COLUMNS)
    ) + "|"

    lines = [header, divider]
    for row in rows:
        lines.append("| " + " | ".join(
            cell.ljust(widths[index]) if COLUMNS[index][1] == "<" else cell.rjust(widths[index])
            for index, cell in enumerate(row)
        ) + " |")

    return lines


def build_solution_steps(result, ascii_only: bool = False) -> List[str]:
    """Lista as travessias da solução encontrada, alternando ida e volta."""
    forward, backward = ("->", "<-") if ascii_only else ("→", "←")
    lines = []
    for step, action in enumerate(result.path, 1):
        is_forward = step % 2 != 0
        direction = f"Ida ({forward})" if is_forward else f"Volta ({backward})"
        group = "{" + ", ".join(map(str, sorted(action))) + "}"
        lines.append(f"- **Passo {step}:** {direction} {group}")
    return lines


def _optimal(results: List[Any]):
    """Melhor resultado encontrado (menor custo), usado para exibir a solução ótima."""
    solved = [r for r in results if r.solved]
    return min(solved, key=lambda r: r.cost) if solved else None


def build_metrics_section(results: List[Any], repetitions: int) -> List[str]:
    content = [
        "## Tabela Comparativa de Desempenho",
        "",
        f"Cada algoritmo foi executado **{repetitions}** vez(es) sobre o mesmo problema.",
        "Custo, número de nós e tamanho da fronteira são determinísticos e se repetem a cada",
        "execução; o tempo de processamento é reportado como média e desvio-padrão das",
        "repetições, medido com `time.perf_counter()` e expresso em microssegundos (µs).",
        "",
    ]
    content.extend(build_table(results))
    content.append("")

    best = _optimal(results)
    if best is not None:
        content.append("## Caminho da Solução Ótima")
        content.append("")
        content.append(
            f"Encontrado pela {best.display_name}: **{best.cost} minutos** em "
            f"{best.solution_length} travessias."
        )
        content.append("")
        content.extend(build_solution_steps(best))
        content.append("")

    return content


def print_metrics_table(results: List[Any], repetitions: int = 1) -> None:
    """
    Formata e exibe os resultados no terminal em formato de tabela Markdown,
    facilitando a cópia direta para o relatório em LaTeX.
    """
    print(f"\n### Resultados da Execução ({repetitions} repetição(ões) por algoritmo)\n")
    for line in build_table(results):
        print(line)

    best = _optimal(results)
    if best is not None:
        print(f"\n### Caminho da Solução Ótima - {best.display_name}, custo {best.cost} min\n")
        for line in build_solution_steps(best, ascii_only=True):
            print(line.replace("**", ""))


def save_metrics_to_markdown(
    results: List[Any],
    filename: str = "resultados.md",
    repetitions: int = 1,
) -> None:
    """
    Grava a seção de métricas no relatório em Markdown.

    A escrita é feita por seção: reexecutar este comando substitui apenas a
    tabela comparativa, preservando as demais seções do arquivo (como o
    mapeamento de transições).
    """
    section = "\n".join(build_metrics_section(results, repetitions))
    replaced = upsert_section(filename, SECTION_ID, section)

    action = "atualizada" if replaced else "criada"
    print(f"\nMétricas avaliadas. Seção de resultados {action} em '{filename}'.")
