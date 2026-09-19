from src.models.problem import BridgeProblem
from src.algorithms.uninformed import BreadthFirstSearch, DepthFirstSearch
from src.algorithms.informed import UniformCostSearch, AStarSearch
from src.utils.metrics_logger import print_metrics_table, save_metrics_to_markdown

def main():
    problem = BridgeProblem()
    
    algorithms = [
        BreadthFirstSearch(),
        DepthFirstSearch(),
        UniformCostSearch(),
        AStarSearch()
    ]
    
    results = []
    
    print("Iniciando resolução do problema Ponte e Tocha...\n")
    for alg in algorithms:
        print(f"Executando {alg.__class__.__name__}...")
        result = alg.execute(problem)
        results.append(result)
        
    print_metrics_table(results)
    save_metrics_to_markdown(results)

if __name__ == "__main__":
    main()