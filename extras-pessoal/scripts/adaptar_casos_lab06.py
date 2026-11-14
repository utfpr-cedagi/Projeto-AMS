"""Adapta os 30 casos de `casos-lab-06-v2.csv` (D02) ao esquema de colunas
da D03 e monta o conjunto de 60 casos pedido pela AO1.

A AO1 (D03) pede ampliar o conjunto de 30 para ≥60 casos, reaproveitando os
30 já usados em D02 e somando 30 novos (`casos-d03-lote1.csv`). Os dois
arquivos ficaram com esquemas incompatíveis depois do ajuste de
`tipo_maquina`/`idade_meses` orientado pelo professor (ver
`extras-pessoal/data/casos-gerados/FONTE-casos-d03-lote1.md`): em
`casos-lab-06-v2.csv`, `tipo_maquina` ainda é a qualidade real do produto
AI4I (L/M/H); nos lotes gerados por `gerador_casos.py` em diante,
`tipo_maquina` é uma família fictícia e a qualidade real mudou para
`qualidade_produto`.

`casos-lab-06-v2.csv` (D02, já entregue e avaliado na N2) NUNCA é
alterado — este script só lê e produz uma cópia adaptada em outro lugar
(`D03/AO1/dados/`).
"""

from __future__ import annotations

from pathlib import Path

import numpy as np
import pandas as pd

from gerador_casos import FAMILIAS_MAQUINA

# Seed própria, distinta do seed=42 do lote1 — sorteio independente, não
# reaproveitado (nada na lógica exige que sejam iguais ou diferentes; só
# importa que cada um seja fixo e documentado, para reprodutibilidade).
SEED_ADAPTACAO = 99

ENTRADA_CASOS_D02 = Path("D02/D2-06-agente-baseline/adaptacao-ams/casos-lab-06-v2.csv")
ENTRADA_DEPARA_D02 = Path("D02/D2-06-agente-baseline/adaptacao-ams/depara-casos-lab-06-v2.csv")
ENTRADA_CASOS_D03 = Path("extras-pessoal/data/casos-gerados/casos-d03-lote1.csv")
ENTRADA_DEPARA_D03 = Path("extras-pessoal/data/casos-gerados/depara-casos-d03-lote1.csv")

SAIDA_DIR = Path("D03/AO1/dados")
SAIDA_ADAPTADO = SAIDA_DIR / "casos-lab06-adaptado-d3.csv"
SAIDA_CASOS_60 = SAIDA_DIR / "casos-60.csv"
SAIDA_DEPARA_60 = SAIDA_DIR / "depara-60.csv"


def adaptar_casos_d02(caminho: Path | str, seed: int = SEED_ADAPTACAO) -> pd.DataFrame:
    """Lê `casos-lab-06-v2.csv` e devolve uma cópia no esquema da D03:
    `tipo_maquina` vira família fictícia (mesma lista de
    `gerador_casos.FAMILIAS_MAQUINA`), o L/M/H real migra para
    `qualidade_produto`, e `idade_meses` é removida."""
    quadro = pd.read_csv(caminho, encoding="utf-8-sig")
    rng = np.random.default_rng(seed)
    quadro = quadro.rename(columns={"tipo_maquina": "qualidade_produto"})
    quadro.insert(2, "tipo_maquina", rng.choice(FAMILIAS_MAQUINA, size=len(quadro)))
    return quadro.drop(columns=["idade_meses"])


def montar_conjunto_ao1() -> None:
    """Gera os três arquivos de `D03/AO1/dados/`: os 30 de D02 adaptados,
    o conjunto de 60 (D02 adaptado + os 30 novos de D03) e o de-para
    combinado."""
    adaptado = adaptar_casos_d02(ENTRADA_CASOS_D02)
    novos = pd.read_csv(ENTRADA_CASOS_D03, encoding="utf-8-sig")

    colunas_em_comum = list(adaptado.columns)
    if list(novos.columns) != colunas_em_comum:
        raise ValueError(
            f"colunas de {ENTRADA_CASOS_D03} não batem com o esquema adaptado: "
            f"{list(novos.columns)} != {colunas_em_comum}"
        )

    casos_60 = pd.concat([adaptado, novos], ignore_index=True)
    if casos_60["id_caso"].duplicated().any():
        raise ValueError("id_caso duplicado entre os dois lotes — confira os prefixos (A.. / B..).")

    depara_d02 = pd.read_csv(ENTRADA_DEPARA_D02, encoding="utf-8-sig")
    depara_d03 = pd.read_csv(ENTRADA_DEPARA_D03, encoding="utf-8-sig")
    depara_60 = pd.concat([depara_d02, depara_d03], ignore_index=True)
    if depara_60["udi"].duplicated().any():
        raise ValueError("UDI real duplicado entre os dois lotes — não deveria acontecer.")

    SAIDA_DIR.mkdir(parents=True, exist_ok=True)
    adaptado.to_csv(SAIDA_ADAPTADO, index=False, encoding="utf-8")
    casos_60.to_csv(SAIDA_CASOS_60, index=False, encoding="utf-8")
    depara_60.to_csv(SAIDA_DEPARA_60, index=False, encoding="utf-8")
    print(f"{len(adaptado)} casos adaptados gravados em {SAIDA_ADAPTADO}")
    print(f"{len(casos_60)} casos gravados em {SAIDA_CASOS_60}")
    print(f"{len(depara_60)} linhas de de-para gravadas em {SAIDA_DEPARA_60}")


if __name__ == "__main__":
    montar_conjunto_ao1()
