# Relatório de desempenho da linha de base — modelo

<!--
Item 3 da N2. Este relatório tem as quatro informações que o slide 28 do
E4 cobra, mais a leitura de onde erra (slide 30) — a saída do medir.py já
traz quase tudo pronto: rode `python medir.py` na pasta do D2-06 (ou do
seu projeto) e cole no lugar marcado. Responda NOS COLCHETES, apagando
nada das seções.
-->

**Projeto:** [nome do seu projeto] · **Data:** [data da medição]

## 1. A métrica primária

[Nome da métrica do seu PEAS, com a fórmula ou o procedimento de cálculo —
como se calcula, sem ambiguidade. Ex.: acerto da decisão — casos com
decisão igual à rotulada, sobre o total.]

## 2. O valor

[A saída do `medir.py`, colada: valor, acertos/total. Ex.: 25/30 = 0.8333.]

## 3. O conjunto

[Sobre quais casos: o arquivo, quantos são, de que período, como se
distribuem pelos rótulos. Se usou o conjunto de reserva do `D2-06`,
declare aqui — sem demérito; a exigência é a declaração.]

## 4. Onde o agente erra

[A lista de erros que o `medir.py` imprime, colada. Depois, dois
parágrafos: o PADRÃO dos erros (todos do mesmo tipo? concentrados em
quais casos?) e a HIPÓTESE do porquê — o que o agente não enxerga quando
erra. Isto é a matéria-prima da análise do item 5.]

## 5. A tabela comparativa de busca (item 4 da N2)

[Cole aqui a tabela completa dos laboratórios 04 e 05 — as 4 linhas não
informadas e as 4 informadas. Exemplo da forma (os números são os SEUS):]

| Busca | Custo | Ações | Nós expandidos | Nós gerados | Prof. máx. | Segundos |
|---|---:|---:|---:|---:|---:|---:|
| largura | 20.0 | 5 | 2786 | 6744 | 5 | 0.0084 |
| custo_uniforme | 20.0 | 5 | 550 | 1954 | 6 | 0.0027 |
| profundidade_limitada(limite=32) | 20.0 | 5 | 6 | 5 | 5 | 0.0001 |
| aprofundamento_iterativo(limite=32) | 20.0 | 5 | 1192 | 3749 | 5 | 0.0057 |
| gulosa[admissivel] | 20.0 | 5 | 6 | 50 | 5 | 0.0001 |
| a_estrela[admissivel] | 20.0 | 5 | 77 | 297 | 5 | 0.0008 |
| gulosa[inadmissivel] | 83.0 | 11 | 12 | 77 | 11 | 0.0002 |
| a_estrela[inadmissivel] | 77.0 | 10 | 11 | 75 | 10 | 0.0002 |

[A pergunta do item 4: o A estrela com a heurística admissível manteve o
custo ótimo e expandiu menos que o custo uniforme? Quanto economizou, e o
que isso diz do seu espaço de estados? Registre também a ressalva de
contagem da profundidade limitada — reconhecer o limite da própria
medição vale nota.]
