---
name: entrega
description: Prepara a branch entrega/D0X_EY a partir de main com só o conteúdo do laboratório/disciplina, seguindo o fluxo de entrega do CLAUDE.md, e para antes do commit para conferência. Use quando o autor disser "entrega", "preparar entrega", "/entrega D03_E01" ou quiser abrir PR para main.
argument-hint: D0X_EY (ex.: D03_E01)
---

# Fluxo de entrega para `main`

Argumento: `$ARGUMENTS` no formato `D0X_EY` (ex.: `D03_E01`). Se vier vazio,
deduza da branch atual (`feature/D0X_EY`) e confirme com o autor.

Regras de fundo: ver "Fluxo de entrega para `main`" no `CLAUDE.md` da raiz.
**Nunca** faça merge de `main` em `uv-setup` nem de `uv-setup` em `main`.

## Passos

1. **Pré-checagem** (pare e pergunte se algo falhar):
   - `git status`: a `feature/D0X_EY` não pode ter mudanças não commitadas
     que deveriam ir na entrega. Se houver, liste e pergunte se commita antes.
   - Rode `.venv\Scripts\python.exe -m pytest` na feature branch. Testes
     vermelhos bloqueiam.
   - Confirme que `entrega/D0X_EY` ainda não existe (`git branch --list`).
     Se existir, pergunte: atualizar a existente ou abortar.

2. **Levantar o que entra.** Compare a feature com `main`:
   `git diff --stat main...feature/D0X_EY`. Monte duas listas e **mostre ao
   autor antes de continuar**:
   - **Entra:** a pasta `D0X/` (ou só os labs do encontro, se o autor
     pedir), seções novas/alteradas do `agent-spec.md`, e outros arquivos
     fora de `D0X/` que o lab exige (caso a caso — pergunte se houver dúvida).
   - **Não entra:** `CLAUDE.md` e `D0X/CLAUDE.md`, `.claude/`,
     `extras-pessoal/`, `pyproject.toml`, `uv.lock`, mudanças em `scripts/`
     ou `README.md` que só falem de `uv`, anotações de trabalho obsoletas.

3. **Criar a branch:**
   `git checkout main && git checkout -b entrega/D0X_EY`

4. **Trazer o conteúdo:** `git checkout feature/D0X_EY -- <caminhos da lista "Entra">`.

5. **Remover explicitamente o que não vai** (o `checkout -- path` não apaga
   sozinho): `git rm --cached -r` / `git rm` de cada item da lista "Não
   entra" que tenha vindo junto dentro de `D0X/` (ex.: `D0X/CLAUDE.md`,
   `__pycache__/`).

6. **Conferência final** — mostre ao autor:
   - `git status`
   - `git diff --cached --stat`
   - Um grep de segurança no staged: nada com `CLAUDE.md`, `.claude/`,
     `extras-pessoal/`, `uv.lock`, `pyproject.toml`.

   Sugira rodar o agente `ams-critico` sobre o staged antes de commitar.

7. **Parar aqui.** Não commite, não dê push e não abra PR sem o autor pedir
   explicitamente. Quando ele pedir: commit com mensagem curta em português
   ("Entrega D0X_EY: ..."), push e `gh pr create --base main`.

Ao final, volte para `feature/D0X_EY` só se o autor pedir.
