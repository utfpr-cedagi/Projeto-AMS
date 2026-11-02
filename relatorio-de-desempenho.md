# Relatório de desempenho da linha de base

**Projeto:** AMS · Assistente de Manutenção Segura · **Data:** 2026-11-02

## 1. A métrica primária

A métrica primária do PEAS (`agent-spec.md` §4) é o **recall da classe
"alto"**: proporção de máquinas realmente de alto risco que o agente
classificou corretamente como alto.

`Recall = máquinas realmente de alto risco classificadas como alto ÷ total de máquinas realmente de alto risco`

O `medir.py` do D2-06 mede, de fábrica, o **acerto geral** (as 3 classes
contra o rótulo) — fica registrado abaixo por completude, mas quem decide
se a linha de base está pronta pro PEAS são o recall e a precisão de
"alto", calculados a partir da mesma lista de erros.

## 2. O valor

Saída de `python medir.py` (pasta `D02/D2-06-agente-baseline`, sobre o
`esqueleto.py` adaptado e `adaptacao-ams/casos-lab-06-v2.csv`):

```
Métrica primária: acerto da decisão (casos com decisão igual à rotulada, sobre o total)
Valor: 21/30 = 0.7
Conjunto: adaptacao-ams/casos-lab-06-v2.csv — 30 casos rotulados {'seguir_operando': 16, 'inspecionar_antes_de_operar': 6, 'parar_para_manutencao': 8}
Onde erra (o rótulo que o agente não deu):
  caso A02: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso A07: decidiu seguir_operando, correto era parar_para_manutencao
  caso A08: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso A09: decidiu inspecionar_antes_de_operar, correto era parar_para_manutencao
  caso A13: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso A17: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso A18: decidiu seguir_operando, correto era parar_para_manutencao
  caso A23: decidiu parar_para_manutencao, correto era inspecionar_antes_de_operar
  caso A28: decidiu seguir_operando, correto era inspecionar_antes_de_operar
```

Traduzindo pra métrica do PEAS (`parar_para_manutencao` = alto risco):

- **Recall "alto"** = 5/8 = **0,625** (3 dos 8 casos de alto risco saíram
  errados: A07, A09, A18) — abaixo da meta de 0,80.
- **Precisão "alto"** = 5/10 = **0,50** (das 10 vezes que decidiu parar, 5
  eram realmente de alto risco; as outras 5 — A02, A08, A13, A17, A23 —
  eram médio) — abaixo da meta de 0,80.
- **Taxa de erro alto→baixo** = 2/8 = **25%** (A07 e A18 foram liberados
  como `seguir_operando` sendo de alto risco) — 5x acima do limite de 5%.

## 3. O conjunto

`adaptacao-ams/casos-lab-06-v2.csv` (pasta `D02/D2-06-agente-baseline`) —
30 casos rotulados com dados **reais** do AI4I2020 (não a reserva
sintética do pacote), distribuídos em 16 `seguir_operando` (baixo), 6
`inspecionar_antes_de_operar` (médio) e 8 `parar_para_manutencao` (alto).
Proveniência em `FONTE-casos-lab-06-v2.md`.

## 4. Onde o agente erra

A lista de erros está colada acima (seção 2). O padrão: o agente erra mais
pro lado de ser **exigente demais** — 5 dos 9 erros (A02, A08, A13, A17,
A23) mandam parar a máquina quando bastava inspecionar, porque a regra
reativa só olha duas variáveis (desgaste e vibração) contra limiares fixos,
sem meio-termo: ou passou do limite e para, ou não passou e segue.

Nos 3 erros mais graves (A07, A09, A18) o problema é o oposto: a máquina
falhou de verdade e nem o desgaste nem a vibração estavam altos no momento
da leitura — o agente não via motivo pra agir, porque a informação que
decidiria não está na percepção do instante (é a observabilidade parcial
do `agent-spec.md` §2, concretizada). Em 1 caso (A28), o erro foi mais
leve: um risco médio que ficou perto dos dois limiares sem passar deles.

## 5. A tabela comparativa de busca (item 4 da N2)

Formulação: `comum/problemas/consultas_ams.py:MAIOR` (D2-04/05), 8 fatos,
14 fontes.

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 22.0 | 1 | 15 | 196 | 2 | 0.0003 |
| custo_uniforme | 10.9 | 6 | 1780 | 2814 | 7 | 0.005 |
| profundidade_limitada(limite=32) | 13.7 | 8 | 9 | 37 | 8 | 0.0001 |
| aprofundamento_iterativo(limite=32) | 22.0 | 1 | 16 | 14 | 1 | 0.0001 |
| gulosa[admissivel] | 22.0 | 1 | 2 | 14 | 1 | 0.0004 |
| a_estrela[admissivel] | 10.9 | 6 | 1558 | 2674 | 7 | 0.0111 |
| gulosa[inadmissivel] | 22.0 | 1 | 2 | 14 | 1 | 0.0001 |
| a_estrela[inadmissivel] | 22.0 | 1 | 2 | 14 | 1 | 0.0 |

**O A* admissível manteve o custo ótimo e expandiu menos que o custo
uniforme? Por quê?** Sim nos dois pontos. Custo: 10.9 nos dois — igual ao
ótimo que a busca em largura (22.0) não acha, porque ela minimiza ações, não
latência. Nós expandidos: 1558 contra 1780 do custo uniforme — **12,5% a
menos**. A diferença é a heurística (a latência da fonte mais barata que
ainda falta cobrir): ela nunca superestima o que falta, então guia a busca
pra longe de ramos caros cedo, sem nunca descartar o caminho ótimo — o
custo uniforme não tem essa informação e expande por ordem de custo
acumulado às cegas, revisitando mais ramos até achar a mesma resposta.

A heurística inadmissível (fatos que faltam × a pior latência) mostra o
contraste: expande só 2 nós (muito rápida), mas erra o resultado — custo
22.0, o dobro do ótimo, porque superestima e empurra a busca direto pra
fonte única cara (igual à busca gulosa). É rápida porque está errada; a
admissível é mais lenta porque garante a otimalidade do A*.
