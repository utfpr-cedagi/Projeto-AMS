"""Gera/atualiza o vault Obsidian do Projeto-AMS em extras-pessoal/obsidian/.

Uso (da raiz do repositório):
    .venv\\Scripts\\python.exe extras-pessoal\\scripts\\gerar_vault.py [--dry-run]

Regras:
- Só sobrescreve notas com `gerado: true` no frontmatter; notas escritas à
  mão (sem essa marca) nunca são tocadas.
- Texto abaixo da linha `<!-- manual -->` de uma nota gerada é preservado.
- Saída determinística (sem timestamps): rodar duas vezes seguidas não muda
  nada.
- Nunca apaga: notas geradas que não correspondem mais a nada são listadas
  como órfãs no relatório.

Ferramenta pessoal (extras-pessoal/), fora do fluxo de entrega.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path

RAIZ = Path(__file__).resolve().parents[2]
VAULT = RAIZ / "extras-pessoal" / "obsidian"
MARCA_MANUAL = "<!-- manual -->"

# Seção do agent-spec.md -> lab que a preenche (da coluna "Entrega" do
# D02/CLAUDE.md e das mensagens de commit; ajuste à mão quando mudar).
SPEC_PARA_LAB = {
    1: ["D2-01"],
    2: ["D2-02"],
    3: ["D2-08"],
    4: ["D2-01", "D2-08"],
    5: ["D2-08"],
    6: ["D2-07"],
    7: ["D2-03"],
}

# Convenção do CLAUDE.md raiz: de onde cada tipo de branch nasce.
def origem_branch(nome: str) -> str | None:
    if nome.startswith("feature/"):
        return "uv-setup"
    if nome.startswith("entrega/"):
        return "main"
    if nome == "uv-setup":
        return "main"
    return None


# --------------------------------------------------------------------------
# utilidades


def git(*args: str) -> str:
    r = subprocess.run(
        ["git", "-c", "core.quotepath=off", *args],
        cwd=RAIZ,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=True,
    )
    return r.stdout


def slug_branch(nome: str) -> str:
    return nome.replace("/", "-")


def frontmatter(campos: dict) -> str:
    linhas = ["---", "gerado: true"]
    for k, v in campos.items():
        if isinstance(v, list):
            if not v:
                linhas.append(f"{k}: []")
            else:
                linhas.append(f"{k}:")
                linhas.extend(f"  - {yaml_str(x)}" for x in v)
        else:
            linhas.append(f"{k}: {yaml_str(v)}")
    linhas.append("---")
    return "\n".join(linhas) + "\n"


def yaml_str(v) -> str:
    s = str(v)
    if s == "" or re.search(r"[:#\[\]{}&*!|>'\"%@`,]", s) or s.strip() != s:
        return '"' + s.replace("\\", "\\\\").replace('"', '\\"') + '"'
    return s


@dataclass
class Relatorio:
    criadas: list[str] = field(default_factory=list)
    atualizadas: list[str] = field(default_factory=list)
    sem_mudanca: list[str] = field(default_factory=list)
    manuais: list[str] = field(default_factory=list)
    escritas: set[Path] = field(default_factory=set)


def escrever(rel: Relatorio, caminho: Path, conteudo: str, dry: bool) -> None:
    rel.escritas.add(caminho.resolve())
    nome = caminho.relative_to(VAULT).as_posix()
    if caminho.exists():
        atual = caminho.read_text(encoding="utf-8")
        if not re.match(r"^---\n(?:.*\n)*?gerado: true\n", atual):
            rel.manuais.append(nome)
            return
        if MARCA_MANUAL in atual:
            cauda = atual.split(MARCA_MANUAL, 1)[1]
            conteudo = conteudo.split(MARCA_MANUAL, 1)[0] + MARCA_MANUAL + cauda
        if atual == conteudo:
            rel.sem_mudanca.append(nome)
            return
        rel.atualizadas.append(nome)
    else:
        rel.criadas.append(nome)
    if not dry:
        caminho.parent.mkdir(parents=True, exist_ok=True)
        caminho.write_text(conteudo, encoding="utf-8", newline="\n")


def rodape_manual() -> str:
    return f"\n{MARCA_MANUAL}\n"


# --------------------------------------------------------------------------
# coleta


@dataclass
class Lab:
    codigo: str  # D2-01, D3-AO1
    nota: str  # nome da nota (sem .md)
    pasta: Path
    disciplina: str  # D02
    titulo: str = ""
    status: str = ""
    entrega: str = ""
    commits: list[str] = field(default_factory=list)


def coletar_labs() -> dict[str, Lab]:
    labs: dict[str, Lab] = {}
    for disc in sorted(RAIZ.glob("D0[0-9]")):
        if not disc.is_dir():
            continue
        tabela = ler_tabela_labs(disc / "CLAUDE.md")
        for p in sorted(disc.iterdir()):
            if not p.is_dir():
                continue
            m = re.match(r"^(D\d-\d\d)-", p.name)
            if m:
                codigo, nota = m.group(1), p.name
            elif p.name.startswith("AO"):
                codigo = f"D{int(disc.name[1:])}-{p.name}"
                nota = codigo
            else:
                continue
            lab = Lab(codigo=codigo, nota=nota, pasta=p, disciplina=disc.name)
            linha = tabela.get(codigo)
            if linha:
                lab.titulo = linha.get("laboratório", "")
                lab.status = linha.get("status", "")
                lab.entrega = linha.get("entrega", "")
            if not lab.titulo:
                lab.titulo = p.name.split("-", 2)[-1].replace("-", " ") if m else "Atividade Orientada " + p.name
            if not lab.status and disc.name == "D02":
                lab.status = "entregue (entrega/D02)"
            labs[codigo] = lab
    return labs


def ler_tabela_labs(claude_md: Path) -> dict[str, dict[str, str]]:
    if not claude_md.exists():
        return {}
    linhas = claude_md.read_text(encoding="utf-8").splitlines()
    res: dict[str, dict[str, str]] = {}
    cab: list[str] | None = None
    for ln in linhas:
        if not ln.startswith("|"):
            cab = None
            continue
        cels = [c.strip() for c in ln.strip().strip("|").split("|")]
        if cab is None:
            if cels and cels[0].lower() == "pasta":
                cab = [c.lower() for c in cels]
            continue
        if set(ln.replace("|", "").strip()) <= {"-", " "}:
            continue
        m = re.search(r"(D\d-\d\d)", cels[0])
        if m and "ainda não extraído" not in cels[0]:
            res[m.group(1)] = {cab[i]: limpar_md(cels[i]) for i in range(min(len(cab), len(cels)))}
    return res


def limpar_md(s: str) -> str:
    return s.replace("**", "").replace("`", "")


@dataclass
class Secao:
    num: int
    titulo: str
    linha: int
    resumo: list[str]
    quando: str

    @property
    def nota(self) -> str:
        return f"agent-spec-{self.num:02d}-{slug(self.titulo)}"


def slug(s: str) -> str:
    import unicodedata

    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode()
    return re.sub(r"[^A-Za-z0-9]+", "-", s).strip("-")


def secoes_do_spec(texto: str) -> list[Secao]:
    linhas = texto.splitlines()
    cabs = [(i, m) for i, ln in enumerate(linhas) if (m := re.match(r"^## (\d+)\. (.+)$", ln))]
    secoes = []
    for k, (i, m) in enumerate(cabs):
        fim = cabs[k + 1][0] if k + 1 < len(cabs) else len(linhas)
        corpo = linhas[i + 1 : fim]
        resumo, quando, em_coment = [], "", False
        for ln in corpo:
            s = ln.strip()
            if s.startswith("<!--"):
                em_coment = "-->" not in s
                continue
            if em_coment:
                em_coment = "-->" not in s
                continue
            if s.startswith("**Quando se preenche:**"):
                quando = s.replace("**Quando se preenche:**", "").strip()
                continue
            if not s or s == "---" or s.startswith("|"):
                continue
            # rótulos soltos (**Performance:**) e placeholders do modelo ([...])
            if re.fullmatch(r"\*\*[^*]+:?\*\*:?", s) or re.fullmatch(r"\[.*\]", s):
                continue
            if len(resumo) < 4:
                resumo.append(s if len(s) <= 220 else s[:217] + "...")
        secoes.append(Secao(int(m.group(1)), m.group(2).strip(), i + 1, resumo, quando))
    return secoes


@dataclass
class Commit:
    hash: str
    curto: str
    data: str
    autor: str
    assunto: str
    corpo: str
    pais: list[str]
    arquivos: list[str]
    branches: list[str] = field(default_factory=list)
    secoes: list[int] = field(default_factory=list)

    @property
    def nota(self) -> str:
        return self.curto


def coletar_commits() -> list[Commit]:
    sep, fim = "\x1f", "\x1e"
    saida = git(
        "log", "--all", "--date=short", "--name-only", "--no-renames",
        f"--format={fim}%H{sep}%h{sep}%ad{sep}%an{sep}%P{sep}%s{sep}%b{sep}",
    )
    commits = []
    for bloco in saida.split(fim)[1:]:
        h, curto, data, autor, pais, assunto, corpo, resto = bloco.split(sep, 7)
        arquivos = [a for a in resto.strip().splitlines() if a.strip()]
        commits.append(Commit(h, curto[:7], data, autor, assunto, corpo.strip(), pais.split(), arquivos))
    return commits


def branches_locais() -> list[str]:
    return [b.strip() for b in git("branch", "--format=%(refname:short)").splitlines() if b.strip()]


def secoes_tocadas(c: Commit) -> list[int]:
    if "agent-spec.md" not in c.arquivos:
        return []
    try:
        diff = git("show", "-U0", "--format=", "--first-parent", c.hash, "--", "agent-spec.md")
        texto = git("show", f"{c.hash}:agent-spec.md")
    except subprocess.CalledProcessError:
        return []
    secs = secoes_do_spec(texto)
    if not secs:
        return []
    tocadas = set()
    for m in re.finditer(r"^@@ -\d+(?:,\d+)? \+(\d+)(?:,(\d+))? @@", diff, re.M):
        ini, n = int(m.group(1)), int(m.group(2) or 1)
        for ln in range(ini, ini + max(n, 1)):
            antes = [s for s in secs if s.linha <= ln]
            if antes:
                tocadas.add(antes[-1].num)
    return sorted(tocadas)


# --------------------------------------------------------------------------
# mapeamento arquivo -> link


AREAS = {
    "src-ams": ("src/ams/", "Pacote instalável `src/ams/` (config, modelos, dados, API...)."),
    "claude-config": (".claude/", "Agentes e skills do Claude Code (`.claude/`)."),
    "extras-pessoal": ("extras-pessoal/", "Produção pessoal fora do fluxo de entrega."),
    "testes": ("tests/", "Suíte pytest sobre `src/ams` (sem rede)."),
    "dados": ("data/", "Amostra, fixtures e casos do dataset AI4I 2020."),
    "notebooks": ("notebooks/", "Notebooks de exploração (EDA da D1)."),
}


def links_do_arquivo(arq: str, labs: dict[str, Lab]) -> str | None:
    m = re.match(r"^D0\d/(D\d-\d\d)", arq)
    if m and m.group(1) in labs:
        return labs[m.group(1)].nota
    m = re.match(r"^D0(\d)/(AO\d+)/", arq)
    if m:
        cod = f"D{m.group(1)}-{m.group(2)}"
        if cod in labs:
            return labs[cod].nota
    m = re.match(r"^(D0\d)/", arq)
    if m and (RAIZ / m.group(1)).is_dir():
        return m.group(1)
    if arq == "agent-spec.md":
        return "agent-spec"
    for nota, (prefixo, _) in AREAS.items():
        if arq.startswith(prefixo):
            return nota
    return None


# --------------------------------------------------------------------------
# geração


def gerar(dry: bool) -> Relatorio:
    rel = Relatorio()
    labs = coletar_labs()
    spec_txt = (RAIZ / "agent-spec.md").read_text(encoding="utf-8")
    secoes = secoes_do_spec(spec_txt)
    sec_por_num = {s.num: s for s in secoes}
    commits = coletar_commits()
    branches = branches_locais()

    # branches que contêm cada commit
    por_branch: dict[str, set[str]] = {}
    for b in branches:
        por_branch[b] = set(git("rev-list", b).split())
    for c in commits:
        c.branches = [b for b in branches if c.hash in por_branch[b]]
        c.secoes = secoes_tocadas(c)
        for arq in c.arquivos:
            alvo = links_do_arquivo(arq, labs)
            for lab in labs.values():
                if alvo == lab.nota and c.curto not in lab.commits:
                    lab.commits.append(c.curto)
    commits_por_lab = {lab.nota: lab.commits for lab in labs.values()}

    # ---- commits
    for c in commits:
        alvos = []
        for arq in c.arquivos:
            alvo = links_do_arquivo(arq, labs)
            if alvo and alvo not in alvos:
                alvos.append(alvo)
        links_spec = [sec_por_num[n].nota for n in c.secoes if n in sec_por_num]
        if links_spec and "agent-spec" in alvos:
            alvos.remove("agent-spec")
        tags = ["commit"]
        discs = sorted({a[:3] for a in alvos if re.match(r"^D\d-", a)})
        tags += [f"disciplina/D0{d[1]}" for d in discs]
        if len(c.pais) > 1:
            tags.append("merge")
        corpo = [
            frontmatter({
                "hash": c.hash, "data": c.data, "autor": c.autor,
                "branches": c.branches, "tags": tags,
            }),
            f"# {c.curto} — {c.assunto}\n",
            f"**Data:** {c.data} · **Autor:** {c.autor}",
            "**Branches:** " + (", ".join(f"[[{slug_branch(b)}]]" for b in c.branches) or "—"),
        ]
        if c.pais:
            corpo.append("**Pais:** " + ", ".join(f"[[{p[:7]}]]" for p in c.pais))
        corpo.append("")
        if c.corpo:
            corpo += [c.corpo, ""]
        if alvos or links_spec:
            corpo.append("## Relacionado\n")
            corpo += [f"- [[{a}]]" for a in alvos + links_spec]
            corpo.append("")
        if c.arquivos:
            corpo.append(f"## Arquivos ({len(c.arquivos)})\n")
            mostrar = c.arquivos[:60]
            corpo += [f"- `{a}`" for a in mostrar]
            if len(c.arquivos) > 60:
                corpo.append(f"- … e mais {len(c.arquivos) - 60}")
            corpo.append("")
        mes = c.data[:7]
        escrever(rel, VAULT / "commits" / mes / f"{c.curto}.md", "\n".join(corpo) + rodape_manual(), dry)

    # ---- labs
    for lab in labs.values():
        arquivos = sorted(
            p.relative_to(RAIZ).as_posix() + ("/" if p.is_dir() else "")
            for p in lab.pasta.iterdir()
            if p.name != "__pycache__"
        )
        secs = [s for s in secoes if lab.codigo in SPEC_PARA_LAB.get(s.num, [])]
        corpo = [
            frontmatter({
                "disciplina": lab.disciplina, "codigo": lab.codigo,
                "status": lab.status or "—", "entrega": lab.entrega or "—",
                "tags": ["lab", f"disciplina/{lab.disciplina}"],
            }),
            f"# {lab.codigo} — {lab.titulo}\n",
            f"Disciplina: [[{lab.disciplina}]] · Pasta: `{lab.pasta.relative_to(RAIZ).as_posix()}/`",
            f"**Status:** {lab.status or '—'}",
        ]
        if lab.entrega:
            corpo.append(f"**Entrega:** {lab.entrega}")
        corpo.append("")
        if secs:
            corpo.append("## Seções do agent-spec que preenche\n")
            corpo += [f"- [[{s.nota}|§{s.num}. {s.titulo}]]" for s in secs]
            corpo.append("")
        corpo.append("## Arquivos\n")
        corpo += [f"- `{a}`" for a in arquivos]
        corpo.append("")
        cs = commits_por_lab[lab.nota]
        if cs:
            corpo.append(f"## Commits ({len(cs)})\n")
            ordem = {c.curto: c for c in commits}
            corpo += [f"- {ordem[h].data} [[{h}]] — {ordem[h].assunto}" for h in cs]
            corpo.append("")
        escrever(rel, VAULT / "labs" / f"{lab.nota}.md", "\n".join(corpo) + rodape_manual(), dry)

    # ---- spec
    for s in secoes:
        labs_sec = [labs[c] for c in SPEC_PARA_LAB.get(s.num, []) if c in labs]
        cs = [c for c in commits if s.num in c.secoes]
        corpo = [
            frontmatter({
                "secao": s.num, "aliases": [f"§{s.num}. {s.titulo}"], "tags": ["spec"],
            }),
            f"# §{s.num}. {s.titulo}\n",
            "Parte de [[agent-spec]].",
        ]
        if s.quando:
            corpo.append(f"**Quando se preenche:** {s.quando}")
        corpo.append("")
        if s.resumo:
            corpo.append("## Resumo (primeiras linhas)\n")
            corpo += [f"> {ln}" for ln in s.resumo]
            corpo.append("")
        if labs_sec:
            corpo.append("## Preenchida em\n")
            corpo += [f"- [[{l.nota}]]" for l in labs_sec]
            corpo.append("")
        if cs:
            corpo.append(f"## Commits que alteraram ({len(cs)})\n")
            corpo += [f"- {c.data} [[{c.curto}]] — {c.assunto}" for c in cs]
            corpo.append("")
        escrever(rel, VAULT / "spec" / f"{s.nota}.md", "\n".join(corpo) + rodape_manual(), dry)

    corpo = [
        frontmatter({"tags": ["spec"]}),
        "# agent-spec.md\n",
        "Documento vivo do AMS — cresce uma seção por laboratório/disciplina.\n",
        "## Seções\n",
    ]
    corpo += [f"- [[{s.nota}|§{s.num}. {s.titulo}]]" for s in secoes]
    escrever(rel, VAULT / "spec" / "agent-spec.md", "\n".join(corpo) + "\n" + rodape_manual(), dry)

    # ---- branches
    hashes_branch = {b: por_branch[b] for b in branches}
    curto = {c.hash: c for c in commits}
    for b in branches:
        outros = set().union(*(hashes_branch[o] for o in branches if o != b)) if len(branches) > 1 else set()
        exclusivos = [curto[h] for h in git("rev-list", b).split() if h not in outros and h in curto]
        ponta = curto.get(git("rev-parse", b).strip())
        org = origem_branch(b)
        corpo = [
            frontmatter({"branch": b, "origem": org or "—", "tags": ["branch"]}),
            f"# {b}\n",
        ]
        if org:
            corpo.append(f"Nasce de [[{slug_branch(org)}]] (convenção do CLAUDE.md).")
        if ponta:
            corpo.append(f"**Ponta:** [[{ponta.curto}]] — {ponta.assunto} ({ponta.data})")
        corpo.append(f"**Commits alcançáveis:** {len(hashes_branch[b])}\n")
        if exclusivos:
            corpo.append(f"## Commits só desta branch ({len(exclusivos)})\n")
            corpo += [f"- {c.data} [[{c.curto}]] — {c.assunto}" for c in exclusivos]
            corpo.append("")
        escrever(rel, VAULT / "branches" / f"{slug_branch(b)}.md", "\n".join(corpo) + rodape_manual(), dry)

    # ---- disciplinas
    discs = sorted({l.disciplina for l in labs.values()})
    for d in discs:
        ls = [l for l in labs.values() if l.disciplina == d]
        corpo = [
            frontmatter({"tags": [f"disciplina/{d}"]}),
            f"# {d}\n",
            f"Resumo e lições em `{d}/CLAUDE.md`. Voltar ao [[00-Indice]].\n",
            "| Lab | Título | Status |",
            "|---|---|---|",
        ]
        corpo += [f"| [[{l.nota}\\|{l.codigo}]] | {l.titulo} | {l.status or '—'} |" for l in ls]
        escrever(rel, VAULT / "disciplinas" / f"{d}.md", "\n".join(corpo) + "\n" + rodape_manual(), dry)

    # ---- áreas fora das disciplinas
    for nota, (prefixo, desc) in AREAS.items():
        cs = [c for c in commits if any(a.startswith(prefixo) for a in c.arquivos)]
        corpo = [frontmatter({"tags": ["area"]}), f"# {prefixo}\n", desc, ""]
        if cs:
            corpo.append(f"## Commits ({len(cs)})\n")
            corpo += [f"- {c.data} [[{c.curto}]] — {c.assunto}" for c in cs]
            corpo.append("")
        escrever(rel, VAULT / "areas" / f"{nota}.md", "\n".join(corpo) + rodape_manual(), dry)

    # ---- índice
    corpo = [
        frontmatter({"tags": ["indice"]}),
        "# AMS — Índice do vault\n",
        "Vault gerado por `extras-pessoal/scripts/gerar_vault.py` "
        "(skill `/obsidian-sync`). Notas com `gerado: true` são reescritas; "
        f"escreva à mão abaixo de `{MARCA_MANUAL}` ou em notas sem essa marca.\n",
        "## Disciplinas\n",
        *[f"- [[{d}]]" for d in discs],
        "",
        "## Documento vivo\n",
        "- [[agent-spec]]",
        "",
        "## Branches\n",
        *[f"- [[{slug_branch(b)}]]" for b in branches],
        "",
        "## Áreas\n",
        *[f"- [[{n}]]" for n in AREAS],
        "",
        "## Decisões\n",
        "- pasta `decisoes/` (notas à mão, tag `#decisao`)",
        "",
        f"## Últimos commits\n",
        *[f"- {c.data} [[{c.curto}]] — {c.assunto}" for c in commits[:10]],
        "",
    ]
    escrever(rel, VAULT / "00-Indice.md", "\n".join(corpo) + rodape_manual(), dry)
    return rel


def orfas(rel: Relatorio) -> list[str]:
    res = []
    if not VAULT.exists():
        return res
    for p in VAULT.rglob("*.md"):
        if ".obsidian" in p.parts or p.resolve() in rel.escritas:
            continue
        txt = p.read_text(encoding="utf-8")
        if re.match(r"^---\n(?:.*\n)*?gerado: true\n", txt):
            res.append(p.relative_to(VAULT).as_posix())
    return sorted(res)


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--dry-run", action="store_true", help="só mostra o que faria")
    a = ap.parse_args()
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    rel = gerar(a.dry_run)
    pref = "[dry-run] " if a.dry_run else ""
    print(f"{pref}criadas: {len(rel.criadas)}")
    print(f"{pref}atualizadas: {len(rel.atualizadas)}")
    for n in rel.atualizadas:
        print(f"    ~ {n}")
    print(f"{pref}sem mudança: {len(rel.sem_mudanca)}")
    print(f"{pref}manuais (não tocadas): {len(rel.manuais)}")
    for n in rel.manuais:
        print(f"    = {n}")
    o = orfas(rel)
    print(f"{pref}órfãs (geradas, sem fonte — revise à mão): {len(o)}")
    for n in o:
        print(f"    ? {n}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
