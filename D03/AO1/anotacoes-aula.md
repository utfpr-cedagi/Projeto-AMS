# AO1 — anotações da aula (o que o professor explicou além do enunciado)

> Baseado nas anotações feitas durante a explicação do professor sobre o
> slide "O que a Atividade Orientada pede" (D3, Encontro 2 de 4, slide 58).
> O enunciado oficial é [`D3-AO1-enunciado.pdf`](D3-AO1-enunciado.pdf) —
> estas notas complementam, não substituem.

## O que entregar até o próximo encontro

O enunciado lista quatro itens, mas o professor foi explícito em aula:
**só os dois primeiros valem para esta entrega** (ver seção
["O que fica para a nota 2"](#o-que-fica-para-a-nota-2-não-fazer-ainda)
abaixo).

### 1. Ampliar o conjunto de 30 para ≥ 60 casos rotulados

- Criar a pasta `AO1/` (já existe, com o enunciado dentro), copiar o
  arquivo dos 30 casos já usados na D2 e acrescentar mais 30 — trazendo
  casos fáceis **e** difíceis, não só os óbvios.
- **Alternativa caso não dê tempo de criar os 30 novos:** usar o arquivo
  `casos-ams-60` que o professor disponibiliza no pacote de arquivos
  auxiliares (vai estar no Moodle). Se essa for a abordagem adotada, isso
  precisa ficar **declarado por escrito** na entrega: "utilizei o arquivo
  casos-ams-60".
- O pacote de arquivos auxiliares do professor também traz
  `comum/reamostragem.py` e `comum/amostra.py` (kit do D3-05) — não são
  necessários para esta entrega, só para a nota 2.

### 2. Duas variantes do mesmo agente, avaliadas sobre os mesmos 60 casos

- **Agente A** = o modelo base que já existe (o da D2).
- **Agente B** = uma variante **de verdade**, não um ajuste cosmético.
  A regra é clara: criar uma mudança que deixe o comportamento do agente
  B realmente diferente do A — trocar a regra de decisão, acrescentar um
  passo de verificação, mudar a fonte consultada primeiro. Não vale mexer
  em temperatura ou reescrever uma frase do prompt.
- **AED rigorosa do conjunto ampliado** (os 60 casos): repetir a mesma
  análise estatística feita hoje no laboratório da manhã — criar um
  notebook e rodar o mesmo `medidas.py` do
  [`D3-03-estatistica-descritiva`](../D3-03-estatistica-descritiva/medidas.py)
  sobre o conjunto de 60, trazendo as mesmas respostas (outliers com
  decisão justificada, faltantes com hipótese de mecanismo) já praticadas
  ali.
- **Latência:** cronometrar a decisão do agente a cada invocação e
  reportar como métrica **p50 e p95** — não a média. Incluir uma frase
  explicando por quê: tempo de resposta tem distribuição de cauda longa
  (poucas chamadas muito lentas puxam a média para cima e escondem o
  tempo "típico"); p50 mostra o caso comum e p95 mostra o pior caso que
  o usuário realmente sente, o que a média mascara.

### Entregável mínimo até o próximo encontro

Um repositório Git contendo:

- `ao1.py` (ou notebook equivalente rodando a avaliação);
- o(s) arquivo(s) de casos (30 + 30 novos, ou o `casos-ams-60` com a
  declaração acima) e o `acertos.csv` das duas variantes;
- o notebook executado, com as células rodadas e as decisões escritas.

## O que fica para a nota 2 (não fazer ainda)

O enunciado também pede um intervalo de confiança, o cálculo de tamanho
de amostra e uma página sobre correlação — mas o professor cancelou isso
em aula para esta entrega: **não precisa fazer até o próximo encontro**,
vai compor a nota 2. O próprio PDF do enunciado já reflete isso (os itens
3 e 4, e o sub-item do intervalo de confiança por reamostragem dentro do
item 2, aparecem riscados no documento):

- Intervalo de confiança por reamostragem (`comum/reamostragem.py`);
- Cálculo de tamanho de amostra e poder (`comum/amostra.py`,
  `casos_para_diferenca`);
- Uma página sobre correlação e causalidade no domínio.

## Nota sobre o tamanho da amostra (contexto, não ação)

O professor reforçou o alerta que já está no enunciado: com 60 casos
pareados, só diferenças acima de dez a doze pontos percentuais se
distinguem de ruído estatístico. Um "não sei ainda" na devolutiva não é
fracasso — é o que a matemática permite com esse tamanho de amostra.
