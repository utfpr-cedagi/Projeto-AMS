# Catálogo de ações — modelo para preencher

<!--
Este arquivo é para preencher: uma linha por ação que o SEU agente vai
poder executar. As perguntas de cada coluna estão aqui em comentário.

As quatro perguntas que decidem se uma linha está boa:
  - Ação de ESCRITA também? As que alteram o mundo são as que exigem
    cuidado — e são justamente as que mais ficam de fora.
  - COMUNICAR é ação? Avisar, escalar, transferir, pedir confirmação:
    entram com entrada, saída e risco como as outras.
  - "É reversível?" pergunta se o efeito pode ser DESFEITO sem custo
    maior que o da própria ação.
  - O risco diz risco DE QUÊ — "baixo" não é descrição; "paga duas vezes
    uma nota que já estava paga" é.

Este catálogo é, literalmente, a lista de ferramentas que você vai
implementar em D10. Cada linha vira uma função com contrato.
-->

| Ação | Entrada | Saída | É reversível? | Risco se errar |
|---|---|---|---|---|
| Consultar a leitura atual dos sensores | id da máquina | temperatura, rotação, torque, desgaste da ferramenta | Sim — só lê | Leitura desatualizada ou sensor com falha leva a classificar o risco errado |
| Consultar o histórico de falhas da máquina | id da máquina | falhas anteriores, datas, causas | Sim — só lê | Histórico incompleto subestima o risco real |
| Ler a descrição da intervenção na ordem de serviço | texto da ordem de serviço | tipo de serviço, componentes envolvidos (há instalação elétrica? trabalho em altura?) | Sim — só lê | Não detectar que há trabalho elétrico ou em altura aponta a NR errada |
| Consultar as normas regulamentares aplicáveis (NR-10/12/35) | tipo de intervenção | trechos e exigências aplicáveis | Sim — só lê | Norma errada ou desatualizada orienta um procedimento inseguro |
| Classificar o nível de risco de falha | leituras de sensores + histórico de falhas | nível (baixo/médio/alto) + justificativa | Sim — é uma classificação, pode ser revisada | Falso "baixo" deixa uma máquina de risco real operando sem bloqueio — o erro mais caro do domínio |
| Recomendar bloqueio e etiquetagem (LOTO) antes da intervenção | classificação de risco + normas aplicáveis | recomendação registrada na OS (bloquear / não bloquear) | Parcialmente — a recomendação pode ser corrigida depois, mas se o técnico já começou a intervenção sem bloqueio por confiar numa recomendação errada de "não precisa", o que acontecer nesse intervalo não se desfaz | Dispensar o bloqueio quando era necessário expõe o técnico a choque elétrico, esmagamento, etc. |
| Escalar a ordem para o supervisor de segurança | ordem de serviço + classificação + motivo (risco alto ou confiança baixa) | notificação enviada ao supervisor | Não — a notificação chegou, não se recolhe | Escalar demais gera fadiga de alarme; escalar de menos deixa um risco real sem segunda avaliação |
| Apresentar a avaliação e a recomendação ao técnico | classificação + normas aplicáveis + recomendação de LOTO | texto com justificativa apresentado ao técnico | Não — a informação errada já pode ter pautado a decisão do técnico antes de qualquer correção | Recomendação mal escrita ou mal priorizada leva o técnico a decidir errado mesmo com dados certos |

**Quem executa cada ação** (o agente sozinho? com confirmação humana? só
humano?): as quatro leituras e a classificação de risco, o agente executa
sozinho — são consulta e cálculo, sem efeito no mundo. "Recomendar LOTO" e
"escalar ao supervisor" também são disparadas pelo agente sozinho, mas são
**recomendação**, não execução: quem decide e age fisicamente continua
sendo o técnico (dominio.md, item 2).

**O que o agente JAMAIS executa sozinho:** bloquear/etiquetar fisicamente a
máquina (LOTO) ou liberar a máquina para operação. O agente recomenda; a
execução e a decisão final são sempre do técnico — é a ação irreversível de
risco alto do domínio, e fica fora do alcance dele.
