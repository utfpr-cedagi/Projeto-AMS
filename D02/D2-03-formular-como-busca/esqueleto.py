"""Laboratório 03 — o seu subproblema formulado como espaço de estados.

Este módulo RODA desde o primeiro momento: traz os cinco componentes do
protocolo implementados sobre dados de exemplo mínimos (um mini-diagnóstico
de 3 verificações). Rode e confira as seis verificações verdes:

    python esqueleto.py

Aí começa o seu trabalho — os TODOs dizem o que trocar pelos dados do SEU
domínio. Caminho padrão: escolha um dos três subproblemas do catálogo
(`comum/problemas/`) e troque os dados, como o `solucao.py` mostra, linha a
linha. Desafio: formule o seu próprio subproblema daqui mesmo.

A regra de ouro do slide 47: o estado descreve a SITUAÇÃO, nunca a história
de como se chegou nela. Duas trilhas que chegam à mesma situação precisam
ser o MESMO estado — o teste de sanidade avisa quando não são.
"""

from __future__ import annotations

# --------------------------------------------------------------------------
# O esqueleto dos dados — TROQUE PELOS DO SEU DOMÍNIO (TODO 1)
# --------------------------------------------------------------------------
# O exemplo é um diagnóstico minúsculo: três verificações, cada uma com o
# tempo que custa e o resultado fixo neste caso. As "essenciais" são as que
# distinguem as hipóteses — o laudo não fecha sem elas.

VERIFICACOES: tuple[tuple[str, float, bool, bool], ...] = (
    # (nome da verificação, custo em minutos, positiva neste caso?, essencial?)
    ("conferir a conexão de rede", 2.0, False, True),
    ("reproduzir o erro numa máquina limpa", 5.0, True, True),
    ("ler o changelog da última atualização", 1.0, False, False),
)

ESSENCIAIS: tuple[str, ...] = tuple(
    nome for nome, _, _, essencial in VERIFICACOES if essencial
)


class MeuProblema:
    """A formulação: em que ordem fazer as verificações do meu domínio.

    Os cinco componentes do protocolo (slide 46) estão implementados e o
    módulo roda — o trabalho é substituir os dados de exemplo (TODO 1) e,
    se a sua fatia de problema pedir, adaptar cada componente (TODOs 2 a 5).
    O estado é o par (feitas, positivas), cada um como TUPLA ORDENADA:
    estados iguais dão o mesmo hash, não importa a ordem em que as
    verificações foram feitas.
    """

    def __init__(self) -> None:
        self._por_nome = {nome: (custo, positivo)
                          for nome, custo, positivo, _ in VERIFICACOES}
        self.estado_inicial: tuple[tuple[str, ...], tuple[str, ...]] = ((), ())

    def acoes(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> list[str]:
        # TODO 2 (opcional): a lista de ações do SEU domínio, numa ordem
        # estável. Aqui: fazer qualquer verificação ainda não feita.
        feitas, _ = estado
        return [nome for nome in self._por_nome if nome not in feitas]

    def transicao(
        self, estado: tuple[tuple[str, ...], tuple[str, ...]], acao: str,
    ) -> tuple[tuple[str, ...], tuple[str, ...]]:
        # TODO 3 (opcional): o estado que resulta da ação. O exemplo soma a
        # verificação às feitas e, se positiva, às positivas — e ORDENA, para
        # a situação (não o caminho até ela) ser o estado.
        feitas, positivas = estado
        _, positivo = self._por_nome[acao]
        novas_feitas = tuple(sorted((*feitas, acao)))
        if positivo:
            return novas_feitas, tuple(sorted((*positivas, acao)))
        return novas_feitas, positivas

    def objetivo(self, estado: tuple[tuple[str, ...], tuple[str, ...]]) -> bool:
        # TODO 4 (opcional): o teste de objetivo do SEU domínio — comece por
        # ele quando formular o seu; é ele que define o que precisa estar no
        # estado. Aqui: todas as essenciais verificadas.
        feitas, _ = estado
        return set(ESSENCIAIS).issubset(feitas)

    def custo(
        self,
        estado: tuple[tuple[str, ...], tuple[str, ...]],
        acao: str,
        estado_seguinte: tuple[tuple[str, ...], tuple[str, ...]],
    ) -> float:
        # TODO 5 (opcional): o custo da ação — tempo, dinheiro, esforço,
        # latência. Custo 1.0 para toda ação é formulação válida, e é um
        # começo honesto. Nunca devolva negativo.
        custo_acao, _ = self._por_nome[acao]
        return custo_acao


MEU_PROBLEMA = MeuProblema()


if __name__ == "__main__":
    import importlib.util
    import sys
    from pathlib import Path

    teste = importlib.util.spec_from_file_location(
        "verificar-formulacao",
        Path(__file__).resolve().parent / "verificar-formulacao.py")
    modulo = importlib.util.module_from_spec(teste)
    sys.modules["verificar-formulacao"] = modulo
    teste.loader.exec_module(modulo)
    raise SystemExit(modulo.main([str(Path(__file__)) + ":MEU_PROBLEMA"]))
