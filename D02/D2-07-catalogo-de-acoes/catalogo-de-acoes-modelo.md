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
| [nome com verbo no infinitivo] | [o que a ação recebe] | [o que ela devolve] | [sim / não / parcialmente — e por quê] | [o que acontece se a ação errar, e para quem] |
| [ex.: consultar o registro da máquina] | [identificador da máquina] | [última manutenção, pendências, leituras] | [sim — só lê] | [falso negativo adia a causa certa; custo de tempo] |
| [ ... ] | | | | |
| [ ... ] | | | | |

**Quem executa cada ação** (o agente sozinho? com confirmação humana? só
humano?): [responda aqui — esta coluna mental vira política em D12]

**O que o agente JAMAIS executa sozinho:** [responda aqui — a ação
irreversível de risco alto que fica fora do alcance dele]
