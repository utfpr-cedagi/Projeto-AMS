# NOTA — entendendo `EstadoDaFrota` (estado interno do lab-06)

Explica a classe `EstadoDaFrota` de [`esqueleto.py`](esqueleto.py) — a
memória do agente, usada pela segunda condição de `decidir()`. Útil pra
quem está vendo o trecho pela primeira vez e quer entender o que o
`return sum(...)` de `falhas_recentes` realmente faz, e por que a janela
de dias existe.

## 1. O que essa classe representa

`EstadoDaFrota` é a **memória** do agente — o que ele já observou do
ambiente, acumulado caso a caso. Isso existe porque o ambiente AMS é
**parcialmente observável** (comentário no topo do arquivo): olhando só
o registro de hoje, o agente não sabe se essa máquina faz parte de uma
família que andou falhando muito ultimamente. Por isso a classe guarda
um histórico e oferece uma pergunta sobre ele: "quantas falhas recentes
essa família teve?"

## 2. `__init__` — os três campos da memória

```python
def __init__(self, janela_dias: int = JANELA_DIAS) -> None:
    self._janela = janela_dias
    self._falhas: list[tuple[str, _date]] = []
    self._ultima_data: _date | None = None
```

- `_janela`: quantos dias contam como "recente" (vem de
  `JANELA_DIAS = 7`).
- `_falhas`: uma lista de pares `(família, data)` — um registro por falha
  **já observada**, não por caso processado. Começa vazia: o agente nasce
  sem memória.
- `_ultima_data`: a data do último registro processado. Começa `None`
  porque, antes do primeiro caso, não existe "hoje" ainda.

## 3. `registrar_desfecho` — como a memória cresce

```python
def registrar_desfecho(self, registro: dict) -> None:
    self._ultima_data = _date.fromisoformat(registro["data"])
    if int(registro.get("falhou_depois", 0)) == 1:
        self._falhas.append(
            (registro["tipo_maquina"], self._ultima_data))
```

O `medir.py` chama isso **depois** de `decidir()`, nunca antes
([`medir.py:42-49`](medir.py#L42-L49)):

```python
decisao = decidir(registro, estado)       # 1. decide com o que já sabia
...
estado.registrar_desfecho(registro)       # 2. só DEPOIS aprende o desfecho
```

É o ciclo "parcialmente observável" que o docstring descreve: o agente
decide sem saber se a máquina de hoje vai falhar, e só depois o ambiente
revela (`falhou_depois`). Se revelou falha, grava `(tipo_maquina, data)`
na lista — senão, não grava nada (não há o que lembrar de um caso sem
falha).

## 4. `falhas_recentes` — o coração do estado

```python
def falhas_recentes(self, familia: str) -> int:
    if self._ultima_data is None:
        return 0
    limite = self._ultima_data.toordinal() - self._janela
    return sum(
        1 for familia_vista, dia in self._falhas
        if familia_vista == familia and dia.toordinal() >= limite)
```

**Linha 1 — guarda de segurança:** se ainda não processou nenhum caso
(`_ultima_data is None`), não tem "hoje" pra calcular janela nenhuma —
devolve 0 sem erro.

**`limite = self._ultima_data.toordinal() - self._janela`:**
`toordinal()` converte uma data em um número inteiro (dias desde uma
data de referência fixa do calendário). Isso transforma "está dentro de
7 dias" numa subtração de inteiros, em vez de lidar com objetos
`timedelta`. `limite` é o primeiro dia que ainda conta como "recente" —
qualquer falha **antes** desse dia já "esqueceu".

**O `return sum(...)`:**

```python
sum(1 for familia_vista, dia in self._falhas
    if familia_vista == familia and dia.toordinal() >= limite)
```

Isso é uma *generator expression* — uma forma compacta de "percorra,
filtre, e processe", tudo numa linha, sem criar uma lista intermediária
na memória. Lendo de dentro pra fora:

1. `for familia_vista, dia in self._falhas` — percorre a lista de
   falhas, e cada **tupla** `(família, data)` é desempacotada direto em
   duas variáveis (`familia_vista`, `dia`).
2. `if familia_vista == familia and dia.toordinal() >= limite` — filtro
   duplo: só conta se for da família perguntada **e** se a data está
   dentro da janela.
3. `1 for ... if ...` — para cada item que passa no filtro, produz o
   valor `1` (não a tupla, não a data — só uma marca "isso conta").
4. `sum(...)` — soma todos esses `1`s, ou seja, **conta quantos itens
   passaram no filtro**.

É um idioma comum em Python: `sum(1 for x in lista if condicao)` é a
forma "pythônica" de escrever "conte quantos elementos de `lista`
satisfazem `condicao`" — equivalente a um
`len([x for x in lista if condicao])`, mas sem montar a lista toda na
memória, só os `1`s voando um a um pro `sum`.

## 5. Vendo a memória crescer e esquecer, com dados reais

Usando as linhas de `tipo_maquina == "H"` do
[`adaptacao-ams/casos-lab-06-v2.csv`](adaptacao-ams/casos-lab-06-v2.csv),
na ordem cronológica em que `medir.py` processa (lembrando: `decidir()`
sempre vê o estado **antes** do próprio desfecho de hoje ser revelado):

| Caso | Dia | H falhou? | `_falhas` (H) *antes* desta decisão | `limite` (hoje − 7 dias) | `falhas_recentes("H")` |
|---|---|---|---|---|---|
| A03 | 04-03 | sim | `[]` | — | **0** |
| A07 | 04-07 | sim (atípico) | `[(H,04-03)]` | 03-31 | **1** (04-03 ≥ 03-31) |
| A08 | 04-08 | não | `[(H,04-03), (H,04-07)]` | 04-01 | **2** |
| A09 | 04-09 | sim | mesma lista | 04-02 | **2** |
| A13 | 04-13 | não | `[(H,04-03),(H,04-07),(H,04-09)]` | 04-06 | **2** — a de 04-03 "envelheceu" e saiu da janela (04-03 < 04-06), mas as outras duas ainda contam |

Em A08, `falhas_recentes("H")` já chega a 2 = `FALHAS_PARA_INSPECAO`,
então a condição de estado **dispararia** `inspecionar_antes_de_operar`
— só que a primeira condição (`vibracao_mm_s = 9,2 > 7,0`) já decide
antes (lembrando: "a ordem importa: a primeira que casar decide" —
[`esqueleto.py:117`](esqueleto.py#L117)), então o agente devolve
`parar_para_manutencao`. O rótulo correto de A08 é
`inspecionar_antes_de_operar` (risco médio) — esse é um dos erros que o
baseline comete, e é exatamente o tipo de caso que a análise escrita do
laboratório pede pra explicar.

Em A13 dá pra ver a **política de esquecimento** funcionando de verdade:
sem a janela de 7 dias, a falha antiga de A03 (04-03) ficaria contando
pra sempre, e a família H nunca mais sairia do "em observação" mesmo
depois de dias tranquilos.
