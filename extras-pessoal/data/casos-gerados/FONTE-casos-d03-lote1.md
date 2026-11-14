# FONTE — procedência de `casos-d03-lote1.csv`

**Arquivo:** `casos-d03-lote1.csv` — 30 casos novos, gerados a partir do
dataset real *AI4I 2020 Predictive Maintenance* (`data/raw/ai4i2020.csv`,
10.000 registros) pelo script pessoal
[`gerador_casos.py`](../../scripts/gerador_casos.py) — ferramenta própria,
não original do curso, por isso fora de `src/ams/`. Útil pra gerar lotes
de casos rotulados pra qualquer disciplina, mas o lote em si fica aqui, em
`extras-pessoal/data/casos-gerados/`, como material de estudo pessoal —
não é dado oficial do projeto (esses são `data/amostra/`, `data/fixtures/`).

Ainda não foi medido contra nenhum agente — ao contrário de
`casos-lab-06-v2.csv` (D02), que já tem `analise_baseline.md` com a métrica
do `baseline.py`.

## Metodologia (igual à do lab-06, generalizada em código)

Mesmas 4 categorias e os mesmos 5 gatilhos de falha documentados pela UCI
(TWF, HDF, PWF, OSF, RNF) usados em `casos-lab-06-v2.csv` — ver
[`D02/D2-06-agente-baseline/adaptacao-ams/FONTE-casos-lab-06-v2.md`](../../../D02/D2-06-agente-baseline/adaptacao-ams/FONTE-casos-lab-06-v2.md)
para a explicação completa de cada gatilho e dos limiares. A diferença é
que aqui a amostragem não foi manual: `gerar_lote()` filtra o dataset bruto
em pools por categoria/mecanismo e sorteia (com seed fixa, reprodutível).

| Categoria | Critério | Quantidade neste lote |
|---|---|---|
| Atípico | `Machine failure=1`, zero flags entre os 5 | 2 |
| Difícil | sem falha real, mas perto de um gatilho (1–2 por mecanismo) | 6 |
| Falha fácil | gatilho isolado e óbvio, um por mecanismo + 1 combinado | 6 |
| Segura | longe de qualquer limiar nas 4 dimensões | 16 |

Garantia de não-repetição: a geração excluiu explicitamente os 30 UDIs já
usados em `casos-lab-06-v2.csv` (via
`D02/D2-06-agente-baseline/adaptacao-ams/depara-casos-lab-06-v2.csv`) —
nenhum dos dois lotes compartilha um UDI de origem.

## Mapeamento de colunas

Parcialmente diferente do lab-06-v2 a partir de 2026-11-14 (ver seção
seguinte) — `temperatura_c`/`horas_desde_manutencao`/`falhou_depois` são
reais; `qualidade_produto` é real (`Type` do AI4I, L/M/H); `tipo_maquina`
é **fictícia**, sorteada (ver seção seguinte); `vibracao_mm_s` é o mesmo
proxy derivado de desvio relativo de RPM/torque, calculado sobre a
mediana **deste** lote de 30 (não a do lab-06-v2); `data` é sequência
sintética de 1 caso/dia a partir de `2026-05-01`, embaralhada entre
categorias. `idade_meses` foi removida (ver seção seguinte).

## Por que `tipo_maquina` muda de significado a partir deste lote

Ajuste feito em 2026-11-14, por orientação do professor (e-mail "Casos
para atividades D03"): em `casos-lab-06-v2.csv` (D02, já entregue e
avaliado), `tipo_maquina` é preenchida com `Type` real do AI4I (L/M/H) —
qualidade do produto, não família de máquina. Esse lote (e os seguintes,
gerados por `gerador_casos.py`) corrige isso de verdade, sem inventar
dado sem lastro: `tipo_maquina` passa a ser uma família fictícia
(TORNO/PRENSA/COMPRESSOR/ROBOT), sorteada com seed fixa — o mesmo padrão
didático que o próprio professor já usa na reserva sintética do pacote
(`D02/D2-06-agente-baseline/casos-de-reserva.csv`, ver `FONTE.md` daquela
pasta). A qualidade real do produto não se perde: passa a ter coluna
própria, `qualidade_produto`.

`idade_meses` também foi removida: era sempre `0` (nenhum campo real do
AI4I corresponde a ela, e `decidir()` nunca a lia), então preencher sem
lastro não era melhor do que não ter a coluna.

`casos-lab-06-v2.csv` (D02) **não foi alterado** — mudar o nome/conteúdo
daquela coluna quebraria `D02/D2-06-agente-baseline/esqueleto.py`
(carregado pelo `carregar_casos()` do pacote do professor, não editável)
e invalidaria a reprodutibilidade do resultado já avaliado da N2 (21/30).
Quem comparar os dois lotes deve saber: em `casos-lab-06-v2.csv`,
`tipo_maquina` = qualidade do produto; aqui em diante, `tipo_maquina` =
família fictícia e `qualidade_produto` = qualidade real.

## De-para (obrigatório, gerado junto)

`depara-casos-d03-lote1.csv` — uma linha por `id_caso`, com o UDI de
origem em `data/raw/ai4i2020.csv`, `product_id`, `categoria`, `mecanismo`,
`risco` e `dificuldade`. Gerado automaticamente por `gerar_lote()` — todo
lote novo feito com `gerador_casos.py` grava este arquivo junto, nunca só
o CSV de casos (sem ele, o rastro até o dataset bruto se perde, como
aconteceu com `casos-lab-06-v2.csv` — ver nota na FONTE daquele lote).

## Como reproduzir / gerar o próximo lote

```powershell
.venv\Scripts\python.exe extras-pessoal\scripts\gerador_casos.py `
  --saida-casos extras-pessoal\data\casos-gerados\casos-d03-lote1.csv `
  --saida-depara extras-pessoal\data\casos-gerados\depara-casos-d03-lote1.csv `
  --excluir-depara D02\D2-06-agente-baseline\adaptacao-ams\depara-casos-lab-06-v2.csv `
  --prefixo B --data-inicio 2026-05-01 --seed 42
```

Pra um próximo lote (ex.: D04), passe também `--excluir-depara
extras-pessoal\data\casos-gerados\depara-casos-d03-lote1.csv` além do
de-para do lab-06, pra nunca reusar UDI de nenhum lote anterior.

## Licença e reúso

Mesma licença do dataset original: CC BY 4.0 (AI4I 2020 Predictive
Maintenance Dataset, UCI Machine Learning Repository, ID 601). Ver
`data/FONTE.md` pra citação completa.
