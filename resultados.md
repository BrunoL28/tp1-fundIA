# Resultados da Execução - Ponte e Tocha

<!-- BEGIN:metricas -->

## Tabela Comparativa de Desempenho

Cada algoritmo foi executado **1000** vez(es) sobre o mesmo problema.
Custo, número de nós e tamanho da fronteira são determinísticos e se repetem a cada
execução; o tempo de processamento é reportado como média e desvio-padrão das
repetições, medido com `time.perf_counter()` e expresso em microssegundos (µs).

| Algoritmo                    | Custo (min) | Travessias | Nós expandidos | Nós gerados | Fronteira máx. | Tempo médio (µs) | Desvio (µs) | Tempo mín. (µs) |
|:-----------------------------|------------:|-----------:|---------------:|------------:|---------------:|-----------------:|------------:|----------------:|
| Busca em Largura (BFS)       |          19 |          5 |             25 |          98 |             10 |            50,36 |       20,34 |           48,10 |
| Busca em Profundidade (DFS)  |          19 |          5 |              9 |          32 |             12 |            20,10 |        4,75 |           19,10 |
| Busca de Custo Mínimo (LCFS) |          17 |          5 |             25 |          98 |             11 |            59,73 |        7,46 |           57,30 |
| Busca A* (h1)                |          17 |          5 |             18 |          71 |             14 |            54,96 |        5,35 |           53,30 |
| Busca A* (h2)                |          17 |          5 |             14 |          57 |             14 |            59,56 |       32,54 |           55,90 |

## Caminho da Solução Ótima

Encontrado pela Busca de Custo Mínimo (LCFS): **17 minutos** em 5 travessias.

- **Passo 1:** Ida (→) {1, 2}
- **Passo 2:** Volta (←) {1}
- **Passo 3:** Ida (→) {5, 10}
- **Passo 4:** Volta (←) {2}
- **Passo 5:** Ida (→) {1, 2}

<!-- END:metricas -->

<!-- BEGIN:transicoes -->

## Grafo do Espaço de Estados e suas Transições

### Como ler esta seção

- **Estado:** `*[1, 2] ~~~ [5, 10]` significa que as pessoas 1 e 2 estão na margem
  esquerda e as pessoas 5 e 10 na margem direita. O asterisco (`*`) marca o lado em
  que a tocha se encontra e `-` indica uma margem vazia.
- **Rótulo:** cada estado recebe um identificador `Exx`, reutilizado como destino nas
  tabelas de transição, o que torna a listagem uma lista de adjacências legível.
- **Sentido:** `→` travessia de ida (esquerda para a direita); `←` travessia de volta.
- **Custo:** tempo da pessoa mais lenta do grupo que atravessa, em minutos.

### Panorama do grafo

| Métrica | Valor |
|:--|--:|
| Pessoas | 4 |
| Configurações concebíveis (2^4 x 2) | 32 |
| Estados alcançáveis (\|V\|) | 30 |
| Transições dirigidas (\|E\|) | 112 |
| Grau de saída (mín. / médio / máx.) | 1 / 3,73 / 10 |
| Estado inicial | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| Estado objetivo | `E29` `[-] ~~~ [1, 2, 5, 10]*` |

Das 32 configurações concebíveis, 2 são
inalcançáveis, porque a tocha acompanha obrigatoriamente quem atravessa: não há como
todas as pessoas estarem à esquerda com a tocha à direita, nem o contrário.

O grafo é **simétrico**: para toda transição (u, v) existe a inversa (v, u) com o
mesmo custo, pois qualquer travessia pode ser desfeita. As 112
arestas dirigidas correspondem, portanto, a 56 arestas não
dirigidas. É essa reversibilidade que cria ciclos no grafo e torna obrigatória a poda
de caminhos múltiplos nas buscas, sem a qual a busca em profundidade não terminaria.

### Representação escolhida: lista de adjacências

Um grafo pode ser representado por uma matriz de adjacências ou por uma lista de
adjacências. A matriz é quadrada e consome espaço proporcional ao quadrado do número
de vértices: aqui seriam 30 x 30 = 900 posições, das
quais apenas 112 (12,4%) seriam não nulas. A matriz seria, portanto, esparsa.

A lista de adjacências guarda, para cada estado, apenas os seus vizinhos de fato, o que
totaliza 112 entradas - cerca de 8 vezes menos memória - e ainda
permite percorrer os sucessores de um estado em tempo proporcional ao seu grau, que é
exatamente a operação executada a cada expansão da busca.

Neste projeto a lista de adjacências não é materializada de antemão pelos algoritmos: a
função sucessora `BridgeProblem.get_successors` a gera sob demanda, estado a estado.
A listagem abaixo é essa mesma lista de adjacências escrita por extenso.

### Índice de estados

| Rótulo | Estado | Já atravessaram | Tocha | Grau de saída |
|:--|:--|--:|:--:|--:|
| `E00` *(inicial)* | `*[1, 2, 5, 10] ~~~ [-]` | 0 | Esquerda | 10 |
| `E01` | `*[1, 2, 5] ~~~ [10]` | 1 | Esquerda | 6 |
| `E02` | `*[1, 2, 10] ~~~ [5]` | 1 | Esquerda | 6 |
| `E03` | `*[1, 5, 10] ~~~ [2]` | 1 | Esquerda | 6 |
| `E04` | `*[2, 5, 10] ~~~ [1]` | 1 | Esquerda | 6 |
| `E05` | `[1, 2, 5] ~~~ [10]*` | 1 | Direita | 1 |
| `E06` | `[1, 2, 10] ~~~ [5]*` | 1 | Direita | 1 |
| `E07` | `[1, 5, 10] ~~~ [2]*` | 1 | Direita | 1 |
| `E08` | `[2, 5, 10] ~~~ [1]*` | 1 | Direita | 1 |
| `E09` | `*[1, 2] ~~~ [5, 10]` | 2 | Esquerda | 3 |
| `E10` | `*[1, 5] ~~~ [2, 10]` | 2 | Esquerda | 3 |
| `E11` | `*[1, 10] ~~~ [2, 5]` | 2 | Esquerda | 3 |
| `E12` | `*[2, 5] ~~~ [1, 10]` | 2 | Esquerda | 3 |
| `E13` | `*[2, 10] ~~~ [1, 5]` | 2 | Esquerda | 3 |
| `E14` | `*[5, 10] ~~~ [1, 2]` | 2 | Esquerda | 3 |
| `E15` | `[1, 2] ~~~ [5, 10]*` | 2 | Direita | 3 |
| `E16` | `[1, 5] ~~~ [2, 10]*` | 2 | Direita | 3 |
| `E17` | `[1, 10] ~~~ [2, 5]*` | 2 | Direita | 3 |
| `E18` | `[2, 5] ~~~ [1, 10]*` | 2 | Direita | 3 |
| `E19` | `[2, 10] ~~~ [1, 5]*` | 2 | Direita | 3 |
| `E20` | `[5, 10] ~~~ [1, 2]*` | 2 | Direita | 3 |
| `E21` | `*[1] ~~~ [2, 5, 10]` | 3 | Esquerda | 1 |
| `E22` | `*[2] ~~~ [1, 5, 10]` | 3 | Esquerda | 1 |
| `E23` | `*[5] ~~~ [1, 2, 10]` | 3 | Esquerda | 1 |
| `E24` | `*[10] ~~~ [1, 2, 5]` | 3 | Esquerda | 1 |
| `E25` | `[1] ~~~ [2, 5, 10]*` | 3 | Direita | 6 |
| `E26` | `[2] ~~~ [1, 5, 10]*` | 3 | Direita | 6 |
| `E27` | `[5] ~~~ [1, 2, 10]*` | 3 | Direita | 6 |
| `E28` | `[10] ~~~ [1, 2, 5]*` | 3 | Direita | 6 |
| `E29` *(objetivo)* | `[-] ~~~ [1, 2, 5, 10]*` | 4 | Direita | 10 |

### Transições estado a estado

Os estados estão agrupados por camada, isto é, pelo número de pessoas que já se
encontram na margem direita. Dentro de cada estado, as ações aparecem da mais
barata para a mais cara.

#### Camada 0 — 0 de 4 pessoas na margem direita

**`E00` `*[1, 2, 5, 10] ~~~ [-]`** — estado inicial

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E08` `[2, 5, 10] ~~~ [1]*` |
| {1, 2} | → | 2 | `E20` `[5, 10] ~~~ [1, 2]*` |
| {2} | → | 2 | `E07` `[1, 5, 10] ~~~ [2]*` |
| {1, 5} | → | 5 | `E19` `[2, 10] ~~~ [1, 5]*` |
| {2, 5} | → | 5 | `E17` `[1, 10] ~~~ [2, 5]*` |
| {5} | → | 5 | `E06` `[1, 2, 10] ~~~ [5]*` |
| {1, 10} | → | 10 | `E18` `[2, 5] ~~~ [1, 10]*` |
| {2, 10} | → | 10 | `E16` `[1, 5] ~~~ [2, 10]*` |
| {5, 10} | → | 10 | `E15` `[1, 2] ~~~ [5, 10]*` |
| {10} | → | 10 | `E05` `[1, 2, 5] ~~~ [10]*` |

#### Camada 1 — 1 de 4 pessoas na margem direita

**`E01` `*[1, 2, 5] ~~~ [10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E18` `[2, 5] ~~~ [1, 10]*` |
| {1, 2} | → | 2 | `E27` `[5] ~~~ [1, 2, 10]*` |
| {2} | → | 2 | `E16` `[1, 5] ~~~ [2, 10]*` |
| {1, 5} | → | 5 | `E26` `[2] ~~~ [1, 5, 10]*` |
| {2, 5} | → | 5 | `E25` `[1] ~~~ [2, 5, 10]*` |
| {5} | → | 5 | `E15` `[1, 2] ~~~ [5, 10]*` |

**`E02` `*[1, 2, 10] ~~~ [5]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E19` `[2, 10] ~~~ [1, 5]*` |
| {1, 2} | → | 2 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {2} | → | 2 | `E17` `[1, 10] ~~~ [2, 5]*` |
| {1, 10} | → | 10 | `E26` `[2] ~~~ [1, 5, 10]*` |
| {2, 10} | → | 10 | `E25` `[1] ~~~ [2, 5, 10]*` |
| {10} | → | 10 | `E15` `[1, 2] ~~~ [5, 10]*` |

**`E03` `*[1, 5, 10] ~~~ [2]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E20` `[5, 10] ~~~ [1, 2]*` |
| {1, 5} | → | 5 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {5} | → | 5 | `E17` `[1, 10] ~~~ [2, 5]*` |
| {1, 10} | → | 10 | `E27` `[5] ~~~ [1, 2, 10]*` |
| {5, 10} | → | 10 | `E25` `[1] ~~~ [2, 5, 10]*` |
| {10} | → | 10 | `E16` `[1, 5] ~~~ [2, 10]*` |

**`E04` `*[2, 5, 10] ~~~ [1]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | → | 2 | `E20` `[5, 10] ~~~ [1, 2]*` |
| {2, 5} | → | 5 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {5} | → | 5 | `E19` `[2, 10] ~~~ [1, 5]*` |
| {2, 10} | → | 10 | `E27` `[5] ~~~ [1, 2, 10]*` |
| {5, 10} | → | 10 | `E26` `[2] ~~~ [1, 5, 10]*` |
| {10} | → | 10 | `E18` `[2, 5] ~~~ [1, 10]*` |

**`E05` `[1, 2, 5] ~~~ [10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {10} | ← | 10 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |

**`E06` `[1, 2, 10] ~~~ [5]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {5} | ← | 5 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |

**`E07` `[1, 5, 10] ~~~ [2]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | ← | 2 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |

**`E08` `[2, 5, 10] ~~~ [1]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |

#### Camada 2 — 2 de 4 pessoas na margem direita

**`E09` `*[1, 2] ~~~ [5, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E26` `[2] ~~~ [1, 5, 10]*` |
| {1, 2} | → | 2 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {2} | → | 2 | `E25` `[1] ~~~ [2, 5, 10]*` |

**`E10` `*[1, 5] ~~~ [2, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E27` `[5] ~~~ [1, 2, 10]*` |
| {1, 5} | → | 5 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {5} | → | 5 | `E25` `[1] ~~~ [2, 5, 10]*` |

**`E11` `*[1, 10] ~~~ [2, 5]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {1, 10} | → | 10 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {10} | → | 10 | `E25` `[1] ~~~ [2, 5, 10]*` |

**`E12` `*[2, 5] ~~~ [1, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | → | 2 | `E27` `[5] ~~~ [1, 2, 10]*` |
| {2, 5} | → | 5 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {5} | → | 5 | `E26` `[2] ~~~ [1, 5, 10]*` |

**`E13` `*[2, 10] ~~~ [1, 5]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | → | 2 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {2, 10} | → | 10 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {10} | → | 10 | `E26` `[2] ~~~ [1, 5, 10]*` |

**`E14` `*[5, 10] ~~~ [1, 2]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {5} | → | 5 | `E28` `[10] ~~~ [1, 2, 5]*` |
| {5, 10} | → | 10 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |
| {10} | → | 10 | `E27` `[5] ~~~ [1, 2, 10]*` |

**`E15` `[1, 2] ~~~ [5, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {5} | ← | 5 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {5, 10} | ← | 10 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {10} | ← | 10 | `E02` `*[1, 2, 10] ~~~ [5]` |

**`E16` `[1, 5] ~~~ [2, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | ← | 2 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {2, 10} | ← | 10 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {10} | ← | 10 | `E03` `*[1, 5, 10] ~~~ [2]` |

**`E17` `[1, 10] ~~~ [2, 5]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | ← | 2 | `E02` `*[1, 2, 10] ~~~ [5]` |
| {2, 5} | ← | 5 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {5} | ← | 5 | `E03` `*[1, 5, 10] ~~~ [2]` |

**`E18` `[2, 5] ~~~ [1, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {1, 10} | ← | 10 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {10} | ← | 10 | `E04` `*[2, 5, 10] ~~~ [1]` |

**`E19` `[2, 10] ~~~ [1, 5]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E02` `*[1, 2, 10] ~~~ [5]` |
| {1, 5} | ← | 5 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {5} | ← | 5 | `E04` `*[2, 5, 10] ~~~ [1]` |

**`E20` `[5, 10] ~~~ [1, 2]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E03` `*[1, 5, 10] ~~~ [2]` |
| {1, 2} | ← | 2 | `E00` `*[1, 2, 5, 10] ~~~ [-]` |
| {2} | ← | 2 | `E04` `*[2, 5, 10] ~~~ [1]` |

#### Camada 3 — 3 de 4 pessoas na margem direita

**`E21` `*[1] ~~~ [2, 5, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | → | 1 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |

**`E22` `*[2] ~~~ [1, 5, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | → | 2 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |

**`E23` `*[5] ~~~ [1, 2, 10]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {5} | → | 5 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |

**`E24` `*[10] ~~~ [1, 2, 5]`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {10} | → | 10 | `E29` `[-] ~~~ [1, 2, 5, 10]*` |

**`E25` `[1] ~~~ [2, 5, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {2} | ← | 2 | `E09` `*[1, 2] ~~~ [5, 10]` |
| {2, 5} | ← | 5 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {5} | ← | 5 | `E10` `*[1, 5] ~~~ [2, 10]` |
| {2, 10} | ← | 10 | `E02` `*[1, 2, 10] ~~~ [5]` |
| {5, 10} | ← | 10 | `E03` `*[1, 5, 10] ~~~ [2]` |
| {10} | ← | 10 | `E11` `*[1, 10] ~~~ [2, 5]` |

**`E26` `[2] ~~~ [1, 5, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E09` `*[1, 2] ~~~ [5, 10]` |
| {1, 5} | ← | 5 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {5} | ← | 5 | `E12` `*[2, 5] ~~~ [1, 10]` |
| {1, 10} | ← | 10 | `E02` `*[1, 2, 10] ~~~ [5]` |
| {5, 10} | ← | 10 | `E04` `*[2, 5, 10] ~~~ [1]` |
| {10} | ← | 10 | `E13` `*[2, 10] ~~~ [1, 5]` |

**`E27` `[5] ~~~ [1, 2, 10]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E10` `*[1, 5] ~~~ [2, 10]` |
| {1, 2} | ← | 2 | `E01` `*[1, 2, 5] ~~~ [10]` |
| {2} | ← | 2 | `E12` `*[2, 5] ~~~ [1, 10]` |
| {1, 10} | ← | 10 | `E03` `*[1, 5, 10] ~~~ [2]` |
| {2, 10} | ← | 10 | `E04` `*[2, 5, 10] ~~~ [1]` |
| {10} | ← | 10 | `E14` `*[5, 10] ~~~ [1, 2]` |

**`E28` `[10] ~~~ [1, 2, 5]*`**

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E11` `*[1, 10] ~~~ [2, 5]` |
| {1, 2} | ← | 2 | `E02` `*[1, 2, 10] ~~~ [5]` |
| {2} | ← | 2 | `E13` `*[2, 10] ~~~ [1, 5]` |
| {1, 5} | ← | 5 | `E03` `*[1, 5, 10] ~~~ [2]` |
| {2, 5} | ← | 5 | `E04` `*[2, 5, 10] ~~~ [1]` |
| {5} | ← | 5 | `E14` `*[5, 10] ~~~ [1, 2]` |

#### Camada 4 — 4 de 4 pessoas na margem direita

**`E29` `[-] ~~~ [1, 2, 5, 10]*`** — **estado objetivo**

> A busca encerra aqui. As travessias abaixo existem no grafo do domínio (nada impede que alguém retorne com a tocha), mas nenhum algoritmo precisa expandi-las depois de atingir o objetivo.

| Ação | Sentido | Custo (min) | Estado resultante |
|:--|:--:|--:|:--|
| {1} | ← | 1 | `E21` `*[1] ~~~ [2, 5, 10]` |
| {1, 2} | ← | 2 | `E09` `*[1, 2] ~~~ [5, 10]` |
| {2} | ← | 2 | `E22` `*[2] ~~~ [1, 5, 10]` |
| {1, 5} | ← | 5 | `E10` `*[1, 5] ~~~ [2, 10]` |
| {2, 5} | ← | 5 | `E12` `*[2, 5] ~~~ [1, 10]` |
| {5} | ← | 5 | `E23` `*[5] ~~~ [1, 2, 10]` |
| {1, 10} | ← | 10 | `E11` `*[1, 10] ~~~ [2, 5]` |
| {2, 10} | ← | 10 | `E13` `*[2, 10] ~~~ [1, 5]` |
| {5, 10} | ← | 10 | `E14` `*[5, 10] ~~~ [1, 2]` |
| {10} | ← | 10 | `E24` `*[10] ~~~ [1, 2, 5]` |

<!-- END:transicoes -->

<!-- BEGIN:heuristicas -->

## Comparação das Heurísticas

As duas heurísticas foram verificadas nos 30 estados alcançáveis e
nas 112 transições do grafo, comparando cada h(n) com o custo real
h\*(n) obtido por uma busca de custo mínimo sobre o grafo invertido.

| Heurística | h(inicial) | h\*(inicial) | Admissível | Consistente | Erro médio h\*−h | Nós expandidos (A\*) | Custo obtido |
|:--|--:|--:|:--:|:--:|--:|--:|--:|
| h₁ = tempo da pessoa mais lenta à esquerda | 10 | 17 | sim | sim | 3,70 | 18 | 17 |
| h₂ = agrupamento das idas + retornos mínimos | 13 | 17 | sim | sim | 2,53 | 14 | 17 |

Como h2(n) >= h1(n) para todo estado sem deixar de ser admissível,
h2 **domina** h1: é mais informativa e poda mais o espaço de busca.
O efeito prático é uma redução de 18 para 14
nós expandidos pela A\* (4 a menos, 22,2%), mantendo o mesmo
custo ótimo da solução - o que era esperado, já que ambas são admissíveis.

<!-- END:heuristicas -->

<!-- BEGIN:escalabilidade -->

## Escalabilidade: crescimento com o número de pessoas

A instância do enunciado (quatro pessoas) é pequena demais para separar os métodos.
Aumentando o grupo - mantendo a ponte com capacidade para duas pessoas e acrescentando
travessias progressivamente mais lentas a partir de [1, 2, 5, 10] -, o espaço de
estados cresce como 2^n x 2 e as diferenças ficam evidentes.

### Tamanho do grafo e solução ótima

| Pessoas | Tempos | Estados (\|V\|) | Transições (\|E\|) | Custo ótimo |
|--:|:--|--:|--:|--:|
| 4 | 1, 2, 5, 10 | 30 | 112 | 17 |
| 5 | 1, 2, 5, 10, 15 | 62 | 320 | 28 |
| 6 | 1, 2, 5, 10, 15, 20 | 126 | 864 | 42 |
| 7 | 1, 2, 5, 10, 15, 20, 25 | 254 | 2240 | 58 |
| 8 | 1, 2, 5, 10, 15, 20, 25, 30 | 510 | 5632 | 77 |

### Nós expandidos

| Pessoas | Busca em Largura (BFS) | Busca em Profundidade (DFS) | Busca de Custo Mínimo (LCFS) | A* (h1) | A* (h2) |
|--:|--:|--:|--:|--:|--:|
| 4 | 25 | 9 | 25 | 18 | 14 |
| 5 | 56 | 12 | 56 | 38 | 26 |
| 6 | 119 | 15 | 117 | 84 | 56 |
| 7 | 246 | 18 | 244 | 179 | 100 |
| 8 | 501 | 21 | 495 | 388 | 223 |

### Tempo médio de processamento (µs)

| Pessoas | Busca em Largura (BFS) | Busca em Profundidade (DFS) | Busca de Custo Mínimo (LCFS) | A* (h1) | A* (h2) |
|--:|--:|--:|--:|--:|--:|
| 4 | 49,7 | 19,7 | 58,8 | 54,3 | 57,1 |
| 5 | 135,3 | 32,9 | 171,4 | 146,2 | 137,1 |
| 6 | 359,8 | 50,0 | 456,3 | 402,3 | 351,5 |
| 7 | 960,1 | 84,2 | 1229,6 | 1167,3 | 820,4 |
| 8 | 2316,1 | 105,5 | 3064,5 | 2831,6 | 2096,0 |

Com 8 pessoas, a Busca de Custo Mínimo expande 495 dos 510 estados do grafo, enquanto a A* com h₂ expande 223 (45,1% do total da busca cega) e chega ao mesmo custo
ótimo. É esse o ganho que a heurística traz e que a instância de quatro pessoas não
deixa enxergar.

Em todas as instâncias testadas, Busca em Largura (BFS) e Busca em Profundidade (DFS) devolveram soluções
subótimas. O DFS é o caso mais eloquente: é de longe quem menos expande e, ainda
assim, nunca encontra a melhor solução - expandir pouco não é sinal de qualidade,
apenas de parar no primeiro ramo que alcança o objetivo.

Um detalhe que a tabela de tempos revela: de h₁ para h₂ os nós expandidos caem
42,5%, mas o tempo cai apenas 26,0%. A heurística mais
informativa poda mais, porém custa mais caro por nó avaliado - ela ordena os tempos
da margem esquerda a cada chamada, enquanto h₁ apenas toma um máximo. O ganho em nós
expandidos não se converte integralmente em ganho de tempo.

<!-- END:escalabilidade -->
