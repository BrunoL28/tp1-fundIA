import matplotlib.pyplot as plt
import networkx as nx

from src.algorithms.informed import AStarSearch
from src.models.problem import BridgeProblem
from src.models.state import State
from src.utils.state_space import StateSpace, explore_state_space

OUTPUT_FILE = "bridge_state_graph.png"


def get_state_label(state: State) -> str:
    """
    Rótulo do estado dentro do nó do grafo. Reaproveita o diagrama usado nos
    relatórios, apenas quebrado em linhas para caber dentro do nó.
    """
    return state.diagram(multiline=True)


def build_graph(space: StateSpace) -> nx.DiGraph:
    graph = nx.DiGraph()

    for state in space.states:
        graph.add_node(get_state_label(state), layer=len(state.right_side))

    for arc in space.all_transitions():
        graph.add_edge(
            get_state_label(arc.from_node),
            get_state_label(arc.to_node),
            label=f"{arc.label} t:{arc.cost}",
        )

    return graph


def optimal_path_edges(problem: BridgeProblem):
    """Arestas do caminho ótimo, sua descrição passo a passo e o custo total."""
    solution = AStarSearch().solve(problem)
    if solution is None:
        return [], [], None

    edges = []
    steps = []
    for number, arc in enumerate(solution.arcs(), 1):
        edges.append((get_state_label(arc.from_node), get_state_label(arc.to_node)))
        direction = "ida  " if arc.is_forward else "volta"
        steps.append(f"{number}. {direction} {arc.label:<8} {arc.cost:>2} min")

    return edges, steps, solution.cost


def generate_state_space_graph(output_file: str = OUTPUT_FILE) -> None:
    print("Mapeando espaço de estados...")
    problem = BridgeProblem()
    space = explore_state_space(problem)
    graph = build_graph(space)
    highlight, steps, optimal_cost = optimal_path_edges(problem)

    print("Gerando imagem do grafo (isto pode levar alguns segundos)...")

    # Layout em camadas: cada coluna reúne os estados com o mesmo número de
    # pessoas já na margem direita, de modo que a figura seja lida da esquerda
    # (todos na margem inicial) para a direita (objetivo).
    positions = nx.multipartite_layout(graph, subset_key="layer", scale=2.6)

    initial_label = get_state_label(space.initial)
    goal_labels = {get_state_label(goal) for goal in space.goals}

    node_colors = []
    for node in graph.nodes():
        if node == initial_label:
            node_colors.append("gold")
        elif node in goal_labels:
            node_colors.append("lightgreen")
        else:
            node_colors.append("lightblue")

    highlight_set = set(highlight)
    regular_edges = [edge for edge in graph.edges() if edge not in highlight_set]

    plt.figure(figsize=(22, 14))

    nx.draw_networkx_nodes(graph, positions, node_color=node_colors, node_size=2600,
                           edgecolors="gray", linewidths=0.8)
    nx.draw_networkx_labels(graph, positions, font_size=7, font_weight="bold")

    # As duas direções de cada par de estados são desenhadas com curvatura para
    # que não se sobreponham.
    nx.draw_networkx_edges(graph, positions, edgelist=regular_edges, edge_color="lightgray",
                           arrows=True, arrowsize=9, width=0.6,
                           connectionstyle="arc3,rad=0.12", node_size=2600)

    if highlight:
        nx.draw_networkx_edges(graph, positions, edgelist=highlight, edge_color="crimson",
                               arrows=True, arrowsize=18, width=2.2,
                               connectionstyle="arc3,rad=0.12", node_size=2600)

        # Os rótulos das arestas não acompanham a curvatura, então a sequência
        # ótima é descrita em um quadro à parte, onde cabe sem sobreposição.
        summary = (
            "Caminho de custo mínimo\n"
            + "\n".join(steps)
            + f"\n{'total':<12}{optimal_cost:>3} min"
        )
        plt.gca().text(
            0.01, 0.16, summary,
            transform=plt.gca().transAxes,
            fontsize=10, family="monospace", color="crimson", va="center",
            bbox=dict(boxstyle="round,pad=0.5", fc="white", ec="crimson", alpha=0.9),
        )

    subtitle = f"{space.num_states} estados, {space.num_transitions} transições"
    if optimal_cost is not None:
        subtitle += f"; em destaque, o caminho de custo mínimo ({optimal_cost} min)"

    plt.title(f"Espaço de Estados - Problema da Ponte e Tocha\n{subtitle}", fontsize=15)
    plt.axis("off")
    plt.savefig(output_file, dpi=200, bbox_inches="tight")
    plt.close()

    print(f"Sucesso! Grafo salvo como '{output_file}' na raiz do projeto.")


if __name__ == "__main__":
    generate_state_space_graph()
