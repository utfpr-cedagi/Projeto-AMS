"""Gerador de lotes de casos rotulados a partir do AI4I2020 real.

Generaliza a metodologia usada em `casos-lab-06-v2.csv` (D02, laboratório
06): nunca sorteia casos às cegas — amostra o dataset bruto
(`data/raw/ai4i2020.csv`) em quatro categorias ancoradas nos cinco
gatilhos de falha documentados pela UCI (TWF, HDF, PWF, OSF, RNF; ver
`D02/D2-06-agente-baseline/adaptacao-ams/FONTE-casos-lab-06-v2.md`), para
garantir que todo lote tem casos fáceis, difíceis e atípicos — nunca só
"bonito e inútil".

Toda chamada de `gerar_lote()` devolve, além do CSV de casos no formato
dos laboratórios (`COLUNAS_CASO`), uma tabela de **de-para** (id_caso →
UDI de origem em `data/raw/ai4i2020.csv`). Isso é obrigatório, não
opcional: sem esse rastro, a procedência de cada linha se perde — foi
exatamente o que aconteceu com `casos-lab-06-v2.csv`, cujo de-para teve
que ser reconstruído manualmente, por casamento de colunas contra o
dataset bruto, meses depois.
"""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date, timedelta
from pathlib import Path

import numpy as np
import pandas as pd

from ams import dados

# Limiares dos 4 gatilhos físicos documentados pela UCI (os mesmos usados
# para classificar casos-lab-06-v2.csv — ver FONTE-casos-lab-06-v2.md).
TWF_JANELA = (200, 240)  # min de desgaste — zona de sorteio de falha por ferramenta
HDF_LIMITE_DELTA = 8.6  # K — falha se delta < limite
HDF_LIMITE_ROTACAO = 1380  # rpm — falha se rotação < limite (as DUAS condições juntas)
PWF_FAIXA_SEGURA = (3500.0, 9000.0)  # W — falha se potência FORA desta faixa
OSF_LIMITES = {"L": 11000.0, "M": 12000.0, "H": 13000.0}  # min·Nm, por tipo de máquina

# Margens usadas só para achar os casos "difíceis" (perto do gatilho, sem cruzá-lo).
MARGEM_DIFICIL_HDF_DELTA = 1.0  # K acima do limite de delta
MARGEM_DIFICIL_HDF_ROTACAO = 100.0  # rpm acima do limite de rotação
MARGEM_DIFICIL_PWF = 200.0  # W de distância da fronteira seguro/inseguro
MARGEM_DIFICIL_OSF = 1000.0  # min·Nm abaixo do limite de sobrecarga

# Distribuição padrão de um lote de 30, replicando casos-lab-06-v2.csv
# (ver FONTE-casos-lab-06-v2.md): 2 atípicos, 6 difíceis (1 TWF + 2 PWF +
# 2 OSF + 1 HDF), 6 falhas fáceis (1 por mecanismo + 1 combinado), 16 seguras.
N_ATIPICO_PADRAO = 2
DISTRIBUICAO_DIFICIL_PADRAO = {"TWF": 1, "PWF_baixo": 1, "PWF_alto": 1, "OSF": 2, "HDF": 1}
DISTRIBUICAO_FALHA_FACIL_PADRAO = {
    "TWF": 1, "HDF": 1, "PWF_baixo": 1, "PWF_alto": 1, "OSF": 1, "combinado": 1,
}
N_SEGURA_PADRAO = 16

COLUNAS_CASO = [
    "id_caso", "data", "tipo_maquina", "idade_meses", "temperatura_c",
    "vibracao_mm_s", "horas_desde_manutencao", "acao_correta",
    "falhou_depois", "risco", "dificuldade",
]
COLUNAS_DEPARA = [
    "id_caso", "udi", "product_id", "categoria", "mecanismo", "risco", "dificuldade",
]

_RISCO_E_DIFICULDADE_POR_CATEGORIA = {
    "atipico": ("alto", "atipico"),
    "dificil": ("medio", "dificil"),
    "falha_facil": ("alto", "facil"),
    "segura": ("baixo", "facil"),
}
_ACAO_POR_RISCO = {
    "alto": "parar_para_manutencao",
    "medio": "inspecionar_antes_de_operar",
    "baixo": "seguir_operando",
}


class ErroGeracao(ValueError):
    """Erro de geração de casos (pool esgotado, parâmetro inconsistente), em português."""


def carregar_udis_usados(caminhos_depara: list[Path | str]) -> set[int]:
    """Lê um ou mais CSVs de de-para já gravados e devolve o conjunto de UDIs
    já usados, para excluí-los de um novo lote (nenhum caso se repete entre
    disciplinas)."""
    udis: set[int] = set()
    for caminho in caminhos_depara:
        quadro = pd.read_csv(caminho, encoding="utf-8-sig")
        udis.update(int(u) for u in quadro["udi"])
    return udis


def _preparar_base(quadro: pd.DataFrame, excluir_udis: set[int]) -> pd.DataFrame:
    base = dados.preparar(quadro)
    base = base[~base["udi"].isin(excluir_udis)].copy()
    base["potencia_w"] = base["potencia_kw"] * 1000.0
    base["osf_limite"] = base["tipo"].astype(str).map(OSF_LIMITES).astype(float)
    base["osf_produto"] = base["desgaste"] * base["torque"]
    return base


def _pool_atipico(base: pd.DataFrame) -> pd.DataFrame:
    return base[base["falha"] & ~base["algum_modo"]]


def _pools_dificil(base: pd.DataFrame) -> dict[str, pd.DataFrame]:
    seguro_e_sem_falha = ~base["falha"]

    twf = base[
        base["desgaste"].between(*TWF_JANELA) & ~base["twf"] & seguro_e_sem_falha
    ]
    hdf = base[
        (
            (base["delta_temperatura"] >= HDF_LIMITE_DELTA)
            & (base["delta_temperatura"] < HDF_LIMITE_DELTA + MARGEM_DIFICIL_HDF_DELTA)
            & (base["rotacao"] < HDF_LIMITE_ROTACAO)
        )
        | (
            (base["rotacao"] >= HDF_LIMITE_ROTACAO)
            & (base["rotacao"] < HDF_LIMITE_ROTACAO + MARGEM_DIFICIL_HDF_ROTACAO)
            & (base["delta_temperatura"] < HDF_LIMITE_DELTA)
        )
    ]
    hdf = hdf[~hdf["hdf"] & seguro_e_sem_falha[hdf.index]]
    pwf_baixo = base[
        base["potencia_w"].between(PWF_FAIXA_SEGURA[0], PWF_FAIXA_SEGURA[0] + MARGEM_DIFICIL_PWF)
        & ~base["pwf"] & seguro_e_sem_falha
    ]
    pwf_alto = base[
        base["potencia_w"].between(PWF_FAIXA_SEGURA[1] - MARGEM_DIFICIL_PWF, PWF_FAIXA_SEGURA[1])
        & ~base["pwf"] & seguro_e_sem_falha
    ]
    osf = base[
        (base["osf_produto"] >= base["osf_limite"] - MARGEM_DIFICIL_OSF)
        & (base["osf_produto"] < base["osf_limite"])
        & ~base["osf"] & seguro_e_sem_falha
    ]
    return {"TWF": twf, "HDF": hdf, "PWF_baixo": pwf_baixo, "PWF_alto": pwf_alto, "OSF": osf}


def _pools_falha_facil(base: pd.DataFrame) -> dict[str, pd.DataFrame]:
    n_flags = base[["twf", "hdf", "pwf", "osf", "rnf"]].sum(axis=1)
    isolado = base[base["falha"] & (n_flags == 1)]
    pwf_isolado = isolado[isolado["pwf"]]
    return {
        "TWF": isolado[isolado["twf"]],
        "HDF": isolado[isolado["hdf"]],
        "PWF_baixo": pwf_isolado[pwf_isolado["potencia_w"] < PWF_FAIXA_SEGURA[0]],
        "PWF_alto": pwf_isolado[pwf_isolado["potencia_w"] > PWF_FAIXA_SEGURA[1]],
        "OSF": isolado[isolado["osf"]],
        "combinado": base[base["falha"] & (n_flags == 2)],
    }


def _pool_segura(base: pd.DataFrame, pools_dificil: dict[str, pd.DataFrame]) -> pd.DataFrame:
    udis_dificeis = pd.concat(pools_dificil.values())["udi"] if pools_dificil else pd.Series(dtype="int64")
    return base[~base["falha"] & ~base["algum_modo"] & ~base["udi"].isin(udis_dificeis)]


def _sortear(pool: pd.DataFrame, n: int, rng: np.random.Generator, rotulo: str) -> pd.DataFrame:
    if len(pool) < n:
        raise ErroGeracao(
            f"pool de '{rotulo}' tem só {len(pool)} candidato(s) no dataset "
            f"(já excluídos os UDIs usados), precisava de {n}."
        )
    indices = rng.choice(pool.index.to_numpy(), size=n, replace=False)
    return pool.loc[indices]


def gerar_lote(
    dataset_bruto: pd.DataFrame,
    *,
    excluir_udis: set[int] | None = None,
    n_atipico: int = N_ATIPICO_PADRAO,
    distribuicao_dificil: dict[str, int] | None = None,
    distribuicao_falha_facil: dict[str, int] | None = None,
    n_segura: int = N_SEGURA_PADRAO,
    prefixo: str = "B",
    data_inicio: date = date(2026, 5, 1),
    seed: int = 42,
) -> tuple[pd.DataFrame, pd.DataFrame]:
    """Sorteia um novo lote de casos reais do AI4I2020, nas 4 categorias de
    dificuldade documentadas (ver FONTE-casos-lab-06-v2.md), sem repetir
    nenhum UDI de `excluir_udis`.

    Args:
        dataset_bruto: CSV bruto do AI4I2020 (`ams.dados.carregar().quadro`,
            ANTES de `preparar()` — esta função chama `preparar()` internamente).
        excluir_udis: UDIs a nunca sortear (de lotes/disciplinas anteriores —
            ver `carregar_udis_usados`).
        n_atipico, distribuicao_dificil, distribuicao_falha_facil, n_segura:
            tamanho de cada categoria; os padrões replicam exatamente a
            distribuição de `casos-lab-06-v2.csv` (30 casos: 2/6/6/16).
        prefixo: prefixo do `id_caso` (ex.: "B" → B01..B30).
        data_inicio: primeira data da sequência sintética (1 caso/dia,
            depois embaralhada entre as categorias — ver FONTE-casos-lab-06-v2.md §3).
        seed: semente do sorteio e do embaralhamento de datas — mesmo seed,
            mesmo lote (reprodutível).

    Returns:
        (casos, depara): DataFrame de casos no formato dos laboratórios
        (`COLUNAS_CASO`) e DataFrame de proveniência (`COLUNAS_DEPARA`).

    Raises:
        ErroGeracao: alguma categoria não tem candidatos suficientes no
            dataset depois de excluir os UDIs já usados.
    """
    distribuicao_dificil = distribuicao_dificil or DISTRIBUICAO_DIFICIL_PADRAO
    distribuicao_falha_facil = distribuicao_falha_facil or DISTRIBUICAO_FALHA_FACIL_PADRAO
    rng = np.random.default_rng(seed)

    base = _preparar_base(dataset_bruto, excluir_udis or set())

    selecionados: list[pd.DataFrame] = []

    atipico = _sortear(_pool_atipico(base), n_atipico, rng, "atipico")
    atipico = atipico.assign(categoria="atipico", mecanismo="nenhum")
    selecionados.append(atipico)

    pools_dificil = _pools_dificil(base)
    for mecanismo, n in distribuicao_dificil.items():
        if n == 0:
            continue
        escolhidos = _sortear(pools_dificil[mecanismo], n, rng, f"dificil/{mecanismo}")
        selecionados.append(escolhidos.assign(categoria="dificil", mecanismo=mecanismo))

    pools_falha_facil = _pools_falha_facil(base)
    for mecanismo, n in distribuicao_falha_facil.items():
        if n == 0:
            continue
        escolhidos = _sortear(pools_falha_facil[mecanismo], n, rng, f"falha_facil/{mecanismo}")
        selecionados.append(escolhidos.assign(categoria="falha_facil", mecanismo=mecanismo))

    segura = _sortear(_pool_segura(base, pools_dificil), n_segura, rng, "segura")
    selecionados.append(segura.assign(categoria="segura", mecanismo="nenhum"))

    linhas = pd.concat(selecionados, ignore_index=True)
    if linhas["udi"].duplicated().any():
        raise ErroGeracao("sorteio produziu UDI repetido entre categorias — rode de novo com outro seed.")

    n_total = len(linhas)
    med_rotacao = linhas["rotacao"].median()
    med_torque = linhas["torque"].median()
    desvio_rotacao = (linhas["rotacao"] - med_rotacao).abs() / med_rotacao
    desvio_torque = (linhas["torque"] - med_torque).abs() / med_torque
    vibracao = (2.0 + 10.0 * (0.5 * desvio_rotacao + 0.5 * desvio_torque)).round(1)

    datas = [data_inicio + timedelta(days=i) for i in range(n_total)]
    rng.shuffle(datas)

    risco_dificuldade = linhas["categoria"].map(_RISCO_E_DIFICULDADE_POR_CATEGORIA)
    risco = risco_dificuldade.map(lambda par: par[0])
    dificuldade = risco_dificuldade.map(lambda par: par[1])

    casos = pd.DataFrame({
        "id_caso": [f"{prefixo}{i + 1:02d}" for i in range(n_total)],
        "data": [d.isoformat() for d in datas],
        "tipo_maquina": linhas["tipo"].astype(str).to_numpy(),
        "idade_meses": 0,
        "temperatura_c": (linhas["temperatura_processo"] - 273.15).round(1).to_numpy(),
        "vibracao_mm_s": vibracao.to_numpy(),
        "horas_desde_manutencao": linhas["desgaste"].astype(float).to_numpy(),
        "acao_correta": risco.map(_ACAO_POR_RISCO).to_numpy(),
        "falhou_depois": linhas["falha"].astype(int).to_numpy(),
        "risco": risco.to_numpy(),
        "dificuldade": dificuldade.to_numpy(),
    })[COLUNAS_CASO]

    depara = pd.DataFrame({
        "id_caso": casos["id_caso"],
        "udi": linhas["udi"].to_numpy(),
        "product_id": linhas["product_id"].to_numpy(),
        "categoria": linhas["categoria"].to_numpy(),
        "mecanismo": linhas["mecanismo"].to_numpy(),
        "risco": risco.to_numpy(),
        "dificuldade": dificuldade.to_numpy(),
    })[COLUNAS_DEPARA]

    return casos, depara


def escrever_lote(caminho_casos: Path | str, caminho_depara: Path | str,
                   casos: pd.DataFrame, depara: pd.DataFrame) -> None:
    """Grava o CSV de casos e o de-para juntos — nunca um sem o outro."""
    Path(caminho_casos).parent.mkdir(parents=True, exist_ok=True)
    Path(caminho_depara).parent.mkdir(parents=True, exist_ok=True)
    casos.to_csv(caminho_casos, index=False, encoding="utf-8")
    depara.to_csv(caminho_depara, index=False, encoding="utf-8")


def _cli() -> None:
    import argparse

    parser = argparse.ArgumentParser(
        description="Gera um novo lote de casos reais do AI4I2020 + de-para de proveniência."
    )
    parser.add_argument("--saida-casos", required=True, type=Path)
    parser.add_argument("--saida-depara", required=True, type=Path)
    parser.add_argument("--excluir-depara", nargs="*", default=[], type=Path,
                         help="CSVs de de-para já gravados, pra nunca repetir UDI entre lotes/disciplinas.")
    parser.add_argument("--prefixo", default="B")
    parser.add_argument("--data-inicio", default="2026-05-01")
    parser.add_argument("--seed", type=int, default=42)
    argumentos = parser.parse_args()

    excluir_udis = carregar_udis_usados(argumentos.excluir_depara) if argumentos.excluir_depara else set()
    dataset_bruto = dados.carregar().quadro
    casos, depara = gerar_lote(
        dataset_bruto,
        excluir_udis=excluir_udis,
        prefixo=argumentos.prefixo,
        data_inicio=date.fromisoformat(argumentos.data_inicio),
        seed=argumentos.seed,
    )
    escrever_lote(argumentos.saida_casos, argumentos.saida_depara, casos, depara)
    print(f"{len(casos)} casos gravados em {argumentos.saida_casos}")
    print(f"de-para gravado em {argumentos.saida_depara}")


if __name__ == "__main__":
    _cli()
