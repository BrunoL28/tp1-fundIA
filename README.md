# Bridge and Torch Puzzle

Implementação computacional do problema da Ponte e da Tocha utilizando algoritmos de busca em espaço de estados, desenvolvida para a disciplina de Fundamentos de Inteligência Artificial.

## Autores
**Arthur Fernandes e Bruno Lima**

## Estrutura de Algoritmos
- **Busca Não Informada:** `BFS` (Busca em Largura) e `DFS` (Busca em Profundidade).
- **Busca Informada:** `Uniform Cost Search (UCS)` (Custo Uniforme) e `A*` (A-Star).

## Espaço de Estados (Grafo)

Abaixo encontra-se a modelagem visual do problema, representando as ramificações e custos (tempos) de transição desde o estado inicial até à meta:

![Grafo do Espaço de Estados](bridge_state_graph.png)

## Como Executar

Este projeto utiliza o `uv` (gerenciador de pacotes e ambientes Python) integrado através de um `Makefile` para facilitar o fluxo de desenvolvimento.

### Pré-requisitos
Certifique-se de ter o [uv](https://github.com/astral-sh/uv) e o `make` instalados na sua máquina.

### Comandos Disponíveis

Na raiz do projeto, utilize os seguintes comandos no terminal:

- **`make setup`**: Cria o ambiente virtual (`.venv`) e instala as dependências exatas definidas no `requirements.txt`.
- **`make test`**: Executa a suíte completa de testes via `pytest` (valida regras de transição, limitação de capacidade e heurística).
- **`make run`**: Executa o comparativo dos quatro algoritmos de busca e gera o arquivo `resultados.md` contendo a tabela de métricas e o caminho da solução ótima.
- **`make transitions`**: Mapeia todo o espaço de estados e **adiciona** ao arquivo `resultados.md` a listagem detalhada de todas as transições válidas e seus custos.
- **`make graph`**: Mapeia o domínio do problema e exporta a visualização da árvore em alta resolução para a imagem `bridge_state_graph.png`.
- **`make clean`**: Limpa diretórios de cache (`__pycache__`, `.pytest_cache`) e destrói o ambiente virtual.
