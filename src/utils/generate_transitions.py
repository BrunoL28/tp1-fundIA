from collections import deque
from src.models.problem import BridgeProblem
from src.models.state import State

def format_state_md(state: State) -> str:
    """Retorna uma representação compacta e original do estado para o Markdown."""
    esq = ", ".join(map(str, sorted(state.left_side))) if state.left_side else "Vazio"
    dir = ", ".join(map(str, sorted(state.right_side))) if state.right_side else "Vazio"
    tocha = "Esquerda" if state.torch_is_left else "Direita"
    return f"`[Esq: {esq} | Dir: {dir} | Tocha: {tocha}]`"

def generate_and_save_transitions(filename: str = "resultados.md"):
    problem = BridgeProblem()
    initial_state = problem.get_initial_state()
    
    frontier = deque([initial_state])
    explored = {initial_state}
    transitions_dict = {}
    
    print("Mapeando o espaço de estados...")
    while frontier:
        state = frontier.popleft()
        transitions_dict[state] = []
        
        for action, next_state, cost in problem.get_successors(state):
            transitions_dict[state].append((action, next_state, cost))
            
            if next_state not in explored:
                explored.add(next_state)
                frontier.append(next_state)

    content = [
        "# Mapeamento de Transições do Espaço de Estados\n",
        f"**Total de estados únicos mapeados:** {len(explored)}\n",
        "---\n"
    ]
    
    for state, transitions in transitions_dict.items():
        content.append(f"### Estado Atual: {format_state_md(state)}")
        if not transitions:
            content.append("- *Nenhum movimento possível (Estado Objetivo).*")
        else:
            for action, next_state, cost in transitions:
                movimento = "Ida" if state.torch_is_left else "Volta"
                content.append(
                    f"- Movimento: **{movimento} {action}** | Custo: {cost} min ➔ "
                    f"Destino: {format_state_md(next_state)}"
                )
        content.append("\n---\n")

    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n".join(content))
        
    print(f"Transições salvas com sucesso. O arquivo '{filename}' foi sobrescrito.")

if __name__ == "__main__":
    generate_and_save_transitions()