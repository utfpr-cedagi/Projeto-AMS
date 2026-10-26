# agent-spec.md — AMS · Assistente de Manutenção Segura

<!--
Este arquivo é para preencher, não para ler e devolver. As perguntas de cada
seção estão em comentário como este: elas não aparecem na pré-visualização,
aparecem no editor. Responda ABAIXO de cada seção, apagando nada delas.

As seções que ainda não foram vistas em aula ficam de pé, com a linha
"quando se preenche" dizendo o encontro em que isso acontece. O documento
cresce a cada laboratório — o de hoje é o primeiro.

Preencha com exemplos concretos do SEU domínio. Uma linha que funcionaria
para qualquer empresa é uma linha genérica — o exemplo do seu segmento
(agente-spec-exemplo.pdf, no mesmo pacote) mostra o contraste.
-->

**Domínio:** AMS · Assistente de Manutenção Segura
**Autor(a):** DANIEL ALVES MARTINHAO · **Última revisão:** 2026-10-26

---

## 1. PEAS

<!-- Perguntas que guiam o preenchimento:
  - Performance: o que conta como sucesso, em uma fórmula? Sobre o quê se
    conta, sobre qual conjunto, quanto é sucesso? Qual termo impede a
    trapaça mais óbvia (fechar rápido sem resolver)?
  - Environment: onde o agente opera? O que existe lá — sistemas, pessoas,
    documentos, ruído? Cite elementos concretos.
  - Actuators: o que o agente pode FAZER? Inclua comunicar e escalar:
    informar a decisão é uma ação, e passar adiante também é.
  - Sensors: o que o agente consegue PERCEBER? Só o que ele enxerga existe
    para ele.
  Um PEAS que menciona tecnologia de solução (banco vetorial, nome de modelo)
  está descrevendo a solução — o PEAS descreve o problema.
-->
**Quando se preenche:** no Laboratório 01, hoje. Refinado na Atividade Orientada.

**Performance:**

[a medida de desempenho com fórmula: sobre o quê se conta, sobre qual conjunto, quanto é sucesso]

Medir se o modelo consegue identificar corretamente casos de máquinas com alto risco de falha. O objetivo é alcançar recall e precisão de pelo menos 80% para a classe “alto” e garantir que no máximo 5% dos casos realmente de alto risco sejam classificados como baixo.

| Intenção | Medida Opoeracional |
|---|---|
| Identificar possível falha iminente (risco baixo / médio / alto) | **Recall da classe "alto" para risco de falha iminente**: proporção de máquinas que realmente apresentavam alto risco de falha e foram corretamente classificadas pelo agente como de alto risco. </br> </br> **Fórmula:** </br> `Recall = quantidade de máquinas realmente de alto risco, que foram classificadas como alto, dividido pela quantidade total de máquinas realmente de alto risco.` </br> </br> **Critério:** recall maior ou igual a 80%.  </br> </br> **Precisão da classe "alto" para risco de falha iminente**: proporção de máquinas classificadas pelo agente como de alto risco que realmente apresentavam alto risco de falha. </br> </br> **Fórmula**: `Precisão = quantidade de máquinas classificadas como alto que realmente eram de alto risco dividido pela quantidade total de máquinas classificadas como alto.` </br> </br> **Critério:** precisão maior ou igual a 80%. </br> </br> *Usando Recall em conjunto com Precision para eveitar um agente que responda alto para tudo e assim termos uma base de respostas sem sentido.* </br></br> **Taxa de classificação como “baixo” dos casos que eram na verdade de alto risco:** proporção de máquinas que realmente apresentavam alto risco de falha, mas foram classificadas pelo agente como de baixo risco. </br> </br> **Fórmula:** `Taxa de erro = máquinas realmente de alto risco classificadas como baixo dividio total de máquinas realmente de alto risco.` </br></br> **Critério:** taxa menor ou igual a 5%. </br> </br>Essa medida controla especificamente os casos de alto risco classificados como baixo; os casos classificados como médio permanecem contabilizados no recall, mas não nessa taxa específica. |

**Environment:**

[onde o agente opera, com elementos concretos — sistemas, pessoas, documentos, ruído]

Planta Industrial, Máquinas de Produção, Ordens de Serviço, Equipe de Manutenção com técnicos de manutenção, supervisores de segurança.

**Actuators:**

[o que o agente pode fazer — inclua comunicar e escalar]

Classificar os níveis de riscos. Apresentar necessidade de bloqueio e etiquetagem antes da manutenção. Definir qual NR é aplicável. Estimar riscos de falhas iminentes. Apresentar procedimentos para intervenção. Escalar a ordem para o supervisor de segurança quando o risco for alto ou a classificação for incerta (baixa confiança do modelo).

**Sensors:**

[o que o agente consegue perceber — só o que ele enxerga existe para ele]

Máquinas, Sensores, historico de falhas, Normals Regulamentares em PDF, Descritivo nas ordens de serviços.

---

## 2. O ambiente em sete dimensões

<!--
Perguntas que guiam o preenchimento (uma por dimensão):
  - Observabilidade: existe algo que muda a decisão e o agente não mede?
  - Número de agentes: existe alguém cujas ações mudam o seu resultado?
    Um humano que reage ao agente conta.
  - Determinismo: a mesma ação no mesmo estado dá sempre o mesmo efeito?
  - Episódico ou sequencial: a decisão de agora afeta as decisões seguintes?
  - Estático ou dinâmico: o ambiente muda enquanto o agente delibera?
  - Discreto ou contínuo: estados e ações são contáveis?
  - Conhecido ou desconhecido: o agente sabe de antemão as regras? (Trata do
    que ele SABE, não do que ele VÊ.)
  Cada classificação vem com uma frase de justificativa — a etiqueta sozinha
  não vale nada.
-->
**Quando se preenche:** no Laboratório 02, no sábado (encontro 2).

[uma linha por dimensão: a classificação e a frase de
justificativa — começando por observabilidade e determinismo]

**Domínio:** AMS · Assistente de Manutenção Segura

| Dimensão | Minha classificação | Justificativa (uma frase) | Consequências |
|---|---|---|---|
| Observabilidade | parcial | O agente recebe as leituras dos sensores, o histórico de falhas e os dados da ordem de serviço, mas não observa diretamente todas as condições da máquina nem os fatores ocultos que podem causar uma falha. | **Precisa** de estado interno, memória e contexto. |
| Número de agentes | único | Um agente especialista que indique a possibilidade iminente de falha na máquina. | **Não Precisa** de protocolo de comunicação e previsão de outro agente. |
| Determinismo | estocástico | A mesma combinação de leituras pode não produzir o mesmo resultado na máquina, pois existem fatores não observados que influenciam a ocorrência de falhas. | **Precisa** considerar valor esperado, novas tentativas e tempo máximo de resposta. |
| Episódico ou sequencial | episódico | Cada ordem de serviço é analisada como um caso independente, e a classificação de uma máquina não altera diretamente a análise das ordens seguintes. | **Não precisa** de planejamento e avaliação de uma trajetória inteira. |
| Estático ou dinâmico | dinâmico | Enquanto a ordem é analisada, a máquina pode continuar operando e suas condições físicas e leituras de sensores podem mudar. | **Precisa** de prazo de resposta e de uma resposta parcial aceitável. |
| Discreto ou contínuo | contínuo | As leituras de temperatura, rotação, torque e desgaste da ferramenta são variáveis numéricas que podem assumir diferentes valores dentro de intervalos contínuos. | **Precisa** de discretização declarada, com granularidade justificada. |
| Conhecido ou desconhecido | desconhecido | Embora as normas sejam documentadas, a relação completa entre as leituras dos sensores, as condições da máquina e a ocorrência de falhas precisa ser estimada a partir do histórico de dados. | **Precisa** de fase de exploração e registro do que foi aprendido. |



---

## 3. Tipo de agente pretendido

<!--
Perguntas que guiam o preenchimento:
  - O tipo mais simples que resolve: reativo simples, baseado em modelo,
    baseado em objetivos, baseado em utilidade, ou um deles com aprendizagem?
  - A caracterização do ambiente (seção 2) é que decide — parcialmente
    observável elimina o reativo simples.
  - Justifique com a dimensão do ambiente que obriga a escolha.
-->
**Quando se preenche:** no sábado (encontro 2, manhã).

[o tipo mais simples que resolve, justificado pela dimensão
do ambiente que o obriga]

---

## 4. Medida de desempenho

<!--
Perguntas que guiam o preenchimento:
  - A fórmula do campo Performance, agora em definição operacional: como se
    calcula, passo a passo, sem ambiguidade?
  - Métrica primária e duas secundárias. As secundárias pegam o que a
    primária deixa passar (custo, latência, reabertura).
  - O conjunto de casos: de onde vêm, quantos são, de que período.
  - O limiar de sucesso e o valor de hoje.
-->
**Quando se preenche:** a fórmula começa no Laboratório 01; a definição
operacional completa — primária, secundárias, conjunto e limiar — é item da
Atividade Orientada.

[métrica primária e duas secundárias, cada uma com: como se
calcula, sobre qual conjunto, qual o limiar de sucesso e o
valor de hoje]

#### **Métrica primária — Recall da classe "alto"**
**Como se calcula:** quantidade de máquinas realmente de alto risco, que foram classificadas como alto, dividido pela quantidade total de máquinas realmente de alto risco.

**Conjunto de dados**: dataset recebido periodicamente com ordens de servico.

**Limiar de sucesso**: maior ou igual a 80%. Valor definido inicialmente, o qual poderá ser ajustado ao receber uma definição clara sobre isso.

**Valor de hoje**: não medido.

#### **Métrica Secundária 1 — Precisão da classe "alto"**
**Como se calcula:** quantidade de máquinas classificadas como alto que são de fato alto dividio pelo total classificado como alto.


**Conjunto de dados**: dataset recebido periodicamente com ordens de servico.

**Limiar de sucesso:** maior ou igual a 80%. Valor definido inicialmente, o qual poderá ser ajustado ao receber uma definição clara sobre isso. 

**Valor de hoje**: não medido.

#### **Secundária 2 — Taxa de erro classificados com baixo e deveria ser alto**
**Como se calcula:** máquinas de risco alto classificadas como baixo dividido pelo total de máquinas de risco alto.

**Conjunto de dados**: dataset recebido periodicamente com ordens de servico.

**Limiar de sucesso:** menor ou igual a 5%. Valor definido inicialmente, o qual poderá ser ajustado ao receber uma definição clara sobre isso. 

**Valor de hoje**: não medido.

---

## 5. Restrições

<!--
Perguntas que guiam o preenchimento:
  - Latência aceitável: a partir de quantos segundos a resposta perde valor?
  - Custo aceitável: quanto pode custar cada resolução?
  - O que o agente jamais pode fazer: a ação irreversível que ele não executa
    sozinho. Esta linha vira política em D12.
  - A troca que você aceita: quanto de qualidade por quanto de custo?
    Um exemplo numérico vale mais que a fórmula.
-->
**Quando se preenche:** na Atividade Orientada.

[latência aceitável, custo aceitável, o que o agente jamais
pode fazer sozinho, e a troca qualidade × custo que você
aceita — com um exemplo numérico]

> 🔶🔶🔶 ANOTAÇÃO DO CLAUDE — APAGUE ESTE BLOCO (ATÉ O MARCADOR DE FECHAMENTO
> ABAIXO) ANTES DE ENVIAR O ARQUIVO PRO PROFESSOR. Não é conteúdo do curso —
> é só um sinalizador pra você achar rápido o que foi inserido agora. 🔶🔶🔶

**Latência aceitável:** até 3–5 segundos por ordem — o `dominio.md`
caracteriza o usuário como "técnico com pouco tempo entre uma ordem e
outra"; acima disso a resposta deixa de caber no fluxo de trabalho.

**Custo aceitável:** o custo real medido por ordem (`llm.py`, preços de
referência US$0,10/US$0,40 por 1M tokens de entrada/saída) fica da ordem
de US$0,0001 por ordem — muito abaixo de qualquer limiar que valeria a
pena formalizar; o teto proposto é R$ 0,05 por ordem, com folga grande.

**O que o agente jamais pode fazer sozinho:** liberar uma máquina pra
operar sem bloqueio/etiquetagem (LOTO) quando a classificação de risco for
"alto" — mesmo com alta confiança do modelo. Consistente com
`dominio.md`: "a decisão final continua sendo do técnico."

**A troca qualidade × custo — função de utilidade:**

```
U(lote) = w_Q·Qualidade − w_C·Custo − w_L·Latência − w_R·Risco
```

| Termo | O que é no AMS | De onde vem |
|---|---|---|
| Qualidade | Recall da classe "alto" (métrica primária, §4) | medido sobre o lote avaliado |
| Custo | custo em R$ do lote (chamadas ao LLM) | `custo_usd` de `llm.py::_registrar`, convertido |
| Latência | segundos até a resposta, média do lote | `latencia_ms/1000`, logado em `log.py` |
| Risco | custo esperado do erro irreversível: P(falso negativo em "alto") × custo de um acidente | P(...) é a Secundária 2 do §4 |

Pesos ilustrativos e exemplo numérico (com os números reais medidos no
lab-06): `w_Q=R$1.000`, `w_C=5`, `w_L=R$2/s`, `w_R=R$500.000` (ordem de
grandeza de um acidente grave — valor ilustrativo, não atuarial); com
recall=0,625, custo≈US$0,00011, latência≈0,8s, P(falso negativo
alto)=0,25:

```
U = 1000×0,625 − 5×0,00011 − 2×0,8 − 500000×0,25 ≈ R$ −124.377
```

O resultado negativo, dominado pelo termo de risco, é o comportamento
esperado de um peso alto nesse termo: nenhum ganho de qualidade, custo ou
latência compensa um erro irreversível.

🔶🔶🔶 FIM DA ANOTAÇÃO DO CLAUDE — apague até aqui 🔶🔶🔶

---

## 6. Catálogo de ações

<!--
Perguntas que guiam o preenchimento:
  - Para cada ação: nome, entrada, saída, é reversível?, qual o risco se
    errar? As quatro colunas são obrigatórias — "baixo" não é descrição de
    risco.
  - Ações de leitura E de escrita: as que alteram o mundo são as que exigem
    cuidado, e são justamente as que mais ficam de fora.
  - Este catálogo é, literalmente, a lista de ferramentas que você vai
    implementar em D10.
-->
**Quando se preenche:** na Atividade Orientada — o pacote `D2-07` traz o
modelo da tabela e dois exemplos preenchidos.

[tabela: nome · entrada · saída · é reversível? · risco se
errar — ações de leitura e de escrita]

---

## 7. Formulação por busca

<!--
Perguntas que guiam o preenchimento:
  - Qual fatia do problema é um espaço de estados? (Nem toda fatia é — e
    reconhecer a que não é vale tanto quanto formular a que é.)
  - Os cinco componentes: estado inicial, ações, modelo de transição, teste
    de objetivo, custo de caminho. Comece pelo teste de objetivo.
  - O estado descreve a SITUAÇÃO, não a história de como se chegou nela.
-->
**Quando se preenche:** no Laboratório 03, sábado à tarde (encontro 2).

**Classe modificada:**

*consultdas_ams.py*

```python
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

# Nomes de fatos/fontes trocados do domínio de produção/estoque pro de
# manutenção segura (latências e estrutura de cobertura IDÊNTICAS às
# anteriores — só o vocabulário muda, os números das buscas não mudam).
# Mapa completo em D02/PLANO-renomeacao-dominio-consultas.md.

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
```


**Resultado - Saída:**
```bash
(ams) PS C:\temp\UTFPR\Projeto-AMS> uv run .\D02\D2-03-formular-como-busca\verificar-formulacao.py 
verificar-formulacao — teste de sanidade da formulação de busca
(sem argumentos: rodando sobre o catálogo — aponte o seu com arquivo.py:ATRIBUTO)

— diagnostico.PEQUENA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

— diagnostico.MAIOR
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

— consultas.PEQUENA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

— consultas.MAIOR
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

— conformidade.PEQUENA
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

— conformidade.MAIOR
  1. estado é hashable ✅
  2. transição é função ✅
  3. ações estáveis na ordem ✅
  4. custo é positivo ou zero ✅
  5. objetivo é alcançável ✅
  6. estado não guarda o caminho ✅
  resumo: 6 ✅ · 0 ⚠️ · 0 ❌

Seis verificações verdes — a formulação pode ir para o agent-spec.md e para o lab-04.
```