# Anotações — Laboratório 02, a descida à mão

> O critério do slide 11: as quatro perguntas respondidas por escrito, com o
> número que sustenta cada resposta. Preencha a tabela rodando o esqueleto
> com as três taxas do slide 12 e copiando a última linha de cada execução.

## A última linha de cada taxa

| Taxa | Última linha da saída (perda, w, b) |
|---|---|
| 0,001 | passo  200 perda 22462.1 w 215.016 b -17.7381 |
| 0,1 | passo  200 perda 0.752176 w 300.008 b 4.91185 |
| 1,5 | passo  200 perda inf w -3.12216e+190 b 4.826e+189 |

## As quatro perguntas do slide 11

**1. A perda está caindo a cada passo, ou oscilando?**

R: 0,001 - A perda cai mas de forma muito lenta. <br>
0,1   - A perda cai de forma mais efeitva até estabilizar <br>
1,5   - A perda aumenta rapidamente. E vai para infinito.


**2. Ela estabiliza, ou continua descendo até o fim?**

R: 0,001 - Continua descendo até o fim, visto que a taxa de aprendizagem é muito pequena. Apos 200 passos a perda ainda é alta, e com valores longe do objetivo. Uma possibilidade seria aumentar o número de passos. <br>
0,1   - Ela estabiliza a partir de 50 passos. <br>
1,5   - Aqui o passo é muito grande, a cada passo a perda aumenta e fica muito grande, tendendo ao infinito.

**3. Os pesos encontrados batem com os que geraram os dados?**

R: 0,001 - Nao (w 215.016 b -17.7381) <br>
0,1   -  Sim (w 300.008 b 4.91185)<br>
1,5   - Nao (w -3.12216e+190 b 4.826e+189)

**4. Se algo divergiu, qual foi o primeiro passo estranho?**

R: 0,001 - Nao divergiu <br>
0,1   -  Nao divergiu<br>
1,5   - Passo 2 indica algo estranho, no passo 161 estoura:

- passo    1 perda 284802
- passo    2 perda 2.14358e+07
- passo  160 perda 2.61423e+304
- passo  161 perda inf


