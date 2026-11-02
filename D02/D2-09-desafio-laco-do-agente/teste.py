"""Testes do desafio — o laço do agente.

Como usar (depois de renomear esqueleto.py para resposta.py):
    python -m pytest teste.py -q

NENHUM teste exige rede: o laço é exercido com funções de chamada
roteirizadas (o mesmo contrato do modo --sem-rede). O que os testes
provam:

  1. o registro de ferramentas está no formato ESTRUTURADO nativo (nada de
     expressão regular caçando "Ação:");
  2. o laço roda de ponta a ponta contra um roteiro: consulta, registra,
     responde — e o rastro sai no formato que o encenar.py apresenta;
  3. o TETO segura: com um roteiro que nunca responde, o laço para no
     limite e marca termino=teto_de_rodadas;
  4. nenhuma cadeia com cara de chave de API no arquivo.
"""

from __future__ import annotations

import importlib.util
import json
import re
import sys
from pathlib import Path

_AQUI = Path(__file__).resolve().parent

_spec = importlib.util.spec_from_file_location("resposta", _AQUI / "resposta.py")
resposta = importlib.util.module_from_spec(_spec)
sys.modules["resposta"] = resposta
_spec.loader.exec_module(resposta)  # type: ignore[union-attr]

_spec_encenar = importlib.util.spec_from_file_location(
    "encenar", _AQUI / "encenar.py")
encenar = importlib.util.module_from_spec(_spec_encenar)
sys.modules["encenar"] = encenar
_spec_encenar.loader.exec_module(encenar)  # type: ignore[union-attr]

# O roteiro que o "modelo" segue nos testes: consulta → registra → responde.
ROTEIRO = [
    {"functionCall": {"name": "consultar_registro",
                      "args": {"maquina": "L14720"}}},
    {"functionCall": {"name": "registrar_recomendacao", "args": {
        "ordem": "OS-2026-0042", "recomendacao": "parar_para_manutencao",
        "justificativa": "pendência de mancal e vibração em alta"}}},
    {"text": "Recomendei parar para manutenção, com a justificativa "
             "registrada na ordem."},
]


def _chamar_roteirizado(roteiro, registro):
    contador = {"chamadas": 0}

    def chamar(conteudos, ferramentas):
        registro["ultimo_contexto"] = [list(c["parts"]) for c in conteudos]
        contador["chamadas"] += 1
        return dict(roteiro[contador["chamadas"] - 1])

    return chamar, contador


def test_as_ferramentas_estao_no_formato_nativo():
    assert len(resposta.FERRAMENTAS) == 2, \
        "duas ferramentas: uma de consulta e uma de escrita"
    for declaracao in resposta.FERRAMENTAS:
        assert declaracao["name"], "declaração sem name"
        assert declaracao["description"], "declaração sem description"
        assert declaracao["parameters"]["type"] == "OBJECT"
    nomes = [f["name"] for f in resposta.FERRAMENTAS]
    assert "consultar_registro" in nomes and \
        "registrar_recomendacao" in nomes


def test_o_laco_roda_de_ponta_a_ponta_com_o_roteiro():
    registro: dict = {}
    chamar, contador = _chamar_roteirizado(ROTEIRO, registro)
    rastro = resposta.laco(resposta.PEDIDO, teto=6, chamar=chamar)
    assert contador["chamadas"] == 3
    assert rastro["resposta_final"]["rodada"] == 3
    nomes = [r["execute_tool"]["chamada"]["nome"]
             for r in rastro["rodadas"] if r["execute_tool"]]
    assert nomes == ["consultar_registro", "registrar_recomendacao"], \
        f"ordem errada do laço: {nomes}"


def test_a_observacao_volta_ao_contexto_na_rodada_seguinte():
    """O coração do laço: o retorno da ferramenta entra no contexto."""
    registro: dict = {}
    chamar, contador = _chamar_roteirizado(ROTEIRO, registro)
    resposta.laco(resposta.PEDIDO, teto=6, chamar=chamar)
    contexto_da_segunda = json.dumps(
        registro["ultimo_contexto"], ensure_ascii=False)
    assert "mancal" in contexto_da_segunda, (
        "o retorno da consulta não entrou no contexto — sem isso o laço "
        "não é laço, é duas chamadas soltas")
    assert "functionResponse" in contexto_da_segunda, (
        "o retorno precisa voltar no formato nativo (functionResponse), "
        "não colado no texto")


def test_o_teto_segura_quando_o_modelo_nao_converge():
    registro: dict = {}
    nunca_responde = [{"functionCall": {
        "name": "consultar_registro", "args": {"maquina": "L14720"}}}] * 50
    chamar, contador = _chamar_roteirizado(nunca_responde, registro)
    rastro = resposta.laco(resposta.PEDIDO, teto=4, chamar=chamar)
    assert contador["chamadas"] == 4
    assert rastro["resposta_final"] is None
    assert rastro["termino"] == "teto_de_rodadas"
    chamadas = [json.dumps(r["execute_tool"]["chamada"], sort_keys=True)
                for r in rastro["rodadas"]]
    assert len(set(chamadas)) == 1, \
        "sem memória, as chamadas repetem — é o sintoma que o teto corta"


def test_o_rastro_do_laco_e_encenavel():
    """O arco do desafio: o laço do aluno sai no formato das demonstrações."""
    chamar, _ = _chamar_roteirizado(ROTEIRO, {})
    rastro = resposta.laco(resposta.PEDIDO, teto=6, chamar=chamar)
    for nome_obrigatorio in ("demonstracao", "pedido_inicial", "ferramentas",
                             "teto_de_rodadas", "rodadas", "resposta_final",
                             "termino"):
        assert nome_obrigatorio in rastro, \
            f"o rastro do laço não tem {nome_obrigatorio!r}"
    encenar.encenar(rastro, pausar=False)          # não pode lançar


def test_nenhuma_chave_no_arquivo():
    dados = (_AQUI / "resposta.py").read_text(encoding="utf-8")
    # Os dois formatos de chave do Gemini: o antigo ("AIza...") e o novo
    # ("AQ...."). Um detector que só conhece um deles deixa passar o outro.
    for padrao in (r"AIza[A-Za-z0-9_-]{20,}", r"AQ\.[A-Za-z0-9_-]{25,}",
                   r"sk-[A-Za-z0-9]{20,}"):
        assert not re.findall(padrao, dados), \
            "chave embutida no código — a chave vem do ambiente"
    assert "GEMINI_API_KEY" in dados, \
        "a chave vem do ambiente, lida de GEMINI_API_KEY"
