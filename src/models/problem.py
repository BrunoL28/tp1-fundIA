import itertools
from typing import List, Tuple
from .state import State

class BridgeProblem:
    def __init__(self):
        # Representamos as pessoas diretamente pelo tempo que levam para atravessar.
        # Isso simplifica o cálculo do custo, já que o ID da pessoa é o próprio tempo.
        self.people = frozenset([1, 2, 5, 10])

    def get_initial_state(self) -> State:
        """
        Retorna o estado inicial: todos no lado esquerdo com a tocha.
        """
        return State(
            left_side=self.people,
            right_side=frozenset(),
            torch_is_left=True
        )

    def get_successors(self, state: State) -> List[Tuple[Tuple[int, ...], State, int]]:
        """
        Função Sucessora: Gera todas as transições válidas a partir do estado atual.
        
        Retorna:
            Lista contendo tuplas no formato: (ação, novo_estado, custo_da_ação)
            - ação: tupla com as pessoas que atravessaram (ex: (1, 2))
            - novo_estado: objeto State resultante
            - custo_da_ação: tempo levado (o maior tempo entre os que atravessam)
        """
        successors = []
        
        # Identifica de qual lado o movimento vai partir
        current_side = state.left_side if state.torch_is_left else state.right_side
        
        # A tocha sempre muda de lado após uma transição
        next_is_left = not state.torch_is_left

        actions = []
        
        # 1. Movimentos de 1 pessoa
        for person in current_side:
            actions.append((person,))
            
        # 2. Movimentos de 2 pessoas (combinações sem repetição)
        for p1, p2 in itertools.combinations(current_side, 2):
            actions.append((p1, p2))

        # 3. Gerar os novos estados e calcular os custos para cada ação válida
        for action in actions:
            action_set = frozenset(action)
            
            if state.torch_is_left:
                # Movimento da Esquerda -> Direita
                new_left = state.left_side - action_set
                new_right = state.right_side | action_set
            else:
                # Movimento da Direita -> Esquerda
                new_left = state.left_side | action_set
                new_right = state.right_side - action_set
                
            new_state = State(
                left_side=new_left,
                right_side=new_right,
                torch_is_left=next_is_left
            )
            
            # O custo da travessia é a velocidade da pessoa mais lenta do grupo
            cost = max(action)
            
            successors.append((action, new_state, cost))
            
        return successors