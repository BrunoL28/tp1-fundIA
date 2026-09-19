import os
from typing import List, Dict, Any

def print_metrics_table(results: List[Dict[str, Any]]) -> None:
    """
    Formata e exibe os resultados no terminal em formato de tabela Markdown,
    facilitando a cópia direta para o relatório em LaTeX.
    """
    header = f"| {'Algoritmo':<20} | {'Custo (min)':<12} | {'Nós Expandidos':<15} | {'Tempo (s)':<12} |"
    divider = f"| {'-'*20} | {'-'*12} | {'-'*15} | {'-'*12} |"
    
    print("\n### Resultados da Execução\n")
    print(header)
    print(divider)
    
    for res in results:
        alg = res['algorithm']
        cost = res['cost']
        nodes = res['nodes_expanded']
        time_s = f"{res['processing_time_s']:.6f}"
        
        print(f"| {alg:<20} | {cost:<12} | {nodes:<15} | {time_s:<12} |")
        
    print("\n### Caminho da Solução Ótima (A*):")
    astar_result = next((r for r in results if r['algorithm'] == 'AStarSearch'), None)
    if astar_result and astar_result['cost'] != float('inf'):
        for step, action in enumerate(astar_result['path'], 1):
            direcao = "->" if step % 2 != 0 else "<-"
            print(f"Passo {step}: Travessia {direcao} {action}")

def save_metrics_to_markdown(results: List[Dict[str, Any]], filename: str = "resultados.md") -> None:
    """
    Gera o arquivo de resultados em formato Markdown com a tabela de métricas.
    Sobrescreve o arquivo se ele já existir.
    """
    header = f"| {'Algoritmo':<20} | {'Custo (min)':<12} | {'Nós Expandidos':<15} | {'Tempo (s)':<12} |"
    divider = f"| {'-'*20} | {'-'*12} | {'-'*15} | {'-'*12} |"
    
    content = [
        "# Resultados da Execução - Ponte e Tocha\n",
        "## Tabela Comparativa de Desempenho\n",
        header,
        divider
    ]
    
    for res in results:
        alg = res['algorithm']
        cost = res['cost']
        nodes = res['nodes_expanded']
        time_s = f"{res['processing_time_s']:.6f}"
        content.append(f"| {alg:<20} | {cost:<12} | {nodes:<15} | {time_s:<12} |")
        
    content.append("\n## Caminho da Solução Ótima (A*)")
    astar_result = next((r for r in results if r['algorithm'] == 'AStarSearch'), None)
    if astar_result and astar_result['cost'] != float('inf'):
        for step, action in enumerate(astar_result['path'], 1):
            direcao = "Ida (->)" if step % 2 != 0 else "Volta (<-)"
            content.append(f"- **Passo {step}:** {direcao} {action}")

    with open(filename, "w", encoding="utf-8") as f:
        f.write("\n".join(content) + "\n")
        
    print(f"Métricas avaliadas. Arquivo '{filename}' gerado com sucesso!")