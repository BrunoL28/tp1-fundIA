from src.models.state import State

def max_time_heuristic(state: State) -> int:
    """
    Retorna o tempo da pessoa mais lenta que ainda está no lado esquerdo.
    Se não houver ninguém no lado esquerdo (objetivo alcançado), retorna 0.
    """
    if not state.left_side:
        return 0
    return max(state.left_side)