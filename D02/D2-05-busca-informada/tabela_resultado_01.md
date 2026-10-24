# Laboratório 04 e 05 - as seis buscas, medidas

Esta tabela parte da tabela do lab-04 (cópia em
`D02/D2-04-busca-nao-informada/tabela_resultado_01.md`, mantida como estava)
e acrescenta as quatro linhas informadas do lab-05 — mesma formulação.

#### 1. Preencha a tabela na entrega: custo, ações, expandidos, gerados, segundos — a saída já sai emMarkdown, pronta para colar.

**Formulação: problemas.consultas_ams:MAIOR**

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

#### 2. Responda: alguma busca achou caminho mais barato que a largura? A resposta depende do seusubproblema — em alguns é sim (custo uniforme vence), em outros não (os custos são parecidos), e as duas respostas rendem análise.
*R: Sim a busca **custo_uniforme**, apresentou um caminho mais barato, porém com mais ações.*

* ***profundidade_limitada**, também se mostrou ser uma possibilidade viável apesar de ter um custo um pouco maior que o **custo_uniforme**, mas ainda assim muiot menor que a busca **largura.***

* ***custo_uniforme**, teve um custo baixo, porém foi a que mais demorou em segundos, talvez por conta da quantidade de 'Nós expandidos' e 'Nós gerados'.*

#### 3. (Lab-05) Escreva o parágrafo da dominância: qual heurística domina a outra, e por quê.
*R: Pela propriedade de dominância (slide 31), entre duas heurísticas admissíveis domina a que
estima mais alto em todo estado, porque estimar mais alto poda mais nós sem comprometer a
otimalidade. Neste subproblema só existe uma heurística admissível — a latência da fonte mais
barata que ainda falta — e ela expande 1558 nós para achar o caminho ótimo de custo 10.9 em 6
ações, o mesmo custo do `custo_uniforme`. A inadmissível (quantidade de fatos que faltam vezes a
pior latência) expande só 2 nós, mas devolve custo 22.0 — quase o dobro do ótimo — porque
superestima e empurra o A* direto para a fonte única cara (a "consultoria externa de capacidade"),
exatamente como o comentário da função no catálogo prevê. A comparação que sobra aqui não é entre
duas admissíveis, e sim o contraste do slide 33: a inadmissível é rápida porque está errada, a
admissível é mais lenta porque preserva a garantia de otimalidade do A*.*

