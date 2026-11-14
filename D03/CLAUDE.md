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

O diário de execução entre laboratórios que ficava solto em
`D03/protocolo.md` foi absorvido pelos notebooks de protocolo estatístico
em [`extras-pessoal/notebooks/`](../extras-pessoal/notebooks/) — hoje não
há mais nada solto na raiz de `D03/` fora dos `D3-0N-slug/`.

## `dados/` de cada lab

Quando um lab tem pasta `dados/` (`D3-01`, `D3-04`), o `dados/FONTE.md`
local já documenta a procedência — nos dois casos vistos até agora, os
vetores `manutencao-*`/`generico-*` vieram pré-calculados do pacote da
disciplina (não foram gerados pelo autor), então `dados/` inteira é do
curso, igual ao resto do lab.

`D03/AO1/dados/` é o primeiro caso diferente: a AO1 não tem pacote de
curso (só o `enunciado.pdf` do professor), então todo o conteúdo de
`dados/` ali é produção própria — os 60 casos de avaliação (30 de D02
adaptados ao esquema novo de `tipo_maquina`/`qualidade_produto` + os 30
novos de D03) e o de-para combinado, gerados por
`extras-pessoal/scripts/adaptar_casos_lab06.py`. Ver
`D03/AO1/dados/FONTE.md` para a proveniência completa e por que o
arquivo original de D02 (`casos-lab-06-v2.csv`) não foi tocado.
