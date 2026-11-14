---
name: obsidian-sync
description: Gera ou atualiza o vault Obsidian do Projeto-AMS em extras-pessoal/obsidian/ — notas por disciplina, laboratório, seção do agent-spec, branch e commit, ligadas por [[links]], para visualizar histórico e relações no grafo do Obsidian. Use quando o autor pedir "atualiza o obsidian", "sincroniza o vault" ou ao fechar um laboratório/disciplina.
---

# Sincronizar o vault Obsidian

Vault: `extras-pessoal/obsidian/` (versionado, fora das entregas pela regra
do `extras-pessoal/`). Abra essa pasta como vault no Obsidian.

## Estrutura

```
extras-pessoal/obsidian/
  00-Indice.md                 # MOC: links para disciplinas, spec, branches
  disciplinas/D02.md, D03.md   # resumo + tabela de labs (do D0N/CLAUDE.md)
  labs/D3-01-vetores-do-meu-dominio.md, ...
  spec/agent-spec-§1-PEAS.md, ...  # uma nota por seção do agent-spec.md
  branches/feature-D03_E01.md, uv-setup.md, main.md, entrega-D02.md
  commits/AAAA-MM/<hash7>.md   # uma nota por commit
  decisoes/<slug>.md           # decisões/lições (dos CLAUDE.md), à mão
```

## Regras de geração

- **Idempotente:** reexecutar não duplica notas. Notas geradas têm
  frontmatter `gerado: true`; só elas são sobrescritas. Notas sem esse
  campo (escritas à mão no Obsidian) **nunca** são tocadas.
- **Commits:** `git log --all --date=short --format=...` + `--name-only`.
  Cada nota de commit tem frontmatter (`hash`, `data`, `autor`, `branches`,
  `tags`) e corpo com a mensagem e links para os labs/seções/arquivos que
  tocou: um arquivo em `D03/D3-01-*/` → `[[D3-01-vetores-do-meu-dominio]]`;
  `agent-spec.md` → link para a seção alterada, quando der para inferir
  pelo diff; senão `[[agent-spec]]`.
- **Labs:** frontmatter com `disciplina`, `status` (da tabela do
  `D0N/CLAUDE.md`), `entrega`; corpo com links para os arquivos do lab
  (caminho relativo ao repo, em texto) e backlinks dos commits.
- **Spec:** uma nota por `## N. Título` do `agent-spec.md`, com resumo de
  2–4 linhas (não copiar a seção inteira) e link para o lab que a preenche.
- **Branches:** quais commits são exclusivos, de onde nasceu (seguindo a
  convenção do `CLAUDE.md`).
- Tags: `#disciplina/D03`, `#lab`, `#spec`, `#commit`, `#decisao`.
- Use uma script Python temporária no scratchpad da sessão para gerar as
  notas de commit (volume grande); escreva as notas de síntese (índice,
  disciplinas, spec) com cuidado, à mão.

## Ao terminar

Informe quantas notas foram criadas, atualizadas e mantidas (manuais), e
sugira um commit separado só para o vault.
