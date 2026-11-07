# FONTE — procedência de `casos-lab-06-v2.csv`

**Arquivo:** `casos-lab-06-v2.csv` — 30 casos curados a partir do dataset
real *AI4I 2020 Predictive Maintenance* (`data/raw/ai4i2020.csv`, 10.000
registros), por orientação do professor, no lugar da reserva sintética do
pacote. Substitui a primeira tentativa (`casos-lab-06.csv`), que foi tirada
em sequência do começo do dataset e não tinha diversidade de dificuldade.

## Os quatro gatilhos de falha documentados pela UCI

Texto oficial da página do dataset
(archive.ics.uci.edu/dataset/601/ai4i+2020+predictive+maintenance+dataset),
usado pra escolher e classificar as 30 linhas:

- **TWF** (tool wear failure): a ferramenta é trocada ou falha num
  instante sorteado entre 200–240 min de desgaste acumulado (120 vezes no
  dataset; falha de fato em 43 dessas vezes — as outras 77 são "trocada a
  tempo", ou seja, seguras apesar do desgaste alto).
- **HDF** (heat dissipation failure): falha se
  `temp. processo − temp. ar < 8,6 K` **e** `rotação < 1380 rpm`.
- **PWF** (power failure): falha se a potência do processo
  (`torque × rotação, em rad/s`) sai do intervalo `[3500, 9000] W`.
- **OSF** (overstrain failure): falha se `desgaste × torque` passa de
  `11.000` min·Nm (produto L) / `12.000` (M) / `13.000` (H).
- **RNF** (random failure): 0,1% de chance de falha, independente de
  qualquer leitura.

Se pelo menos um desses mecanismos dispara, `Machine failure = 1` — mas
**9 registros no dataset inteiro** têm `Machine failure = 1` sem NENHUM
dos cinco mecanismos marcado: falhas sem explicação visível em nenhuma das
regras documentadas. É o achado mais forte pra "caso atípico" real.

## Como as 30 linhas foram escolhidas (por categoria)

| Categoria | Critério | UDIs |
|---|---|---|
| Atípico (2) | `Machine failure=1`, zero flags entre as 5, leituras comuns | 1438, 2750 |
| Difícil (6) | sem falha real, mas perto de um gatilho (1–2 por mecanismo) | 593 (TWF), 1210 e 1401 (PWF, os dois lados), 160 e 332 (OSF), 131 (HDF) |
| Falha fácil (6) | gatilho isolado e óbvio, um por mecanismo + 1 combinado | 1088 (TWF), 4079 (HDF), 51 e 604 (PWF, os dois lados), 747 (OSF), 3612 (TWF+RNF) |
| Segura/fácil (16) | longe de qualquer limiar nas 4 dimensões, espalhada por tipo (14 L / 7 M / 9 H, proporção parecida com a real do dataset: L 50%/M 30%/H 20%) e por faixa de desgaste | ver `casos-lab-06-v2.csv`, coluna `risco=baixo` |

## Mapeamento de colunas (AI4I2020 → estrutura do lab-06)

| Coluna de destino | Origem | Natureza |
|---|---|---|
| `id_caso` | gerado: `A01`..`A30` | gerado |
| `data` | sequência sintética, 1 caso/dia a partir de `2026-04-01` | **sintética** — o AI4I2020 não tem timestamp real; a data só existe pra `EstadoDaFrota` do `esqueleto.py` ter uma ordem cronológica pra acumular estado |
| `tipo_maquina` | `Type` (L/M/H) | real — reinterpretado de "variante de qualidade do produto" pra "tipo de máquina", já que o AMS não tem uma família de máquina equivalente no dataset |
| `idade_meses` | não existe no AI4I2020 | **placeholder fixo `0`** — `decidir()` não usa este campo hoje; marcado como "não disponível no dataset real" em vez de inventar um valor plausível |
| `temperatura_c` | `Process temperature [K] - 273.15` | real, convertida de Kelvin pra Celsius |
| `vibracao_mm_s` | **derivada**: `2,0 + 10·(0,5·desvio_relativo_RPM + 0,5·desvio_relativo_Torque)` em relação à mediana das 30 linhas | **proxy calculado** — o AI4I2020 não mede vibração; isto NÃO é um sensor real |
| `horas_desde_manutencao` | `Tool wear [min]`, usado diretamente | real — minutos de desgaste da ferramenta desde a última troca é um análogo direto de "horas desde manutenção" |
| `acao_correta` | derivada do `risco`: alto → `parar_para_manutencao`; médio → `inspecionar_antes_de_operar`; baixo → `seguir_operando` | derivada de dado real + regra física |
| `falhou_depois` | `Machine failure` (0/1) | real, direto |
| `risco` *(coluna nova)* | ver tabela de categorias acima | derivada dos 4 gatilhos reais |
| `dificuldade` *(coluna nova)* | ver tabela de categorias acima | derivada dos 4 gatilhos reais |

## Recalibração de `esqueleto.py`: concluída

Os limiares originais do pacote (`LIMITE_TEMPERATURA = 78.0` e
`LIMITE_VIBRACAO = 7.0`) foram calibrados pra escala da reserva sintética —
fora de escala pra este arquivo, onde `temperatura_c` fica toda entre
33–38°C (nunca perto de 78). `LIMITE_TEMPERATURA` foi removida e
substituída por `LIMITE_DESGASTE = 150.0` sobre `horas_desde_manutencao`
(o gatilho real de TWF, que começa a sortear falha a partir de 200 min de
desgaste acumulado). `LIMITE_VIBRACAO = 7.0` foi mantido, porque a faixa
do proxy derivado já cai nessa escala por construção. Justificativa
completa e números da medição em `RESUMO-LAB06.md` §5.

## De-para (reconstruído)

Este lote foi montado por amostragem manual (ver tabela de UDIs acima),
sem gravar um de-para linha-a-linha na época. O arquivo
`depara-casos-lab-06-v2.csv` (uma linha por `id_caso`, com UDI, `product_id`,
categoria e mecanismo) foi reconstruído depois, por casamento de colunas
contra `data/raw/ai4i2020.csv` (`tipo_maquina`, `temperatura_c`,
`horas_desde_manutencao`, `falhou_depois`) — os 9 casos "difíceis"/"atípicos"
batem direto com os UDIs já documentados acima; os 21 restantes exigiram
desambiguação por busca combinatória sobre a fórmula de `vibracao_mm_s`
(ela depende da mediana de RPM/torque das 30 linhas, então o UDI certo é o
único que reproduz exatamente os valores gravados no CSV — erro 0,0 em
todas as 30 linhas, o que confirma a reconstrução). Lotes gerados depois
deste (ver `data/casos-gerados/`) usam `ams.gerador_casos`, que grava o
de-para automaticamente — essa reconstrução manual não deve ser necessária
de novo.

## Licença e reúso

Mesma licença do dataset original: CC BY 4.0 (AI4I 2020 Predictive
Maintenance Dataset, UCI Machine Learning Repository, ID 601). Ver
`data/FONTE.md` pra citação completa.
