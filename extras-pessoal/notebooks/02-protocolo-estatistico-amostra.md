# AMS — Protocolo estatístico sobre o AI4I2020

Gerado por `notebooks/gerar_relatorio_protocolo_estatistico.py` a partir de `amostra/ai4i2020.csv (200 linhas)` (`C:\temp\UTFPR\Projeto-AMS\data\amostra\ai4i2020.csv`). Acompanha `02-protocolo-estatistico.ipynb` — mesmas 8 seções, mas aqui a narrativa é recalculada a cada rodada; o notebook tem o código e os gráficos.

---

## 1 — Visão geral e qualidade dos dados

| medida | valor |
|---|---:|
| linhas | 200 |
| UDIs únicos | 200 |
| duplicados | 0 |
| colunas com valor faltante | 0 |

Distribuição de `tipo`:

| tipo | n | % |
|---|---:|---:|
| L | 119 | 59.5 |
| M | 60 | 30.0 |
| H | 21 | 10.5 |

**Conclusão:** 200 linhas, 200 UDIs únicos, 0 duplicados e zero valores faltantes — confirmado, não assumido. `tipo` é fortemente desbalanceado (`L` domina com 59,5%, `H` é minoria com 10,5%) — qualquer diferença de taxa de falha por tipo (seção 6) parte de amostras de tamanhos bem diferentes.

---

## 2 — Estatística descritiva univariada

| variável | média | mediana | desvio | assimetria | curtose | Q1 | Q3 | AIQ | normaltest p |
|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 300.1115 | 300.2000 | 2.0807 | 0.1202 | -0.8710 | 298.3000 | 301.8000 | 3.5000 | 0.0000 |
| temperatura_processo | 310.0475 | 310.1000 | 1.5444 | 0.0590 | -0.4501 | 308.8000 | 311.1000 | 2.3000 | 0.2740 |
| rotacao | 1528.5300 | 1472.0000 | 201.5680 | 2.6463 | 10.4921 | 1410.5000 | 1611.5000 | 201.0000 | 0.0000 |
| torque | 41.4785 | 43.1000 | 10.6072 | -0.3032 | -0.1096 | 33.4000 | 49.0500 | 15.6500 | 0.2073 |
| desgaste | 112.7750 | 115.0000 | 66.3876 | -0.0286 | -1.1791 | 57.5000 | 171.5000 | 114.0000 | 0.0000 |
| delta_temperatura | 9.9360 | 9.7000 | 1.0131 | 0.0542 | -1.0079 | 9.2000 | 10.9000 | 1.7000 | 0.0000 |
| potencia_kw | 6.4494 | 6.5532 | 1.1516 | -0.2287 | -0.1371 | 5.6291 | 7.2605 | 1.6314 | 0.3902 |

**Conclusão:** nem toda variável de sensor tem a mesma forma. `desgaste` é a mais próxima de simétrica desta rodada (assimetria -0,03), enquanto `rotacao` é a mais assimétrica (assimetria 2,65, curtose 10,49). `potencia_kw` é a variável em que o `normaltest` tem o maior p-valor desta rodada (p=0,390, não rejeita normalidade a 5%); 4 de 7 variáveis rejeitam normalidade a 5% nesta rodada (n=200 — lembrar que o poder do teste cresce com n: com amostra pequena, rejeitar fica mais difícil mesmo quando a forma não é de fato normal). `desgaste` é a de curtose mais negativa (curtose -1,18), sinal de distribuição mais achatada/uniforme que as demais.

---

## 3 — Outliers via IQR

Regra do boxplot (fora de `[Q1 − 1,5·AIQ, Q3 + 1,5·AIQ]`), mesma do `D3-03/medidas.py`.

| variável | n extremos | % extremos | % dos extremos que falharam |
|---|---:|---:|---:|
| temperatura_ar | 0 | 0.00 | — |
| temperatura_processo | 0 | 0.00 | — |
| rotacao | 8 | 4.00 | 12.5 |
| torque | 0 | 0.00 | — |
| desgaste | 0 | 0.00 | — |
| delta_temperatura | 0 | 0.00 | — |
| potencia_kw | 1 | 0.50 | 100.0 |

**Conclusão:** 5 de 7 variáveis não têm nenhum outlier pela regra do boxplot nesta rodada (`temperatura_ar`, `temperatura_processo`, `torque`, `desgaste`, `delta_temperatura`).
 Das que têm outlier, `potencia_kw` concentra a maior taxa de falha dentro do grupo extremo (100,0%, contra 4,0% de taxa de falha geral) — outlier com concentração de falha bem acima da taxa geral é sinal, não ruído, e a decisão caso a caso (como o `D3-03/medidas.py` pede) tende a manter esses pontos: são justamente os casos que o projeto existe para detectar.

---

## 4 — Correlação bivariada

**Pearson**

| var | temperatura_ar | temperatura_processo | rotacao | torque | desgaste | delta_temperatura | potencia_kw |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 1.00 | 0.89 | 0.03 | 0.03 | -0.00 | -0.70 | 0.05 |
| temperatura_processo | 0.89 | 1.00 | -0.02 | 0.07 | 0.02 | -0.29 | 0.08 |
| rotacao | 0.03 | -0.02 | 1.00 | -0.85 | 0.06 | -0.10 | -0.78 |
| torque | 0.03 | 0.07 | -0.85 | 1.00 | -0.10 | 0.04 | 0.98 |
| desgaste | -0.00 | 0.02 | 0.06 | -0.10 | 1.00 | 0.02 | -0.13 |
| delta_temperatura | -0.70 | -0.29 | -0.10 | 0.04 | 0.02 | 1.00 | 0.03 |
| potencia_kw | 0.05 | 0.08 | -0.78 | 0.98 | -0.13 | 0.03 | 1.00 |

**Spearman**

| var | temperatura_ar | temperatura_processo | rotacao | torque | desgaste | delta_temperatura | potencia_kw |
|---|---:|---:|---:|---:|---:|---:|---:|
| temperatura_ar | 1.00 | 0.87 | -0.00 | 0.01 | 0.02 | -0.72 | 0.03 |
| temperatura_processo | 0.87 | 1.00 | -0.03 | 0.04 | 0.04 | -0.30 | 0.06 |
| rotacao | -0.00 | -0.03 | 1.00 | -0.89 | 0.00 | -0.05 | -0.77 |
| torque | 0.01 | 0.04 | -0.89 | 1.00 | -0.11 | 0.03 | 0.97 |
| desgaste | 0.02 | 0.04 | 0.00 | -0.11 | 1.00 | 0.03 | -0.15 |
| delta_temperatura | -0.72 | -0.30 | -0.05 | 0.03 | 0.03 | 1.00 | 0.02 |
| potencia_kw | 0.03 | 0.06 | -0.77 | 0.97 | -0.15 | 0.02 | 1.00 |

**Conclusão:** maior diferença absoluta entre Pearson e Spearman nesta rodada: 0,060 — concordância alta, não há relação não-linear forte escondida que só o Spearman capturaria. Torque×rotação (Pearson, via `analise.py`): -0,852 (negativa — coerente com potência aproximadamente constante). `potencia_kw` correlaciona 0,980 com torque e -0,783 com rotação — é função determinística dos dois, não uma terceira variável independente; um classificador que use os três como preditores separados está contando a mesma informação mais de uma vez.

---

## 5 — Falha vs. não-falha, por variável

| variável | mediana não-falhou | mediana falhou | Mann-Whitney p | efeito rank-biserial |
|---|---:|---:|---:|---:|
| desgaste | 111.5000 | 203.0000 | 0.0039 | -0.6035 |
| delta_temperatura | 9.7000 | 9.7000 | 0.4467 | 0.1595 |
| torque | 43.0000 | 46.9500 | 0.3529 | -0.1947 |
| potencia_kw | 6.5466 | 6.7497 | 0.4596 | -0.1576 |

**Conclusão:** `desgaste` é a variável que mais separa falha de não-falha nesta rodada (efeito rank-biserial -0,60) — confirma a intuição de que o acionador nominal do modo de falha separa mais. 1 de 4 variáveis têm Mann-Whitney p < 0,05 nesta rodada (n=200 — com amostra pequena, um p-valor alto pode só refletir falta de poder estatístico, não ausência de diferença real; o tamanho de efeito continua a melhor bússola).

---

## 6 — Tipo de produto × falha

| tipo | não falhou | falhou | taxa de falha (%) |
|---|---:|---:|---:|
| H | 20 | 1 | 4.76 |
| L | 114 | 5 | 4.20 |
| M | 58 | 2 | 3.33 |

qui-quadrado: 0.11 · p-valor: 0.9447 · Cramér's V: 0.024

**Conclusão:** a associação NÃO é estatisticamente significativa nesta rodada (p=0,945 ≥ 0,05 — com n=200, não há evidência suficiente de associação entre tipo e falha), e Cramér's V = 0,024 é efeito muito pequeno — tipo de produto desloca a taxa de falha, mas é pequeno perto do que os mecanismos físicos (seção 7) explicam; vale como fator secundário, não decisivo sozinho.

---

## 7 — Os cinco mecanismos de falha, quantificados

Limiares oficiais de `ams.gerador_casos`, testados como regra preditiva contra a flag real de cada modo.

| mecanismo | recall | precisão | casos reais | casos previstos pela regra |
|---|---:|---:|---:|---:|
| TWF (zona de desgaste 200-240min) | 1.000 | 0.125 | 3 | 24 |
| HDF (delta<8,6K e rotação<1380rpm) | 1.000 | 1.000 | 1 | 1 |
| PWF (potência fora de 3500-9000W) | 1.000 | 1.000 | 2 | 2 |
| OSF (desgaste x torque >= limite por tipo) | 1.000 | 1.000 | 3 | 3 |

RNF: 0 caso(s) reais em 200 (0,000%) — nenhuma variável de sensor prevê isso, é ruído puro por definição.

**Conclusão:** `HDF`, `PWF`, `OSF` reproduzem a flag real com recall e precisão praticamente perfeitos nesta rodada — confirma o mecanismo documentado pela UCI, é checagem de sanidade, não achado novo. `TWF` tem a pior precisão (12,5%, apesar do recall alto (100,0%)) — a regra acerta "onde olhar" bem mais do que acerta "o quê vai acontecer". RNF fica fora desta tabela de propósito: é um piso de erro irredutível para qualquer classificador baseado nesses dados, inclusive o da seção 8.

---

## 8 — Proposta de classificador agregado (baixo / médio / alto)

`alto`: TWF, HDF, PWF ou OSF sinalizados. `médio`: nenhum limiar cruzado, mas dentro da margem de "caso difícil" de `ams.gerador_casos`. `baixo`: o resto. Critérios de `agent-spec.md` §4: recall e precisão da classe alto ≥ 80%, taxa de "alto" classificado como "baixo" ≤ 5%.

| nível de risco | n | taxa de falha real (%) |
|---|---:|---:|
| baixo | 161 | 0.00 |
| medio | 12 | 0.00 |
| alto | 27 | 29.63 |

| métrica | valor | critério | resultado |
|---|---:|---:|---|
| recall da classe 'alto' | 100,0% | ≥ 80% | PASSA |
| precisão da classe 'alto' | 29,6% | ≥ 80% | NÃO PASSA |
| taxa 'alto' classificado baixo | 0,0% | ≤ 5% | PASSA |

**Conclusão:** a regra física simples bate 2 dos 3 critérios do `agent-spec.md` §4 nesta rodada. Recall 100,0% e taxa de "alto" classificado como "baixo" 0,0% passam. Precisão 29,6% não chega perto do critério — a regra "alto" é um OU entre quatro mecanismos, e o(s) mais fraco(s) em precisão (seção 7) arrastam a precisão do conjunto para baixo. Esta é uma baseline estatística por regras, não um modelo treinado — atualizar o `agent-spec.md` §4 com estes números é decisão separada do autor, fora deste relatório.

---

## Síntese da rodada

1. A forma das variáveis varia mais do que se espera de "tudo é sensor físico" (seção 2): `rotacao` é a mais assimétrica desta rodada (assimetria 2,65), `potencia_kw` é a que o `normaltest` menos rejeita (p=0,390), e 4 de 7 variáveis rejeitam normalidade a 5% nesta rodada.
2. Extremos estatísticos (seção 3) concentram sinal, não ruído, em pelo menos uma variável: `potencia_kw` tem 100,0% de taxa de falha dentro do seu próprio grupo de outliers. 5 de 7 variáveis não têm outlier nenhum pela regra do boxplot nesta rodada.
3. `potencia_kw` é redundante com torque×rotação (seção 4): correlaciona 0,980 com torque e -0,783 com rotação — não entra como terceira variável independente num classificador futuro.
4. Na comparação falha x não-falha por variável (seção 5), `desgaste` é quem mais separa os dois grupos nesta rodada (efeito rank-biserial -0,60), confirmando a intuição de que o acionador nominal do modo de falha separa mais.
5. Tipo de produto x falha (seção 6): Cramér's V = 0,024 (associação NÃO significativa nesta rodada) — efeito pequeno perto do que os mecanismos físicos explicam.
6. Os mecanismos físicos (seção 7) se confirmam com recall e precisão praticamente perfeitos em `HDF`, `PWF`, `OSF`; `TWF` é o mais fraco em precisão (12,5%). RNF (0 caso(s), 0,000%) é um piso de erro irredutível para qualquer classificador baseado nesses dados.
7. A regra agregada (seção 8) bate 2 dos 3 critérios do `agent-spec.md` §4 nesta rodada: recall 100,0%, precisão 29,6%, taxa 'alto'→'baixo' 0,0%.
