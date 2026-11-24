"""Testes de `ams.baseline.carregar_casos`: os dois esquemas de casos.

O esquema da D2 tem `idade_meses`; o da D3 (AO1) não tem. O carregador
precisa ler os dois, sem rede e sem depender dos arquivos do repositório.
"""

from __future__ import annotations

import csv
from pathlib import Path

from ams.baseline import carregar_casos, medir

COMUNS = ["id_caso", "data", "tipo_maquina", "temperatura_c", "vibracao_mm_s",
          "horas_desde_manutencao", "acao_correta", "falhou_depois"]

CASOS = [
    {"id_caso": "C02", "data": "2026-03-02", "tipo_maquina": "PRENSA",
     "temperatura_c": "36.0", "vibracao_mm_s": "8.1", "horas_desde_manutencao": "20",
     "acao_correta": "parar_para_manutencao", "falhou_depois": "1"},
    {"id_caso": "C01", "data": "2026-03-01", "tipo_maquina": "TORNO",
     "temperatura_c": "35.0", "vibracao_mm_s": "2.5", "horas_desde_manutencao": "10",
     "acao_correta": "seguir_operando", "falhou_depois": "0"},
]


def _gravar(caminho: Path, colunas: list[str], linhas: list[dict]) -> Path:
    with caminho.open("w", encoding="utf-8-sig", newline="") as arquivo:
        escritor = csv.DictWriter(arquivo, fieldnames=colunas)
        escritor.writeheader()
        escritor.writerows(linhas)
    return caminho


def test_esquema_d3_sem_idade_meses(tmp_path: Path) -> None:
    caminho = _gravar(tmp_path / "d3.csv", COMUNS, CASOS)
    casos = carregar_casos(caminho)
    assert [c["id_caso"] for c in casos] == ["C01", "C02"]   # ordem cronológica
    assert "idade_meses" not in casos[0]
    assert casos[1]["vibracao_mm_s"] == 8.1
    assert casos[1]["falhou_depois"] == 1
    assert medir(caminho)["acerto_geral"] == 1.0


def test_esquema_d2_com_idade_meses(tmp_path: Path) -> None:
    colunas = COMUNS[:3] + ["idade_meses"] + COMUNS[3:]
    linhas = [dict(c, idade_meses="48") for c in CASOS]
    casos = carregar_casos(_gravar(tmp_path / "d2.csv", colunas, linhas))
    assert casos[0]["idade_meses"] == 48   # convertida para int quando existe
