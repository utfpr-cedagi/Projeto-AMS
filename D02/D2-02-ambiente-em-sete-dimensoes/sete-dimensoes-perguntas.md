# Sete dimensões — perguntas para o meu ambiente

<!--
Este arquivo é o formulário do Laboratório 02: preencha DENTRO dele, na
seção do seu domínio, no fim. As perguntas por dimensão estão em comentário
como este — aparecem no editor, não na pré-visualização.

Em cada dimensão, a resposta tem duas partes obrigatórias: a classificação
e UMA FRASE de justificativa. A justificativa é o que a rubrica pontua — a
etiqueta sozinha não vale nada (slide 32). Quando a resposta honesta for
"depende", escreva de que depende e em que situação cada resposta se
aplica: isso é caracterização melhor, não pior.

Copie a tabela preenchida para a seção 2 do seu agent-spec.md ao terminar.
-->

## As sete perguntas (as mesmas do slide 22)

| Dimensão | A pergunta que ela faz |
|---|---|
| Observabilidade | O agente enxerga tudo o que precisa para decidir? |
| Número de agentes | Existe outro agente cujas ações afetam o resultado? |
| Determinismo | A mesma ação no mesmo estado dá sempre o mesmo efeito? |
| Episódico ou sequencial | A decisão de agora afeta as decisões seguintes? |
| Estático ou dinâmico | O ambiente muda enquanto o agente delibera? |
| Discreto ou contínuo | Estados e ações são contáveis ou variam sem degraus? |
| Conhecido ou desconhecido | O agente sabe de antemão as regras do ambiente? |

## O que prestar atenção em cada uma

- **Observabilidade** — o teste que decide: existe algo que muda a decisão
  correta e que o agente não mede? Se existe, é parcialmente observável,
  e o projeto precisa de estado interno. Quase todo domínio real é
  parcialmente observável; a resposta honesta aqui costuma ser "parcial".
- **Número de agentes** — um humano operador conta, se ele reage ao que o
  agente faz. Se a sua resposta for multiagente, a D11 será central para
  o seu projeto, e não periférica.
- **Determinismo** — é sobre o efeito das ações, não sobre a observação.
  E atenção: qualquer sistema que chame um modelo de linguagem tem uma
  ação estocástica no meio.
- **Episódico ou sequencial** — classificar um lote é episódico; conduzir
  um atendimento é sequencial. A consequência prática é o custo de
  avaliação: episódico avalia casos independentes, sequencial exige
  avaliar trajetórias inteiras.
- **Estático ou dinâmico** — dinâmico impõe prazo: resposta tardia é
  resposta errada. O caso do meio tem nome: semidinâmico, quando o
  ambiente não muda mas a nota do agente cai com a espera.
- **Discreto ou contínuo** — busca funciona sobre enumeração; contínuo
  precisa ser discretizado antes, e toda discretização perde informação.
  Se você discretizar, a granularidade é decisão declarada, com custo dos
  dois lados.
- **Conhecido ou desconhecido** — a distinção que mais confunde: trata do
  que o agente SABE sobre as regras, e não do que ele VÊ. Sistema legado
  sem documentação é ambiente desconhecido, mesmo que se enxergue tudo
  nele.

## As respostas do meu domínio

**Domínio:** [título curto do domínio]

| Dimensão | Minha classificação | Justificativa (uma frase) |
|---|---|---|
| Observabilidade | [total / parcial] | [por quê] |
| Número de agentes | [único / multiagente] | [por quê] |
| Determinismo | [determinístico / estocástico] | [por quê] |
| Episódico ou sequencial | [episódico / sequencial] | [por quê] |
| Estático ou dinâmico | [estático / dinâmico / semidinâmico] | [por quê] |
| Discreto ou contínuo | [discreto / contínuo] | [por quê] |
| Conhecido ou desconhecido | [conhecido / desconhecido] | [por quê] |

**O que a tabela de consequências obriga no meu projeto** (conferir no
`tabela-de-consequencias.pdf` e colar aqui as linhas que se aplicam):

[responda aqui — pode começar pelas que NÃO se aplicam, que valem igual]
