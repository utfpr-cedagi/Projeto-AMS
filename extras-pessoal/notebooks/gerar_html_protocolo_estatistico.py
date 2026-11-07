"""Gera o HTML interativo que acompanha `02-protocolo-estatistico.ipynb`.

Os gráficos aqui são os de COMPARAÇÃO — os que ganham de verdade com
hover/zoom/filtro (Plotly). O notebook continua em matplotlib/seaborn para
o restante da análise (estilo do `01-eda.ipynb`); este script roda à parte
porque Plotly não participa do ambiente de execução do notebook.

Uso:
    .venv/Scripts/python.exe extras-pessoal/notebooks/gerar_html_protocolo_estatistico.py
"""

from __future__ import annotations

import sys
from pathlib import Path

import plotly.graph_objects as go
from plotly.subplots import make_subplots

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "scripts"))

from ams.dados import carregar, preparar  # noqa: E402
from gerador_casos import (  # noqa: E402
    HDF_LIMITE_DELTA,
    HDF_LIMITE_ROTACAO,
    OSF_LIMITES,
    PWF_FAIXA_SEGURA,
    TWF_JANELA,
)

COR_NAO_FALHA, COR_FALHA = "#4c72b0", "#c44e52"  # mesma paleta do notebook/01-eda
CORES_TIPO = {"L": "#55a868", "M": "#8172b3", "H": "#ccb974"}
NUMERICAS = ["temperatura_ar", "temperatura_processo", "rotacao", "torque",
             "desgaste", "delta_temperatura", "potencia_kw"]


def _carregar() -> "pd.DataFrame":
    dataset = carregar()
    df = preparar(dataset.quadro)
    df["potencia_w"] = df["potencia_kw"] * 1000.0
    df["osf_produto"] = df["desgaste"] * df["torque"]
    df["osf_limite"] = df["tipo"].astype(str).map(OSF_LIMITES).astype(float)
    return df


def figura_dispersao(df) -> go.Figure:
    """Torque x rotação: alterna a cor entre falha e tipo de produto."""
    hover = (
        "UDI %{customdata[0]} (%{customdata[1]})<br>"
        "torque %{x} Nm · rotação %{y} rpm<br>"
        "desgaste %{customdata[2]} min · delta_T %{customdata[3]:.1f} K<br>"
        "falhou: %{customdata[4]}<extra></extra>"
    )
    customdata = df[["udi", "product_id", "desgaste", "delta_temperatura", "falha"]].to_numpy()

    fig = go.Figure()
    for valor, cor, nome in [(False, COR_NAO_FALHA, "não falhou"), (True, COR_FALHA, "falhou")]:
        mascara = df["falha"] == valor
        fig.add_trace(go.Scattergl(
            x=df.loc[mascara, "torque"], y=df.loc[mascara, "rotacao"],
            mode="markers", name=nome, marker=dict(color=cor, size=5, opacity=0.55),
            customdata=customdata[mascara.to_numpy()], hovertemplate=hover, visible=True,
        ))
    for tipo, cor in CORES_TIPO.items():
        mascara = df["tipo"] == tipo
        fig.add_trace(go.Scattergl(
            x=df.loc[mascara, "torque"], y=df.loc[mascara, "rotacao"],
            mode="markers", name=f"tipo {tipo}", marker=dict(color=cor, size=5, opacity=0.55),
            customdata=customdata[mascara.to_numpy()], hovertemplate=hover, visible=False,
        ))

    fig.update_layout(
        title="Torque x rotação — colorir por falha ou por tipo de produto",
        xaxis_title="torque (Nm)", yaxis_title="rotação (rpm)",
        updatemenus=[dict(
            type="buttons", direction="left", x=0.0, xanchor="left", y=1.18, showactive=True,
            buttons=[
                dict(label="por falha", method="update",
                     args=[{"visible": [True, True, False, False, False]}]),
                dict(label="por tipo", method="update",
                     args=[{"visible": [False, False, True, True, True]}]),
            ],
        )],
        legend=dict(orientation="h", y=1.1),
        height=520,
    )
    return fig


def figura_mecanismos(df) -> go.Figure:
    """Os quatro mecanismos previsíveis (TWF/HDF/PWF/OSF), lado a lado."""
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("TWF — desgaste e a janela de risco",
                         "HDF — fronteira delta x rotação",
                         "PWF — potência e a faixa segura",
                         "OSF — produto desgaste x torque vs. limite por tipo"),
    )

    fig.add_trace(go.Histogram(x=df["desgaste"], marker_color=COR_NAO_FALHA, name="desgaste",
                                showlegend=False), row=1, col=1)
    fig.add_vrect(x0=TWF_JANELA[0], x1=TWF_JANELA[1], fillcolor=COR_FALHA, opacity=0.15,
                  line_width=0, row=1, col=1, annotation_text="janela TWF")

    for valor, cor, nome in [(False, COR_NAO_FALHA, "sem HDF"), (True, COR_FALHA, "HDF")]:
        mascara = df["hdf"] == valor
        fig.add_trace(go.Scattergl(x=df.loc[mascara, "rotacao"], y=df.loc[mascara, "delta_temperatura"],
                                    mode="markers", marker=dict(color=cor, size=4, opacity=0.5),
                                    name=nome, showlegend=False), row=1, col=2)
    fig.add_hline(y=HDF_LIMITE_DELTA, line_dash="dash", line_color="gray", row=1, col=2)
    fig.add_vline(x=HDF_LIMITE_ROTACAO, line_dash="dash", line_color="gray", row=1, col=2)

    fig.add_trace(go.Histogram(x=df["potencia_w"], marker_color=COR_NAO_FALHA, name="potência",
                                showlegend=False), row=2, col=1)
    fig.add_vrect(x0=PWF_FAIXA_SEGURA[0], x1=PWF_FAIXA_SEGURA[1], fillcolor=COR_NAO_FALHA,
                  opacity=0.12, line_width=0, row=2, col=1, annotation_text="faixa segura")

    for valor, cor, nome in [(False, COR_NAO_FALHA, "sem OSF"), (True, COR_FALHA, "OSF")]:
        mascara = df["osf"] == valor
        fig.add_trace(go.Scattergl(x=df.loc[mascara, "osf_limite"], y=df.loc[mascara, "osf_produto"],
                                    mode="markers", marker=dict(color=cor, size=4, opacity=0.5),
                                    name=nome, showlegend=False), row=2, col=2)
    limites = sorted(df["osf_limite"].unique())
    fig.add_trace(go.Scatter(x=limites, y=limites, mode="lines", line=dict(color="gray", dash="dash"),
                              showlegend=False), row=2, col=2)

    fig.update_xaxes(title_text="desgaste (min)", row=1, col=1)
    fig.update_xaxes(title_text="rotação (rpm)", row=1, col=2)
    fig.update_yaxes(title_text="delta_temperatura (K)", row=1, col=2)
    fig.update_xaxes(title_text="potência (W)", row=2, col=1)
    fig.update_xaxes(title_text="limite OSF por tipo (min·Nm)", row=2, col=2)
    fig.update_yaxes(title_text="desgaste x torque (min·Nm)", row=2, col=2)
    fig.update_layout(title="Os quatro mecanismos de falha previsíveis, com a fronteira física", height=750)
    return fig


def figura_boxplot_variavel(df) -> go.Figure:
    """Falha x não-falha, com um dropdown pra trocar a variável."""
    fig = go.Figure()
    for i, coluna in enumerate(NUMERICAS):
        fig.add_trace(go.Box(y=df.loc[~df["falha"], coluna], name="não falhou",
                              marker_color=COR_NAO_FALHA, visible=(i == 0), showlegend=(i == 0)))
        fig.add_trace(go.Box(y=df.loc[df["falha"], coluna], name="falhou",
                              marker_color=COR_FALHA, visible=(i == 0), showlegend=(i == 0)))

    botoes = []
    for i, coluna in enumerate(NUMERICAS):
        visivel = [False] * (2 * len(NUMERICAS))
        visivel[2 * i], visivel[2 * i + 1] = True, True
        botoes.append(dict(label=coluna, method="update",
                            args=[{"visible": visivel}, {"yaxis": {"title": coluna}}]))

    fig.update_layout(
        title="Falha x não-falha, por variável (escolha abaixo)",
        updatemenus=[dict(active=0, buttons=botoes, x=0.0, xanchor="left", y=1.18)],
        yaxis_title=NUMERICAS[0], height=500,
    )
    return fig


def figura_correlacao(df) -> go.Figure:
    matriz = df[NUMERICAS].corr(method="pearson").round(3)
    fig = go.Figure(go.Heatmap(
        z=matriz.values, x=matriz.columns, y=matriz.columns, zmid=0,
        colorscale="RdBu_r", text=matriz.values, texttemplate="%{text}",
        hovertemplate="%{y} x %{x}: %{z}<extra></extra>",
    ))
    fig.update_layout(title="Correlação de Pearson entre as variáveis numéricas", height=550)
    return fig


def montar_pagina(figuras: list[tuple[str, go.Figure]], caminho: str) -> None:
    partes = [
        "<!doctype html><html><head><meta charset='utf-8'>"
        "<title>AMS — protocolo estatístico (interativo)</title>"
        "<style>body{font-family:sans-serif;max-width:1100px;margin:2rem auto;padding:0 1rem}"
        "h1{font-size:1.4rem}h2{font-size:1.1rem;border-top:1px solid #ddd;padding-top:1.5rem}</style>"
        "</head><body>"
        "<h1>AMS — protocolo estatístico (gráficos interativos)</h1>"
        "<p>Acompanha <code>02-protocolo-estatistico.ipynb</code> — "
        "hover, zoom e os botões/dropdown de cada gráfico trocam o que é "
        "comparado sem precisar reabrir o notebook.</p>"
    ]
    for i, (titulo, fig) in enumerate(figuras):
        incluir_js = "cdn" if i == 0 else False
        partes.append(f"<h2>{titulo}</h2>")
        partes.append(fig.to_html(full_html=False, include_plotlyjs=incluir_js))
    partes.append("</body></html>")

    with open(caminho, "w", encoding="utf-8") as arquivo:
        arquivo.write("\n".join(partes))


def main() -> None:
    df = _carregar()
    figuras = [
        ("Torque x rotação", figura_dispersao(df)),
        ("Os cinco mecanismos de falha", figura_mecanismos(df)),
        ("Falha x não-falha, por variável", figura_boxplot_variavel(df)),
        ("Correlação entre variáveis numéricas", figura_correlacao(df)),
    ]
    destino = "notebooks/extra-pessoal/02-protocolo-estatistico.html"
    montar_pagina(figuras, destino)
    print(f"gerado: {destino}")


if __name__ == "__main__":
    main()
