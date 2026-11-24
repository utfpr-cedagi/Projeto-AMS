# Pares que surpreenderam — Laboratório 01

> O slide 19 do D3-E1 pede DOIS casos anotados: um par PRÓXIMO sem razão
> aparente e um par DISTANTE que deveria estar junto. Eles voltam na D7,
> quando a turma montar o próprio índice de recuperação — escreva aqui e
> guarde este arquivo no seu repositório.

## Um par PRÓXIMO sem razão aparente

- Índices do par: (30, 31)
- As duas frases:
  - primeira: "Abra a válvula de alívio antes de iniciar o teste hidrostático do vaso."
  - segunda: "Feche a válvula de alívio antes de iniciar o teste hidrostático do vaso."
- Cosseno medido: 0,9426 (euclidiana 0,3389, com `NORMALIZAR = True`)
- Por que essa proximidade surpreendeu: é o 2º par mais próximo de todo o conjunto, mas as duas frases mandam fazer exatamente o oposto uma da outra — abrir e fechar a mesma válvula, no mesmo procedimento.

R: A mudança de uma única palavra ("Abra"/"Feche") inverte o sentido da instrução, mas a estrutura quase idêntica confunde o vetor. O perigo real é o modelo usar a semelhança textual como atalho e julgar ações contrárias como equivalentes. Isso pode induzir a erros graves, como abrir uma válvula de alívio quando o correto seria fechar.

## Um par DISTANTE que deveria estar junto

- Índices do par: (15, 16)
- As duas frases:
  - primeira: "A pista externa do rolamento do ventilador apresenta pitting avançado."
  - segunda: "A superfície do anel giratório do ventilador está coberta de pequenos buracos de desgaste."
- Cosseno medido: 0,4529 (euclidiana 1,0460, com `NORMALIZAR = True`)
- Por que essa distância surpreendeu: as duas frases descrevem o mesmo defeito, na mesma peça — uma com o jargão técnico, a outra com palavras comuns.

R: "pista externa do rolamento" e "anel giratório" são a mesma peça, e "pitting avançado" é literalmente "coberto de pequenos buracos de desgaste" — mas as duas frases quase não compartilham palavra nenhuma. Um técnico que descreve o defeito com palavras do dia a dia pode não recuperar a instrução ou o histórico escritos em jargão técnico, mesmo tratando exatamente do mesmo problema.

## O que a comparação com NORMALIZAR = True mudou

- Alguma ordem mudou? De qual par: não. A ordem dos pares por cosseno é idêntica nas duas rodadas, e os valores de cosseno também não mudam. O que muda são só os valores de distância euclidiana — o par (30, 31), por exemplo, vai de 0,3389 (normalizado) para 1,3691 (sem normalizar).

R: O cosseno já divide pelo produto das normas dos dois vetores, então ele ignora o comprimento de cada vetor por definição — normalizar ou não dá exatamente o mesmo resultado. 

