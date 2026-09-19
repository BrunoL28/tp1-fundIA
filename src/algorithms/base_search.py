import statistics
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from src.models.path import Path
from src.models.problem import BridgeProblem

DEFAULT_MAX_EXPANSIONS = 15000
DEFAULT_REPETITIONS = 1


@dataclass
class SearchMetrics:
    """
    Métricas de uma execução de busca.

    Convenção única para todos os algoritmos (ver `BaseSearch.count_expansion`):
    - `nodes_expanded`: caminhos retirados da fronteira e efetivamente
      expandidos, isto é, cujos vizinhos foram gerados. O caminho-solução não
      conta como expandido, pois a busca termina antes de expandi-lo.
    - `nodes_generated`: caminhos criados pela expansão (inclui os descartados
      em seguida pela poda de caminhos múltiplos). Não inclui o caminho inicial.
    - `max_frontier_size`: maior número de caminhos simultaneamente na
      fronteira, uma medida do custo de memória da estratégia.
    """
    algorithm: str
    display_name: str
    solution: Optional[Path] = None
    path: List[tuple] = field(default_factory=list)
    cost: float = float("inf")
    nodes_expanded: int = 0
    nodes_generated: int = 0
    max_frontier_size: int = 0
    elapsed_us: float = 0.0
    solved: bool = False
    cutoff: bool = False

    @property
    def solution_length(self) -> int:
        return len(self.path)


@dataclass
class AggregatedMetrics:
    """
    Resultado consolidado de N repetições do mesmo algoritmo.

    Custo, caminhos expandidos/gerados e fronteira máxima são determinísticos e
    se repetem a cada execução; o que varia entre repetições é o tempo de
    processamento, por isso ele é reportado como média, desvio-padrão e mínimo.
    """
    algorithm: str
    display_name: str
    repetitions: int
    solution: Optional[Path]
    path: List[tuple]
    cost: float
    nodes_expanded: int
    nodes_generated: int
    max_frontier_size: int
    mean_time_us: float
    stdev_time_us: float
    min_time_us: float
    solved: bool
    cutoff: bool

    @property
    def solution_length(self) -> int:
        return len(self.path)


class BaseSearch(ABC):
    """
    Interface base para todos os algoritmos de busca.

    Implementa o procedimento geral de busca: a fronteira é um conjunto de
    caminhos, inicializada com o caminho de custo zero formado pelo nó
    inicial; a cada passo um caminho <n_0, ..., n_k> é selecionado e
    removido; se n_k satisfaz o objetivo, o caminho é a solução; caso
    contrário, ele é expandido nos caminhos <n_0, ..., n_k, n> para cada
    vizinho n de n_k. O que distingue as estratégias é apenas o critério de
    seleção do próximo caminho, definido em `solve`.
    """

    display_name = "Busca"

    def __init__(self, max_expansions: int = DEFAULT_MAX_EXPANSIONS):
        # Limite de segurança para evitar buscas excessivamente longas, útil para o DFS
        self.max_expansions = max_expansions
        self._reset_counters()

    # ------------------------------------------------------------------
    # Contadores compartilhados: garantem que os algoritmos meçam exatamente
    # a mesma coisa, tornando a tabela comparativa justa.
    # ------------------------------------------------------------------
    def _reset_counters(self) -> None:
        self.nodes_expanded = 0
        self.nodes_generated = 0
        self.max_frontier_size = 0
        self.cutoff_reached = False

    def count_expansion(self) -> None:
        """Registra que um caminho foi retirado da fronteira e será expandido."""
        self.nodes_expanded += 1

    def count_generated(self, amount: int = 1) -> None:
        """Registra caminhos criados pela expansão."""
        self.nodes_generated += amount

    def observe_frontier(self, size: int) -> None:
        """Atualiza o pico de ocupação da fronteira."""
        if size > self.max_frontier_size:
            self.max_frontier_size = size

    def expansion_limit_reached(self) -> bool:
        """Corte de segurança exigido pelo enunciado para buscas muito longas."""
        if self.nodes_expanded >= self.max_expansions:
            self.cutoff_reached = True
            return True
        return False

    @abstractmethod
    def solve(self, problem: BridgeProblem) -> Optional[Path]:
        """
        Método central da busca: devolve o caminho-solução ou None.
        Implementado pelas classes filhas (BFS, DFS, Custo Mínimo, A*).
        """
        pass

    def run_once(self, problem: BridgeProblem) -> SearchMetrics:
        """
        Executa a busca uma única vez, medindo o tempo com `perf_counter`.

        `time.process_time()` não serve aqui: no Windows sua granularidade
        efetiva é o quantum do escalonador (~15,6 ms), enquanto as buscas neste
        problema levam dezenas ou centenas de microssegundos - daí a tabela de
        tempos vir inteiramente zerada. `perf_counter` é monotônico e tem
        resolução de nanossegundos.
        """
        self._reset_counters()

        start = time.perf_counter()
        solution = self.solve(problem)
        elapsed_us = (time.perf_counter() - start) * 1_000_000

        metrics = SearchMetrics(
            algorithm=self.__class__.__name__,
            display_name=self.display_name,
            nodes_expanded=self.nodes_expanded,
            nodes_generated=self.nodes_generated,
            max_frontier_size=self.max_frontier_size,
            elapsed_us=elapsed_us,
            cutoff=self.cutoff_reached,
        )

        if solution is not None:
            metrics.solution = solution
            metrics.path = solution.actions()
            metrics.cost = solution.cost
            metrics.solved = True

        return metrics

    def execute(self, problem: BridgeProblem, repetitions: int = DEFAULT_REPETITIONS) -> AggregatedMetrics:
        """
        Executa a busca `repetitions` vezes e consolida as métricas.

        O enunciado pede a comparação dos métodos em termos de valores médios;
        repetir a busca é o que permite estimar o tempo de processamento com
        estabilidade, já que uma única execução é curta demais para ser medida
        com confiança.
        """
        if repetitions < 1:
            raise ValueError("O número de repetições deve ser no mínimo 1.")

        samples: List[SearchMetrics] = [self.run_once(problem) for _ in range(repetitions)]
        times = [sample.elapsed_us for sample in samples]
        reference = samples[0]

        return AggregatedMetrics(
            algorithm=reference.algorithm,
            display_name=reference.display_name,
            repetitions=repetitions,
            solution=reference.solution,
            path=reference.path,
            cost=reference.cost,
            nodes_expanded=reference.nodes_expanded,
            nodes_generated=reference.nodes_generated,
            max_frontier_size=reference.max_frontier_size,
            mean_time_us=statistics.fmean(times),
            stdev_time_us=statistics.stdev(times) if len(times) > 1 else 0.0,
            min_time_us=min(times),
            solved=reference.solved,
            cutoff=reference.cutoff,
        )
