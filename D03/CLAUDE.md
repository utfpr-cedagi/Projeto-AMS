# D03 — Disciplina 3 do curso CEDAGI

Uma pasta por laboratório, numerada `D3-0N-slug`; cada pacote extrai na
raiz do repositório (não é um projeto separado) — mesmo padrão de `D02`.

## Laboratórios

| Pasta | Laboratório | Status |
|---|---|---|
| `D3-01-vetores-do-meu-dominio` | Vetores do meu domínio | entregue |
| `D3-02-descida-de-gradiente` | Descida de gradiente, à mão | em andamento (`anotacoes.md` ainda tem as 4 perguntas em branco) |
| `D3-03-estatistica-descritiva` | Estatística descritiva | pacote extraído, ainda não iniciado |
| `D3-04-mapa-do-espaco` | Mapa do espaço (vetores) | pacote extraído, ainda não iniciado |

Cada lab tem o critério de aceite e os passos completos no seu
`enunciado.pdf` — leia-o antes de supor o formato de uma entrega.

## Curso vs. produção própria

Decisão do autor: em D03, os laboratórios ficam na estrutura **exatamente
como o pacote do curso entrega** — tudo dentro da pasta `D3-0N-slug/`,
sem subpasta separando o que é do curso do que é autoral (entrega final,
notas, dados próprios ficam soltos ao lado de `enunciado.pdf`/`esqueleto.py`/
`teste.py`, ex.: `pares-surpreendentes.md` e `saida-esqueleto.txt` em
`D3-01`, `anotacoes.md` em `D3-02`).

Isso é diferente do que `D02/D2-06-agente-baseline/` faz (lá existe uma
subpasta `adaptacao-ams/` com tudo que o autor produziu — ver
[`D02/CLAUDE.md`](../D02/CLAUDE.md)). Essa separação por subpasta **não foi
estendida pra D03** — foi tentada e revertida de propósito nos dois labs em
andamento (`D3-01`, `D3-02`): o autor preferiu manter a estrutura que o
professor passou. `adaptacao-ams/` continua sendo uma particularidade só de
`D2-06`, não um padrão do projeto.

O que fica fora de qualquer `D3-0N-slug/`, solto na raiz de `D03/`, é
produção própria por natureza (não há pacote de curso nesse nível):

- `protocolo.md` — diário de execução entre laboratórios (saídas de
  terminal capturadas, organizadas por `## Lab 0N`).

`data/casos-gerados/` (fora de `D03/`, em `data/` na raiz do repo) — lotes
de casos novos gerados por `ams.gerador_casos`, reusáveis por qualquer
disciplina futura, não só D03. Esse, sim, saiu da raiz solta de `D03/` por
não ser conteúdo de disciplina nenhuma.

## `dados/` de cada lab

Quando um lab tem pasta `dados/` (`D3-01`, `D3-04`), o `dados/FONTE.md`
local já documenta a procedência — nos dois casos vistos até agora, os
vetores `manutencao-*`/`generico-*` vieram pré-calculados do pacote da
disciplina (não foram gerados pelo autor), então `dados/` inteira é do
curso, igual ao resto do lab.
