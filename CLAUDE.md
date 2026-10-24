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

## Lições aprendidas e convenções por disciplina

Lições específicas de cada disciplina (ex.: os bugs comuns dos laboratórios
de busca do D02) ficam no `CLAUDE.md` daquela pasta — ver
[`D02/CLAUDE.md`](D02/CLAUDE.md) — para não carregar em sessões que não
mexem ali.
