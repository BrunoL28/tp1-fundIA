from typing import List

from src.models.state import State
from src.utils.markdown_report import upsert_section
from src.utils.state_space import StateSpace, explore_state_space

SECTION_ID = "transicoes"


def format_state(space: StateSpace, state: State) -> str:
    """Rótulo + diagrama do estado, ambos em code span para preservar o `*` da tocha."""
    return f"`{space.label(state)}` `{state.diagram()}`"


def _decimal(value: float, places: int = 2) -> str:
    """Formata número no padrão brasileiro (vírgula decimal)."""
    return f"{value:.{places}f}".replace(".", ",")


def build_legend() -> List[str]:
    return [
        "### Como ler esta seção",
        "",
        "- **Estado:** `*[1, 2] ~~~ [5, 10]` significa que as pessoas 1 e 2 estão na margem",
        "  esquerda e as pessoas 5 e 10 na margem direita. O asterisco (`*`) marca o lado em",
        "  que a tocha se encontra e `-` indica uma margem vazia.",
        "- **Rótulo:** cada estado recebe um identificador `Exx`, reutilizado como destino nas",
        "  tabelas de transição, o que torna a listagem uma lista de adjacências legível.",
        "- **Sentido:** `→` travessia de ida (esquerda para a direita); `←` travessia de volta.",
        "- **Custo:** tempo da pessoa mais lenta do grupo que atravessa, em minutos.",
        "",
    ]


def build_overview(space: StateSpace) -> List[str]:
    goal = space.goals[0]
    people = len(space.initial.left_side)
    combinations = 2 ** people * 2

    lines = [
        "### Panorama do grafo",
        "",
        "| Métrica | Valor |",
        "|:--|--:|",
        f"| Pessoas | {people} |",
        f"| Configurações concebíveis (2^{people} x 2) | {combinations} |",
        f"| Estados alcançáveis (\\|V\\|) | {space.num_states} |",
        f"| Transições dirigidas (\\|E\\|) | {space.num_transitions} |",
        f"| Grau de saída (mín. / médio / máx.) | {space.min_out_degree} / "
        f"{_decimal(space.average_out_degree)} / {space.max_out_degree} |",
        f"| Estado inicial | {format_state(space, space.initial)} |",
        f"| Estado objetivo | {format_state(space, goal)} |",
        "",
        f"Das {combinations} configurações concebíveis, {combinations - space.num_states} são",
        "inalcançáveis, porque a tocha acompanha obrigatoriamente quem atravessa: não há como",
        "todas as pessoas estarem à esquerda com a tocha à direita, nem o contrário.",
        "",
    ]

    if space.is_symmetric:
        lines.extend([
            "O grafo é **simétrico**: para toda transição (u, v) existe a inversa (v, u) com o",
            f"mesmo custo, pois qualquer travessia pode ser desfeita. As {space.num_transitions}",
            f"arestas dirigidas correspondem, portanto, a {space.num_transitions // 2} arestas não",
            "dirigidas. É essa reversibilidade que cria ciclos no grafo e torna obrigatória a poda",
            "de caminhos múltiplos nas buscas, sem a qual a busca em profundidade não terminaria.",
            "",
        ])

    return lines


def build_representation(space: StateSpace) -> List[str]:
    """Justifica a escolha da lista de adjacências sobre a matriz de adjacências."""
    cells = space.adjacency_matrix_cells
    occupied = space.num_transitions
    percent = _decimal(100 * space.density, 1)

    return [
        "### Representação escolhida: lista de adjacências",
        "",
        "Um grafo pode ser representado por uma matriz de adjacências ou por uma lista de",
        "adjacências. A matriz é quadrada e consome espaço proporcional ao quadrado do número",
        f"de vértices: aqui seriam {space.num_states} x {space.num_states} = {cells} posições, das",
        f"quais apenas {occupied} ({percent}%) seriam não nulas. A matriz seria, portanto, esparsa.",
        "",
        "A lista de adjacências guarda, para cada estado, apenas os seus vizinhos de fato, o que",
        f"totaliza {occupied} entradas - cerca de {cells // occupied} vezes menos memória - e ainda",
        "permite percorrer os sucessores de um estado em tempo proporcional ao seu grau, que é",
        "exatamente a operação executada a cada expansão da busca.",
        "",
        "Neste projeto a lista de adjacências não é materializada de antemão pelos algoritmos: a",
        "função sucessora `BridgeProblem.get_successors` a gera sob demanda, estado a estado.",
        "A listagem abaixo é essa mesma lista de adjacências escrita por extenso.",
        "",
    ]


def build_index(space: StateSpace) -> List[str]:
    lines = [
        "### Índice de estados",
        "",
        "| Rótulo | Estado | Já atravessaram | Tocha | Grau de saída |",
        "|:--|:--|--:|:--:|--:|",
    ]

    for state in space.states:
        marker = ""
        if state == space.initial:
            marker = " *(inicial)*"
        elif state.is_goal():
            marker = " *(objetivo)*"

        lines.append(
            f"| `{space.label(state)}`{marker} | `{state.diagram()}` | "
            f"{len(state.right_side)} | {state.torch_side_name} | {space.out_degree(state)} |"
        )

    lines.append("")
    return lines


def build_transition_table(space: StateSpace, arcs) -> List[str]:
    lines = [
        "| Ação | Sentido | Custo (min) | Estado resultante |",
        "|:--|:--:|--:|:--|",
    ]

    for arc in arcs:
        direction = "→" if arc.is_forward else "←"
        lines.append(
            f"| {arc.label} | {direction} | {arc.cost} | "
            f"{format_state(space, arc.to_node)} |"
        )

    lines.append("")
    return lines


def build_layers(space: StateSpace) -> List[str]:
    lines = [
        "### Transições estado a estado",
        "",
        "Os estados estão agrupados por camada, isto é, pelo número de pessoas que já se",
        "encontram na margem direita. Dentro de cada estado, as ações aparecem da mais",
        "barata para a mais cara.",
        "",
    ]

    total_people = len(space.initial.left_side)
    for layer in range(total_people + 1):
        layer_states = [s for s in space.states if len(s.right_side) == layer]
        if not layer_states:
            continue

        lines.append(f"#### Camada {layer} — {layer} de {total_people} pessoas na margem direita")
        lines.append("")

        for state in layer_states:
            header = f"**{format_state(space, state)}**"
            if state == space.initial:
                header += " — estado inicial"
            elif state.is_goal():
                header += " — **estado objetivo**"

            lines.append(header)
            lines.append("")

            if state.is_goal():
                lines.append(
                    "> A busca encerra aqui. As travessias abaixo existem no grafo do domínio "
                    "(nada impede que alguém retorne com a tocha), mas nenhum algoritmo precisa "
                    "expandi-las depois de atingir o objetivo."
                )
                lines.append("")

            lines.extend(build_transition_table(space, space.successors(state)))

    return lines


def build_transitions_section(space: StateSpace) -> str:
    content = ["## Grafo do Espaço de Estados e suas Transições", ""]
    content.extend(build_legend())
    content.extend(build_overview(space))
    content.extend(build_representation(space))
    content.extend(build_index(space))
    content.extend(build_layers(space))
    return "\n".join(content)


def generate_and_save_transitions(filename: str = "resultados.md") -> None:
    print("Mapeando o espaço de estados...")
    space = explore_state_space()

    section = build_transitions_section(space)
    replaced = upsert_section(filename, SECTION_ID, section)

    action = "atualizada" if replaced else "criada"
    print(
        f"Espaço de estados mapeado: {space.num_states} estados e "
        f"{space.num_transitions} transições."
    )
    print(f"Seção de transições {action} em '{filename}'.")


if __name__ == "__main__":
    generate_and_save_transitions()
