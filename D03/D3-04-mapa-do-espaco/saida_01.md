## Execucao esqueleto.py manutencao
``` bash
(ams) PS C:\temp\UTFPR\Projeto-AMS\D03\D3-04-mapa-do-espaco> uv run .\esqueleto.py manutencao 
== Laboratório 04 — o mapa do meu domínio
conjunto: manutencao · 200 frases · 384 dimensões · normalizado (slide 55)
métodos: componentes principais (determinístico) · vizinhança (t-SNE, semente 20260901 — declarada na figura)
mapas: mapa-do-espaco.png (índices anotados) · pontos: mapa-pontos.csv

próximo passo: escolha no mapa três pares de pontos VIZINHOS e confira (o passo 4 do slide 52), por exemplo:
  python esqueleto.py manutencao --pares 4,9 22,77 150,181

conferência: pares-conferidos.md — anote nele as quatro respostas do slide 53 e o caso em que o mapa enganou, e rode python -m pytest teste.py -q

pendências do critério do slide 52:
  - os três pares do passo 4 ainda não foram conferidos — rode com --pares (ex.: --pares 4,9 22,77 150,181)
  - faltam respostas no pares-conferidos.md (0 de 4: as quatro perguntas do slide 53)
(ams) PS C:\temp\UTFPR\Projeto-AMS\D03\D3-04-mapa-do-espaco> 
```

Pontos PCA
- 123,41
- 35,36

Pontos Vizinhanca
- 105,167


``` bash
(ams) PS C:\temp\UTFPR\Projeto-AMS\D03\D3-04-mapa-do-espaco> uv run .\esqueleto.py manutencao --pares 123,41 35,36 105,167       
== Laboratório 04 — o mapa do meu domínio
conjunto: manutencao · 200 frases · 384 dimensões · normalizado (slide 55)
métodos: componentes principais (determinístico) · vizinhança (t-SNE, semente 20260901 — declarada na figura)
mapas: mapa-do-espaco.png (índices anotados) · pontos: mapa-pontos.csv

conferência (passo 4 do slide 52) — o cosseno ORIGINAL de cada par escolhido no mapa:
  (123,  41) cos +0.1846  NÃO confirma
  ( 35,  36) cos +0.9780  confirma
  (105, 167) cos +0.5892  confirma

conferência: pares-conferidos.md — anote nele as quatro respostas do slide 53 e o caso em que o mapa enganou, e rode python -m pytest teste.py -q

pendências do critério do slide 52:
  - faltam respostas no pares-conferidos.md (0 de 5: as quatro perguntas do slide 53 e o caso em que o mapa enganou)
```

## Execucao pytest — um teste vermelho, causa identificada

```
PS C:\temp\UTFPR\Projeto-AMS\D03\D3-04-mapa-do-espaco> python -m pytest teste.py -q
.....F..                                                                [100%]
FAILED teste.py::test_a_vizinhanca_muda_com_outra_semente - AssertionError: sementes diferentes devolveram mapas iguais
assert 0.0 > 1.0
```

Os outros 7 testes passam (TAREFAS 1 e 2 corretas, pares-conferidos.md
fechado). Só `test_a_vizinhanca_muda_com_outra_semente` falha, e continua
falhando mesmo rodando com o cwd certo (a pasta do laboratório).

Causa confirmada com um script isolado: `TSNE(init="pca", random_state=1)`
e `TSNE(init="pca", random_state=42)` sobre a mesma matriz devolvem
embeddings **bit-a-bit idênticos** (`max abs diff: 0.0`); trocando pra
`init="random"` as duas sementes já dão resultados diferentes
(`max abs diff: ~7.08`). No código-fonte do `scikit-learn==1.9.0` instalado
(`TSNE._fit`), quando `init == "pca"` a inicialização vem de
`PCA(n_components=2, random_state=random_state).fit_transform(X)` — e para
o tamanho deste conjunto o `PCA` resolve `svd_solver="full"` (SVD exata,
determinística), que ignora `random_state`. Sem nenhuma outra fonte de
aleatoriedade na otimização do t-SNE, a "semente" de `reduzir_vizinhanca`
fica inerte nesta versão da biblioteca — contrariando a premissa do slide
54 ("duas execuções PODEM dar figuras diferentes").

Não é erro nas TAREFAS 1/2 nem no uso do `esqueleto.py`: é uma
característica do `scikit-learn==1.9.0` fixado no `pyproject.toml` da raiz
do repo (pino do projeto inteiro, não deste lab). `esqueleto.py` e
`teste.py` ficam como o pacote entregou — só esta nota registra a causa.
