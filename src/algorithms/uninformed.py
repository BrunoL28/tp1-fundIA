from collections import deque
from typing import Optional, Set
from src.models.problem import BridgeProblem
from src.models.node import Node
from src.algorithms.base_search import BaseSearch

class BreadthFirstSearch(BaseSearch):
    """
    Busca em Largura (BFS).
    Explora o espaço de estados nível por nível utilizando uma fila (FIFO).
    """
    def solve(self, problem: BridgeProblem) -> Optional[Node]:
        initial_node = Node(state=problem.get_initial_state())
        
        if initial_node.state.is_goal():
            return initial_node
            
        frontier = deque([initial_node])
        frontier_states = {initial_node.state}
        explored: Set = set()
        
        while frontier:
            # Prevenção contra processamento excessivo
            if self.nodes_expanded >= self.max_expansions:
                return None
                
            node = frontier.popleft()
            frontier_states.remove(node.state)
            explored.add(node.state)
            self.nodes_expanded += 1
            
            for action, next_state, cost in problem.get_successors(node.state):
                child = Node(
                    state=next_state,
                    parent=node,
                    action=action,
                    path_cost=node.path_cost + cost
                )
                
                if next_state not in explored and next_state not in frontier_states:
                    # No BFS, verificamos o objetivo no momento da geração do nó
                    if child.state.is_goal():
                        self.nodes_expanded += 1
                        return child
                    frontier.append(child)
                    frontier_states.add(next_state)
                    
        return None


class DepthFirstSearch(BaseSearch):
    """
    Busca em Profundidade (DFS).
    Explora o ramo mais profundo disponível utilizando uma pilha (LIFO).
    """
    def solve(self, problem: BridgeProblem) -> Optional[Node]:
        initial_node = Node(state=problem.get_initial_state())
        
        frontier = [initial_node]
        frontier_states = {initial_node.state}
        explored: Set = set()
        
        while frontier:
            if self.nodes_expanded >= self.max_expansions:
                return None
                
            node = frontier.pop()
            frontier_states.remove(node.state)
            
            # No DFS, verificamos o objetivo após a extração da fronteira
            if node.state.is_goal():
                return node
                
            explored.add(node.state)
            self.nodes_expanded += 1
            
            # Inverter a ordem dos sucessores garante uma expansão consistente 
            # da esquerda para a direita na árvore.
            for action, next_state, cost in reversed(problem.get_successors(node.state)):
                child = Node(
                    state=next_state,
                    parent=node,
                    action=action,
                    path_cost=node.path_cost + cost
                )
                
                if next_state not in explored and next_state not in frontier_states:
                    frontier.append(child)
                    frontier_states.add(next_state)
                    
        return None