"""Encena um rastro gravado de agente — sem cliente de API e sem rede.

Este programa é a DEMONSTRAÇÃO: lê o registro que a própria aplicação fez
do laço (o rastro, em JSON) e o apresenta rodada a rodada, com pausa para
o professor conduzir. Ele NÃO importa biblioteca de rede nenhuma e NÃO
instancia cliente de modelo — o rastro é o registro do que aconteceu, e
apresentá-lo é leitura de arquivo, não chamada.

Uso (da pasta da demonstração):

    python encenar.py                       # o rastro padrão (completo.json)
    python encenar.py rastros/sem-memoria.json
    python encenar.py --tudo                # sem pausas entre rodadas

Serve às DUAS demonstrações (demo-01 e demo-02): as duas pastas carregam
cópias byte a byte idênticas deste arquivo, e o teste de cada uma confere
o comportamento. Mudou aqui, copie para a outra pasta no mesmo passo.

Depende só da biblioteca padrão. `rich`, se estiver instalado, deixa o
rastro legível projetado — sem ele, o programa degrada para texto simples
em vez de falhar (a demonstração não pode depender de dependência).
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

try:
    from rich.console import Console

    _console: Console | None = Console()
except ImportError:            # pragma: no cover - caminho sem rich
    _console = None

PADRAO = Path(__file__).resolve().parent / "rastros" / "completo.json"

# Os cinco campos da rodada (slide D2-E4 50): o rótulo em português e, entre
# parênteses, o nome técnico — na primeira aparição o professor nomeia em
# voz alta, para a turma reconhecer em D10.
ROTULOS = {
    "entrada": "A entrada da rodada (a percepção)",
    "historico": "O histórico acumulado (a sequência de percepções)",
    "chamada": "O pedido de ferramenta — execute_tool (a ação escolhida)",
    "retorno": "O retorno da ferramenta (a observação do ambiente)",
    "tokens": "Os contadores de tokens (usage — o custo da deliberação)",
}


def _mostrar(titulo: str, linhas: list[str]) -> None:
    """Uma caixa por bloco — com rich quando há, texto simples quando não."""
    if _console is not None:
        _console.print(f"[bold cyan]{titulo}[/bold cyan]")
        for linha in linhas:
            _console.print(f"  {linha}")
        _console.print()
        return
    print(f"\n=== {titulo} ===")
    for linha in linhas:
        print(f"  {linha}")


def _pausar(rodada_atual: int, total: int, pausar: bool) -> None:
    if not pausar:
        return
    try:
        input(f"\n— rodada {rodada_atual} de {total} · Enter para a "
              "próxima (Ctrl+C encerra)… ")
    except EOFError:            # sem terminal interativo (teste, pipe)
        print()


def _campo(registro: dict, chave: str, vazio: str = "(nada)") -> str:
    valor = registro.get(chave)
    if valor is None:
        return vazio
    if isinstance(valor, (dict, list)):
        return json.dumps(valor, ensure_ascii=False)
    return str(valor)


def _rodada(registro: dict) -> None:
    """Os cinco campos de UMA rodada, na ordem da tabela do slide 50."""
    agente = registro.get("invoke_agent", {})
    ferramenta = registro.get("execute_tool")
    _mostrar(f"RODADA {registro.get('numero')} — invoke_agent "
             "(uma chamada ao modelo)", [
        f"{ROTULOS['entrada']}: "
        f"{_campo(agente, 'entrada_da_rodada')}",
        f"{ROTULOS['historico']}: "
        f"{len(agente.get('historico_acumulado', []))} item(ns) — "
        f"{_campo(agente, 'historico_acumulado')}",
        f"Registro de ferramentas enviado nesta chamada: "
        f"{_campo(agente, 'registro_de_ferramentas')}",
    ])
    if ferramenta:
        chamada = ferramenta.get("chamada", {})
        _mostrar(ROTULOS["chamada"], [
            f"o PROGRAMA executa — o modelo só pediu: "
            f"{chamada.get('nome')}({_campo(chamada, 'argumentos')})",
        ])
        _mostrar(ROTULOS["retorno"], [
            _campo(ferramenta, "retorno"),
        ])
    else:
        _mostrar(ROTULOS["chamada"], [
            "(nenhuma — nesta rodada o modelo não pediu ferramenta)",
        ])
    usage = registro.get("usage", {})
    _mostrar(ROTULOS["tokens"], [
        f"promptTokenCount: {usage.get('promptTokenCount')} · "
        f"candidatesTokenCount: {usage.get('candidatesTokenCount')} · "
        f"totalTokenCount: {usage.get('totalTokenCount')}",
    ])
    raciocinio = registro.get("raciocinio")
    if raciocinio:
        _mostrar("O texto de raciocínio do modelo", [raciocinio])


def encenar(rastro: dict, pausar: bool = True) -> None:
    """Apresenta o rastro inteiro, rodada a rodada, com pausas."""
    meta = [
        f"Demonstração: {rastro.get('demonstracao')}",
        f"Pedido inicial: {rastro.get('pedido_inicial')}",
        f"Ferramentas no registro: "
        f"{_campo(rastro, 'ferramentas')}",
        f"Teto de rodadas: {rastro.get('teto_de_rodadas')}",
    ]
    _mostrar("O rastro gravado", meta)
    rodadas = rastro.get("rodadas", [])
    total = len(rodadas)
    for indice, registro in enumerate(rodadas):
        _rodada(registro)
        if indice < total - 1:
            _pausar(registro.get("numero", indice + 1), total, pausar)
    _fecho(rastro)


def _fecho(rastro: dict) -> None:
    """A conta de custo que o slide D2-E4 49 pede visível."""
    rodadas = rastro.get("rodadas", [])
    tokens = sum(int(r.get("usage", {}).get("totalTokenCount") or 0)
                 for r in rodadas)
    resposta = rastro.get("resposta_final")
    if resposta:
        termino = (f"resposta final na rodada {resposta.get('rodada')} — "
                   f"o laço terminou")
    else:
        termino = (f"sem resposta final — o laço parou por TETO DE RODADAS "
                   f"({rastro.get('teto_de_rodadas')})")
    linhas = [
        f"Rodadas chamadas ao modelo: {len(rodadas)}",
        f"Total de tokens: {tokens}",
        f"Como terminou: {termino}",
    ]
    if resposta and resposta.get("texto"):
        linhas.append(f"Texto final: {resposta['texto']}")
    _mostrar("TOTAL — a conta da demonstração", linhas)


def main(argv: list[str] | None = None) -> int:
    leitor = argparse.ArgumentParser(
        description="Encena um rastro gravado de agente (sem rede).")
    leitor.add_argument("rastro", nargs="?", default=None,
                        help=f"caminho do JSON (padrão: {PADRAO.name})")
    leitor.add_argument("--tudo", action="store_true",
                        help="sem pausas entre rodadas")
    argumentos = leitor.parse_args(argv)

    caminho = Path(argumentos.rastro) if argumentos.rastro else PADRAO
    if not caminho.is_file():
        print(f"ERRO: rastro não encontrado: {caminho}", file=sys.stderr)
        print("O que fazer: rode da pasta da demonstração, ou passe o "
              "caminho — ex.: python encenar.py rastros/completo.json",
              file=sys.stderr)
        return 1
    rastro = json.loads(caminho.read_text(encoding="utf-8"))
    encenar(rastro, pausar=not argumentos.tudo)
    return 0


if __name__ == "__main__":
    sys.exit(main())
