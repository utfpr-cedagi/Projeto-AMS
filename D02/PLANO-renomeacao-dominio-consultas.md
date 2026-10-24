# Plano pendente: re-rotular `consultas_ams.py` para o domínio de manutenção

> **Nota:** este arquivo é uma anotação de trabalho (não é entregável do
> curso) — registra um plano já aprovado, ainda não executado, pra não se
> perder se a conversa com o Claude for interrompida. Pode apagar depois
> de aplicado (ou antes de enviar qualquer coisa pro professor).
>
> **Ponto de restauração:** commit `71c7d99` ("D02 labs 03-06: catálogo de
> busca corrigido, baseline do agente e restrições do PEAS"), na branch
> `feature/D02_E04` — é o estado antes desta renomeação.

## Contexto

`consultas_ams.py` (usado nos labs 03, 04 e 05) descreve um cenário de
**planejamento de produção/estoque** ("peças vendidas", "insumos em
estoque", "prazo do fornecedor"), enquanto o resto do `agent-spec.md`
(PEAS, dimensões, medida de desempenho, restrições) é sobre **diagnóstico
de falha e manutenção segura**. O demo do professor (`encenar.py`,
`demo-02-agente-dissecado`) reforça que o formato natural de "Consultas"
pro domínio de manutenção é consultar histórico de intervenções, leituras
de sensores e pendências — não dados de produção.

Com a entrega de D02 ainda em aberto, a decisão foi pela opção de menor
custo e risco: **re-rotular os nomes dos fatos e fontes para o vocabulário
de manutenção, mantendo EXATAMENTE as mesmas latências e a mesma
estrutura de cobertura** (qual fonte fornece quais fatos). Como a busca só
enxerga números e cardinalidade de conjuntos — não o texto em si — os
resultados já medidos e escritos nos labs 04 e 05 (tabela de 8 linhas,
parágrafo da dominância) **continuam válidos sem precisar re-rodar nada**.
Só muda o vocabulário.

Alternativas consideradas e descartadas: (A) só anotar a escolha de
domínio sem mexer no código — rejeitada por não resolver a inconsistência
de fato; (C) reformular os fatos/fontes de verdade, com latências novas e
re-rodando todas as buscas — rejeitada por exigir re-rodar e reescrever
os labs 04/05 já medidos, por um ganho que é só de leitura, não de
aprendizado ou nota.

## O mapa de renomeação

### Instância PEQUENA

| Antigo (produção) | Novo (manutenção) |
|---|---|
| "qtde de maquinas totais" | "histórico de falhas da máquina" |
| "qtde de maquinas em manutenção" | "normas regulamentares aplicáveis (NR)" |
| "qtde de maquinas disponíveis" | "leitura atual dos sensores" |
| "maquinas com manutenção programada" | "manutenção preventiva programada" |

| Fonte (antiga) | Fonte (nova) | Latência | Fatos fornecidos (iguais, só o texto muda) |
|---|---|---|---|
| Depto Producao — Qtde Máquinas | painel de sensores — leitura atual | 1.2 | leitura atual |
| Depto Manutenção | sistema de manutenção — status | 2.0 | NR aplicáveis + preventiva programada |
| Depto Compras | histórico de falhas (sistema) | 6.0 | histórico de falhas |
| relatório semanal da produção | relatório semanal de manutenção | 4.5 | histórico de falhas + leitura atual |
| Depto Administrativo | auditoria completa de manutenção | 15.0 | todos os 4 |

Pergunta nova (era "quantas máquinas disponíveis, considerando manutenção
programada?"): **"a máquina X pode ser liberada hoje, sem risco?"**

### Instância MAIOR

| Antigo (produção) | Novo (manutenção) |
|---|---|
| "qtde de pecas vendidas no período" | "histórico de intervenções anteriores" |
| "qtde de pecas produzidas por maquina" | "leitura atual de vibração" |
| "qtde de pecas produzidas por dia" | "leitura atual de temperatura do mancal" |
| "qtde de dias até o final do período" | "tempo decorrido desde a última manutenção" |
| "qtde total de pecas esperadas no período" | "tendência das últimas leituras de vibração" |
| "qtde de maquinas disponíveis para produção" | "pendências abertas na ordem de serviço" |
| "qtde de insumos em estoque" | "disponibilidade de peça de reposição" |
| "prazo de entrega do fornecedor de insumos" | "prazo de entrega da peça de reposição" |

| Fonte (antiga) | Fonte (nova) | Latência | Fatos (mesma cobertura de antes) |
|---|---|---|---|
| ERP — pedidos do período | sistema de manutenção — histórico de intervenções | 0.9 | histórico de intervenções |
| painel de capacidade da fábrica | sensor de vibração — leitura atual | 1.1 | vibração atual |
| apontamento de produção diário | sensor de temperatura — leitura atual | 1.3 | temperatura atual |
| calendário de produção | registro de manutenção — última intervenção | 0.7 | tempo desde última manutenção |
| sistema de manutenção — máquinas disponíveis | ordem de serviço — pendências abertas | 1.0 | pendências abertas |
| WMS — estoque de insumos | almoxarifado — peças de reposição | 1.2 | disponibilidade de peça |
| portal do fornecedor | portal do fornecedor de peças | 3.5 | prazo de entrega da peça |
| robô de email do PCP | robô de email da manutenção | 2.8 | disponibilidade + prazo da peça |
| planejamento de vendas e operações (S&OP) | sistema de manutenção — histórico completo | 4.0 | histórico de intervenções + tendência de vibração |
| relatório de capacidade instalada | relatório de condição da máquina | 5.0 | vibração atual + pendências abertas |
| painel do PCP | painel de monitoramento preditivo | 6.5 | temperatura + tempo desde manutenção + tendência |
| ERP — módulo de planejamento completo | sistema de manutenção — módulo completo | 9.0 | histórico + tendência + tempo desde manutenção |
| reunião com gestor de produção | reunião com o técnico responsável | 14.0 | vibração + temperatura + pendências + peça + prazo |
| consultoria externa de capacidade | consultoria externa de engenharia de manutenção | 22.0 | todos os 8 |

Pergunta nova (era "a produção programada poderá ser atendida neste
período?"): **"a máquina L14720 pode ser liberada para operação,
inspecionada antes, ou precisa parar para manutenção?"** — o mesmo tipo de
pergunta do demo do professor.

Os comentários internos que citam nomes antigos (ex.: "a consultoria
externa de capacidade" no docstring de `heuristica_inadmissivel`) também
são atualizados para os novos nomes.

## Arquivos a editar (aplicar a MESMA renomeação nos quatro lugares)

1. `D02/D2-03-formular-como-busca/comum/problemas/consultas_ams.py`
2. `D02/D2-04-busca-nao-informada/comum/problemas/consultas_ams.py`
3. `D02/D2-05-busca-informada/comum/problemas/consultas_ams.py`
4. `agent-spec.md` §7 — o bloco de código colado e a prosa da "pergunta"
   acima dele (o texto hoje já está desatualizado em relação ao arquivo
   real — será sincronizado com a versão renomeada)

Cada arquivo ganha um comentário curto no topo (mapa de tradução
compacto, não a versão inteira duplicada) pra comparar rápido sem precisar
abrir o `git diff`:

```python
# Nomes de fatos/fontes trocados do domínio de produção/estoque pro de
# manutenção segura (latências e estrutura de cobertura IDÊNTICAS às
# anteriores — só o vocabulário muda, os números das buscas não mudam).
# Mapa completo em D02/PLANO-renomeacao-dominio-consultas.md.
```

## O que NÃO vai ser tocado

- Latências (`1.2`, `6.0`, etc.) e a estrutura de `fornece` (quais fatos
  cada fonte entrega) — exatamente as mesmas, só renomeadas.
- `D02/D2-04-busca-nao-informada/tabela_resultado_01.md` e
  `D02/D2-05-busca-informada/tabela_resultado_01.md` — os números
  continuam válidos; não referenciam nomes de fato/fonte específicos.
- O bloco "Resultado - Saída" do `agent-spec.md` §7 (a saída do
  `verificar-formulacao.py`) — é uma pendência SEPARADA e já conhecida
  (mostra o catálogo do professor rodando, não `consultas_ams.py`); fica
  de fora deste plano.
- `comum/busca.py`, os três arquivos de catálogo do professor
  (`diagnostico.py`, `consultas.py`, `conformidade.py`) — fechados, como
  sempre.
- Nenhuma ação de git (além do commit de checkpoint já feito).

## Verificação (depois de aplicar)

- Rodar, em cada uma das três pastas (D2-03, D2-04, D2-05):
  `PYTHONIOENCODING=utf-8 python verificar-formulacao.py comum/problemas/consultas_ams.py:PEQUENA comum/problemas/consultas_ams.py:MAIOR`
  — esperar 6 ✅ / 0 ⚠️ / 0 ❌ nas duas instâncias, igual a antes.
- Rodar `python esqueleto.py` em D2-04 e D2-05 e comparar a tabela
  impressa com os valores já escritos em `tabela_resultado_01.md` — devem
  bater exatamente (mesmo custo, ações, nós expandidos/gerados).
- Rodar `pytest teste.py -q` em D2-05 — deve continuar 6/6 verde.
