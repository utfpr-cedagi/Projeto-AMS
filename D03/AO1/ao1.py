"""AO1 da D3: compara a linha de base (A) com a variante B nos mesmos 60 casos.

Adaptado do arquivo de apoio do professor (`apoio-professor/ao1.py`).
Rode com o .venv do projeto, de qualquer pasta:
    .venv\\Scripts\\python.exe D03\\AO1\\ao1.py
ou, de dentro do notebook `03-estatistica.ipynb`, com `%run ao1.py`.

Gera `acertos.csv` (nesta mesma pasta), uma linha por caso e uma coluna
por variante, com 0 (errou) e 1 (acertou): o arquivo que os labs 05 e 06
leem.
"""
import csv
import time
from pathlib import Path

import numpy as np

# Do próprio projeto, src/ams/baseline.py:
# decidir() é a variante A; EstadoDaFrota guarda as falhas recentes; carregar_casos() lê o CSV.
# Os limiares da A são reaproveitados pela B (sem números novos).
from ams.baseline import (
    LIMITE_DESGASTE,
    LIMITE_VIBRACAO,
    EstadoDaFrota,
    carregar_casos,
    decidir,
)

PASTA = Path(__file__).resolve().parent

# Os 60 casos rotulados do autor: 30 da D2 (A01-A30) + 30 novos (B01-B30).
# Procedência em dados/FONTE.md.
ARQUIVO_DE_CASOS = PASTA / "dados" / "casos-60.csv"
ARQUIVO_DE_ACERTOS = PASTA / "acertos.csv"


# --- Variante B ---------------------------------------------------------------
# A minha mudança:
# R: acrescentei um PASSO DE VERIFICAÇÃO antes de parar a máquina. A variante
#    A para com uma única evidência de sensor (a primeira condição que casa
#    decide). A B conta as evidências independentes de risco e só manda parar
#    quando duas ou mais confirmam:
#      - sensor: vibração acima de LIMITE_VIBRACAO (7,0 mm/s);
#      - desgaste: horas desde a manutenção >= LIMITE_DESGASTE (150 h);
#      - histórico: ao menos UMA falha recente da mesma família de máquina.
#    2 ou mais evidências -> parar_para_manutencao (risco confirmado);
#    exatamente 1 evidência -> inspecionar_antes_de_operar (sinal isolado
#      pede verificação, não parada para manutenção; a inspeção com acesso
#      físico à máquina também exige bloqueio/LOTO, conforme a NR-12);
#    nenhuma evidência -> seguir_operando.
#    São DUAS mudanças em relação à A, e as duas são declaradas:
#      1. a regra de decisão: confirmação por duas fontes no lugar de "a
#         primeira condição que casa decide" (a mudança principal);
#      2. o corte do histórico: a A só usa o histórico com >= 2 falhas
#         recentes (FALHAS_PARA_INSPECAO); a B conta o histórico como
#         evidência já com >= 1. Sem isso, o histórico raramente somaria
#         como segunda evidência.
#    Os limiares de vibração e desgaste são os mesmos da A.
#    A B é experimental: serve para a comparação da AO1, não foi adotada
#    como agente.

def contar_evidencias(caso, estado):
    """Quantas fontes independentes apontam risco neste caso (0 a 3)."""
    return sum([
        caso["vibracao_mm_s"] > LIMITE_VIBRACAO,
        caso["horas_desde_manutencao"] >= LIMITE_DESGASTE,
        estado.falhas_recentes(caso["tipo_maquina"]) >= 1,
    ])


def decidir_b(caso, estado):
    evidencias = contar_evidencias(caso, estado)
    if evidencias >= 2:
        return "parar_para_manutencao"
    if evidencias == 1:
        return "inspecionar_antes_de_operar"
    return "seguir_operando"


# --- Acertos de A e B nos mesmos casos (item 1 do enunciado) -------------------
# 1 = acertou a ação, 0 = errou.

def contar_acertos(casos, funcao_de_decisao):
    estado = EstadoDaFrota()
    acertos = []
    decisoes = []
    for caso in casos:
        decisao = funcao_de_decisao(caso, estado)
        decisoes.append(decisao)
        acertos.append(1 if decisao == caso["acao_correta"] else 0)
        estado.registrar_desfecho(caso)   # o agente fica sabendo se a máquina falhou
    return acertos, decisoes


casos = carregar_casos(ARQUIVO_DE_CASOS)
acertos_a, decisoes_a = contar_acertos(casos, decidir)
acertos_b, decisoes_b = contar_acertos(casos, decidir_b)

with open(ARQUIVO_DE_ACERTOS, "w", newline="") as arquivo:
    escritor = csv.writer(arquivo)
    escritor.writerow(["linha_de_base", "variante_b"])
    for i in range(len(casos)):
        escritor.writerow([acertos_a[i], acertos_b[i]])

print(len(casos), "casos")
print("A acertou", sum(acertos_a), "· B acertou", sum(acertos_b))
print("decisões diferentes entre A e B:",
      sum(a != b for a, b in zip(decisoes_a, decisoes_b)))
for i in range(len(casos)):
    if acertos_a[i] != acertos_b[i]:
        print("discordam no", casos[i]["id_caso"], "· A:", acertos_a[i], "· B:", acertos_b[i])

if acertos_a == acertos_b:
    print("A e B acertaram os mesmos casos. A regra nova da B já foi escrita?")


# --- Latência de A e B, p50 e p95 (item 2 do enunciado) ------------------------
# Cronometra cada decisão, passando 50 vezes pelos casos.

def medir_latencia(funcao_de_decisao, rodadas=50):
    tempos = []
    for _ in range(rodadas):
        estado = EstadoDaFrota()
        for caso in casos:
            inicio = time.perf_counter()
            funcao_de_decisao(caso, estado)
            tempos.append((time.perf_counter() - inicio) * 1_000_000)   # em microssegundos
            estado.registrar_desfecho(caso)
    return np.array(tempos)


tempos_a = medir_latencia(decidir)
tempos_b = medir_latencia(decidir_b)
tempos = tempos_a   # nome do arquivo de apoio do professor (linha de base)

for nome, t in [("A", tempos_a), ("B", tempos_b)]:
    print(f"latência {nome} (µs) em", len(t), "decisões:",
          "p50", round(np.percentile(t, 50), 2),
          "· p95", round(np.percentile(t, 95), 2),
          "· média", round(np.mean(t), 2),
          "· máximo", round(np.max(t), 2))


# O intervalo de confiança e o tamanho de amostra ficam no notebook (depois do E3, entregues com a N2).
