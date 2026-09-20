"""
Gráficos do experimento de escalabilidade para o relatório.

Os dados são lidos das tabelas já gravadas em `resultados.md` pelo
`scaling_experiment`, e não recalculados: assim as figuras do relatório mostram
exatamente os mesmos números das tabelas, medidos na mesma execução.
"""

import math
import re
import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Dict, List, Sequence, Tuple

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from src.utils.scaling_experiment import (  # noqa: E402
    ELAPSED_HEADING,
    EXPANDED_HEADING,
    SECTION_ID,
)

DEFAULT_REPORT = Path("resultados.md")
DEFAULT_OUTPUT_DIR = Path("relatorio") / "figuras"
STATE_GRAPH_IMAGE = Path("bridge_state_graph.png")

# Uma cor fixa por método, na ordem em que os métodos aparecem nas tabelas.
# A sequência é a paleta categórica validada para daltonismo (pares
# adjacentes distinguíveis) - o rótulo direto no fim de cada linha garante a
# identificação mesmo sem a cor.
SERIES_COLORS = ("#2a78d6", "#eb6834", "#1baf7a", "#eda100", "#e87ba4")
INK_PRIMARY = "#0b0b0b"
INK_SECONDARY = "#52514e"
GRID_COLOR = "#e6e5e1"

# Nomes curtos para os rótulos diretos, quando o nome da tabela é longo.
SHORT_NAMES = {
    "Busca em Largura (BFS)": "BFS",
    "Busca em Profundidade (DFS)": "DFS",
    "Busca de Custo Mínimo (LCFS)": "Custo Mínimo",
}


@dataclass
class ScalingData:
    sizes: List[int]
    expanded: Dict[str, List[int]]
    elapsed_us: Dict[str, List[float]]


def _parse_table(text: str, heading: str) -> Tuple[List[str], List[List[str]]]:
    """Lê a primeira tabela Markdown de `text`: (cabeçalho, linhas de dados)."""
    rows = []
    for line in text.splitlines():
        line = line.strip()
        if not line.startswith("|"):
            if rows:
                break
            continue
        rows.append([cell.strip() for cell in line.strip("|").split("|")])

    if len(rows) < 2:
        raise ValueError(f"Não há tabela logo após '{heading}' em resultados.md.")

    header, body = rows[0], [row for row in rows[1:] if not set(row[0]) <= set(":-")]
    return header, body


def _number(cell: str) -> float:
    """
    Converte um número gravado pelo relatório ('1229,6', vírgula decimal) para
    float. Um ponto decimal é aceito tal e qual; nenhum separador de milhar é
    esperado, então nada é descartado silenciosamente.
    """
    return float(cell.replace(",", "."))


def _table_after(text: str, heading: str) -> Tuple[List[str], List[List[str]]]:
    position = text.find(heading)
    if position < 0:
        raise ValueError(f"Cabeçalho '{heading}' não encontrado na seção '{SECTION_ID}'.")
    return _parse_table(text[position + len(heading):], heading)


def parse_scaling_tables(report: str) -> ScalingData:
    """Extrai as tabelas de nós expandidos e de tempo da seção de escalabilidade."""
    match = re.search(
        rf"<!-- BEGIN:{SECTION_ID} -->(.*?)<!-- END:{SECTION_ID} -->", report, re.DOTALL
    )
    if match is None:
        raise ValueError(
            f"Seção '{SECTION_ID}' não encontrada; execute o experimento de escalabilidade antes."
        )
    section = match.group(1)

    header, rows = _table_after(section, EXPANDED_HEADING)
    sizes = [int(row[0]) for row in rows]
    expanded = {
        name: [int(row[index]) for row in rows]
        for index, name in enumerate(header[1:], start=1)
    }

    header, rows = _table_after(section, ELAPSED_HEADING)
    if len(rows) != len(sizes):
        raise ValueError(
            f"As tabelas de nós expandidos e de tempo têm números de linhas diferentes "
            f"({len(sizes)} e {len(rows)}); reexecute o experimento de escalabilidade."
        )
    elapsed = {
        name: [_number(row[index]) for row in rows]
        for index, name in enumerate(header[1:], start=1)
    }

    return ScalingData(sizes=sizes, expanded=expanded, elapsed_us=elapsed)


def _spread(values: Sequence[float], min_gap: float) -> List[float]:
    """
    Afasta rótulos que cairiam uns sobre os outros (em escala logarítmica),
    empurrando para cima o que for preciso e preservando a ordem.
    """
    # Em escala log um valor nulo não tem posição; usa-se um piso positivo.
    floor = 1e-3
    order = sorted(range(len(values)), key=lambda i: values[i])
    placed = [0.0] * len(values)
    previous = None
    for index in order:
        position = math.log10(max(values[index], floor))
        if previous is not None and position - previous < min_gap:
            position = previous + min_gap
        placed[index] = position
        previous = position
    return [10 ** position for position in placed]


def _draw_lines(sizes: List[int], series: Dict[str, Sequence[float]], ylabel: str, output: Path) -> None:
    fig, ax = plt.subplots(figsize=(6.4, 3.9), dpi=200)
    fig.subplots_adjust(left=0.11, right=0.86, top=0.96, bottom=0.14)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    names = list(series)
    label_positions = _spread([series[name][-1] for name in names], min_gap=0.075)

    for index, name in enumerate(names):
        color = SERIES_COLORS[index % len(SERIES_COLORS)]
        # A primeira série (BFS) costuma coincidir com a busca de custo mínimo;
        # tracejada e por cima, continua visível onde as duas se sobrepõem.
        first = index == 0
        ax.plot(sizes, series[name], color=color, linewidth=1.8, marker="o",
                markersize=5.5, markeredgecolor="white", markeredgewidth=1.0,
                linestyle=(0, (4, 2.5)) if first else "-",
                label=name, zorder=4 if first else 3)
        ax.annotate(
            SHORT_NAMES.get(name, name),
            xy=(sizes[-1], label_positions[index]), xytext=(9, 0),
            textcoords="offset points", va="center", ha="left",
            fontsize=8, color=INK_PRIMARY,
        )

    ax.set_yscale("log")
    ax.set_xticks(sizes)
    ax.set_xlabel("Número de pessoas", color=INK_SECONDARY, fontsize=9)
    ax.set_ylabel(ylabel, color=INK_SECONDARY, fontsize=9)
    ax.tick_params(which="both", colors=INK_SECONDARY, labelsize=8, length=0)
    ax.grid(True, axis="y", which="major", color=GRID_COLOR, linewidth=0.7, zorder=0)
    ax.grid(False, axis="x")
    for side in ("top", "right", "left"):
        ax.spines[side].set_visible(False)
    ax.spines["bottom"].set_color(GRID_COLOR)
    ax.set_xlim(sizes[0] - 0.2, sizes[-1] + 1.4)
    ax.legend(frameon=False, fontsize=7.5, loc="upper left", labelcolor=INK_PRIMARY)

    fig.savefig(output, bbox_inches="tight", facecolor="white")
    plt.close(fig)


def generate_charts(report_file=DEFAULT_REPORT, output_dir=DEFAULT_OUTPUT_DIR) -> List[Path]:
    """Gera os gráficos de escalabilidade e devolve os caminhos gravados."""
    data = parse_scaling_tables(Path(report_file).read_text(encoding="utf-8"))

    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    nodes_file = output_dir / "escalabilidade_nos.png"
    _draw_lines(data.sizes, data.expanded, "Nós expandidos (escala log)", nodes_file)

    time_file = output_dir / "escalabilidade_tempo.png"
    _draw_lines(data.sizes, data.elapsed_us, "Tempo médio (µs, escala log)", time_file)

    return [nodes_file, time_file]


def main() -> None:
    written = generate_charts()
    if STATE_GRAPH_IMAGE.exists():
        # O relatório é autocontido: leva a sua própria cópia do grafo.
        destination = DEFAULT_OUTPUT_DIR / STATE_GRAPH_IMAGE.name
        shutil.copyfile(STATE_GRAPH_IMAGE, destination)
        written.append(destination)
    for path in written:
        print(f"Gravado: {path}")


if __name__ == "__main__":
    main()
