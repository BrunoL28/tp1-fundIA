.PHONY: setup test run graph clean

setup:
	@echo "Criando ambiente virtual e instalando dependencias com UV..."
	uv venv
	uv pip install -r requirements.txt

test:
	@echo "Executando suite de testes..."
	uv run pytest -v

run:
	@echo "Executando os algoritmos de busca..."
	uv run python -m src.main

transitions:
	@echo "Mapeando transicoes e sobrescrevendo resultados.md..."
	uv run python -m src.utils.generate_transitions

graph:
	@echo "Gerando a visualizacao do grafo..."
	uv run python -m src.utils.generate_graph

clean:
	@echo "Limpando arquivos temporarios e cache..."
	rm -rf .venv
	rm -rf .pytest_cache
	rm -rf __pycache__
	rm -rf src/*/__pycache__