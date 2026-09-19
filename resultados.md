# Resultados da Execução - Ponte e Tocha

## Tabela Comparativa de Desempenho

| Algoritmo            | Custo (min)  | Nós Expandidos  | Tempo (s)    |
| -------------------- | ------------ | --------------- | ------------ |
| BreadthFirstSearch   | 19           | 21              | 0.000000     |
| DepthFirstSearch     | 19           | 9               | 0.000000     |
| UniformCostSearch    | 17           | 26              | 0.000000     |
| AStarSearch          | 17           | 19              | 0.000000     |

## Caminho da Solução Ótima (A*)
- **Passo 1:** Ida (->) (1, 2)
- **Passo 2:** Volta (<-) (1,)
- **Passo 3:** Ida (->) (10, 5)
- **Passo 4:** Volta (<-) (2,)
- **Passo 5:** Ida (->) (1, 2)
# Mapeamento de Transições do Espaço de Estados

**Total de estados únicos mapeados:** 30

---

### Estado Atual: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Direita]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Direita]`
- Movimento: **Ida (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Direita]`
- Movimento: **Ida (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Direita]`
- Movimento: **Ida (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Direita]`
- Movimento: **Ida (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Direita]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Direita]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Direita]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`
- Movimento: **Volta (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`
- Movimento: **Volta (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`
- Movimento: **Volta (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Direita]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Volta (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Direita]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Volta (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Direita]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 5, 10 | Dir: Vazio | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Direita]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Direita]`
- Movimento: **Ida (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Direita]`
- Movimento: **Ida (10, 2)** | Custo: 10 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Ida (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Esquerda]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Esquerda]`
- Movimento: **Volta (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Volta (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Esquerda]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Esquerda]`
- Movimento: **Volta (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`
- Movimento: **Volta (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Esquerda]`
- Movimento: **Volta (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 1, 5, 10 | Dir: 2 | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Esquerda]`
- Movimento: **Volta (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 2, 10 | Dir: 5 | Tocha: Esquerda]`
- Movimento: **Volta (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 2, 5 | Dir: 10 | Tocha: Esquerda]`
- Movimento: **Volta (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 2, 5, 10 | Dir: 1 | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Esquerda]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Esquerda]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Direita]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Esquerda]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Direita]`
- Movimento: **Ida (10, 2)** | Custo: 10 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Direita]`
- Movimento: **Ida (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`
- Movimento: **Volta (1,)** | Custo: 1 min ➔ Destino: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Esquerda]`
- Movimento: **Volta (2,)** | Custo: 2 min ➔ Destino: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Esquerda]`
- Movimento: **Volta (10,)** | Custo: 10 min ➔ Destino: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Esquerda]`
- Movimento: **Volta (5,)** | Custo: 5 min ➔ Destino: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Esquerda]`
- Movimento: **Volta (1, 2)** | Custo: 2 min ➔ Destino: `[Esq: 1, 2 | Dir: 5, 10 | Tocha: Esquerda]`
- Movimento: **Volta (1, 10)** | Custo: 10 min ➔ Destino: `[Esq: 1, 10 | Dir: 2, 5 | Tocha: Esquerda]`
- Movimento: **Volta (1, 5)** | Custo: 5 min ➔ Destino: `[Esq: 1, 5 | Dir: 2, 10 | Tocha: Esquerda]`
- Movimento: **Volta (2, 10)** | Custo: 10 min ➔ Destino: `[Esq: 2, 10 | Dir: 1, 5 | Tocha: Esquerda]`
- Movimento: **Volta (2, 5)** | Custo: 5 min ➔ Destino: `[Esq: 2, 5 | Dir: 1, 10 | Tocha: Esquerda]`
- Movimento: **Volta (10, 5)** | Custo: 10 min ➔ Destino: `[Esq: 5, 10 | Dir: 1, 2 | Tocha: Esquerda]`

---

### Estado Atual: `[Esq: 1 | Dir: 2, 5, 10 | Tocha: Esquerda]`
- Movimento: **Ida (1,)** | Custo: 1 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 2 | Dir: 1, 5, 10 | Tocha: Esquerda]`
- Movimento: **Ida (2,)** | Custo: 2 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 10 | Dir: 1, 2, 5 | Tocha: Esquerda]`
- Movimento: **Ida (10,)** | Custo: 10 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---

### Estado Atual: `[Esq: 5 | Dir: 1, 2, 10 | Tocha: Esquerda]`
- Movimento: **Ida (5,)** | Custo: 5 min ➔ Destino: `[Esq: Vazio | Dir: 1, 2, 5, 10 | Tocha: Direita]`

---
