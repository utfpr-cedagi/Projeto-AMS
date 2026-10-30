"""Subproblema 2 do catálogo: a sequência de consultas para responder uma pergunta.

A formulação vem do plano da D2, seção 9 (catálogo de subproblemas):
Estado: o que já se sabe. Ação: consultar uma fonte. Custo: latência da
consulta. Objetivo: ter todos os dados que a resposta exige.

O sabor do caso: uma fonte costuma entregar VÁRIOS fatos de uma vez. O
caminho ótimo pode ser uma fonte cara que fecha tudo, ou duas baratas que
juntas fecham — e é exatamente esse tipo de escolha que a busca compara.
Uma consulta repetida (todos os fatos já sabidos) é permitida, custa a
latência inteira e não muda o estado: a busca em grafo a descarta.

Os dados são inventados e moram nas constantes do módulo — troque pelos do
seu domínio (lab-03) sem tocar na classe.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Fonte:
    """Uma fonte que pode ser consultada, e o que ela entrega."""

    nome: str
    latencia: float              # custo da consulta (segundos)
    fornece: tuple[str, ...]     # os fatos que a consulta devolve

# A pergunta: "a máquina X pode ser liberada hoje, sem risco?" — quatro
# fatos, cinco fontes. O caminho ótimo é a combinação de fontes baratas; a
# fonte única (auditoria completa) é a mais cara.
FATOS_PEQUENOS: frozenset[str] = frozenset({
    "histórico de falhas da máquina",
    "normas regulamentares aplicáveis (NR)",
    "leitura atual dos sensores",
    "manutenção preventiva programada",
})

FONTES_PEQUENAS: tuple[Fonte, ...] = (
    Fonte("painel de sensores — leitura atual", 1.2, ("leitura atual dos sensores",)),
    Fonte("sistema de manutenção — status", 2.0, ("normas regulamentares aplicáveis (NR)", "manutenção preventiva programada")),
    Fonte("histórico de falhas (sistema)", 6.0, ("histórico de falhas da máquina",)),
    Fonte("relatório semanal de manutenção", 4.5, ("histórico de falhas da máquina",
                                                  "leitura atual dos sensores")),
    Fonte("auditoria completa de manutenção", 15.0, ("histórico de falhas da máquina",
                                         "normas regulamentares aplicáveis (NR)",
                                         "leitura atual dos sensores",
                                         "manutenção preventiva programada")),
)

# A pergunta maior: "a máquina L14720 pode ser liberada para operação,
# inspecionada antes, ou precisa parar para manutenção?" — oito fatos,
# catorze fontes. A maioria das fontes é barata e específica; só a
# consultoria externa cobre tudo de uma vez, por um preço bem mais alto do
# que combinar as fontes baratas.
FATOS_MAIORES: frozenset[str] = frozenset({
    "histórico de intervenções anteriores",
    "leitura atual de vibração",
    "leitura atual de temperatura do mancal",
    "tempo decorrido desde a última manutenção",
    "tendência das últimas leituras de vibração",
    "pendências abertas na ordem de serviço",
    "disponibilidade de peça de reposição",
    "prazo de entrega da peça de reposição",
})
FONTES_MAIORES: tuple[Fonte, ...] = (
    Fonte("sistema de manutenção — histórico de intervenções", 0.9, ("histórico de intervenções anteriores",)),
    Fonte("sensor de vibração — leitura atual", 1.1, ("leitura atual de vibração",)),
    Fonte("sensor de temperatura — leitura atual", 1.3, ("leitura atual de temperatura do mancal",)),
    Fonte("registro de manutenção — última intervenção", 0.7, ("tempo decorrido desde a última manutenção",)),
    Fonte("ordem de serviço — pendências abertas", 1.0, ("pendências abertas na ordem de serviço",)),
    Fonte("almoxarifado — peças de reposição", 1.2, ("disponibilidade de peça de reposição",)),
    Fonte("portal do fornecedor de peças", 3.5, ("prazo de entrega da peça de reposição",)),
    Fonte("robô de email da manutenção", 2.8, ("disponibilidade de peça de reposição",
                                                "prazo de entrega da peça de reposição")),
    Fonte("sistema de manutenção — histórico completo", 4.0, ("histórico de intervenções anteriores",
                                                               "tendência das últimas leituras de vibração")),
    Fonte("relatório de condição da máquina", 5.0, ("leitura atual de vibração",
                                                     "pendências abertas na ordem de serviço")),
    Fonte("painel de monitoramento preditivo", 6.5, ("leitura atual de temperatura do mancal",
                                 "tempo decorrido desde a última manutenção",
                                 "tendência das últimas leituras de vibração")),
    Fonte("sistema de manutenção — módulo completo", 9.0, ("histórico de intervenções anteriores",
                                                          "tendência das últimas leituras de vibração",
                                                          "tempo decorrido desde a última manutenção")),
    Fonte("reunião com o técnico responsável", 14.0, ("leitura atual de vibração",
                                                    "leitura atual de temperatura do mancal",
                                                    "pendências abertas na ordem de serviço",
                                                    "disponibilidade de peça de reposição",
                                                    "prazo de entrega da peça de reposição")),
    Fonte("consultoria externa de engenharia de manutenção", 22.0, ("histórico de intervenções anteriores",
                                                       "leitura atual de vibração",
                                                       "leitura atual de temperatura do mancal",
                                                       "tempo decorrido desde a última manutenção",
                                                       "tendência das últimas leituras de vibração",
                                                       "pendências abertas na ordem de serviço",
                                                       "disponibilidade de peça de reposição",
                                                       "prazo de entrega da peça de reposição")),
)

class Consultas:
    """O problema de busca: que fontes consultar, em que ordem.

    O estado é o conjunto de fatos já sabidos, como tupla ordenada —
    estados com os mesmos fatos são o mesmo hash, não importa a ordem
    das consultas.
    """

    def __init__(self, fatos_necessarios: frozenset[str], fontes: tuple[Fonte, ...]):
        self.fatos_necessarios = fatos_necessarios
        self.fontes = fontes
        self._por_nome = {f.nome: f for f in fontes}
        self.estado_inicial: tuple[str, ...] = ()

    def acoes(self, estado: tuple[str, ...]) -> list[str]:
        return [f.nome for f in self.fontes]

    def transicao(self, estado: tuple[str, ...], acao: str) -> tuple[str, ...]:
        # o estado é um CONJUNTO de fatos: consultar fonte que só repete o
        # que já se sabe devolve o MESMO estado — sem o set(), cada consulta
        # redundante criaria um estado novo com o fato duplicado.
        return tuple(sorted(set(estado) | set(self._por_nome[acao].fornece)))

    def objetivo(self, estado: tuple[str, ...]) -> bool:
        return self.fatos_necessarios.issubset(estado)

    def custo(self, estado: tuple[str, ...], acao: str, estado_seguinte: tuple[str, ...]) -> float:
        return self._por_nome[acao].latencia

    def heuristica_admissivel(self, estado: tuple[str, ...]) -> float:
        """A latência da consulta mais barata que ainda entrega um fato faltante.

        Admissível: enquanto faltar fato, é obrigatório consultar PELO MENOS
        uma fonte que ajude — e nenhuma consulta custa menos do que a menor
        latência útil. Ignora quantas consultas ainda virão depois dessa.
        """
        sabidos = set(estado)
        faltantes = self.fatos_necessarios - sabidos
        if not faltantes:
            return 0.0
        uteis = [f.latencia for f in self.fontes
                 if set(f.fornece) & faltantes]
        return min(uteis)

    def heuristica_inadmissivel(self, estado: tuple[str, ...]) -> float:
        """Pior caso por fato: cada fato que falta vai custar a consulta mais lenta.

        NÃO é admissível, e é tentadora por isso: "cada dado que falta é uma
        consulta, e consulta pode demorar o máximo" é o cálculo pessimista
        que se escreve de primeira. Ela ignora que uma consulta única entrega
        vários fatos — e por isso faz a fonte cara que resolve tudo parecer
        o caminho mais promissor: o A* com ela mergulha na consulta lenta e
        devolve caminho mais caro que o ótimo (o lab-05 mede o dano).
        """
        sabidos = set(estado)
        faltantes = len(self.fatos_necessarios - sabidos)
        pior_latencia = max(f.latencia for f in self.fontes)
        return float(faltantes * pior_latencia)


PEQUENA = Consultas(FATOS_PEQUENOS, FONTES_PEQUENAS)
MAIOR = Consultas(FATOS_MAIORES, FONTES_MAIORES)
