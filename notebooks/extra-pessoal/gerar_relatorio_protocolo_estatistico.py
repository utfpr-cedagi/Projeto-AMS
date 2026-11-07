"""Gera o relatório estatístico (.md) de `02-protocolo-estatistico.ipynb`.

Mesmas 8 seções do notebook (visão geral, descritiva univariada, outliers
IQR, correlação, falha x variável, tipo x falha, os cinco mecanismos,
classificador agregado), mas a narrativa é **computada a partir do que saiu
daquela rodada** — nunca um número fixo no texto. É por isso que o notebook
existe: lá, as células de markdown tinham número escrito à mão, e trocar a
fonte do dado (`FONTE_DADOS = "raw"` ou `"amostra"`, célula 1) deixava a
prosa dizendo uma coisa e a tabela dizendo outra. Aqui, sempre que o dataset
mudar de novo, basta rodar de novo.

Uso:
    .venv/Scripts/python.exe notebooks/extra-pessoal/gerar_relatorio_protocolo_estatistico.py            # gera os dois (amostra e raw)
    .venv/Scripts/python.exe notebooks/extra-pessoal/gerar_relatorio_protocolo_estatistico.py --fonte raw
    .venv/Scripts/python.exe notebooks/extra-pessoal/gerar_relatorio_protocolo_estatistico.py --fonte amostra
"""

from __future__ import annotations

import argparse
from pathlib import Path

import pandas as pd
from scipy import stats

from ams import analise
from ams.dados import RAIZ_DO_PACOTE, Dataset, carregar, preparar
from ams.gerador_casos import (
    HDF_LIMITE_DELTA,
    HDF_LIMITE_ROTACAO,
    MARGEM_DIFICIL_HDF_DELTA,
    MARGEM_DIFICIL_HDF_ROTACAO,
    MARGEM_DIFICIL_OSF,
    MARGEM_DIFICIL_PWF,
    OSF_LIMITES,
    PWF_FAIXA_SEGURA,
    TWF_JANELA,
)

NUMERICAS = ["temperatura_ar", "temperatura_processo", "rotacao", "torque",
             "desgaste", "delta_temperatura", "potencia_kw"]
CRITERIO_RECALL_ALTO = 0.80
CRITERIO_PRECISAO_ALTO = 0.80
CRITERIO_TAXA_ALTO_PARA_BAIXO = 0.05


def _br(valor: float, casas: int = 2) -> str:
    """Formata em português (vírgula decimal) — só para prosa, nunca tabela."""
    return f"{valor:,.{casas}f}".replace(",", "@").replace(".", ",").replace("@", ".")


def _n(valor: float, casas: int = 4) -> str:
    """Formata em tabela (ponto decimal, como o resto do projeto)."""
    return f"{valor:.{casas}f}"


def _pct(fracao: float, casas: int = 1) -> str:
    return "—" if pd.isna(fracao) else _br(fracao * 100, casas) + "%"


def carregar_fonte(fonte: str) -> tuple[Dataset, pd.DataFrame]:
    caminho = RAIZ_DO_PACOTE / "data" / fonte / "ai4i2020.csv"
    dataset = carregar(caminho=caminho)
    df = preparar(dataset.quadro)
    df["potencia_w"] = df["potencia_kw"] * 1000.0
    df["osf_produto"] = df["desgaste"] * df["torque"]
    df["osf_limite"] = df["tipo"].astype(str).map(OSF_LIMITES).astype(float)
    return dataset, df


def secao1_visao_geral(df: pd.DataFrame) -> tuple[dict, list[str]]:
    faltantes = df.isna().sum()
    faltantes = faltantes[faltantes > 0]
    contagem_tipo = df["tipo"].value_counts()
    pct_tipo = (contagem_tipo / len(df) * 100).round(1)
    dominante, minoria = contagem_tipo.idxmax(), contagem_tipo.idxmin()

    linhas = [
        "## 1 — Visão geral e qualidade dos dados",
        "",
        "| medida | valor |",
        "|---|---:|",
        f"| linhas | {len(df)} |",
        f"| UDIs únicos | {df['udi'].nunique()} |",
        f"| duplicados | {df.duplicated().sum()} |",
        f"| colunas com valor faltante | {len(faltantes)} |",
        "",
        "Distribuição de `tipo`:",
        "",
        "| tipo | n | % |",
        "|---|---:|---:|",
    ]
    linhas += [f"| {t} | {n} | {_n(pct_tipo[t], 1)} |" for t, n in contagem_tipo.items()]
    linhas += [
        "",
        f"**Conclusão:** {len(df)} linhas, {df['udi'].nunique()} UDIs únicos, "
        f"{df.duplicated().sum()} duplicados e "
        f"{'zero valores faltantes' if not len(faltantes) else f'{len(faltantes)} coluna(s) com faltante'} "
        f"— confirmado, não assumido. `tipo` {'é fortemente desbalanceado' if pct_tipo.max() - pct_tipo.min() > 20 else 'tem distribuição relativamente próxima entre categorias'} "
        f"(`{dominante}` domina com {_br(pct_tipo[dominante], 1)}%, `{minoria}` é minoria com "
        f"{_br(pct_tipo[minoria], 1)}%) — qualquer diferença de taxa de falha por tipo (seção 6) "
        "parte de amostras de tamanhos bem diferentes.",
        "",
    ]
    destaques = {
        "desbalanceado": bool(pct_tipo.max() - pct_tipo.min() > 20),
        "dominante": dominante, "pct_dominante": float(pct_tipo[dominante]),
        "minoria": minoria, "pct_minoria": float(pct_tipo[minoria]),
    }
    return destaques, linhas


def secao2_descritiva(df: pd.DataFrame) -> tuple[pd.DataFrame, dict, list[str]]:
    resumo = pd.DataFrame({
        "media": df[NUMERICAS].mean(),
        "mediana": df[NUMERICAS].median(),
        "desvio_padrao": df[NUMERICAS].std(),
        "assimetria": df[NUMERICAS].skew(),
        "curtose": df[NUMERICAS].kurt(),
        "Q1": df[NUMERICAS].quantile(0.25),
        "Q3": df[NUMERICAS].quantile(0.75),
    })
    resumo["AIQ"] = resumo["Q3"] - resumo["Q1"]
    resumo["normaltest_p"] = [stats.normaltest(df[c]).pvalue for c in NUMERICAS]

    mais_simetrica = resumo["assimetria"].abs().idxmin()
    mais_assimetrica = resumo["assimetria"].abs().idxmax()
    mais_normal = resumo["normaltest_p"].idxmax()
    rejeitam_normalidade = resumo.index[resumo["normaltest_p"] < 0.05].tolist()
    mais_uniforme = resumo["curtose"].idxmin()

    linhas = [
        "## 2 — Estatística descritiva univariada",
        "",
        "| variável | média | mediana | desvio | assimetria | curtose | Q1 | Q3 | AIQ | normaltest p |",
        "|---|---:|---:|---:|---:|---:|---:|---:|---:|---:|",
    ]
    for var, linha in resumo.iterrows():
        linhas.append(
            f"| {var} | {_n(linha['media'])} | {_n(linha['mediana'])} | {_n(linha['desvio_padrao'])} "
            f"| {_n(linha['assimetria'])} | {_n(linha['curtose'])} | {_n(linha['Q1'])} | {_n(linha['Q3'])} "
            f"| {_n(linha['AIQ'])} | {_n(linha['normaltest_p'])} |"
        )
    linhas += [
        "",
        f"**Conclusão:** nem toda variável de sensor tem a mesma forma. `{mais_simetrica}` é a mais "
        f"próxima de simétrica desta rodada (assimetria {_br(resumo.loc[mais_simetrica, 'assimetria'])}), "
        f"enquanto `{mais_assimetrica}` é a mais assimétrica (assimetria "
        f"{_br(resumo.loc[mais_assimetrica, 'assimetria'])}, curtose "
        f"{_br(resumo.loc[mais_assimetrica, 'curtose'])}). `{mais_normal}` é a variável em que o "
        f"`normaltest` tem o maior p-valor desta rodada (p={_br(resumo.loc[mais_normal, 'normaltest_p'], 3)}"
        f"{', não rejeita normalidade a 5%' if resumo.loc[mais_normal, 'normaltest_p'] >= 0.05 else ', mesmo assim rejeita a 5% — nenhuma variável passou neste tamanho de amostra'}); "
        f"{len(rejeitam_normalidade)} de {len(NUMERICAS)} variáveis rejeitam normalidade a 5% nesta rodada "
        f"(n={len(df)} — lembrar que o poder do teste cresce com n: com amostra pequena, rejeitar fica mais "
        "difícil mesmo quando a forma não é de fato normal). "
        f"`{mais_uniforme}` é a de curtose mais negativa (curtose {_br(resumo.loc[mais_uniforme, 'curtose'])}), "
        "sinal de distribuição mais achatada/uniforme que as demais.",
        "",
    ]
    destaques = {
        "mais_assimetrica": mais_assimetrica,
        "assimetria_mais_assimetrica": float(resumo.loc[mais_assimetrica, "assimetria"]),
        "mais_normal": mais_normal,
        "p_mais_normal": float(resumo.loc[mais_normal, "normaltest_p"]),
        "n_rejeitam_normalidade": len(rejeitam_normalidade),
    }
    return resumo, destaques, linhas


def secao3_outliers(df: pd.DataFrame, resumo: pd.DataFrame) -> tuple[pd.DataFrame, dict, list[str]]:
    limite_inferior = resumo["Q1"] - 1.5 * resumo["AIQ"]
    limite_superior = resumo["Q3"] + 1.5 * resumo["AIQ"]

    outliers = pd.DataFrame(index=NUMERICAS)
    outliers["n_extremos"] = [
        int(((df[c] < limite_inferior[c]) | (df[c] > limite_superior[c])).sum())
        for c in NUMERICAS
    ]
    outliers["pct_extremos"] = outliers["n_extremos"] / len(df)
    outliers["pct_extremos_que_falharam"] = [
        df.loc[(df[c] < limite_inferior[c]) | (df[c] > limite_superior[c]), "falha"].mean()
        if outliers.loc[c, "n_extremos"] > 0 else float("nan")
        for c in NUMERICAS
    ]
    taxa_falha_geral = analise.taxa_falha_geral(df)

    sem_outlier = outliers.index[outliers["n_extremos"] == 0].tolist()
    com_outlier = outliers[outliers["n_extremos"] > 0].sort_values(
        "pct_extremos_que_falharam", ascending=False
    )

    linhas = [
        "## 3 — Outliers via IQR",
        "",
        "Regra do boxplot (fora de `[Q1 − 1,5·AIQ, Q3 + 1,5·AIQ]`), mesma do `D3-03/medidas.py`.",
        "",
        "| variável | n extremos | % extremos | % dos extremos que falharam |",
        "|---|---:|---:|---:|",
    ]
    for var, linha in outliers.iterrows():
        linhas.append(
            f"| {var} | {int(linha['n_extremos'])} | {_n(linha['pct_extremos'] * 100, 2)} "
            f"| {'—' if pd.isna(linha['pct_extremos_que_falharam']) else _n(linha['pct_extremos_que_falharam'] * 100, 1)} |"
        )

    linhas.append("")
    if sem_outlier:
        linhas.append(
            f"**Conclusão:** {len(sem_outlier)} de {len(NUMERICAS)} variáveis não têm nenhum outlier "
            f"pela regra do boxplot nesta rodada ({', '.join(f'`{v}`' for v in sem_outlier)})."
        )
    else:
        linhas.append("**Conclusão:** todas as variáveis desta rodada têm pelo menos um outlier.")
    if len(com_outlier):
        destaque = com_outlier.index[0]
        linhas.append(
            f" Das que têm outlier, `{destaque}` concentra a maior taxa de falha dentro do grupo extremo "
            f"({_br(com_outlier.loc[destaque, 'pct_extremos_que_falharam'] * 100, 1)}%, contra "
            f"{_br(taxa_falha_geral * 100, 1)}% de taxa de falha geral) — outlier com concentração de falha "
            "bem acima da taxa geral é sinal, não ruído, e a decisão caso a caso (como o `D3-03/medidas.py` "
            "pede) tende a manter esses pontos: são justamente os casos que o projeto existe para detectar."
        )
    linhas.append("")
    destaques = {
        "n_sem_outlier": len(sem_outlier),
        "sem_outlier": sem_outlier,
        "melhor_outlier": com_outlier.index[0] if len(com_outlier) else None,
        "pct_falha_melhor_outlier": (
            float(com_outlier.iloc[0]["pct_extremos_que_falharam"]) if len(com_outlier) else None
        ),
    }
    return outliers, destaques, linhas


def secao4_correlacao(df: pd.DataFrame) -> tuple[dict, list[str]]:
    pearson = df[NUMERICAS].corr(method="pearson")
    spearman = df[NUMERICAS].corr(method="spearman")
    diferenca_max = (pearson - spearman).abs().to_numpy()
    import numpy as np
    diferenca_max = diferenca_max[~np.eye(len(NUMERICAS), dtype=bool)].max()

    torque_rotacao = analise.correlacao_torque_rotacao(df)
    potencia_torque = pearson.loc["potencia_kw", "torque"]
    potencia_rotacao = pearson.loc["potencia_kw", "rotacao"]

    def tabela_matriz(matriz: pd.DataFrame, titulo: str) -> list[str]:
        cabecalho = "| var | " + " | ".join(matriz.columns) + " |"
        separador = "|---|" + "---:|" * len(matriz.columns)
        linhas_tabela = [f"**{titulo}**", "", cabecalho, separador]
        for var, linha in matriz.iterrows():
            linhas_tabela.append(f"| {var} | " + " | ".join(_n(v, 2) for v in linha) + " |")
        linhas_tabela.append("")
        return linhas_tabela

    linhas = ["## 4 — Correlação bivariada", ""]
    linhas += tabela_matriz(pearson, "Pearson")
    linhas += tabela_matriz(spearman, "Spearman")
    linhas += [
        f"**Conclusão:** maior diferença absoluta entre Pearson e Spearman nesta rodada: "
        f"{_br(diferenca_max, 3)} — "
        f"{'concordância alta' if diferenca_max < 0.1 else 'alguma divergência'}, "
        f"{'não há relação não-linear forte escondida que só o Spearman capturaria' if diferenca_max < 0.1 else 'vale olhar com mais cuidado o(s) par(es) onde os dois mais discordam'}. "
        f"Torque×rotação (Pearson, via `analise.py`): {_br(torque_rotacao, 3)} "
        f"({'negativa' if torque_rotacao < 0 else 'positiva'} — coerente com potência aproximadamente "
        "constante). `potencia_kw` correlaciona "
        f"{_br(potencia_torque, 3)} com torque e {_br(potencia_rotacao, 3)} com rotação — é função "
        "determinística dos dois, não uma terceira variável independente; um classificador que use os três "
        "como preditores separados está contando a mesma informação mais de uma vez.",
        "",
    ]
    destaques = {"potencia_torque": float(potencia_torque), "potencia_rotacao": float(potencia_rotacao),
                 "torque_rotacao": float(torque_rotacao)}
    return destaques, linhas


def secao5_grupo(df: pd.DataFrame) -> tuple[pd.DataFrame, dict, list[str]]:
    variaveis_grupo = ["desgaste", "delta_temperatura", "torque", "potencia_kw"]
    acionadores_nominais = {"desgaste", "delta_temperatura"}

    registros = []
    for coluna in variaveis_grupo:
        grupo_0 = df.loc[~df["falha"], coluna]
        grupo_1 = df.loc[df["falha"], coluna]
        if len(grupo_0) == 0 or len(grupo_1) == 0:
            registros.append({"variavel": coluna, "mediana_nao_falhou": grupo_0.median() if len(grupo_0) else float("nan"),
                               "mediana_falhou": grupo_1.median() if len(grupo_1) else float("nan"),
                               "mannwhitney_p": float("nan"), "efeito_rank_biserial": float("nan")})
            continue
        estatistica_u, p_valor = stats.mannwhitneyu(grupo_1, grupo_0, alternative="two-sided")
        efeito_rank_biserial = 1 - (2 * estatistica_u) / (len(grupo_0) * len(grupo_1))
        registros.append({
            "variavel": coluna, "mediana_nao_falhou": grupo_0.median(), "mediana_falhou": grupo_1.median(),
            "mannwhitney_p": p_valor, "efeito_rank_biserial": efeito_rank_biserial,
        })
    tabela = pd.DataFrame(registros).set_index("variavel")

    linhas = [
        "## 5 — Falha vs. não-falha, por variável",
        "",
        "| variável | mediana não-falhou | mediana falhou | Mann-Whitney p | efeito rank-biserial |",
        "|---|---:|---:|---:|---:|",
    ]
    for var, linha in tabela.iterrows():
        linhas.append(
            f"| {var} | {_n(linha['mediana_nao_falhou'])} | {_n(linha['mediana_falhou'])} "
            f"| {'—' if pd.isna(linha['mannwhitney_p']) else _n(linha['mannwhitney_p'])} "
            f"| {'—' if pd.isna(linha['efeito_rank_biserial']) else _n(linha['efeito_rank_biserial'])} |"
        )

    valida = tabela.dropna(subset=["efeito_rank_biserial"])
    destaques = {"melhor_separador": None, "efeito_melhor_separador": None, "melhor_e_nominal": None}
    linhas.append("")
    if len(valida):
        ranking = valida["efeito_rank_biserial"].abs().sort_values(ascending=False)
        melhor = ranking.index[0]
        significativos = valida.index[valida["mannwhitney_p"] < 0.05].tolist()
        melhor_e_nominal = melhor in acionadores_nominais
        destaques.update(melhor_separador=melhor, efeito_melhor_separador=float(tabela.loc[melhor, "efeito_rank_biserial"]),
                          melhor_e_nominal=melhor_e_nominal)
        linhas.append(
            f"**Conclusão:** `{melhor}` é a variável que mais separa falha de não-falha nesta rodada "
            f"(efeito rank-biserial {_br(tabela.loc[melhor, 'efeito_rank_biserial'])}) — "
            + ("confirma a intuição de que o acionador nominal do modo de falha separa mais."
               if melhor_e_nominal else
               "ao contrário da intuição óbvia de que o acionador nominal (`desgaste`/`delta_temperatura`) "
               "separaria mais: aqui quem mais separa não é o acionador nominal de nenhum modo isoladamente, "
               "o que sugere efeito cruzado entre mecanismos (ex.: OSF usa desgaste×torque, PWF usa potência).")
            + f" {len(significativos)} de {len(valida)} variáveis têm Mann-Whitney p < 0,05 nesta rodada"
            + (f" (n={len(df)} — com amostra grande, significância estatística deixa de ser notícia; o "
               "tamanho de efeito, não o p-valor, é o que compara as variáveis entre si)." if len(df) >= 1000
               else f" (n={len(df)} — com amostra pequena, um p-valor alto pode só refletir falta de poder "
               "estatístico, não ausência de diferença real; o tamanho de efeito continua a melhor bússola).")
        )
    else:
        linhas.append("**Conclusão:** amostra pequena demais para calcular o teste em algum grupo.")
    linhas.append("")
    return tabela, destaques, linhas


def secao6_tipo(df: pd.DataFrame) -> tuple[dict, list[str]]:
    tabela_contingencia = pd.crosstab(df["tipo"], df["falha"])
    qui2, p_valor, graus_liberdade, esperado = stats.chi2_contingency(tabela_contingencia)
    n = tabela_contingencia.to_numpy().sum()
    menor_dimensao = min(tabela_contingencia.shape) - 1
    cramers_v = (qui2 / (n * menor_dimensao)) ** 0.5
    taxa_por_tipo = analise.taxa_falha_por_tipo(df)

    if cramers_v < 0.1:
        porte = "efeito muito pequeno"
    elif cramers_v < 0.3:
        porte = "efeito pequeno"
    elif cramers_v < 0.5:
        porte = "efeito médio"
    else:
        porte = "efeito grande"

    linhas = [
        "## 6 — Tipo de produto × falha",
        "",
        "| tipo | não falhou | falhou | taxa de falha (%) |",
        "|---|---:|---:|---:|",
    ]
    for tipo in tabela_contingencia.index:
        nao_falhou, falhou = tabela_contingencia.loc[tipo, False], tabela_contingencia.loc[tipo, True]
        linhas.append(f"| {tipo} | {nao_falhou} | {falhou} | {_n(taxa_por_tipo[tipo], 2)} |")
    linhas += [
        "",
        f"qui-quadrado: {_n(qui2, 2)} · p-valor: {_n(p_valor, 4)} · Cramér's V: {_n(cramers_v, 3)}",
        "",
        f"**Conclusão:** a associação "
        + ("é estatisticamente significativa (p < 0,05)" if p_valor < 0.05
           else f"NÃO é estatisticamente significativa nesta rodada (p={_br(p_valor, 3)} ≥ 0,05 — "
           f"com n={n}, não há evidência suficiente de associação entre tipo e falha)")
        + f", e Cramér's V = {_br(cramers_v, 3)} é {porte} — "
        + ("tipo de produto desloca a taxa de falha, mas é pequeno perto do que os mecanismos físicos "
           "(seção 7) explicam; vale como fator secundário, não decisivo sozinho."
           if cramers_v < 0.3 else
           "tipo de produto tem peso considerável na taxa de falha nesta rodada, vale olhar com mais "
           "atenção como fator do agente."),
        "",
    ]
    destaques = {"cramers_v": float(cramers_v), "p_valor": float(p_valor), "significativo": bool(p_valor < 0.05)}
    return destaques, linhas


def secao7_mecanismos(df: pd.DataFrame) -> tuple[dict, list[str]]:
    previsto_twf = df["desgaste"].between(*TWF_JANELA)
    previsto_hdf = (df["delta_temperatura"] < HDF_LIMITE_DELTA) & (df["rotacao"] < HDF_LIMITE_ROTACAO)
    previsto_pwf = ~df["potencia_w"].between(*PWF_FAIXA_SEGURA)
    previsto_osf = df["osf_produto"] >= df["osf_limite"]

    def recall_precisao(previsto, real):
        verdadeiro_positivo = int((previsto & real).sum())
        recall = verdadeiro_positivo / real.sum() if real.sum() else float("nan")
        precisao = verdadeiro_positivo / previsto.sum() if previsto.sum() else float("nan")
        return recall, precisao, int(real.sum()), int(previsto.sum())

    mecanismos = [
        ("TWF (zona de desgaste 200-240min)", previsto_twf, df["twf"]),
        ("HDF (delta<8,6K e rotação<1380rpm)", previsto_hdf, df["hdf"]),
        ("PWF (potência fora de 3500-9000W)", previsto_pwf, df["pwf"]),
        ("OSF (desgaste x torque >= limite por tipo)", previsto_osf, df["osf"]),
    ]
    registros = []
    for nome, previsto, real in mecanismos:
        recall, precisao, n_real, n_previsto = recall_precisao(previsto, real)
        registros.append({"mecanismo": nome, "recall": recall, "precisao": precisao,
                           "casos_reais": n_real, "casos_previstos": n_previsto})
    tabela = pd.DataFrame(registros).set_index("mecanismo")

    n_rnf = int(df["rnf"].sum())
    pct_rnf = df["rnf"].mean()

    linhas = [
        "## 7 — Os cinco mecanismos de falha, quantificados",
        "",
        "Limiares oficiais de `ams.gerador_casos`, testados como regra preditiva contra a flag real "
        "de cada modo.",
        "",
        "| mecanismo | recall | precisão | casos reais | casos previstos pela regra |",
        "|---|---:|---:|---:|---:|",
    ]
    for nome, linha in tabela.iterrows():
        linhas.append(
            f"| {nome} | {_n(linha['recall'], 3)} | {_n(linha['precisao'], 3)} "
            f"| {int(linha['casos_reais'])} | {int(linha['casos_previstos'])} |"
        )
    linhas.append("")
    linhas.append(
        f"RNF: {n_rnf} caso(s) reais em {len(df)} ({_br(pct_rnf * 100, 3)}%) — nenhuma variável de sensor "
        "prevê isso, é ruído puro por definição."
    )

    validos = tabela.dropna(subset=["recall", "precisao"])
    quase_perfeitos: list[str] = []
    pior_precisao = None
    linhas.append("")
    if len(validos):
        quase_perfeitos = validos.index[(validos["recall"] >= 0.99) & (validos["precisao"] >= 0.99)].tolist()
        pior_precisao = validos["precisao"].idxmin()
        linhas.append(
            f"**Conclusão:** "
            + (f"{', '.join(f'`{m.split(chr(32))[0]}`' for m in quase_perfeitos)} "
               f"{'reproduzem' if len(quase_perfeitos) > 1 else 'reproduz'} a flag real com recall e "
               "precisão praticamente perfeitos nesta rodada — confirma o mecanismo documentado pela UCI, "
               "é checagem de sanidade, não achado novo. "
               if quase_perfeitos else "nenhum mecanismo reproduz a flag real com recall e precisão "
               "praticamente perfeitos nesta rodada. ")
            + f"`{pior_precisao.split(' ')[0]}` tem a pior precisão "
            f"({_br(validos.loc[pior_precisao, 'precisao'] * 100, 1)}%"
            + (f", apesar do recall alto ({_br(validos.loc[pior_precisao, 'recall'] * 100, 1)}%)"
               if validos.loc[pior_precisao, "recall"] >= 0.7 else "")
            + ") — a regra acerta \"onde olhar\" bem mais do que acerta \"o quê vai acontecer\". "
            "RNF fica fora desta tabela de propósito: é um piso de erro irredutível para qualquer "
            "classificador baseado nesses dados, inclusive o da seção 8."
        )
    else:
        linhas.append("**Conclusão:** nenhum mecanismo teve casos suficientes nesta rodada para medir recall/precisão.")
    linhas.append("")
    return {"previsto_twf": previsto_twf, "previsto_hdf": previsto_hdf,
            "previsto_pwf": previsto_pwf, "previsto_osf": previsto_osf,
            "tabela": tabela, "quase_perfeitos": [m.split(" ")[0] for m in quase_perfeitos],
            "pior_precisao": pior_precisao.split(" ")[0] if pior_precisao else None,
            "precisao_pior": float(validos.loc[pior_precisao, "precisao"]) if pior_precisao else None,
            "n_rnf": n_rnf, "pct_rnf": float(pct_rnf)}, linhas


def secao8_classificador(df: pd.DataFrame, mecanismos: dict) -> tuple[dict, list[str]]:
    previsto_twf, previsto_hdf = mecanismos["previsto_twf"], mecanismos["previsto_hdf"]
    previsto_pwf, previsto_osf = mecanismos["previsto_pwf"], mecanismos["previsto_osf"]

    medio_hdf = (
        ((df["delta_temperatura"] >= HDF_LIMITE_DELTA) &
         (df["delta_temperatura"] < HDF_LIMITE_DELTA + MARGEM_DIFICIL_HDF_DELTA) &
         (df["rotacao"] < HDF_LIMITE_ROTACAO)) |
        ((df["rotacao"] >= HDF_LIMITE_ROTACAO) &
         (df["rotacao"] < HDF_LIMITE_ROTACAO + MARGEM_DIFICIL_HDF_ROTACAO) &
         (df["delta_temperatura"] < HDF_LIMITE_DELTA))
    )
    medio_pwf = (
        df["potencia_w"].between(PWF_FAIXA_SEGURA[0], PWF_FAIXA_SEGURA[0] + MARGEM_DIFICIL_PWF) |
        df["potencia_w"].between(PWF_FAIXA_SEGURA[1] - MARGEM_DIFICIL_PWF, PWF_FAIXA_SEGURA[1])
    )
    medio_osf = (df["osf_produto"] >= df["osf_limite"] - MARGEM_DIFICIL_OSF) & (df["osf_produto"] < df["osf_limite"])

    alto = previsto_twf | previsto_hdf | previsto_pwf | previsto_osf
    medio = ~alto & (medio_hdf | medio_pwf | medio_osf)

    risco = pd.Series("baixo", index=df.index)
    risco[medio] = "medio"
    risco[alto] = "alto"
    df = df.assign(risco_previsto=risco)

    contagem_risco = df["risco_previsto"].value_counts()
    taxa_por_risco = df.groupby("risco_previsto", observed=True)["falha"].mean()

    real_alto = df["falha"] & (df["risco_previsto"] == "alto")
    recall_alto = real_alto.sum() / df["falha"].sum() if df["falha"].sum() else float("nan")
    precisao_alto = (real_alto.sum() / (df["risco_previsto"] == "alto").sum()
                      if (df["risco_previsto"] == "alto").sum() else float("nan"))
    taxa_alto_para_baixo = ((df["falha"] & (df["risco_previsto"] == "baixo")).sum() / df["falha"].sum()
                             if df["falha"].sum() else float("nan"))

    def status(valor, limite, maior_e_melhor):
        if pd.isna(valor):
            return "sem casos suficientes"
        passou = (valor >= limite) if maior_e_melhor else (valor <= limite)
        return "PASSA" if passou else "NÃO PASSA"

    linhas = [
        "## 8 — Proposta de classificador agregado (baixo / médio / alto)",
        "",
        "`alto`: TWF, HDF, PWF ou OSF sinalizados. `médio`: nenhum limiar cruzado, mas dentro da margem "
        "de \"caso difícil\" de `ams.gerador_casos`. `baixo`: o resto. Critérios de `agent-spec.md` §4: "
        f"recall e precisão da classe alto ≥ {int(CRITERIO_RECALL_ALTO*100)}%, taxa de \"alto\" "
        f"classificado como \"baixo\" ≤ {int(CRITERIO_TAXA_ALTO_PARA_BAIXO*100)}%.",
        "",
        "| nível de risco | n | taxa de falha real (%) |",
        "|---|---:|---:|",
    ]
    for nivel in ["baixo", "medio", "alto"]:
        n_nivel = int(contagem_risco.get(nivel, 0))
        taxa = taxa_por_risco.get(nivel, float("nan"))
        linhas.append(f"| {nivel} | {n_nivel} | {'—' if pd.isna(taxa) else _n(taxa * 100, 2)} |")

    linhas += [
        "",
        "| métrica | valor | critério | resultado |",
        "|---|---:|---:|---|",
        f"| recall da classe 'alto' | {_pct(recall_alto)} | ≥ {int(CRITERIO_RECALL_ALTO*100)}% | "
        f"{status(recall_alto, CRITERIO_RECALL_ALTO, True)} |",
        f"| precisão da classe 'alto' | {_pct(precisao_alto)} | ≥ {int(CRITERIO_PRECISAO_ALTO*100)}% | "
        f"{status(precisao_alto, CRITERIO_PRECISAO_ALTO, True)} |",
        f"| taxa 'alto' classificado baixo | {_pct(taxa_alto_para_baixo)} | ≤ {int(CRITERIO_TAXA_ALTO_PARA_BAIXO*100)}% | "
        f"{status(taxa_alto_para_baixo, CRITERIO_TAXA_ALTO_PARA_BAIXO, False)} |",
        "",
    ]

    resultados = [status(recall_alto, CRITERIO_RECALL_ALTO, True),
                  status(precisao_alto, CRITERIO_PRECISAO_ALTO, True),
                  status(taxa_alto_para_baixo, CRITERIO_TAXA_ALTO_PARA_BAIXO, False)]
    n_passou = resultados.count("PASSA")
    linhas += [
        f"**Conclusão:** a regra física simples bate {n_passou} dos 3 critérios do `agent-spec.md` §4 "
        "nesta rodada. "
        + (f"Recall {_pct(recall_alto)} e taxa de \"alto\" classificado como \"baixo\" {_pct(taxa_alto_para_baixo)} passam. "
           if resultados[0] == "PASSA" and resultados[2] == "PASSA" else "")
        + (f"Precisão {_pct(precisao_alto)} "
           + ("também passa" if resultados[1] == "PASSA" else "não chega perto do critério")
           + " — a regra \"alto\" é um OU entre quatro mecanismos, e o(s) mais fraco(s) em precisão "
           "(seção 7) arrastam a precisão do conjunto para baixo.")
        + " Esta é uma baseline estatística por regras, não um modelo treinado — atualizar o "
        "`agent-spec.md` §4 com estes números é decisão separada do autor, fora deste relatório.",
        "",
    ]
    destaques = {"recall_alto": float(recall_alto) if not pd.isna(recall_alto) else None,
                 "precisao_alto": float(precisao_alto) if not pd.isna(precisao_alto) else None,
                 "taxa_alto_para_baixo": float(taxa_alto_para_baixo) if not pd.isna(taxa_alto_para_baixo) else None,
                 "n_passou": n_passou, "resultados": resultados}
    return destaques, linhas


def secao_sintese(d: dict) -> list[str]:
    """Síntese final — reaproveita os destaques que cada seção já calculou."""
    d1, d2, d3, d4, d5, d6, d7, d8 = (d["s1"], d["s2"], d["s3"], d["s4"], d["s5"], d["s6"], d["s7"], d["s8"])

    pontos = [
        f"A forma das variáveis varia mais do que se espera de \"tudo é sensor físico\" (seção 2): "
        f"`{d2['mais_assimetrica']}` é a mais assimétrica desta rodada (assimetria "
        f"{_br(d2['assimetria_mais_assimetrica'])}), `{d2['mais_normal']}` é a que o `normaltest` menos "
        f"rejeita (p={_br(d2['p_mais_normal'], 3)}), e {d2['n_rejeitam_normalidade']} de {len(NUMERICAS)} "
        "variáveis rejeitam normalidade a 5% nesta rodada.",
    ]
    if d3["melhor_outlier"]:
        pontos.append(
            f"Extremos estatísticos (seção 3) concentram sinal, não ruído, em pelo menos uma variável: "
            f"`{d3['melhor_outlier']}` tem {_br(d3['pct_falha_melhor_outlier'] * 100, 1)}% de taxa de falha "
            f"dentro do seu próprio grupo de outliers. {d3['n_sem_outlier']} de {len(NUMERICAS)} variáveis "
            "não têm outlier nenhum pela regra do boxplot nesta rodada."
        )
    else:
        pontos.append(
            f"Nenhuma variável teve outlier concentrando falha nesta rodada; "
            f"{d3['n_sem_outlier']} de {len(NUMERICAS)} variáveis não têm outlier nenhum."
        )
    pontos.append(
        f"`potencia_kw` é redundante com torque×rotação (seção 4): correlaciona "
        f"{_br(d4['potencia_torque'], 3)} com torque e {_br(d4['potencia_rotacao'], 3)} com rotação — não "
        "entra como terceira variável independente num classificador futuro."
    )
    if d5["melhor_separador"]:
        pontos.append(
            f"Na comparação falha x não-falha por variável (seção 5), `{d5['melhor_separador']}` é quem "
            f"mais separa os dois grupos nesta rodada (efeito rank-biserial {_br(d5['efeito_melhor_separador'])})"
            + (", confirmando a intuição de que o acionador nominal do modo de falha separa mais."
               if d5["melhor_e_nominal"] else
               " — e não é o acionador \"nominal\" de nenhum modo isoladamente, sinal de efeito cruzado "
               "entre mecanismos.")
        )
    pontos.append(
        f"Tipo de produto x falha (seção 6): Cramér's V = {_br(d6['cramers_v'], 3)} "
        f"({'associação estatisticamente significativa' if d6['significativo'] else 'associação NÃO significativa nesta rodada'}) "
        "— efeito pequeno perto do que os mecanismos físicos explicam."
    )
    if d7["quase_perfeitos"]:
        pontos.append(
            f"Os mecanismos físicos (seção 7) se confirmam com recall e precisão praticamente perfeitos em "
            f"{', '.join(f'`{m}`' for m in d7['quase_perfeitos'])}; `{d7['pior_precisao']}` é o mais fraco "
            f"em precisão ({_br(d7['precisao_pior'] * 100, 1)}%). RNF ({d7['n_rnf']} caso(s), "
            f"{_br(d7['pct_rnf'] * 100, 3)}%) é um piso de erro irredutível para qualquer classificador "
            "baseado nesses dados."
        )
    if d8["n_passou"] is not None:
        pontos.append(
            f"A regra agregada (seção 8) bate {d8['n_passou']} dos 3 critérios do `agent-spec.md` §4 nesta "
            f"rodada: recall {_pct(d8['recall_alto'])}, precisão {_pct(d8['precisao_alto'])}, taxa "
            f"'alto'→'baixo' {_pct(d8['taxa_alto_para_baixo'])}."
        )

    linhas = ["## Síntese da rodada", ""]
    linhas += [f"{i}. {texto}" for i, texto in enumerate(pontos, start=1)]
    linhas.append("")
    return linhas


def gerar_relatorio(fonte: str) -> str:
    dataset, df = carregar_fonte(fonte)
    destaques: dict = {}

    partes = [
        "# AMS — Protocolo estatístico sobre o AI4I2020",
        "",
        f"Gerado por `notebooks/gerar_relatorio_protocolo_estatistico.py` a partir de `{dataset.fonte}` "
        f"(`{dataset.caminho}`). Acompanha `02-protocolo-estatistico.ipynb` — mesmas 8 seções, mas aqui a "
        "narrativa é recalculada a cada rodada; o notebook tem o código e os gráficos.",
        "",
        "---",
        "",
    ]
    destaques["s1"], linhas1 = secao1_visao_geral(df)
    partes += linhas1
    partes.append("---")
    partes.append("")
    resumo, destaques["s2"], linhas2 = secao2_descritiva(df)
    partes += linhas2
    partes.append("---")
    partes.append("")
    _, destaques["s3"], linhas3 = secao3_outliers(df, resumo)
    partes += linhas3
    partes.append("---")
    partes.append("")
    destaques["s4"], linhas4 = secao4_correlacao(df)
    partes += linhas4
    partes.append("---")
    partes.append("")
    _, destaques["s5"], linhas5 = secao5_grupo(df)
    partes += linhas5
    partes.append("---")
    partes.append("")
    destaques["s6"], linhas6 = secao6_tipo(df)
    partes += linhas6
    partes.append("---")
    partes.append("")
    mecanismos, linhas7 = secao7_mecanismos(df)
    destaques["s7"] = mecanismos
    partes += linhas7
    partes.append("---")
    partes.append("")
    destaques["s8"], linhas8 = secao8_classificador(df, mecanismos)
    partes += linhas8
    partes.append("---")
    partes.append("")
    partes += secao_sintese(destaques)

    return "\n".join(partes)


def main() -> None:
    analisador = argparse.ArgumentParser(description=__doc__)
    analisador.add_argument("--fonte", choices=["amostra", "raw", "ambos"], default="ambos",
                             help="qual dataset usar (padrão: ambos)")
    analisador.add_argument("--saida-dir", default=None,
                             help="pasta de saída dos .md (padrão: a pasta deste script)")
    argumentos = analisador.parse_args()

    pasta_saida = Path(argumentos.saida_dir) if argumentos.saida_dir else Path(__file__).resolve().parent
    fontes = ["amostra", "raw"] if argumentos.fonte == "ambos" else [argumentos.fonte]

    for fonte in fontes:
        relatorio = gerar_relatorio(fonte)
        destino = pasta_saida / f"02-protocolo-estatistico-{fonte}.md"
        destino.write_text(relatorio, encoding="utf-8", newline="\n")
        print(f"gerado: {destino}")


if __name__ == "__main__":
    main()
