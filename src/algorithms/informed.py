import heapq
from typing import Optional, Set
from src.models.problem import BridgeProblem
from src.models.node import Node
from src.algorithms.base_search import BaseSearch
from src.utils.heuristics import max_time_heuristic

class UniformCostSearch(BaseSearch):
    """
    Busca de Custo Mínimo (Lowest-Cost-First Search).
    Expande o nó com o menor custo g(n) acumulado até ao momento.
    """
    def solve(self, problem: BridgeProblem) -> Optional[Node]:
        initial_state = problem.get_initial_state()
        initial_node = Node(state=initial_state)
        
        # A fronteira é tratada como uma fila de prioridades (min-heap)
        # O contador 'seq' serve apenas como critério de desempate secundário
        # caso dois nós tenham o mesmo custo, evitando que o heapq tente comparar instâncias de Node.
        seq = 0
        frontier = [(initial_node.path_cost, seq, initial_node)]
        
        explored = {}
        
        while frontier:
            if self.nodes_expanded >= self.max_expansions:
                return None
                
            current_cost, _, node = heapq.heappop(frontier)
            
            # Se o estado já foi explorado com um custo menor ou igual, ignoramos
            if node.state in explored and explored[node.state] <= current_cost:
                continue
                
            explored[node.state] = current_cost
            self.nodes_expanded += 1
            
            # Verificação de objetivo ao expandir o nó
            if node.state.is_goal():
                return node
                
            for action, next_state, action_cost in problem.get_successors(node.state):
                new_cost = current_cost + action_cost
                
                # Apenas adicionamos à fronteira se for um caminho mais barato para o estado
                if next_state not in explored or new_cost < explored[next_state]:
                    child = Node(
                        state=next_state,
                        parent=node,
                        action=action,
                        path_cost=new_cost
                    )
                    seq += 1
                    heapq.heappush(frontier, (child.path_cost, seq, child))
                    
        return None


class AStarSearch(BaseSearch):
    """
    Busca A* (A-Star).
    Expande o nó com a menor estimativa f(n) = g(n) + h(n).
    """
    def solve(self, problem: BridgeProblem) -> Optional[Node]:
        initial_state = problem.get_initial_state()
        initial_node = Node(
            state=initial_state,
            heuristic=max_time_heuristic(initial_state)
        )
        
        seq = 0
        # A fila de prioridade ordena os caminhos considerando f(p)
        frontier = [(initial_node.total_cost, seq, initial_node)]
        
        explored = {}
        
        while frontier:
            if self.nodes_expanded >= self.max_expansions:
                return None
                
            current_f, _, node = heapq.heappop(frontier)
            
            if node.state in explored and explored[node.state] <= node.path_cost:
                continue
                
            explored[node.state] = node.path_cost
            self.nodes_expanded += 1
            
            if node.state.is_goal():
                return node
                
            for action, next_state, action_cost in problem.get_successors(node.state):
                new_g = node.path_cost + action_cost
                
                if next_state not in explored or new_g < explored[next_state]:
                    h_val = max_time_heuristic(next_state)
                    child = Node(
                        state=next_state,
                        parent=node,
                        action=action,
                        path_cost=new_g,
                        heuristic=h_val
                    )
                    seq += 1
                    # A prioridade é dada pelo total_cost (f(p) = path_cost + heuristic)
                    heapq.heappush(frontier, (child.total_cost, seq, child))
                    
        return None