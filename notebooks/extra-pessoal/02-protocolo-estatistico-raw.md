# AMS — Protocolo estatístico sobre o AI4I2020

Gerado por `notebooks/gerar_relatorio_protocolo_estatistico.py` a partir de `raw/ai4i2020.csv (10000 linhas)` (`C:\temp\UTFPR\Projeto-AMS\data\raw\ai4i2020.csv`). Acompanha `02-protocolo-estatistico.ipynb` — mesmas 8 seções, mas aqui a narrativa é recalculada a cada rodada; o notebook tem o código e os gráficos.

---

## 1 — Visão geral e qualidade dos dados

| medida | valor |
|---|---:|
| linhas | 10000 |
| UDIs únicos | 10000 |
| duplicados | 0 |
| colunas com valor faltante | 0 |

Distribuição de `tipo`:

| tipo | n | % |
|---|---:|---:|
| L | 6000 | 60.0 |
| M | 2997 | 30.0 |
| H | 1003 | 10.0 |

**Conclusão:** 10000 linhas, 10000 UDIs únicos, 0 duplicados e zero valores faltantes — confirmado, não assumido. `tipo` é fortemente desbalanceado (`L` domina com 60,0%, `H` é minoria com 10,0%) — qualquer diferença de taxa de falha por tipo (seção 6) parte de amostras de tamanhos bem diferentes.

---

## 2 — Estatística descritiva univariada

| variável | média | mediana | desvio | assimetria | curtose | Q1 | Q3 | AIQ | normaltest p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 300.0049 | 300.1000 | 2.0003 | 0.1143 | -0.8360 | 298.3000 | 301.5000 | 3.2000 | 0.0000 |
| temperatura_processo | 310.0056 | 310.1000 | 1.4837 | 0.0150 | -0.4997 | 308.8000 | 311.1000 | 2.3000 | 0.0000 |
| rotacao | 1538.7761 | 1503.0000 | 179.2841 | 1.9932 | 7.3929 | 1423.0000 | 1612.0000 | 189.0000 | 0.0000 |
| torque | 39.9869 | 40.1000 | 9.9689 | -0.0095 | -0.0132 | 33.2000 | 46.8000 | 13.6000 | 0.8992 |
| desgaste | 107.9510 | 108.0000 | 63.6541 | 0.0273 | -1.1667 | 53.0000 | 162.0000 | 109.0000 | 0.0000 |
| delta_temperatura | 10.0006 | 9.8000 | 1.0011 | -0.0725 | -0.9858 | 9.3000 | 11.0000 | 1.7000 | 0.0000 |
| potencia_kw | 6.2797 | 6.2710 | 1.0674 | 0.0083 | 0.1582 | 5.5612 | 7.0030 | 1.4418 | 0.0098 |

**Conclusão:** nem toda variável de sensor tem a mesma forma. `potencia_kw` é a mais próxima de simétrica desta rodada (assimetria 0,01), enquanto `rotacao` é a mais assimétrica (assimetria 1,99, curtose 7,39). `torque` é a variável em que o `normaltest` tem o maior p-valor desta rodada (p=0,899, não rejeita normalidade a 5%); 6 de 7 variáveis rejeitam normalidade a 5% nesta rodada (n=10000 — lembrar que o poder do teste cresce com n: com amostra pequena, rejeitar fica mais difícil mesmo quando a forma não é de fato normal). `desgaste` é a de curtose mais negativa (curtose -1,17), sinal de distribuição mais achatada/uniforme que as demais.

---

## 3 — Outliers via IQR

Regra do boxplot (fora de `[Q1 − 1,5·AIQ, Q3 + 1,5·AIQ]`), mesma do `D3-03/medidas.py`.

| variável | n extremos | % extremos | % dos extremos que falharam |
|---|---:|---:|---:|
| temperatura_ar | 0 | 0.00 | — |
| temperatura_processo | 0 | 0.00 | — |
| rotacao | 418 | 4.18 | 8.4 |
| torque | 69 | 0.69 | 89.9 |
| desgaste | 0 | 0.00 | — |
| delta_temperatura | 0 | 0.00 | — |
| potencia_kw | 60 | 0.60 | 100.0 |

**Conclusão:** 4 de 7 variáveis não têm nenhum outlier pela regra do boxplot nesta rodada (`temperatura_ar`, `temperatura_processo`, `desgaste`, `delta_temperatura`).
 Das que têm outlier, `potencia_kw` concentra a maior taxa de falha dentro do grupo extremo (100,0%, contra 3,4% de taxa de falha geral) — outlier com concentração de falha bem acima da taxa geral é sinal, não ruído, e a decisão caso a caso (como o `D3-03/medidas.py` pede) tende a manter esses pontos: são justamente os casos que o projeto existe para detectar.

---

## 4 — Correlação bivariada

**Pearson**

| var | temperatura_ar | temperatura_processo | rotacao | torque | desgaste | delta_temperatura | potencia_kw |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 1.00 | 0.88 | 0.02 | -0.01 | 0.01 | -0.70 | -0.01 |
| temperatura_processo | 0.88 | 1.00 | 0.02 | -0.01 | 0.01 | -0.27 | -0.01 |
| rotacao | 0.02 | 0.02 | 1.00 | -0.88 | 0.00 | -0.02 | -0.81 |
| torque | -0.01 | -0.01 | -0.88 | 1.00 | -0.00 | 0.01 | 0.98 |
| desgaste | 0.01 | 0.01 | 0.00 | -0.00 | 1.00 | -0.01 | -0.00 |
| delta_temperatura | -0.70 | -0.27 | -0.02 | 0.01 | -0.01 | 1.00 | 0.01 |
| potencia_kw | -0.01 | -0.01 | -0.81 | 0.98 | -0.00 | 0.01 | 1.00 |

**Spearman**

| var | temperatura_ar | temperatura_processo | rotacao | torque | desgaste | delta_temperatura | potencia_kw |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 1.00 | 0.86 | 0.01 | -0.01 | 0.01 | -0.71 | -0.01 |
| temperatura_processo | 0.86 | 1.00 | 0.02 | -0.01 | 0.01 | -0.27 | -0.01 |
| rotacao | 0.01 | 0.02 | 1.00 | -0.92 | 0.00 | -0.01 | -0.82 |
| torque | -0.01 | -0.01 | -0.92 | 1.00 | -0.00 | 0.00 | 0.98 |
| desgaste | 0.01 | 0.01 | 0.00 | -0.00 | 1.00 | -0.01 | -0.00 |
| delta_temperatura | -0.71 | -0.27 | -0.01 | 0.00 | -0.01 | 1.00 | 0.00 |
| potencia_kw | -0.01 | -0.01 | -0.82 | 0.98 | -0.00 | 0.00 | 1.00 |

**Conclusão:** maior diferença absoluta entre Pearson e Spearman nesta rodada: 0,041 — concordância alta, não há relação não-linear forte escondida que só o Spearman capturaria. Torque×rotação (Pearson, via `analise.py`): -0,875 (negativa — coerente com potência aproximadamente constante). `potencia_kw` correlaciona 0,979 com torque e -0,806 com rotação — é função determinística dos dois, não uma terceira variável independente; um classificador que use os três como preditores separados está contando a mesma informação mais de uma vez.

---

## 5 — Falha vs. não-falha, por variável

| variável | mediana não-falhou | mediana falhou | Mann-Whitney p | efeito rank-biserial |
|---|---:|---:|---:|---:|
| desgaste | 107.0000 | 165.0000 | 0.0000 | -0.3242 |
| delta_temperatura | 9.8000 | 9.3000 | 0.0000 | 0.3247 |
| torque | 39.9000 | 53.7000 | 0.0000 | -0.5405 |
| potencia_kw | 6.2430 | 7.6114 | 0.0000 | -0.4913 |

**Conclusão:** `torque` é a variável que mais separa falha de não-falha nesta rodada (efeito rank-biserial -0,54) — ao contrário da intuição óbvia de que o acionador nominal (`desgaste`/`delta_temperatura`) separaria mais: aqui quem mais separa não é o acionador nominal de nenhum modo isoladamente, o que sugere efeito cruzado entre mecanismos (ex.: OSF usa desgaste×torque, PWF usa potência). 4 de 4 variáveis têm Mann-Whitney p < 0,05 nesta rodada (n=10000 — com amostra grande, significância estatística deixa de ser notícia; o tamanho de efeito, não o p-valor, é o que compara as variáveis entre si).

---

## 6 — Tipo de produto × falha

| tipo | não falhou | falhou | taxa de falha (%) |
|---|---:|---:|---:|
| H | 982 | 21 | 2.09 |
| L | 5765 | 235 | 3.92 |
| M | 2914 | 83 | 2.77 |

qui-quadrado: 13.75 · p-valor: 0.0010 · Cramér's V: 0.037

**Conclusão:** a associação é estatisticamente significativa (p < 0,05), e Cramér's V = 0,037 é efeito muito pequeno — tipo de produto desloca a taxa de falha, mas é pequeno perto do que os mecanismos físicos (seção 7) explicam; vale como fator secundário, não decisivo sozinho.

---

## 7 — Os cinco mecanismos de falha, quantificados

Limiares oficiais de `ams.gerador_casos`, testados como regra preditiva contra a flag real de cada modo.

| mecanismo | recall | precisão | casos reais | casos previstos pela regra |
|---|---:|---:|---:|---:|
| TWF (zona de desgaste 200-240min) | 0.935 | 0.054 | 46 | 790 |
| HDF (delta<8,6K e rotação<1380rpm) | 1.000 | 1.000 | 115 | 115 |
| PWF (potência fora de 3500-9000W) | 1.000 | 1.000 | 95 | 95 |
| OSF (desgaste x torque >= limite por tipo) | 1.000 | 1.000 | 98 | 98 |

RNF: 19 caso(s) reais em 10000 (0,190%) — nenhuma variável de sensor prevê isso, é ruído puro por definição.

**Conclusão:** `HDF`, `PWF`, `OSF` reproduzem a flag real com recall e precisão praticamente perfeitos nesta rodada — confirma o mecanismo documentado pela UCI, é checagem de sanidade, não achado novo. `TWF` tem a pior precisão (5,4%, apesar do recall alto (93,5%)) — a regra acerta "onde olhar" bem mais do que acerta "o quê vai acontecer". RNF fica fora desta tabela de propósito: é um piso de erro irredutível para qualquer classificador baseado nesses dados, inclusive o da seção 8.

---

## 8 — Proposta de classificador agregado (baixo / médio / alto)

`alto`: TWF, HDF, PWF ou OSF sinalizados. `médio`: nenhum limiar cruzado, mas dentro da margem de "caso difícil" de `ams.gerador_casos`. `baixo`: o resto. Critérios de `agent-spec.md` §4: recall e precisão da classe alto ≥ 80%, taxa de "alto" classificado como "baixo" ≤ 5%.

| nível de risco | n | taxa de falha real (%) |
|---|---:|---:|
| baixo | 8342 | 0.10 |
| medio | 658 | 0.30 |
| alto | 1000 | 32.90 |

| métrica | valor | critério | resultado |
|---|---:|---:|---|
| recall da classe 'alto' | 97,1% | ≥ 80% | PASSA |
| precisão da classe 'alto' | 32,9% | ≥ 80% | NÃO PASSA |
| taxa 'alto' classificado baixo | 2,4% | ≤ 5% | PASSA |

**Conclusão:** a regra física simples bate 2 dos 3 critérios do `agent-spec.md` §4 nesta rodada. Recall 97,1% e taxa de "alto" classificado como "baixo" 2,4% passam. Precisão 32,9% não chega perto do critério — a regra "alto" é um OU entre quatro mecanismos, e o(s) mais fraco(s) em precisão (seção 7) arrastam a precisão do conjunto para baixo. Esta é uma baseline estatística por regras, não um modelo treinado — atualizar o `agent-spec.md` §4 com estes números é decisão separada do autor, fora deste relatório.

---

## Síntese da rodada

1. A forma das variáveis varia mais do que se espera de "tudo é sensor físico" (seção 2): `rotacao` é a mais assimétrica desta rodada (assimetria 1,99), `torque` é a que o `normaltest` menos rejeita (p=0,899), e 6 de 7 variáveis rejeitam normalidade a 5% nesta rodada.
2. Extremos estatísticos (seção 3) concentram sinal, não ruído, em pelo menos uma variável: `potencia_kw` tem 100,0% de taxa de falha dentro do seu próprio grupo de outliers. 4 de 7 variáveis não têm outlier nenhum pela regra do boxplot nesta rodada.
3. `potencia_kw` é redundante com torque×rotação (seção 4): correlaciona 0,979 com torque e -0,806 com rotação — não entra como terceira variável independente num classificador futuro.
4. Na comparação falha x não-falha por variável (seção 5), `torque` é quem mais separa os dois grupos nesta rodada (efeito rank-biserial -0,54) — e não é o acionador "nominal" de nenhum modo isoladamente, sinal de efeito cruzado entre mecanismos.
5. Tipo de produto x falha (seção 6): Cramér's V = 0,037 (associação estatisticamente significativa) — efeito pequeno perto do que os mecanismos físicos explicam.
6. Os mecanismos físicos (seção 7) se confirmam com recall e precisão praticamente perfeitos em `HDF`, `PWF`, `OSF`; `TWF` é o mais fraco em precisão (5,4%). RNF (19 caso(s), 0,190%) é um piso de erro irredutível para qualquer classificador baseado nesses dados.
7. A regra agregada (seção 8) bate 2 dos 3 critérios do `agent-spec.md` §4 nesta rodada: recall 97,1%, precisão 32,9%, taxa 'alto'→'baixo' 2,4%.
