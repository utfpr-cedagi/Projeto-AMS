# FONTE — procedência dos dados da AO1 (`D03/AO1/dados/`)

**Arquivos:** `casos-60.csv` (o conjunto de avaliação da AO1, 60 casos) e
`depara-60.csv` (proveniência linha a linha), mais `casos-lab06-adaptado-d3.csv`
(os 30 casos de D02, isolados, já no esquema novo — ver "Por que existe
esse arquivo à parte" abaixo).

Diferente dos outros `dados/` já vistos em D03 (`D3-01`, `D3-04`, onde o
conteúdo vem pronto do pacote do curso), este é o primeiro caso de `dados/`
com conteúdo gerado pelo autor — a AO1 não tem pacote de curso, é
inteiramente produção própria por natureza.

## De onde vêm as duas metades

- **Casos A01–A30** (abril/2026): os mesmos 30 casos reais do AI4I2020 já
  usados em `D02/D2-06-agente-baseline/adaptacao-ams/casos-lab-06-v2.csv`
  (ver `FONTE-casos-lab-06-v2.md` naquela pasta para a proveniência
  completa — categorias, UDIs, fórmulas). **O arquivo original de D02 não
  foi alterado.**
- **Casos B01–B30** (maio/2026): 30 casos novos, também tirados de
  linhas reais do AI4I2020, gerados por um script pessoal do autor
  (`gerador_casos.py`, lote `casos-d03-lote1.csv`). O script e o lote
  ficam na área de estudo pessoal do autor, **fora desta entrega**; nesta
  pasta os casos B01–B30 existem só dentro de `casos-60.csv`, e a
  proveniência linha a linha (UDI de origem) está em `depara-60.csv`.
  Nenhum UDI real se repete entre as duas metades (o lote foi gerado
  excluindo explicitamente os UDIs de D02).

**Pedido do professor (anotações de aula, D03/AO1):** copiar os 30 casos já
usados na D2 e somar mais 30, totalizando 60, para a avaliação da AO1
(arquivo `acertos.csv` dos laboratórios 05/06).

## Por que existe `casos-lab06-adaptado-d3.csv` à parte

Os dois arquivos de origem ficaram com esquemas de coluna incompatíveis
depois do ajuste de `tipo_maquina`/`idade_meses` pedido pelo professor
(mesmo e-mail "Casos para atividades D03"): em `casos-lab-06-v2.csv`
(D02), `tipo_maquina` ainda é a qualidade real do produto AI4I (L/M/H);
em `casos-d03-lote1.csv` (D03) em diante, `tipo_maquina` é uma família de
máquina fictícia e a qualidade real foi pra `qualidade_produto`.

Não dava pra corrigir isso no arquivo original de D02 — ele é lido pelo
`esqueleto.py` do professor (pacote fechado, não editável) e já foi
avaliado na N2 (21/30); mudar sua coluna/significado quebraria essa
reprodutibilidade. A solução foi adaptar uma CÓPIA, só para a D03:

- Um script pessoal do autor (`adaptar_casos_lab06.py`, fora desta
  entrega, como o gerador) lê
  `casos-lab-06-v2.csv`, renomeia `tipo_maquina` → `qualidade_produto`
  (preserva o L/M/H real), sorteia uma `tipo_maquina` nova (família
  fictícia, mesma lista `FAMILIAS_MAQUINA` de `gerador_casos.py`:
  TORNO/PRENSA/COMPRESSOR/ROBOT — o mesmo padrão didático que o professor
  já usa na reserva sintética do pacote), com seed fixa `99` (distinta do
  `seed=42` do lote1: são sorteios independentes, nenhum dos dois reaproveita
  o outro), e remove `idade_meses`.
- O resultado é gravado em `casos-lab06-adaptado-d3.csv` — mesmos dados
  reais (data, temperatura, vibração, horas desde manutenção, ação
  correta, falha, risco, dificuldade) de `casos-lab-06-v2.csv`, só muda o
  que estava embutido em `tipo_maquina`/`idade_meses`.
- Esse arquivo adaptado é então concatenado com o lote
  `casos-d03-lote1.csv` para formar `casos-60.csv` (o lote não tem cópia
  à parte nesta pasta: os casos dele estão só dentro de `casos-60.csv`). O de-para
  das duas metades (`depara-casos-lab-06-v2.csv` + `depara-casos-d03-lote1.csv`)
  é concatenado da mesma forma em `depara-60.csv`.

## Como reproduzir

Os três arquivos desta pasta são o resultado final e já estão
versionados; para usar a AO1 não é preciso gerá-los de novo. Os scripts
que os geram (`gerador_casos.py` e `adaptar_casos_lab06.py`) são
determinísticos (seeds fixas 42 e 99), mas ficam na área pessoal do
autor, fora desta entrega.

## Nota sobre as datas

As duas metades não se misturam cronologicamente: A01–A30 cobrem
2026-04-01 a 2026-04-30, B01–B30 cobrem maio/2026 (datas embaralhadas
dentro do mês, herdadas de `casos-d03-lote1.csv`). Quem rodar
`baseline.medir()` sobre `casos-60.csv` (que ordena por `data`) processa o
bloco de abril inteiro antes de começar o de maio — `EstadoDaFrota` não
mistura família/falha das duas metades num mesmo instante, mas acumula
normalmente dentro de cada bloco.

**Ordem das linhas em `acertos.csv`:** o `ao1.py` usa o mesmo
`carregar_casos` (que ordena por `data`), então as linhas do
`acertos.csv` seguem a **ordem de data**, não a ordem de `id_caso` de
`casos-60.csv`. As linhas 1–30 coincidem (A01–A30 já estão em ordem de
data); de B01 em diante não. Para cruzar um acerto com o seu caso,
ordene `casos-60.csv` por `data` (as 60 datas são distintas) antes de
alinhar por posição.

## Licença e reúso

Mesma licença do dataset original: CC BY 4.0 (AI4I 2020 Predictive
Maintenance Dataset, UCI Machine Learning Repository, ID 601). Ver
`data/FONTE.md` (raiz do projeto) para citação completa.
