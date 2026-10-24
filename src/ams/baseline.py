"""Agente de linha de base: regras explícitas, sem modelo de linguagem.

Linha de base do Laboratório 06 (D02) para o agente AMS — percepção (o
registro de uma leitura), decisão (regras explícitas com limiares),
ação (a recomendação) e memória (estado interno por família de máquina).
É o número contra o qual o agente baseado em LLM (D10) será comparado:
sem ele, "melhorou" é opinião.

Estrutura (slide 22, D2-E4): `decidir(registro, estado)` com duas
condições — a primeira REATIVA (só a leitura do instante) e a segunda
consultando ESTADO INTERNO (falhas recentes já observadas da mesma
família de máquina). As duas ficam porque o ambiente AMS é parcialmente
observável (`agent-spec.md` §2: falta a descrição da ordem de serviço) —
um ambiente totalmente observável dispensaria o estado interno.

Limiares calibrados contra `D02/D2-06-agente-baseline/casos-lab-06-v2.csv`
(30 casos reais do AI4I2020 — ver `FONTE-casos-lab-06-v2.md` naquela
pasta) e validados em `D02/D2-06-agente-baseline/analise_baseline.md`:
recall da classe "alto" = 0,625, precisão = 0,50, acerto geral = 0,70.
A temperatura absoluta NÃO entrou nos limiares porque, no AI4I2020, ela
não causa nenhum dos quatro modos de falha documentados (só a diferença
processo−ar entra no modo HDF) — o sinal real usado é o desgaste da
ferramenta (`horas_desde_manutencao`), que é o gatilho real do modo TWF.
"""

from __future__ import annotations

import csv
from datetime import date as _date
from pathlib import Path

# --------------------------------------------------------------------------
# Limiares das regras — ver a análise em D02/D2-06-agente-baseline/
# analise_baseline.md para a justificativa de cada valor.
# --------------------------------------------------------------------------
LIMITE_VIBRACAO = 7.0      # mm/s — acima disso, para (separa os 2 extremos
                            # do proxy derivado de RPM/torque do resto)
LIMITE_DESGASTE = 150.0    # horas desde a manutenção — acima disso, para
                            # (zona real de risco do modo TWF: 200-240 min)
FALHAS_PARA_INSPECAO = 2   # falhas observadas da família → inspecionar
JANELA_DIAS = 7             # "recentes" = dentro desta janela


class EstadoDaFrota:
    """O que o agente já observou: falhas por família de máquina, dentro
    de uma janela de dias — sem a janela, duas falhas antigas deixariam a
    família inteira em inspeção para sempre (o agente não sabe o futuro,
    só acumula os desfechos que o ambiente já revelou)."""

    def __init__(self, janela_dias: int = JANELA_DIAS) -> None:
        self._janela = janela_dias
        self._falhas: list[tuple[str, _date]] = []
        self._ultima_data: _date | None = None

    def falhas_recentes(self, familia: str) -> int:
        """Quantas falhas desta família o agente viu, dentro da janela."""
        if self._ultima_data is None:
            return 0
        limite = self._ultima_data.toordinal() - self._janela
        return sum(
            1 for familia_vista, dia in self._falhas
            if familia_vista == familia and dia.toordinal() >= limite
        )

    def registrar_desfecho(self, registro: dict) -> None:
        """O ambiente revela o desfecho do caso (percepção parcialmente
        observável: só se sabe depois). Sem desfecho, nada a registrar."""
        self._ultima_data = _date.fromisoformat(registro["data"])
        if int(registro.get("falhou_depois", 0)) == 1:
            self._falhas.append((registro["tipo_maquina"], self._ultima_data))


def decidir(registro: dict, estado: EstadoDaFrota) -> str:
    """Uma rodada de decisão: percepção entra, ação sai.

    A ordem importa — a primeira condição que casa decide:

    1. Reativa: vibração ou desgaste da ferramenta acima do limiar →
       `parar_para_manutencao` (risco imediato, não espera o estado).
    2. Estado interno: duas ou mais falhas recentes da mesma família de
       máquina → `inspecionar_antes_de_operar` (precaução por padrão
       observado, mesmo sem leitura crítica agora).
    3. Caso contrário → `seguir_operando`.

    Limitação conhecida (ver análise): como só duas variáveis entram na
    condição reativa, falhas reais sem desgaste nem vibração elevados
    (p.ex. causadas por potência fora de faixa) passam despercebidas —
    ponto cego estrutural de um agente de regras com poucas variáveis.
    """
    if registro["vibracao_mm_s"] > LIMITE_VIBRACAO or \
            registro["horas_desde_manutencao"] >= LIMITE_DESGASTE:
        return "parar_para_manutencao"
    if estado.falhas_recentes(registro["tipo_maquina"]) >= FALHAS_PARA_INSPECAO:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"


def carregar_casos(caminho: str | Path) -> list[dict]:
    """Lê um CSV de casos rotulados, em ordem cronológica — a ordem
    importa porque o estado interno se acumula caso a caso. Espera as
    colunas: id_caso, data, tipo_maquina, idade_meses, temperatura_c,
    vibracao_mm_s, horas_desde_manutencao, acao_correta, falhou_depois.
    encoding utf-8-sig: tolera o BOM que o Excel costuma gravar.
    """
    with Path(caminho).open(encoding="utf-8-sig", newline="") as arquivo:
        casos = list(csv.DictReader(arquivo))
    casos.sort(key=lambda registro: registro["data"])
    for registro in casos:
        registro["idade_meses"] = int(registro["idade_meses"])
        registro["temperatura_c"] = float(registro["temperatura_c"])
        registro["vibracao_mm_s"] = float(registro["vibracao_mm_s"])
        registro["horas_desde_manutencao"] = float(registro["horas_desde_manutencao"])
        registro["falhou_depois"] = int(registro["falhou_depois"])
    return casos


def medir(caminho: str | Path) -> dict:
    """Roda o agente sobre os casos rotulados e devolve a métrica primária
    do PEAS (`agent-spec.md` §4: recall da classe "alto" —
    `parar_para_manutencao`), mais precisão da classe "alto" e acerto
    geral como secundárias. É o critério de aceite do Laboratório 06:
    "baseline.py roda sobre 30 casos e devolve a métrica primária".

    Returns:
        Dicionário com `recall_alto`, `precisao_alto`, `acerto_geral`,
        `total` e `erros` (lista de casos em que a decisão divergiu do
        rótulo, para alimentar a análise de onde o agente erra).
    """
    casos = carregar_casos(caminho)
    estado = EstadoDaFrota()
    acertos = 0
    reais_alto = presos_alto = acertos_alto = 0
    erros: list[dict] = []
    for registro in casos:
        decisao = decidir(registro, estado)
        correta = registro["acao_correta"]
        if decisao == correta:
            acertos += 1
        else:
            erros.append({
                "id_caso": registro["id_caso"],
                "decidiu": decisao,
                "correta": correta,
            })
        if correta == "parar_para_manutencao":
            reais_alto += 1
        if decisao == "parar_para_manutencao":
            presos_alto += 1
            if decisao == correta:
                acertos_alto += 1
        estado.registrar_desfecho(registro)
    total = len(casos)
    return {
        "metrica_primaria": "recall da classe alto",
        "recall_alto": acertos_alto / reais_alto if reais_alto else 0.0,
        "precisao_alto": acertos_alto / presos_alto if presos_alto else 0.0,
        "acerto_geral": acertos / total if total else 0.0,
        "total": total,
        "erros": erros,
    }
