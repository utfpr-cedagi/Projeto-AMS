# Laboratório 06 — resumo e explicação detalhada do que foi feito

Este documento reúne, em ordem, tudo que foi feito neste laboratório: da
primeira tentativa de amostragem (descartada) até o agente de linha de
base copiado para o projeto. Os arquivos finais estão listados no fim.

---

## 1. Contexto e objetivo do laboratório

O Laboratório 06 pede o primeiro agente de regras do projeto AMS, **sem
modelo de linguagem**: percepção (uma leitura de sensor) → decisão
(regras explícitas com limiares) → ação (recomendação) → medida (a
métrica primária do PEAS, sobre 30 casos rotulados). O número que sai
daqui é a **linha de base** contra a qual o agente baseado em LLM (D10)
vai ser comparado — sem ela, "melhorou" é opinião.

O pacote (`enunciado.pdf`) oferece dois caminhos: **padrão** (preencher um
esqueleto pronto com os limiares do próprio domínio) e **desafio**
(escrever o agente do zero). Foi seguido o caminho **padrão**.

Originalmente o pacote trazia uma reserva sintética pronta
(`casos-de-reserva.csv`, calibrada pela coordenação do curso). O professor
orientou, no entanto, montar o conjunto de 30 casos a partir de uma
**amostragem real do dataset AI4I2020** (o mesmo dataset de todo o
projeto AMS), não da reserva — o que trouxe decisões adicionais que a
reserva já resolvia de fábrica.

---

## 2. Primeira tentativa (`casos-lab-06.csv`) — por que foi descartada

A primeira amostra foi tirada em sequência do começo do dataset bruto
(`data/raw/ai4i2020.csv`). Ao classificar essas 30 linhas pelos gatilhos
físicos reais de falha do AI4I2020 (ver seção 3), o resultado foi **22
casos seguros e 8 falhas, mas ZERO casos difíceis (quase-falha) e ZERO
atípicos** — a amostra simplesmente não passava perto de nenhum limiar de
risco. Isso violava a exigência do próprio enunciado: *"inclua casos
fáceis, casos difíceis e pelo menos dois atípicos: conjunto só de casos
fáceis produz um número bonito e inútil."*

Esse arquivo foi mantido no repositório (não editado) por um tempo, mas
**nunca foi o conjunto usado na entrega** — foi substituído pela v2,
abaixo. Como está em formato bruto do AI4I2020 (14 colunas) e não roda com
o que `carregar_casos()` espera hoje (as 9 colunas do formato do lab), ele
foi removido do repositório — este relato fica como registro de por que a
primeira amostragem foi descartada.

---

## 3. Segunda tentativa (`casos-lab-06-v2.csv`) — amostragem deliberada

Em vez de amostrar às cegas e reclassificar depois, as 30 linhas foram
**escolhidas deliberadamente** a partir dos 10.000 registros completos,
usando os próprios gatilhos de falha documentados oficialmente pela UCI
(texto trazido para a conversa, que confirmou os limiares já validados
empiricamente contra o dataset inteiro):

| Modo | Gatilho documentado |
|---|---|
| **TWF** (desgaste) | falha sorteada aleatoriamente quando o desgaste da ferramenta está entre 200–240 min (120 casos no dataset; só 43 falham de fato — as outras 77 são "trocada a tempo", ou seja, seguras apesar do desgaste alto) |
| **HDF** (dissipação de calor) | falha se `temp. processo − temp. ar < 8,6 K` **e** `rotação < 1380 rpm` |
| **PWF** (potência) | falha se `torque × rotação (rad/s)` sai de `[3500, 9000] W` |
| **OSF** (sobrecarga) | falha se `desgaste × torque` passa de 11.000 (produto L) / 12.000 (M) / 13.000 (H) min·Nm |
| **RNF** (aleatória) | 0,1% de chance de falha, independente de tudo |

Achado importante: **9 registros no dataset inteiro têm falha real sem
nenhum dos cinco mecanismos marcado** — falhas sem explicação visível em
nenhuma regra documentada. Esse é o equivalente real mais forte do "a
falha que os sensores não veem".

As 30 linhas foram escolhidas em 4 categorias, por UDI específico (listado
em `FONTE-casos-lab-06-v2.md`):

- **2 atípicos** — falha real, zero flags, leituras comuns.
- **6 difíceis** — sem falha real, mas perto de um gatilho (um a dois por
  mecanismo: TWF, os dois lados do PWF, OSF, HDF).
- **6 falhas "fáceis"** — gatilho isolado e óbvio, um por mecanismo (mais
  um caso com dois mecanismos simultâneos).
- **16 seguras** — longe de qualquer limiar, com mistura de tipo de
  máquina parecida com a proporção real do dataset (L 50%/M 30%/H 20%).

Resultado: **16 baixo / 6 médio / 8 alto** de risco, e **22 fácil / 6
difícil / 2 atípico** de dificuldade — agora genuinamente ancorado nos
gatilhos reais, não em um ajuste estatístico sobre uma amostra ruim.

As datas (coluna `data`) foram depois **reembaralhadas de forma uniforme**
entre as categorias: a primeira versão atribuía datas em blocos (todos os
atípicos primeiro, depois os difíceis, etc.), o que agrupava artificialmente
as falhas reais nos primeiros dias do mês — e isso distorceria o
funcionamento do estado interno (`EstadoDaFrota`), que acumula falhas por
família de máquina dentro de uma janela de dias. Com as datas
intercaladas, os 8 casos de falha ficam espalhados ao longo dos 30 dias,
como aconteceria de verdade.

## 4. Mapeamento de colunas (AI4I2020 → estrutura esperada pelo lab-06)

O `esqueleto.py` (herdado do padrão `casos-de-reserva.csv`) espera 9
colunas específicas. Nem todas existem no AI4I2020 real — a tabela abaixo
mostra o que é dado real, o que foi derivado e o que é placeholder:

| Coluna | Origem | Natureza |
|---|---|---|
| `id_caso` | gerado: `A01`..`A30` | gerado |
| `data` | sequência sintética, 1/dia a partir de 2026-04-01, intercalada (ver §3) | **sintética** — o AI4I2020 não tem timestamp real |
| `tipo_maquina` | coluna `Type` (L/M/H) do dataset | real |
| `idade_meses` | não existe no AI4I2020 | **placeholder fixo `0`** — `decidir()` não usa este campo |
| `temperatura_c` | `Process temperature [K] − 273,15` | real, convertida |
| `vibracao_mm_s` | **derivada**: `2,0 + 10·(0,5·desvio relativo de RPM + 0,5·desvio relativo de torque)` em relação à mediana da amostra | **proxy calculado** — o AI4I2020 não mede vibração |
| `horas_desde_manutencao` | `Tool wear [min]`, usado direto | real |
| `acao_correta` | derivada do `risco` (ver tabela de categorias) | derivada |
| `falhou_depois` | `Machine failure` (0/1) | real |
| `risco` *(coluna extra, pedida)* | ver §3 | derivada dos gatilhos reais |
| `dificuldade` *(coluna extra, pedida)* | ver §3 | derivada dos gatilhos reais |

Detalhes completos (os UDIs exatos de cada categoria, a fórmula da
vibração passo a passo) estão em
`D02/D2-06-agente-baseline/adaptacao-ams/FONTE-casos-lab-06-v2.md`.

---

## 5. Recalibração do `esqueleto.py`

Os limiares originais do pacote (calibrados para a reserva sintética) não
faziam sentido na escala real do AI4I2020:

- **`LIMITE_TEMPERATURA = 78.0`°C foi removido.** No AI4I2020 real, a
  temperatura absoluta **não causa nenhum** dos quatro modos de falha
  documentados (só a *diferença* processo−ar entra no modo HDF) — e os
  valores reais ficam todos entre 33–38°C, nunca perto de 78. Mantê-lo
  faria a condição reativa nunca disparar por temperatura.
- **Substituído por `LIMITE_DESGASTE = 150.0`** sobre
  `horas_desde_manutencao` — um gatilho real (a zona de sorteio de falha
  por desgaste no AI4I2020 começa em 200 min). 150 fica acima das 16
  leituras seguras da amostra (nenhum falso positivo) e abaixo da maioria
  dos casos de risco médio/alto.
- **`LIMITE_VIBRACAO = 7.0` foi mantido** — a faixa do proxy derivado caiu
  na mesma escala por construção, e 7,0 separa bem os dois valores
  claramente extremos (11,3 e 9,2) do resto (≤4,6).
- `FALHAS_PARA_INSPECAO = 2` e `JANELA_DIAS = 7` (estado interno) foram
  mantidos sem alteração — são uma heurística de manutenção genericamente
  razoável, não específica da reserva.

A versão anterior de cada trecho alterado ficou comentada no próprio
`esqueleto.py`, para comparação.

---

## 6. Medição (`python medir.py`)

Métrica primária do PEAS (`agent-spec.md` §4: **recall da classe
"alto"**):

| Métrica | Valor |
|---|---|
| Recall da classe "alto" | **5/8 = 0,625** |
| Precisão da classe "alto" | 5/10 = 0,50 |
| Acerto geral (3 classes) | 21/30 = 0,70 |

**Onde o agente erra, e por quê** (análise completa em
`analise_baseline.md`):

1. **Conservador demais na maioria dos erros (5 de 9):** qualquer caso que
   cruze o limiar de desgaste ou vibração vira direto
   `parar_para_manutencao`, mesmo quando o risco real era só
   `inspecionar_antes_de_operar` — a regra reativa não tem nível
   intermediário, só sabe dizer "pare" ou "não é comigo".
2. **O erro mais perigoso, em 3 casos:** falhas reais não detectadas a
   tempo, porque nenhuma das duas variáveis monitoradas estava elevada —
   são exatamente os padrões que o AI4I2020 documenta como invisíveis a
   um único sensor (falha por potência, que depende de torque × rotação;
   e as falhas "atípicas", sem nenhum sinal visível). Confirma, com
   números, o ponto cego estrutural de um agente de regras com poucas
   variáveis.

---

## 7. `pytest teste.py` — 6 passam, 4 falham (esperado e documentado)

As 4 falhas são consequência direta de ter trocado tanto o conjunto de
casos quanto a variável da regra reativa — o próprio `teste.py` avisa no
cabeçalho que isso aconteceria ("as famílias 1 e 2 continuam valendo; a
família 3 é o gabarito da reserva"). `teste.py` **não foi editado** (é o
arquivo de verificação da disciplina):

1. `test_condicao_reativa_para_com_temperatura_alta` — testava o limiar de
   temperatura antigo, que não existe mais.
2. `test_as_trinta_decisoes_batem_com_o_gabarito` — gabarito com IDs
   `C01..C30` da reserva; o conjunto novo usa `A01..A30`.
3. `test_a_metrica_final_da_reserva_e_25_de_30` — gabarito 25/30
   hard-coded da reserva; o conjunto real dá 21/30.
4. `test_o_medidor_roda_sobre_outro_arquivo_sem_tocar_em_codigo` — usa um
   CSV de teste embutido com temperatura alta (82°C), esperando acionar o
   limiar antigo.

Nenhuma é um defeito em `decidir()` — são testes cujo conteúdo é
específico da reserva sintética ou do limiar antigo.

---

## 8. Decisão sobre o tipo de agente (estado interno mantido)

`agent-spec.md` §2 classifica o ambiente AMS como **parcialmente
observável** ("falta a descrição da ordem de serviço"). O enunciado só
libera apagar a condição de estado interno (`EstadoDaFrota`) para quem
caracterizou o ambiente como totalmente observável — por isso ela foi
**mantida**.

---

## 9. Cópia final para o pacote do projeto

Copiadas `decidir`, `EstadoDaFrota` e `carregar_casos` para
**`src/ams/baseline.py`** — o caminho que a entrega final cobra. A cópia:

- segue as convenções do pacote `src/ams/` (docstrings no padrão
  Google, `from __future__ import annotations`, nomes em português);
- traz os limiares já recalibrados (seção 5) e remove a linguagem de TODO
  do esqueleto de laboratório, já que esta é a versão definitiva;
- documenta no próprio docstring do módulo os números da medição (seção
  6) e a limitação estrutural conhecida (ponto cego multivariado).

Verificado: `from ams import baseline` importa sem erro e reproduz os
mesmos 21/30 de acerto medidos em `medir.py`.

**Gap encontrado numa conferência posterior contra o enunciado, e
fechado:** o critério de aceite diz literalmente *"baseline.py roda sobre
30 casos e devolve a métrica primária"* — mas a primeira cópia só trazia
`decidir`/`EstadoDaFrota`/`carregar_casos` (as peças da decisão), sem
nenhuma função que rodasse sobre os casos e devolvesse a métrica. O
recall da classe "alto" tinha sido calculado uma vez, à mão, num script de
terminal. Acrescentei `baseline.medir(caminho)`, que roda os 30 casos e
devolve `recall_alto`, `precisao_alto`, `acerto_geral` e a lista de erros
— verificado que reproduz exatamente os mesmos números já documentados
acima (recall 0,625, precisão 0,50, acerto geral 0,70, os mesmos 9 erros).

---

## 10. Arquivos deste laboratório (estado final)

Os arquivos originais do pacote (`enunciado.pdf`, `COMO-USAR-A-
RESERVA.pdf`, `FONTE.md`, `casos-de-reserva.csv`, `esqueleto.py`,
`medir.py`, `teste.py`) ficam na raiz de `D02/D2-06-agente-baseline/`. Tudo
que foi produzido neste trabalho (dados e análise) está em
`D02/D2-06-agente-baseline/adaptacao-ams/`:

| Arquivo | O que é |
|---|---|
| `casos-lab-06-v2.csv` | amostra final usada, curada pelos gatilhos reais |
| `FONTE-casos-lab-06-v2.md` | procedência da v2: UDIs por categoria, mapeamento de colunas, aviso sobre limiares |
| `analise_baseline.md` | métrica primária, análise de erro, justificativa da recalibração, explicação das 4 falhas esperadas do `teste.py` |
| `RESUMO-LAB06.md` | este arquivo |

Fora desta subpasta: `esqueleto.py` tem as regras recalibradas
(`LIMITE_DESGASTE` no lugar de `LIMITE_TEMPERATURA`) e aponta pra
`adaptacao-ams/casos-lab-06-v2.csv`; `medir.py`/`teste.py` não foram
alterados (arquivos da disciplina); `src/ams/baseline.py` é a versão
definitiva do agente, copiada para o pacote do projeto.

Todo este trabalho já está commitado: commit `71c7d99` ("D02 labs 03-06:
catálogo de busca corrigido, baseline do agente e restrições do PEAS"),
branch `feature/D02_E04`.
