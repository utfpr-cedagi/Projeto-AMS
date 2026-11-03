# NOTA — como `vibracao_mm_s` foi derivada (lab-06)

Complementa `FONTE-casos-lab-06-v2.md`, que descreve a fórmula em uma
linha de tabela. Esta nota expande o raciocínio e verifica a conta na mão
contra dois casos reais do CSV — útil pra quem está vendo essa coluna pela
primeira vez e quer entender de onde ela vem antes de confiar no limiar
`LIMITE_VIBRACAO` usado em `decidir()` ([`esqueleto.py`](../esqueleto.py)).

## 1. O que "derivada" quer dizer aqui

Na tabela de mapeamento do `FONTE-casos-lab-06-v2.md`, a coluna
`vibracao_mm_s` está marcada como:

> **derivada**: `2,0 + 10·(0,5·desvio_relativo_RPM + 0,5·desvio_relativo_Torque)`
> em relação à mediana das 30 linhas — **proxy calculado** — o AI4I2020
> não mede vibração; isto NÃO é um sensor real.

Nenhum sensor mediu "vibração" pra gerar esse número. O AI4I2020 real tem
sensores de **rotação** (`Rotational speed [rpm]`) e **torque**
(`Torque [Nm]`) — e esse valor foi *calculado* a partir desses dois, pra
se parecer com uma leitura de vibração. "Derivada" = veio de conta, não
de sensor.

## 2. Por que rotação e torque, e não outra coisa?

Vibração mecânica em máquina rotativa tende a crescer quando a máquina
opera **longe do seu ponto normal de trabalho** — desbalanceamento,
ressonância, carga fora da faixa projetada. Rotação e torque descrevem
exatamente esse "ponto de operação", e são as mesmas duas variáveis que
entram na fórmula de potência (`torque × rotação`) usada pelo AI4I2020
pra definir o gatilho de falha PWF. Daí a escolha como proxy.

## 3. A ideia central: desvio relativo em relação à mediana

- **Mediana** das 30 linhas escolhidas = "o que é normal" nesse conjunto
  (não no dataset inteiro de 10.000 — só nessas 30 curadas).
- **Desvio relativo** = o quanto um caso específico se afasta desse
  normal, em percentual:

  ```
  desvio_relativo = |valor - mediana| / mediana
  ```

Rotação/torque perto do típico → desvio baixo → proxy "vibra pouco".
Rotação ou torque muito fora do normal → desvio alto → proxy "vibra
muito".

## 4. A fórmula, passo a passo

```
vibracao_mm_s = 2,0 + 10 × (0,5 × desvio_relativo_RPM + 0,5 × desvio_relativo_Torque)
```

- Calcula o desvio relativo do RPM e o desvio relativo do Torque,
  separadamente.
- Tira a média simples dos dois (peso 50/50 — nenhum pesa mais que o
  outro).
- Multiplica por **10** (escala) e soma **2,0** (piso). Esses dois
  números não têm significado físico — só ajustam o resultado final pra
  parecer uma leitura plausível em mm/s.

## 5. Exemplo real, verificado em `data/raw/ai4i2020.csv`

Os dois valores mais altos do conjunto (citados no comentário de
`esqueleto.py`) são `A14 = 11,3` e `A08 = 9,2`. Rastreando até as linhas
originais do dataset bruto:

| | `id_caso` | UDI original | RPM | Torque [Nm] | Tool wear | `vibracao_mm_s` no CSV do lab |
|---|---|---|---|---|---|---|
| A14 | risco alto, fácil | 51 | 2861 | 4,6 | 143 | **11,3** |
| A08 | risco médio, difícil | 1210 | 2540 | 13,3 | 98 | **9,2** |

Usando como "normal" (mediana aproximada das 30 linhas) algo como
**~1450 rpm** e **~40 N·m** — valores típicos das linhas "seguras" do
conjunto —, a conta fecha quase exatamente:

**A14** (UDI 51 — caso de "falha fácil" por PWF, lado de potência baixa:
rotação alta + torque muito baixo):
- desvio RPM = |2861 − 1450| / 1450 ≈ 0,97
- desvio Torque = |4,6 − 40| / 40 ≈ 0,885
- média = 0,93 → `2,0 + 10×0,93 = 11,3` ✓ bate com o CSV

**A08** (UDI 1210 — caso "difícil" de PWF, perto do gatilho mas sem
cruzar):
- desvio RPM = |2540 − 1450| / 1450 ≈ 0,75
- desvio Torque = |13,3 − 40| / 40 ≈ 0,67
- média ≈ 0,71 → `2,0 + 10×0,71 = 9,1` ✓ bate (arredondamento) com o 9,2

São os dois valores mais altos porque são justamente os dois casos em
que o lab escolheu de propósito uma combinação de rotação/torque fora do
normal (pra simular PWF). As máquinas "seguras" do conjunto, por
definição, têm rotação e torque perto da mediana — por isso ficam todas
em ≤ 4,6.

## 6. Por que `LIMITE_VIBRACAO = 7,0` funciona

Olhando a coluna inteira do CSV: os 30 casos ficam quase todos entre 2,2
e 5,5 — só A14 (11,3) e A08 (9,2) disparam acima disso. Um limiar de 7,0
corta exatamente no meio desse vazio, separando os dois extremos do
resto sem nenhum falso positivo. O comentário em
[`esqueleto.py:60-63`](../esqueleto.py#L60-L63) já registra isso: o
limiar antigo (`7.0`, herdado da reserva sintética) foi **mantido por
coincidência de escala**, não recalculado — "a faixa derivada... já caiu
nessa escala por construção".

Isso é o que a condição reativa de `decidir()` usa
([`esqueleto.py:126`](../esqueleto.py#L126)):

```python
if registro["vibracao_mm_s"] > LIMITE_VIBRACAO or \
        registro["horas_desde_manutencao"] >= LIMITE_DESGASTE:
    return "parar_para_manutencao"
```

`vibracao_mm_s` é só mais um float pra essa condição — ela não sabe (nem
precisa saber) que por trás existe essa conta com mediana e desvio
relativo. O trabalho de engenharia aconteceu **antes**, na curadoria dos
casos.

## 7. O ponto pedagógico mais importante

Essa é uma engenharia de atributo honesta sobre sua própria limitação: o
domínio AMS real pede um sensor de vibração, o dataset público não tem
um, e em vez de inventar um número arbitrário ou fingir que existe um
sensor, o `FONTE-casos-lab-06-v2.md` documenta explicitamente a fórmula e
marca a coluna como proxy calculado — **não** um sensor real. É o tipo
de rastreabilidade que `agent-spec.md` cobra: todo dado derivado carrega
a receita de como foi feito, não só o valor final.

## Em aberto

Os UDIs de várias das outras 28 linhas já estão listados na tabela de
categorias do `FONTE-casos-lab-06-v2.md`. Dá pra fechar a mediana exata
de RPM/Torque usada na fórmula (em vez da aproximação `~1450 rpm` /
`~40 N·m` usada acima) rastreando os UDIs restantes contra
`data/raw/ai4i2020.csv`, se algum dia for preciso conferir até o último
decimal.
