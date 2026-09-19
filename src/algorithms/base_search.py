import time
from abc import ABC, abstractmethod
from typing import Dict, Any, List, Optional
from src.models.problem import BridgeProblem
from src.models.node import Node

class BaseSearch(ABC):
    """
    Interface base para todos os algoritmos de busca.
    Garante a consistência na execução e na coleta de métricas (RF05).
    """
    def __init__(self):
        self.nodes_expanded = 0
        # Limite de segurança para evitar buscas excessivamente longas, útil para o DFS
        self.max_expansions = 15000 

    @abstractmethod
    def solve(self, problem: BridgeProblem) -> Optional[Node]:
        """
        Método central da busca.
        Deve ser implementado pelas classes filhas (BFS, DFS, UCS, A*).
        """
        pass

    def execute(self, problem: BridgeProblem) -> Dict[str, Any]:
        """
        Executa a busca medindo o tempo de processamento e estruturando as métricas[cite: 1].
        """
        self.nodes_expanded = 0
        
        # Utilizamos process_time para medir o tempo real de CPU dedicado ao processo
        start_time = time.process_time()
        
        goal_node = self.solve(problem)
        
        end_time = time.process_time()
        processing_time = end_time - start_time
        
        if goal_node:
            path_actions = self._reconstruct_path(goal_node)
            cost = goal_node.path_cost
        else:
            path_actions = []
            cost = float('inf')

        return {
            "algorithm": self.__class__.__name__,
            "path": path_actions,
            "cost": cost,
            "nodes_expanded": self.nodes_expanded,
            "processing_time_s": processing_time
        }

    def _reconstruct_path(self, node: Node) -> List[tuple]:
        """
        Navega de trás para frente usando os ponteiros 'parent' para listar 
        as ações tomadas desde o estado inicial até o objetivo.
        """
        path = []
        current = node
        while current.parent is not None:
            path.append(current.action)
            current = current.parent
            
        # Inverte a lista para retornar a ordem cronológica do início ao fim
        return path[::-1]