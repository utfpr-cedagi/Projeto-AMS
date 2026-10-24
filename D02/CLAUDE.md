# D02 — Fundamentos de Agentes Inteligentes

Disciplina 2 do curso CEDAGI, sobre fundamentos de agentes e busca. Uma
pasta por laboratório, numerada `D2-0N-slug`; cada pacote extrai na raiz do
repositório (não é um projeto separado).

## Encontros e laboratórios

| Pasta | Laboratório | Quando | Entrega |
|---|---|---|---|
| `D2-01-peas-do-meu-agente` | PEAS do agente | Encontro 1, bloco 3 | 4 campos do PEAS + fórmula de performance, em `agent-spec.md` §1 |
| `D2-02-ambiente-em-sete-dimensoes` | Ambiente em 7 dimensões | Encontro 2, manhã | `agent-spec.md` §2, uma frase de justificativa por dimensão |
| `D2-03-formular-como-busca` | Formular como busca | Encontro 2, tarde | `agent-spec.md` §7 + `verificar-formulacao.py` com as 6 verificações verdes |
| `D2-04-busca-nao-informada` | As 4 buscas, medidas | Encontro 3, bloco 2 | Tabela de `esqueleto.py` + conclusão escrita — **item 4 da entrega final, 25% da nota** |
| `D2-05-...` (ainda não extraído) | Busca informada (gulosa/A*) | — | Acrescenta as linhas de heurística à MESMA tabela do lab-04 |

Cada lab tem o critério de aceite e os passos completos no seu
`enunciado.pdf` — leia-o antes de supor o formato de uma entrega.

## Os dois caminhos (regra do curso inteira)

Todo laboratório de D02 oferece:

- **Padrão**: adaptar um exemplo pronto do catálogo (`comum/problemas/`)
  para o domínio AMS — trocar dados, não a classe.
- **Desafio**: formular/implementar do zero, sem abrir o motor
  (`comum/busca.py`).

Trocar de caminho é livre a qualquer momento, nos dois sentidos, **sem
justificar e sem custar nota**. Se travar mais de ~10 min no desafio, o
próprio enunciado recomenda migrar para o padrão.

## O padrão "catálogo de subproblemas" (desde o lab-03)

Cada laboratório de busca (`D2-03` em diante) carrega sua própria cópia de
`comum/` — **não é compartilhada entre pastas**:

- `comum/busca.py` — motor genérico (as buscas: largura, custo uniforme,
  profundidade limitada, aprofundamento iterativo e, a partir do lab-05,
  gulosa e A*). Não conhece problema nenhum — fechado, não editar.
- `comum/problemas/diagnostico.py`, `consultas.py`, `conformidade.py` — três
  subproblemas de referência do professor (ordem de verificações / sequência
  de consultas / roteiro de conformidade), cada um com uma instância
  `PEQUENA` e `MAIOR`. São exemplo de ESTILO — não é pra editar, é pra
  copiar o padrão.
- `comum/problemas/consultas_ams.py` — **a adaptação do aluno** (domínio
  AMS, no formato "sequência de consultas"), com as mesmas instâncias
  `PEQUENA`/`MAIOR`. É o único arquivo do catálogo que muda de laboratório
  pra laboratório.

Todo problema implementa o protocolo `Problema`: `estado_inicial`,
`acoes()`, `transicao()`, `objetivo()`, `custo()` e — a partir do lab-05 —
`heuristica_admissivel()`/`heuristica_inadmissivel()`.

**Atenção**: como cada pasta `D2-0N` tem sua PRÓPRIA cópia de `comum/`, uma
correção em `consultas_ams.py` feita numa pasta **não se propaga** pras
outras — precisa ser replicada manualmente se o mesmo erro estiver lá
também. Em 2026-10-24, a cópia de `D2-04` foi corrigida (fato
`"qtde total de pecas esperadas no período"` exigido por `FATOS_MAIORES`
sem nenhuma `Fonte` que o fornecesse) e `FONTES_MAIORES` foi expandida de 3
para 14 fontes para dar contraste real entre as buscas; a cópia de `D2-03`
ainda não recebeu a mesma correção — vale revisar antes de fechar aquele
laboratório (o trecho colado em `agent-spec.md` §7 também carrega essa
versão desatualizada, com um typo adicional: `"produizdas"` em
`FATOS_MAIORES` não bate com `"produzidas"` usado em `FONTES_MAIORES`).

## Lições aprendidas (vale lembrar antes de mexer em dados de busca)

- **Fato inalcançável é o bug mais comum nos subproblemas de busca**
  (`comum/problemas/`): ao editar `FATOS_*`/`FONTES_*` (ou equivalente em
  `diagnostico.py`/`conformidade.py`), confira que TODO fato/item exigido
  aparece em pelo menos uma fonte/ação — um nome digitado diferente (typo)
  ou um fato esquecido torna o objetivo inalcançável, e todas as buscas
  esgotam o espaço sem achar solução (custo 0.0, 0 ações). Depois de editar
  constantes, rode o laboratório (`esqueleto.py`) e, quando existir no
  pacote, `verificar-formulacao.py` — ele confere isso como uma das seis
  propriedades.
- **O estado não pode guardar a história do caminho** — só a SITUAÇÃO
  atual (ex.: o conjunto de fatos já sabidos, não a sequência de consultas
  que levou até ali). O próprio material da disciplina já cometeu esse erro
  uma vez: o espaço inflou de 1.500 para 117 mil expansões até o teste de
  sanidade pegar. É a verificação 6 do `verificar-formulacao.py`.
- Um subproblema "interessante" pra comparar buscas (ritmo do lab-04) tem
  ao menos uma fonte única cara que resolve tudo sozinha (poucas ações,
  custo alto) e uma combinação de fontes baratas que resolve mais barato
  (mais ações) — é o que separa visivelmente `busca_em_largura` (minimiza
  ações) de `custo_uniforme` (minimiza custo) na tabela, e é exatamente a
  pergunta que o laboratório pede para responder por escrito.

## Ferramentas de verificação

- `verificar-formulacao.py` (a partir do D2-03) — teste de sanidade com 6
  verificações: estado hashable, transição é função, ações estáveis na
  ordem, custo ≥ 0, objetivo alcançável, estado não guarda o caminho.
  Sem argumento testa o catálogo inteiro; com `arquivo.py:ATRIBUTO` testa a
  formulação do aluno.
- `esqueleto.py` (a partir do D2-04) — roda as buscas sobre a constante
  `FORMULACAO` (topo do arquivo) e imprime a tabela em Markdown, pronta
  para colar na entrega.
- `teste.py` / `pytest` — valida a implementação própria do caminho desafio
  contra o motor, nos três subproblemas do catálogo e na formulação do
  aluno.

## Ressalvas a registrar na análise escrita (lab-04 e seguintes)

- `nos_expandidos` da `profundidade_limitada` conta diferente das outras
  buscas (ela é recursiva, sem fronteira — conta entradas na recursão, sem
  repetidos). Não é "mais eficiente", é medição com definição diferente.
- Custo uniforme pior que largura em custo = bug de formulação (custo
  negativo ou transição que não é função), nunca resultado esperado — nesse
  caso volte ao `verificar-formulacao.py` do lab-03.
