# O mapa do meu domínio — conferência (Laboratório 04)

Conjunto: manutencao · 384 dimensões antes da redução
Escolha registrada (slide 55): normalizado · semente da vizinhança: 20260901
Mapas: mapa-do-espaco.png (componentes principais à esquerda, vizinhança à direita) · pontos: mapa-pontos.csv

## Passo 4 — os três pares que você escolheu no mapa (slide 52)

| par | cosseno original | a vizinhança visual |
|---|---|---|
| (123, 41) | +0.1846 | NÃO confirma |
| (35, 36) | +0.9780 | confirma |
| (105, 167) | +0.5892 | confirma |

## As quatro perguntas do slide 53

1. Os dois métodos produzem os mesmos agrupamentos? <br>
R: Não, sao agrupamentos diferentes

2. Há grupo que só aparece em um deles? <br>
R: Sim por exemplo o 123,41

3. Os vizinhos visuais confirmam no cosseno original? <br>
R: Dois deles sim: (35,36) e (105, 167).

4. O que aconteceria com um vetor novo, fora do conjunto? <br>
R: No PCA como é deterministica, ela simplismente adiciona o ponto novo e os demais permanecem no mesmo lugar. No t-SNE, não ha aplicacao para o novo ponto, e portanto precisa recriar o mapa inteiro novo.

## O caso em que o mapa enganou (critério do slide 52)

Par e o que a figura sugeria, e o que o cosseno original disse:

R: caso (123,41) a figura mostrava os pontos proximos, mas o coseno resultou em 0.1846
