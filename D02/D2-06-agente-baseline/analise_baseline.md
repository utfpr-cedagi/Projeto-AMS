# Laboratório 06 — linha de base (AMS, dados reais do AI4I2020)

## 1. Métrica primária do PEAS (`agent-spec.md` §4)

**Recall da classe "alto"** = máquinas de risco alto classificadas como
alto ÷ total de máquinas de risco alto no conjunto.

- **Valor:** 5/8 = **0,625**, sobre `casos-lab-06-v2.csv` (30 casos, 8 de
  risco alto — ver `FONTE-casos-lab-06-v2.md`).
- **Precisão da classe "alto"** (métrica secundária do PEAS): 5/10 =
  **0,50** (de 10 vezes que o agente disse "parar", só 5 eram de fato
  risco alto).
- **Acerto geral** (as 3 classes): 21/30 = **0,70** — é o que `medir.py`
  imprime de fábrica; fica registrado aqui por completude, mas a métrica
  que importa pro PEAS é o recall/precisão de "alto" acima.

## 2. Onde o agente erra, e por quê

**O agente erra pro lado conservador na maioria das vezes (5 dos 9 erros):
qualquer caso que cruze o limiar de desgaste (≥150h) ou de vibração
(>7,0) vira direto `parar_para_manutencao`, mesmo quando o risco real era
só `inspecionar_antes_de_operar` (casos A02, A08, A13, A17, A23) — a regra
reativa devolve a decisão mais severa assim que UM limiar é cruzado, sem
distinguir "perto do limite" de "claramente perigoso".** Isso é
consequência direta de como `decidir()` está estruturado: a primeira
condição que casa decide (slide 22), e a condição reativa não tem um nível
intermediário — ela só sabe dizer "pare" ou "não é comigo".

**O erro mais perigoso é o oposto, em 3 casos (A07, A09, A18): falhas reais
que o baseline não detectou a tempo, porque nenhuma das duas variáveis
monitoradas (desgaste, vibração) estava elevada nesses casos — são
exatamente os padrões que o próprio AI4I2020 documenta como não visíveis a
um único sensor** (A07 é uma falha sem nenhum dos quatro modos físicos
documentados disparando; A18 é uma falha por potência — que depende de
torque × rotação, não de desgaste nem da vibração derivada; A09 só foi
parcialmente pego pelo estado interno, que rebaixou a decisão pra
"inspecionar" em vez de "parar"). Confirma, com números, a limitação
estrutural de um agente de regras com só 2 variáveis reativas: ele tem um
ponto cego garantido contra qualquer combinação multivariada que nenhuma
das duas cubra sozinha.

## 3. Decisão sobre o tipo de agente

Mantida a condição com estado interno (`EstadoDaFrota`) — `agent-spec.md`
§2 classifica o ambiente como **parcialmente observável** ("não existe
hoje a descrição da ordem de serviço"), e o enunciado só libera apagar
essa condição pra quem caracterizou o ambiente como totalmente observável.

## 4. Recalibração feita (ver `esqueleto.py`, comentários com a versão anterior)

- `LIMITE_TEMPERATURA` (78°C, da reserva sintética) foi **removido** do
  `decidir()` — a temperatura absoluta não causa nenhum dos 4 modos de
  falha documentados do AI4I2020 real (só a *diferença* processo-ar entra
  no HDF), e os valores reais ficam todos entre 33–38°C, nunca perto de
  78. Substituído por `LIMITE_DESGASTE = 150.0` sobre
  `horas_desde_manutencao`, que É um gatilho real (a zona de sorteio de
  falha por desgaste do AI4I2020 começa em 200 min; 150 fica acima das 16
  leituras seguras da amostra, sem nenhum falso positivo nelas).
- `LIMITE_VIBRACAO` (7,0) foi mantido — a faixa do proxy derivado (RPM e
  torque) caiu na mesma escala por construção, e 7,0 separa bem os 2
  valores claramente extremos (A14=11,3 e A08=9,2) do resto (≤4,6).

## 5. `pytest teste.py` — 6 passam, 4 falham (esperado, documentado)

```
PYTHONIOENCODING=utf-8 python -m pytest teste.py -v
6 passed, 4 failed
```

As 4 falhas são consequência direta e esperada de ter trocado tanto o
conjunto de casos quanto as variáveis da regra reativa — o próprio
cabeçalho do `teste.py` avisa: *"Se o seu domínio é outro, as famílias 1 e
2 é que continuam valendo — adapte-as aos SEUS limiares. A 3 é o gabarito
do conjunto de reserva."* Não editei `teste.py` (é o arquivo de
verificação da disciplina):

1. `test_condicao_reativa_para_com_temperatura_alta` — testava o limiar de
   temperatura antigo, que não existe mais no `decidir()`.
2. `test_as_trinta_decisoes_batem_com_o_gabarito` — gabarito hard-coded
   pros IDs `C01..C30` da reserva; nosso conjunto usa `A01..A30`.
3. `test_a_metrica_final_da_reserva_e_25_de_30` — gabarito hard-coded
   25/30 da reserva; nosso conjunto real dá 21/30.
4. `test_o_medidor_roda_sobre_outro_arquivo_sem_tocar_em_codigo` — o CSV
   de teste embutido no próprio teste usa um valor de temperatura alto
   (82°C) esperando acionar o limiar antigo, que não existe mais.

Nenhuma dessas é um defeito em `decidir()` — são testes cujo conteúdo
(IDs, gabarito numérico, variável monitorada) é específico da reserva
sintética ou do limiar antigo, exatamente como o próprio arquivo avisa que
aconteceria ao trocar de domínio.

## Próximo passo

Quando os números acima estiverem validados, copiar `decidir`,
`EstadoDaFrota` e `carregar_casos` para `src/ams/baseline.py` — o caminho
que a entrega final cobra.
