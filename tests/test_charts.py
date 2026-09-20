from src.utils import generate_charts as charts

SAMPLE_REPORT = """# Resultados da Execução - Ponte e Tocha

<!-- BEGIN:escalabilidade -->

## Escalabilidade

### Nós expandidos

| Pessoas | Busca em Largura (BFS) | A* (h2) |
|--:|--:|--:|
| 4 | 25 | 14 |
| 5 | 56 | 26 |

### Tempo médio de processamento (µs)

| Pessoas | Busca em Largura (BFS) | A* (h2) |
|--:|--:|--:|
| 4 | 49,7 | 57,1 |
| 5 | 135,3 | 137,1 |

<!-- END:escalabilidade -->
"""


def test_parse_scaling_tables_reads_sizes_series_and_brazilian_decimals():
    data = charts.parse_scaling_tables(SAMPLE_REPORT)

    assert data.sizes == [4, 5]
    assert data.expanded == {"Busca em Largura (BFS)": [25, 56], "A* (h2)": [14, 26]}
    assert data.elapsed_us == {"Busca em Largura (BFS)": [49.7, 135.3], "A* (h2)": [57.1, 137.1]}


def test_generate_charts_writes_one_png_per_metric(tmp_path):
    report = tmp_path / "resultados.md"
    report.write_text(SAMPLE_REPORT, encoding="utf-8")
    output_dir = tmp_path / "figuras"

    written = charts.generate_charts(str(report), str(output_dir))

    assert sorted(path.name for path in written) == [
        "escalabilidade_nos.png",
        "escalabilidade_tempo.png",
    ]
    assert all(path.exists() and path.stat().st_size > 0 for path in written)
