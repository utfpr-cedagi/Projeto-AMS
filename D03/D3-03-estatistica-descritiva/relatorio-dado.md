# O meu dado, com rigor — relatório do Laboratório 03

Conjunto: `data\amostra\ai4i2020.csv` · 200 linhas · 14 variáveis

Medidas geradas pelo `medidas.py`: desvio padrão amostral (ddof=1),
quartis por interpolação linear, extremos pela regra da amplitude
interquartil — fora de 1,5 × a caixa (slide 24). As medidas são do
programa; as decisões são SUAS. Preencha todos os blocos `R:` e
confira com `python teste.py`.

## Medidas por variável

| variável | tipo | n | faltantes | média | mediana | desvio | Q1 | Q3 | AIQ | mín | máx |
|---|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| UDI | numérica | 200 | 0 | 5027.1950 | 5014.5000 | 2837.9039 | 2779.7500 | 7459.5000 | 4679.7500 | 138.0000 | 9998.0000 |
| Product ID | categórica (200 valores; moda: L53351) | 200 | 0 | — | — | — | — | — | — | — | — |
| Type | categórica (3 valores; moda: L) | 200 | 0 | — | — | — | — | — | — | — | — |
| Air temperature [K] | numérica | 200 | 0 | 300.1115 | 300.2000 | 2.0807 | 298.3000 | 301.8000 | 3.5000 | 295.6000 | 304.2000 |
| Process temperature [K] | numérica | 200 | 0 | 310.0475 | 310.1000 | 1.5444 | 308.8000 | 311.1000 | 2.3000 | 306.1000 | 313.8000 |
| Rotational speed [rpm] | numérica | 200 | 0 | 1528.5300 | 1472.0000 | 201.5680 | 1410.5000 | 1611.5000 | 201.0000 | 1278.0000 | 2678.0000 |
| Torque [Nm] | numérica | 200 | 0 | 41.4785 | 43.1000 | 10.6072 | 33.4000 | 49.0500 | 15.6500 | 10.7000 | 66.7000 |
| Tool wear [min] | numérica | 200 | 0 | 112.7750 | 115.0000 | 66.3876 | 57.5000 | 171.5000 | 114.0000 | 0.0000 | 240.0000 |
| Machine failure | numérica | 200 | 0 | 0.0400 | 0.0000 | 0.1965 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| TWF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| HDF | numérica | 200 | 0 | 0.0050 | 0.0000 | 0.0707 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| PWF | numérica | 200 | 0 | 0.0100 | 0.0000 | 0.0997 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| OSF | numérica | 200 | 0 | 0.0150 | 0.0000 | 0.1219 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 1.0000 |
| RNF | numérica | 200 | 0 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 | 0.0000 |

## Extremos marcados (fora de 1,5 × a caixa — slide 24)

### Extremos de `Rotational speed [rpm]` — 8 valor(es), limites [1109.0000; 1913.0000]

| linha | valor |
|---:|---:|
| 4 | 2678.0000 |
| 54 | 2355.0000 |
| 59 | 2025.0000 |
| 86 | 2009.0000 |
| 91 | 1927.0000 |
| 114 | 2370.0000 |
| 122 | 1931.0000 |
| 133 | 2595.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter, caso a caso. As 8 linhas têm torque correspondente muito abaixo
da mediana (13,7–22,0 Nm, contra mediana geral de 43,1 Nm) — coerente com a
relação inversa torque×rotação que a D1 confirmou (potência
aproximadamente constante, pergunta 3). Não são erro de digitação: são
pontos reais no canto extremo da curva de potência constante. A linha 4 é
o caso mais extremo — ao mesmo tempo o mínimo de Torque (10,7 Nm) e o
máximo de Rotational speed (2678 rpm) do conjunto — e é a única das 8 que
de fato falhou (Machine failure=1, PWF=1), confirmando que o canto é onde
o risco mora.

### Extremos de `Machine failure` — 8 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 9 | 1.0000 |
| 23 | 1.0000 |
| 77 | 1.0000 |
| 83 | 1.0000 |
| 89 | 1.0000 |
| 132 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter — as 8 linhas são os eventos de interesse do domínio (falha
real), não erro de dado. `Machine failure` tem prevalência baixa (4% nesta
amostra), então Q1=Q3=0 e qualquer valor 1 cai fora da caixa por
construção da regra do IQR — é um artefato estrutural de indicador raro,
não uma anomalia a corrigir. Cada uma das 8 linhas mapeia para exatamente
um modo de falha (TWF/HDF/PWF/OSF), exceto a linha 77, que tem PWF e OSF
simultaneamente (torque 66,7 Nm, o máximo do conjunto) — confirma o que a
D1 já tinha visto (pergunta 5: existem casos com dois modos ao mesmo
tempo). Remover qualquer uma destas linhas jogaria fora justamente o
evento que o AMS existe para prever.

### Extremos de `TWF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 23 | 1.0000 |
| 83 | 1.0000 |
| 168 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter as 3 linhas — mesmo artefato estrutural do grupo anterior
(indicador raro com Q1=Q3=0), e as 3 ocorrências de falha por desgaste de
ferramenta (Tool Wear Failure) são exatamente o tipo de evento que a
análise de desgaste da D1 (pergunta 2) apontou como sinal relevante, só
que aqui confirmado pelo modo específico, não só pela variável contínua.

### Extremos de `HDF` — 1 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 89 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter — único caso de Heat Dissipation Failure na amostra, mesmo
artefato estrutural (indicador raro, Q1=Q3=0). A D1 (pergunta 4) já tinha
isolado o limiar de 8,6 K de ΔT como gatilho deste modo especificamente;
esta linha é a materialização desse gatilho nesta amostra, não um erro.

### Extremos de `PWF` — 2 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 4 | 1.0000 |
| 77 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter as 2 linhas — mesmo artefato estrutural (indicador raro). As
duas são exatamente as linhas que a física torque×rotação da D1
(pergunta 3) previa: linha 4 no canto rotação-alta/torque-baixo (ver
`Rotational speed` acima) e linha 77 no canto oposto, torque-alto (66,7
Nm, o máximo do conjunto), além de ser o único caso com dois modos
simultâneos (PWF e OSF). Power Failure é o modo que a D1 já tinha
nomeado como "a formalização" desse padrão — remover essas linhas
apagaria a confirmação numérica de uma conclusão já prevista.

### Extremos de `OSF` — 3 valor(es), limites [0.0000; 0.0000]

| linha | valor |
|---:|---:|
| 9 | 1.0000 |
| 77 | 1.0000 |
| 132 | 1.0000 |

Decisão sobre ESTES extremos — manter ou remover, caso a caso,
com o motivo (slide 25: quem remove sem dizer, mente por omissão):

R: Manter as 3 linhas — mesmo artefato estrutural (indicador raro). As
3 ocorrências de Overstrain Failure têm torque alto (56,7–66,7 Nm, acima
do Q3 geral de 49,05), coerente com o modo ser definido por
torque×desgaste excessivo; a linha 77 soma OSF a PWF (ver acima), o único
caso de sobreposição de modos na amostra, já esperado pela D1 (pergunta
5).


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: Sim, mais visivelmente em `Rotational speed [rpm]`: média 1528,53
contra mediana 1472,00 (diferença de ~56,5 rpm, a maior separação
relativa da tabela). É a cauda dos 8 extremos de alta rotação puxando a
média pra cima — exatamente o padrão de cauda longa que o enunciado avisa
pra variável de valor/tempo (slide 30).

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: 25 extremos ao todo (8 em `Rotational speed`, 8 em `Machine failure`,
3 em `TWF`, 1 em `HDF`, 2 em `PWF`, 3 em `OSF`). Mantive os 25 — nenhum é
erro de digitação identificável; os 8 de rotação são pontos físicos reais
no canto da curva de potência constante, e os 17 restantes são eventos de
falha reais ou artefato estrutural da regra do IQR sobre indicador raro
(Q1=Q3=0).

**3. Algum faltante parece do terceiro mecanismo?**

R: Não há como avaliar — nenhuma variável desta amostra tem valor
faltante (todas com 0 faltantes na tabela). Vale registrar uma distinção:
a inconsistência "falha sem modo" que a D1 achou na base completa (27
casos) não é um faltante no sentido do slide 26 — não há NaN em nenhuma
coluna — é uma contradição lógica entre `Machine failure` e os 5 modos,
um mecanismo de qualidade de dado diferente do framework de missingness.

**4. O que a análise da D1 não tinha visto?**

R: Três coisas. (a) A regra do IQR expõe que todo indicador binário raro
(prevalência baixa) vira "extremo" por construção, porque Q1=Q3=0 — a D1
não tinha quantificado extremos formalmente, só olhado distribuições. (b)
Nesta amostra de 200 linhas, nenhum `Machine failure=1` ficou sem modo —
diferente dos 27 casos que a D1 achou na base completa de 10.000 linhas
(~0,27%); com 200 linhas o esperado seria ~0,5 caso, então é plausível que
a amostra simplesmente não capture esse tipo raro de inconsistência —
achado sobre o tamanho da amostra, não sobre o domínio. (c) A linha 4
isola numericamente o canto extremo que a D1 só tinha mostrado
visualmente no scatter torque×rotação (pergunta 3): é ao mesmo tempo o
mínimo de Torque e o máximo de Rotational speed do conjunto, e o único
desses 8 extremos que de fato falhou (PWF).

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: A D1 foi exploratória e visual — KDE, scatter, correlação, uma frase
de conclusão por gráfico. A D3-03 é quantitativa e linha a linha: limites
numéricos de 1,5×IQR, linhas específicas marcadas, decisão escrita caso a
caso. As duas convergem: a D1 já suspeitava que falhas se aglomeram nos
cantos da curva torque×rotação e que modos se sobrepõem; a D3-03 confirma
isso com as linhas exatas (4 e 77). O que muda pra D5: nenhuma das 25
linhas extremas foi removida, então qualquer modelo treinado a partir
daqui continua vendo o canto extremo onde o risco mora — se a D5 tivesse
removido esses extremos "para limpar o dado", estaria jogando fora
justamente os casos que a D1 apontou como mais informativos para prever
falha.
