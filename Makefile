.PHONY: setup test run transitions heuristics report graph clean

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

report: run transitions heuristics
	@echo "Relatorio completo gerado em resultados.md."

graph:
	@echo "Gerando a visualizacao do grafo..."
	uv run python -m src.utils.generate_graph

clean:
	@echo "Limpando arquivos temporarios e cache..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/*/__pycache__
