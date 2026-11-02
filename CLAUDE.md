# AMS — Projeto Integrador (CEDAGI/UTFPR)

Repositório do Projeto Integrador da pós-graduação **CEDAGI/UTFPR — Curso de
Especialização em Desenvolvimento de Agentes Inteligentes**. Curso de 15
meses; cada disciplina (D1, D2, D3...) entrega uma peça do mesmo agente.
Autor: Daniel Martinhao.

## Domínio do projeto

**AMS — Assistente de Manutenção Segura**: dada uma ordem de serviço
(máquina + leitura de sensores + descrição da intervenção), o sistema estima
o nível de risco de falha, indica as normas regulamentares aplicáveis
(NR-10/12/35) e recomenda bloqueio/etiquetagem (LOTO) antes da intervenção.
A decisão final é sempre do técnico — o sistema é apoio, não substituto.
Dataset: *AI4I 2020 Predictive Maintenance* (UCI #601), 10.000 registros.
Detalhes completos em [`dominio.md`](dominio.md).

## Estrutura

- [`src/ams/`](src/ams/) — pacote instalável (config, modelos Pydantic,
  dados, análise, vetores, log, cliente LLM, API FastAPI). Tabela de camadas
  no [`README.md`](README.md).
- [`notebooks/01-eda.ipynb`](notebooks/01-eda.ipynb) — exploração de dados (D1).
- `data/` — `amostra/` (200 linhas versionadas) e `fixtures/` (respostas do
  modelo gravadas p/ modo offline) são versionados; `raw/` não é.
- `tests/` — pytest sobre `src/ams`, nunca toca rede (69 testes).
- [`agent-spec.md`](agent-spec.md) — **documento vivo**: cresce uma seção
  por laboratório/disciplina (PEAS, dimensões do ambiente, tipo de agente,
  formulação por busca, ...). É o principal artefato de entrega do curso —
  cada seção tem um comentário HTML com as perguntas que a guiam e uma linha
  "quando se preenche".
- `D0N/` (ex.: [`D02/`](D02/)) — uma pasta por disciplina, com uma subpasta
  por laboratório (`D2-01-...`, `D2-02-...`). Ver [`D02/CLAUDE.md`](D02/CLAUDE.md)
  para o padrão dos laboratórios de busca em andamento.

## Como rodar

```powershell
.venv\Scripts\python.exe scripts\baixar-dados.py      # baixa o dataset (opcional — já tem amostra)
.venv\Scripts\python.exe -m ams.cliente_llm            # avalia 20 ordens de serviço
.venv\Scripts\python.exe -m pytest                     # 69 testes, sem rede
uvicorn ams.api:app --reload                            # API local, /docs
```

Gerenciador de pacotes é `uv` (`uv sync` sincroniza do `uv.lock`). Sem a
chave do Gemini no `.env`, o cliente roda em modo offline
(`AMS_MODO_OFFLINE=1`) lendo `data/fixtures/` — mesma validação, mesmo log.

## Convenção de branches

- `feature/D0X_EY` — uma branch por disciplina+encontro (ex.:
  `feature/D02_E04` = disciplina 2, encontro 4). É onde o trabalho de cada
  laboratório acontece.
- `uv-setup` — branch de infraestrutura (migração do projeto para `uv`),
  paralela ao trabalho de disciplina.
- `main` — só recebe merge ao final do ciclo de trabalho; durante o dia as
  branches de feature ficam à frente dela.
- `CLAUDE.md` (este arquivo e os das subpastas) viaja junto nas branches de
  trabalho (`feature/D0X_EY`, `uv-setup`); levar para `main` é decisão
  separada do autor, feita junto com o resto do commit do dia.

## Fluxo de entrega para `main`

`main` guarda a estrutura inicial que o professor passou (sem `uv`, sem
`CLAUDE.md`) — o trabalho de cada disciplina acontece em
`feature/D0X_EY`, mas só uma branch de entrega, criada a partir de `main`,
abre PR pra lá.

1. Trabalhe normalmente em `feature/D0X_EY` (criada a partir de `uv-setup`).
2. Pra entregar, crie uma branch a partir de `main`:
   `git checkout main && git checkout -b entrega/D0X_EY`.
3. Traga só o código do laboratório/disciplina:
   `git checkout feature/D0X_EY -- D0X/` (mais qualquer arquivo relacionado
   fora de `D0X/`, como seções novas do `agent-spec.md` — caso a caso).
4. Remova explicitamente o que não deve ir (o `checkout -- path` não apaga
   sozinho o que falta no destino): `CLAUDE.md`/`D0X/CLAUDE.md`,
   anotações de trabalho já aplicadas e obsoletas, `pyproject.toml`/
   `uv.lock` e qualquer mudança em `scripts/`/`README.md` que só fale de
   `uv`.
5. Confira com `git status` / `git diff --cached --stat` antes de commitar.
6. Abra o PR de `entrega/D0X_EY` para `main`.

Nunca faça merge de `main` em `uv-setup` — são linhas de história
separadas de propósito (`uv-setup` carrega a migração; `main` não).

`entrega/D02` foi o caso retroativo: cobriu a disciplina inteira de uma vez
(D2-01 a D2-09), já que esse padrão por encontro só passou a valer a partir
da D3.

## Lições aprendidas e convenções por disciplina

Lições específicas de cada disciplina (ex.: os bugs comuns dos laboratórios
de busca do D02) ficam no `CLAUDE.md` daquela pasta — ver
[`D02/CLAUDE.md`](D02/CLAUDE.md) — para não carregar em sessões que não
mexem ali.
