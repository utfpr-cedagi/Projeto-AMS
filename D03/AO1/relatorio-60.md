# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `dados\casos-60.csv` · 60 linhas · 11 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| id_caso | categórica (60 valores; moda: B30) | 60 | 0 | — | — | — | — | — | — | — | — |
| data | categórica (60 valores; moda: 2026-04-01) | 60 | 0 | — | — | — | — | — | — | — | — |
| tipo_maquina | categórica (4 valores; moda: ROBOT) | 60 | 0 | — | — | — | — | — | — | — | — |
| qualidade_produto | categórica (3 valores; moda: L) | 60 | 0 | — | — | — | — | — | — | — | — |
| temperatura_c | numérica | 60 | 0 | 36.7033 | 36.8500 | 1.5445 | 35.4250 | 37.8250 | 2.4000 | 33.4000 | 39.9000 |
| vibracao_mm_s | numérica | 60 | 0 | 3.8367 | 3.4000 | 1.9182 | 2.4750 | 4.5000 | 2.0250 | 2.1000 | 11.3000 |
| horas_desde_manutencao | numérica | 60 | 0 | 110.1833 | 100.0000 | 70.1771 | 52.2500 | 170.7500 | 118.5000 | 0.0000 | 240.0000 |
| acao_correta | categórica (3 valores; moda: seguir_operando) | 60 | 0 | — | — | — | — | — | — | — | — |
| falhou_depois | numérica | 60 | 0 | 0.2667 | 0.0000 | 0.4459 | 0.0000 | 1.0000 | 1.0000 | 0.0000 | 1.0000 |
| risco | categórica (3 valores; moda: baixo) | 60 | 0 | — | — | — | — | — | — | — | — |
| dificuldade | categórica (3 valores; moda: facil) | 60 | 0 | — | — | — | — | — | — | — | — |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `vibracao_mm_s` — 4 valor(es), limites [-0.5625; 7.5375]

| linha | valor |
|---:|---:|
| 8 | 9.2000 |
| 14 | 11.3000 |
| 34 | 9.7000 |
| 41 | 9.7000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Ficam os 4. Não são erro: o proxy de vibração sai da mesma fórmula sobre RPM e torque reais. A14 e B11 são falhas reais; A08 e B04 são casos difíceis rotulados inspecionar. Se saíssem: n = 56, média de vibração 3,84 → 3,40, mediana 3,40 → 3,35, e a classe parar perderia 2 dos 16 casos.


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: Sim, em `vibracao_mm_s`: média 3,84 contra mediana 3,40, por causa dos 4 extremos. Em temperatura (36,70 × 36,85) e horas (110 × 100), as duas ficam próximas.

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: 4 extremos, todos em vibração (A08, A14, B04, B11), e mantive os 4.

**3. Algum faltante parece do terceiro mecanismo?**

R: Não. Há 0 faltantes, porque o AI4I é completo. Em ordens de serviço reais, o caso provável seria a leitura que falta justamente na máquina com defeito, e essas linhas não poderiam ser descartadas.

**4. O que a análise da D1 não tinha visto?**

R: (1) O conjunto é desbalanceado: responder sempre "seguir" acerta 53%. (2) `falhou_depois` coincide 100% com a classe parar: é o desfecho, não entrada. (3) Os extremos aparecem agora no proxy de vibração, e metade deles não são falhas.

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: A avaliação usa 60 casos escolhidos, não a base inteira da D1: 27% de falhas contra cerca de 3,4% na base. Por isso o acerto geral precisa vir com o recall da classe alto, e as variantes são comparadas nos mesmos 60 casos. Nada foi removido nem imputado.
