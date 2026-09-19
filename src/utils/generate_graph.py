import networkx as nx
import matplotlib.pyplot as plt
from collections import deque
from src.models.problem import BridgeProblem
from src.models.state import State

def format_state_for_print(state: State) -> str:
    """Formata o estado para o output textual no terminal."""
    pessoas_inicio = ", ".join(map(str, sorted(state.left_side))) if state.left_side else "Ninguém"
    tocha = "inicio" if state.torch_is_left else "final"
    return f"(Pessoas no início: [{pessoas_inicio}], Tocha: {tocha})"

def get_state_label(state: State) -> str:
    """Formata o estado para exibição legível no nó do grafo visual."""
    esq = ",".join(map(str, sorted(state.left_side))) if state.left_side else "Vazio"
    dir = ",".join(map(str, sorted(state.right_side))) if state.right_side else "Vazio"
    tocha = "Esq" if state.torch_is_left else "Dir"
    return f"Esq: [{esq}]\nDir: [{dir}]\nT: {tocha}"

def generate_state_space_graph():
    problem = BridgeProblem()
    initial_state = problem.get_initial_state()
    
    G = nx.DiGraph()
    frontier = deque([initial_state])
    explored = {initial_state}
    
    # Dicionário para armazenar as transições e imprimir posteriormente
    transitions_dict = {}
    
    # Adiciona o nó inicial
    G.add_node(get_state_label(initial_state))
    
    print("Mapeando espaço de estados...")
    while frontier:
        state = frontier.popleft()
        current_label = get_state_label(state)
        
        transitions_dict[state] = []
        
        for action, next_state, cost in problem.get_successors(state):
            next_label = get_state_label(next_state)
            
            # Adiciona o nó e a aresta (transição) visual
            G.add_node(next_label)
            G.add_edge(current_label, next_label, label=f"{list(action)} (t:{cost})")
            
            # Regista a transição para o terminal
            transitions_dict[state].append((next_state, cost))
            
            if next_state not in explored:
                explored.add(next_state)
                frontier.append(next_state)

    print("\nGerando imagem do grafo (isto pode levar alguns segundos)...")
    
    plt.figure(figsize=(20, 14))
    pos = nx.spring_layout(G, k=0.9, iterations=50)
    
    node_colors = []
    for node in G.nodes():
        if node == get_state_label(initial_state):
            node_colors.append("gold")
        elif "Esq: [Vazio]" in node:
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightblue")
            
    nx.draw(
        G, pos, 
        with_labels=True, 
        node_color=node_colors, 
        node_size=4000, 
        font_size=8, 
        font_weight="bold", 
        arrows=True,
        arrowsize=15,
        edge_color="gray"
    )
    
    edge_labels = nx.get_edge_attributes(G, 'label')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=7, font_color="red")
    
    plt.title("Espaço de Estados - Problema da Ponte e Tocha", fontsize=16)
    
    output_file = "bridge_state_graph.png"
    plt.savefig(output_file, dpi=300, bbox_inches="tight")
    print(f"Sucesso! Grafo salvo como '{output_file}' na raiz do projeto.")

if __name__ == "__main__":
    generate_state_space_graph()