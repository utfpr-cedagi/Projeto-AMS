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

R: Manter os 4, caso a caso. A08 (9,2 mm/s; inspecionar, difícil) e B04 (9,7; inspecionar, difícil) são casos em que vibração alta sozinha não justificava parar. Estão no conjunto justamente para testar se o agente distingue sinal isolado de risco confirmado. A14 (11,3; parar, falhou) e B11 (9,7; parar, falhou) são falhas reais. Nenhum é erro de digitação: `vibracao_mm_s` é um proxy calculado pela mesma fórmula sobre RPM e torque reais do AI4I (`NOTA-vibracao-mm-s.md` da D2). O extremo reflete RPM e torque longe da mediana, coerente com a curva de potência vista na D1. Se fossem removidos: n cairia para 56, a média de vibração de 3,84 para 3,40, a mediana de 3,40 para 3,35, e a classe parar perderia 2 dos seus 16 casos. A comparação A×B perderia justamente os casos que mais distinguem as variantes.


## Faltantes (os três mecanismos do slide 26)

Nenhuma variável tem valores faltantes.

## As quatro perguntas do slide 29

**1. Média e mediana se separam em alguma variável? Em qual?**

R: Sim, em `vibracao_mm_s`: média 3,84 contra mediana 3,40, uma diferença de 0,44 mm/s (cerca de 13% da mediana; assimetria ≈ 2,3), puxada pelos 4 extremos. Sem eles, a média fica em 3,40 e a mediana em 3,35. Nas outras numéricas as duas ficam próximas: `temperatura_c` 36,70 × 36,85 e `horas_desde_manutencao` 110,2 × 100,0 (10 h de diferença numa AIQ de 118,5, sem extremos). Em `falhou_depois`, a média 0,27 é a proporção de falhas (16/60), e a mediana 0 só diz que a maioria não falhou.

**2. Quantos extremos foram marcados, e quantos você decidiu manter?**

R: 4 extremos marcados, todos em `vibracao_mm_s`: linhas 8, 14, 34 e 41, que são os casos A08, A14, B04 e B11. Mantive os 4. Diferente do Lab 03, aqui `falhou_depois` não gera extremos. Com 16/60 = 27% de falhas, Q3 = 1 e a caixa cobre o 0 e o 1. Na amostra do Lab 03 a falha era rara (4%), então todo 1 caía fora da caixa por construção da regra.

**3. Algum faltante parece do terceiro mecanismo?**

R: Não. Há 0 faltantes nas 11 colunas, porque o conjunto foi montado a partir de linhas completas do AI4I, que não tem faltantes: os 30 casos da D2 adaptados e os 30 do gerador. Numa operação real, o candidato ao terceiro mecanismo (perdido por causa do próprio valor) seria uma leitura de sensor não registrada justamente porque a máquina estava parada ou com defeito. Isso proibiria descartar as linhas incompletas. A descrição textual da OS, que a §2 do `agent-spec.md` lista entre as entradas do agente, não existe no conjunto de avaliação. É uma lacuna por desenho do conjunto, não uma célula faltante.

**4. O que a análise da D1 não tinha visto?**

R: Três coisas. (1) O balanceamento do conjunto de avaliação. A D1 olhou a base inteira, com cerca de 3,4% de falhas. Aqui os casos foram escolhidos: a classe parar tem 16/60 (27%) e seguir tem 32/60 (53%). Um agente que sempre mandasse seguir acertaria 53%. A D1 não precisava considerar esse piso, e ele relativiza os 58% da linha de base. (2) `falhou_depois` coincide 100% com `acao_correta` = parar: vale 1 em 16 de 16 casos e 0 em todos os outros. O rótulo foi derivado do desfecho, então `falhou_depois` não pode ser entrada do agente; só realimenta o `EstadoDaFrota` depois da decisão. (3) Os extremos agora aparecem numa variável derivada (`vibracao_mm_s`, proxy de RPM e torque), não nas medidas brutas. A D1 viu os extremos de rotação; aqui eles reaparecem transformados, e metade deles (2 de 4) são casos difíceis rotulados inspecionar, não falhas.

## Comparação com a análise exploratória da D1

O que mudou de lá para cá — o que a análise de lá não tinha visto,
e o que estas decisões escritas mudam no conjunto que a D5 vai usar:

R: O conjunto que importa para avaliar o agente não é a base da D1 (10.000 linhas), e sim estes 60 casos escolhidos, com outra estrutura: classes desbalanceadas a favor de seguir (53%), falhas super-representadas (27%, contra cerca de 3,4% na base) e 16 casos difíceis ou atípicos de propósito. Isso muda duas coisas daqui em diante. O acerto geral (métrica primária) precisa vir sempre acompanhado do recall da classe alto e do piso trivial de 53%. E qualquer comparação entre variantes precisa usar estes mesmos 60 casos, pareados. As decisões escritas aqui não alteram o conjunto: nenhuma remoção e nenhuma imputação. O `acertos.csv` e o notebook usam os 60 casos exatamente como estão em `dados/casos-60.csv`.
