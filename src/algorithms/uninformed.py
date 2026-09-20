"""
Estratégias de busca desinformadas ("cegas").

Nenhuma delas usa informação prévia sobre onde o objetivo provavelmente está:
BFS seleciona o caminho com menor número de arestas e a Busca pelo Primeiro
Caminho de Custo Mínimo (lowest-cost-first search) seleciona o caminho de menor
custo acumulado. As três compartilham o mesmo procedimento geral de busca,
variando apenas o critério de seleção do próximo caminho da fronteira.
"""

import heapq
from collections import deque
from typing import Optional, Set

from src.algorithms.base_search import BaseSearch
from src.models.path import Path
from src.models.problem import BridgeProblem


class BreadthFirstSearch(BaseSearch):
    """
    Busca em Largura (BFS).

    A fronteira é uma fila FIFO de caminhos: a cada iteração é selecionado um
    caminho com o menor número de arestas, o que equivale a explorar o grafo em
    níveis a partir do nó inicial.
    """

    display_name = "Busca em Largura (BFS)"

    def solve(self, problem: BridgeProblem) -> Optional[Path]:
        initial = Path(problem.get_initial_state())

        frontier = deque([initial])
        frontier_states = {initial.end()}
        explored: Set = set()
        self.observe_frontier(len(frontier))

        while frontier:
            # Prevenção contra processamento excessivo
            if self.expansion_limit_reached():
                return None

            path = frontier.popleft()
            node = path.end()
            frontier_states.discard(node)

            # O teste de objetivo é feito sobre o caminho selecionado, no
            # momento em que ele é removido da fronteira.
            if node.is_goal():
                return path

            explored.add(node)
            self.count_expansion()

            for arc in problem.get_successors(node):
                self.count_generated()

                # Poda de caminhos múltiplos: um estado já explorado ou já
                # presente na fronteira não precisa entrar de novo, pois
                # qualquer caminho até ele já foi (ou será) considerado.
                if arc.to_node in explored or arc.to_node in frontier_states:
                    continue

                frontier.append(path.extend(arc))
                frontier_states.add(arc.to_node)
                self.observe_frontier(len(frontier))

        return None


class DepthFirstSearch(BaseSearch):
    """
    Busca em Profundidade (DFS).

    A fronteira é uma pilha LIFO de caminhos: a cada iteração é selecionado o
    caminho mais recentemente adicionado, aprofundando um ramo antes de
    considerar alternativas.

    A poda de caminhos múltiplos é indispensável aqui: como toda travessia é
    reversível, o grafo tem ciclos e um DFS sem verificação de estados
    repetidos ficaria preso indefinidamente indo e voltando pela ponte.
    """

    display_name = "Busca em Profundidade (DFS)"

    def solve(self, problem: BridgeProblem) -> Optional[Path]:
        initial = Path(problem.get_initial_state())

        frontier = [initial]
        frontier_states = {initial.end()}
        explored: Set = set()
        self.observe_frontier(len(frontier))

        while frontier:
            if self.expansion_limit_reached():
                return None

            path = frontier.pop()
            node = path.end()
            frontier_states.discard(node)

            if node.is_goal():
                return path

            explored.add(node)
            self.count_expansion()

            # Inverter a ordem dos sucessores faz com que a pilha os desempilhe
            # na ordem em que a função sucessora os gerou.
            for arc in reversed(problem.get_successors(node)):
                self.count_generated()

                if arc.to_node in explored or arc.to_node in frontier_states:
                    continue

                frontier.append(path.extend(arc))
                frontier_states.add(arc.to_node)
                self.observe_frontier(len(frontier))

        return None


class LowestCostFirstSearch(BaseSearch):
    """
    Busca pelo Primeiro Caminho de Custo Mínimo (lowest-cost-first search),
    também conhecida como Busca de Custo Uniforme (UCS).

    Procedimento análogo ao da BFS, porém, em vez de selecionar o caminho com o
    menor número de arestas, seleciona o caminho de menor custo acumulado até o
    momento. A fronteira é tratada como uma fila de prioridades (`heapq`),
    ordenada por cost(p).

    Como o custo de toda travessia é positivo, o primeiro caminho até o
    objetivo a ser selecionado é necessariamente um caminho de custo mínimo -
    daí a garantia de otimalidade que a BFS não oferece.
    """

    display_name = "Busca de Custo Mínimo (LCFS)"

    def solve(self, problem: BridgeProblem) -> Optional[Path]:
        initial = Path(problem.get_initial_state())

        # O contador 'seq' é apenas um critério de desempate estável para custos
        # iguais, evitando que o heapq precise comparar instâncias de Path.
        seq = 0
        frontier = [(initial.cost, seq, initial)]
        self.observe_frontier(len(frontier))

        # Poda de caminhos múltiplos: menor custo já confirmado para cada estado.
        explored = {}

        # Menor custo já colocado na fronteira para cada estado. Sem isso, um
        # mesmo estado entra no heap uma vez por caminho que chega até ele,
        # mesmo quando o novo caminho é mais caro do que outro já enfileirado.
        best_cost = {initial.end(): initial.cost}

        while frontier:
            if self.expansion_limit_reached():
                return None

            cost, _, path = heapq.heappop(frontier)
            node = path.end()

            # Já existe um caminho igual ou mais barato até este estado.
            if node in explored and explored[node] <= cost:
                continue

            explored[node] = cost

            if node.is_goal():
                return path

            self.count_expansion()

            for arc in problem.get_successors(node):
                self.count_generated()
                new_cost = cost + arc.cost

                if new_cost < best_cost.get(arc.to_node, float("inf")):
                    best_cost[arc.to_node] = new_cost
                    seq += 1
                    heapq.heappush(frontier, (new_cost, seq, path.extend(arc)))
                    self.observe_frontier(len(frontier))

        return None
