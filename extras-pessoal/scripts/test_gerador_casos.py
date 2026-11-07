"""Testes do gerador de lotes de casos (categorização, de-para, determinismo).

Nenhum teste toca `data/raw/`: o dataset de entrada é um CSV sintético
pequeno (mesmas colunas e BOM do UCI, via `conftest.gerar_csv`), com uma
linha construída manualmente para cada categoria/mecanismo — valores
escolhidos para cair exatamente em cada pool e em nenhum outro.
"""

from __future__ import annotations

from datetime import date
from pathlib import Path

import pytest
from conftest import LINHA_VALIDA, gerar_csv
from pandas.testing import assert_frame_equal

from ams.dados import carregar
from gerador_casos import (
    COLUNAS_CASO,
    COLUNAS_DEPARA,
    ErroGeracao,
    carregar_udis_usados,
    gerar_lote,
)

# omega(1551 rpm) ≈ 162,39 rad/s — usado para calibrar a potência (torque × ω)
# das linhas de PWF sem reescrever a conta em cada uma.
_OMEGA_1551 = 1551 * 2 * 3.141592653589793 / 60


def _linha(udi: int, **overrides: object) -> dict[str, str]:
    linha = dict(LINHA_VALIDA)
    linha["UDI"] = str(udi)
    linha["Product ID"] = f"L{udi}"
    linha["Type"] = "L"
    for campo, valor in overrides.items():
        linha[campo] = str(valor)
    return linha


# UDI -> (categoria, mecanismo) esperados, pras linhas com candidato único
# no dataset sintético (sem ambiguidade de sorteio).
_ESPERADO_FORCADO = {
    101: ("dificil", "TWF"),
    102: ("dificil", "HDF"),
    103: ("dificil", "PWF_baixo"),
    104: ("dificil", "PWF_alto"),
    105: ("dificil", "OSF"),
    106: ("falha_facil", "TWF"),
    107: ("falha_facil", "HDF"),
    108: ("falha_facil", "PWF_baixo"),
    109: ("falha_facil", "PWF_alto"),
    110: ("falha_facil", "OSF"),
    111: ("falha_facil", "combinado"),
}


@pytest.fixture
def dataset_sintetico(tmp_path: Path):
    linhas = [
        # 2 atípicos (falha real, nenhum dos 5 mecanismos) — pool com 2
        # candidatos, pra testar sorteio + determinismo.
        _linha(100, **{"Machine failure": 1, "Tool wear [min]": 10}),
        _linha(115, **{"Machine failure": 1, "Tool wear [min]": 15}),
        # difíceis: perto de cada gatilho, sem disparar
        _linha(101, **{"Tool wear [min]": 220}),  # TWF: dentro da janela 200-240
        _linha(102, **{  # HDF: delta 8,7 K (perto do limite 8,6) e rotação baixa
            "Air temperature [K]": "300.0", "Process temperature [K]": "308.7",
            "Rotational speed [rpm]": 1300, "Tool wear [min]": 50,
        }),
        _linha(103, **{"Torque [Nm]": "22.0", "Tool wear [min]": 50}),  # PWF perto do piso (~3573 W)
        _linha(104, **{"Torque [Nm]": "54.8", "Tool wear [min]": 50}),  # PWF perto do teto (~8899 W)
        _linha(105, **{"Torque [Nm]": "105.0", "Tool wear [min]": 100}),  # OSF perto do limite (10500 < 11000)
        # falhas fáceis: um mecanismo isolado cada + 1 combinado
        _linha(106, **{"Machine failure": 1, "TWF": 1, "Tool wear [min]": 50}),
        _linha(107, **{  # HDF de verdade: delta baixo e rotação baixa
            "Machine failure": 1, "HDF": 1,
            "Air temperature [K]": "300.0", "Process temperature [K]": "307.0",
            "Rotational speed [rpm]": 1200, "Tool wear [min]": 50,
        }),
        _linha(108, **{"Machine failure": 1, "PWF": 1, "Torque [Nm]": "10.0", "Tool wear [min]": 50}),
        _linha(109, **{"Machine failure": 1, "PWF": 1, "Torque [Nm]": "60.0", "Tool wear [min]": 50}),
        _linha(110, **{"Machine failure": 1, "OSF": 1, "Torque [Nm]": "50.0", "Tool wear [min]": 300}),
        _linha(111, **{"Machine failure": 1, "TWF": 1, "RNF": 1, "Tool wear [min]": 50}),  # combinado
        # seguras: longe de qualquer limiar
        _linha(112, **{"Tool wear [min]": 10}),
        _linha(113, **{"Tool wear [min]": 20}),
        _linha(114, **{"Tool wear [min]": 30}),  # usado só no teste de exclusão de UDI
    ]
    caminho = gerar_csv(linhas, tmp_path / "ai4i2020.csv")
    return carregar(caminho, validar_com_pydantic=False).quadro


_DISTRIBUICAO_DIFICIL = {"TWF": 1, "HDF": 1, "PWF_baixo": 1, "PWF_alto": 1, "OSF": 1}


def _gerar(dataset_sintetico, **overrides):
    parametros = dict(
        excluir_udis={114},
        n_atipico=1,
        distribuicao_dificil=_DISTRIBUICAO_DIFICIL,
        n_segura=2,
        prefixo="T",
        data_inicio=date(2026, 1, 1),
        seed=7,
    )
    parametros.update(overrides)
    return gerar_lote(dataset_sintetico, **parametros)


def test_gera_as_quatro_categorias_sem_repetir_udi(dataset_sintetico) -> None:
    casos, depara = _gerar(dataset_sintetico)

    assert list(casos.columns) == COLUNAS_CASO
    assert list(depara.columns) == COLUNAS_DEPARA
    assert len(casos) == len(depara) == 1 + 5 + 6 + 2
    assert set(casos["id_caso"]) == set(depara["id_caso"])
    assert depara["udi"].is_unique


def test_exclui_udi_informado(dataset_sintetico) -> None:
    _, depara = _gerar(dataset_sintetico)
    assert 114 not in set(depara["udi"])


def test_categoriza_cada_mecanismo_corretamente(dataset_sintetico) -> None:
    _, depara = _gerar(dataset_sintetico)
    por_udi = depara.set_index("udi")[["categoria", "mecanismo"]]

    for udi, esperado in _ESPERADO_FORCADO.items():
        obtido = tuple(por_udi.loc[udi])
        assert obtido == esperado, f"UDI {udi}: esperado {esperado}, veio {obtido}"

    atipico_escolhido = depara.loc[depara["categoria"] == "atipico", "udi"].iloc[0]
    assert atipico_escolhido in {100, 115}


def test_acao_correta_deriva_do_risco(dataset_sintetico) -> None:
    casos, _ = _gerar(dataset_sintetico)
    mapa = {"alto": "parar_para_manutencao", "medio": "inspecionar_antes_de_operar", "baixo": "seguir_operando"}
    for risco, acao_esperada in mapa.items():
        subconjunto = casos[casos["risco"] == risco]
        assert not subconjunto.empty
        assert (subconjunto["acao_correta"] == acao_esperada).all()


def test_mesmo_seed_gera_o_mesmo_lote(dataset_sintetico) -> None:
    casos1, depara1 = _gerar(dataset_sintetico)
    casos2, depara2 = _gerar(dataset_sintetico)
    assert_frame_equal(casos1.reset_index(drop=True), casos2.reset_index(drop=True))
    assert_frame_equal(depara1.reset_index(drop=True), depara2.reset_index(drop=True))


def test_erro_claro_quando_pool_nao_tem_candidatos_suficientes(dataset_sintetico) -> None:
    with pytest.raises(ErroGeracao, match="segura"):
        _gerar(dataset_sintetico, n_segura=5)


def test_carregar_udis_usados_le_varios_csvs(tmp_path: Path) -> None:
    caminho1 = tmp_path / "depara1.csv"
    caminho2 = tmp_path / "depara2.csv"
    caminho1.write_text("id_caso,udi\nA01,10\nA02,20\n", encoding="utf-8")
    caminho2.write_text("id_caso,udi\nB01,20\nB02,30\n", encoding="utf-8")
    assert carregar_udis_usados([caminho1, caminho2]) == {10, 20, 30}
