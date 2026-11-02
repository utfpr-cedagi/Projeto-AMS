# Análise — o que a N2 ensina sobre o problema do AMS

## O que torna o problema difícil

A **observabilidade parcial** (`agent-spec.md` §2) não é rótulo aqui: a
linha de base errou os casos A07 e A09 (`relatorio-de-desempenho.md` §4)
porque a máquina falhou de verdade sem que desgaste nem vibração
estivessem altos na leitura do instante — a informação que decidiria não
está na percepção do momento, só apareceria num padrão ao longo do tempo
que a regra reativa não guarda.

O **determinismo estocástico** (§2) soma a isso: a mesma combinação de
leituras pode ou não anteceder falha, então qualquer limiar fixo erra
sistematicamente para um dos dois lados. Nesta linha de base, errou para o
lado de ser exigente demais — 5 dos 9 erros (A02, A08, A13, A17, A23)
mandam parar quando bastava inspecionar, porque a regra só tem "passou do
limite" ou "não passou", sem meio-termo.

O terceiro fator é o **custo desigual de reunir evidência**, que a
formulação por busca (§7) deixa visível em números: as 14 fontes da
formulação MAIOR vão de 0,7 a 22,0 de latência. A tabela comparativa
(`relatorio-de-desempenho.md` §5) mostra o preço de ignorar isso — a
heurística inadmissível expande só 2 nós mas erra o custo em quase o
dobro (22,0 contra o ótimo 10,9), porque empurra a busca direto pra fonte
única cara sem medir o que realmente falta.

## Que tipo de agente o problema realmente exige

A observabilidade parcial já elimina o reativo simples — por isso mantive
a condição com estado interno (`EstadoDaFrota`) no `baseline.py`, em vez
de apagá-la, decisão que `analise_baseline.md` já registrava.

Mas "baseado em modelo" (guardar estado) não é suficiente, e é esse o
ajuste que fiz em `agent-spec.md` §3 nesta rodada: a medida de desempenho
(§4) trata os erros de forma **assimétrica** — um falso "baixo" (máquina
de risco alto liberada) tem limite próprio de 5%, bem mais apertado que o
recall geral de 80%. Decidir qual ação minimiza o custo esperado, sabendo
que errar para um lado é mais caro que errar para o outro, é exatamente o
que um **agente baseado em utilidade** faz e um agente baseado em modelo
(sem função de utilidade) não — ele só teria "bateu o limiar, sim ou não".

Isso também explica por que a busca informada (A*) é a peça que falta na
linha de base: ela decide quando vale a pena consultar mais uma fonte
barata e quando a fonte cara única já compensa — o mesmo tipo de troca
que a função de utilidade do agente final vai fazer entre inspecionar
(custo baixo, risco de deixar passar) e parar (custo alto, risco de parar
à toa).

## O que isto muda no projeto

A D10 precisa de um classificador que pondere os dois tipos de erro de
forma diferente (a linha de base trata todo erro igual, por isso erra
21/30 com viés pro lado conservador). Precisa também de um sinal de
histórico — não só a leitura do instante — para pegar casos como A07 e
A09. A estratégia de busca por custo de fontes (§7), por outro lado, é
onde a linha de base já é competitiva por padrão: o ganho real está em
decidir **quais** fontes consultar e quando parar de buscar, não em
consultar mais.
