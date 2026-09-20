.PHONY: setup test run transitions heuristics scaling report graph charts clean

# Numero de repeticoes de cada algoritmo no calculo do tempo medio.
REPS ?= 1000

setup:
	@echo "Criando ambiente virtual e instalando dependencias com UV..."
	uv venv
	uv pip install -r requirements.txt

test:
	@echo "Executando suite de testes..."
	uv run pytest -v

run:
	@echo "Executando os algoritmos de busca ($(REPS) repeticoes por algoritmo)..."
	uv run python -m src.main --repeticoes $(REPS)

transitions:
	@echo "Mapeando o grafo do espaco de estados e suas transicoes..."
	uv run python -m src.utils.generate_transitions

heuristics:
	@echo "Verificando admissibilidade e consistencia das heuristicas..."
	uv run python -m src.utils.heuristic_analysis

scaling:
	@echo "Executando o experimento de escalabilidade (4 a 8 pessoas)..."
	uv run python -m src.utils.scaling_experiment

report: run transitions heuristics scaling
	@echo "Relatorio completo gerado em resultados.md."

graph:
	@echo "Gerando a visualizacao do grafo..."
	uv run python -m src.utils.generate_graph

charts:
	@echo "Gerando os graficos de escalabilidade para o relatorio..."
	uv run python -m src.utils.generate_charts

clean:
	@echo "Limpando arquivos temporarios e cache..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/*/__pycache__
