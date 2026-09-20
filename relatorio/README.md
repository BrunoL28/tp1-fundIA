# Relatório (LaTeX)

Esqueleto do relatório pedido na Seção 3 do enunciado. As tabelas, figuras,
definições formais e o pseudocódigo já estão preenchidos com os números de
`resultados.md`; a prosa de cada seção está marcada com `% TODO grupo:` e deve
ser escrita pelo grupo.

## Compilar

- **Overleaf:** envie a pasta `relatorio/` inteira (inclusive `figuras/`),
  defina `main.tex` como arquivo principal e o compilador como *pdfLaTeX*.
- **Local** (MiKTeX ou TeX Live): `latexmk -pdf main.tex` dentro desta pasta.

## Atualizar figuras e números

Na raiz do repositório: `make report` regenera `resultados.md`, `make graph`
regenera o grafo e `make charts` regenera `figuras/` (inclusive a cópia do
grafo). Depois, confira se os números das tabelas em `main.tex` continuam
iguais aos de `resultados.md` - os nós expandidos e custos não mudam; os tempos
mudam a cada máquina.

## Regra do enunciado sobre IA

Relatórios com marcas evidentes de IA generativa (trechos de prompt, respostas
em primeira pessoa) não serão corrigidos. Escrevam a prosa com as próprias
palavras e removam todos os comentários `% TODO grupo:` antes de entregar.
