"""Fixtures usadas só por `test_gerador_casos.py` (ferramenta pessoal, fora
da suíte oficial em `tests/`).

Cópia mínima de `tests/conftest.py`: só `LINHA_VALIDA` e `gerar_csv`, que é
tudo que este teste importa de lá.
"""

from __future__ import annotations

import csv
import io
from pathlib import Path

# Uma linha válida canônica, na forma das colunas originais do CSV do UCI
LINHA_VALIDA = {
    "UDI": "1",
    "Product ID": "M14860",
    "Type": "M",
    "Air temperature [K]": "298.1",
    "Process temperature [K]": "308.6",
    "Rotational speed [rpm]": "1551",
    "Torque [Nm]": "42.8",
    "Tool wear [min]": "0",
    "Machine failure": "0",
    "TWF": "0",
    "HDF": "0",
    "PWF": "0",
    "OSF": "0",
    "RNF": "0",
}

COLUNAS_ORIGINAIS = list(LINHA_VALIDA)


def gerar_csv(linhas: list[dict[str, str]], caminho: Path) -> Path:
    """Grava um CSV de teste com as colunas originais do dataset e BOM UTF-8."""
    buffer = io.StringIO()
    escritor = csv.DictWriter(buffer, fieldnames=COLUNAS_ORIGINAIS)
    escritor.writeheader()
    escritor.writerows(linhas)
    # utf-8-sig grava com BOM, imitando o arquivo oficial do UCI
    caminho.write_text(buffer.getvalue(), encoding="utf-8-sig")
    return caminho
