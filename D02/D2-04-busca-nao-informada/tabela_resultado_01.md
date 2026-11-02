# Laboratório 04 - as quatro buscas, medidas

#### 1. Preencha a tabela na entrega: custo, ações, expandidos, gerados, segundos — a saída já sai emMarkdown, pronta para colar.

**Formulação: problemas.consultas_ams:MAIOR**

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 22.0 | 1 | 15 | 196 | 2 | 0.0003 |
| custo_uniforme | 10.9 | 6 | 1780 | 2814 | 7 | 0.005 |
| profundidade_limitada(limite=32) | 13.7 | 8 | 9 | 37 | 8 | 0.0001 |
| aprofundamento_iterativo(limite=32) | 22.0 | 1 | 16 | 14 | 1 | 0.0001 |

#### 2. Responda: alguma busca achou caminho mais barato que a largura? A resposta depende do seu subproblema — em alguns é sim (custo uniforme vence), em outros não (os custos são parecidos), e as duas respostas rendem análise.
*R: Sim a busca **custo_uniforme**, apresentou um caminho mais barato, porém com mais ações. Além disso tem uma quantidade muito grande de nós expandidos e gerados, quando se compara com os outros tipos de buscas.*

* ***profundidade_limitada**, também se mostrou ser uma possibilidade viável apesar de ter um custo um pouco maior que o **custo_uniforme**, mas ainda assim muiot menor que a busca **largura.***

* ***custo_uniforme**, teve um custo baixo, porém foi a que mais demorou em segundos, talvez por conta da quantidade de 'Nós expandidos' e 'Nós gerados'.*



