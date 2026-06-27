# -*- coding: utf-8 -*-
"""Gera as figuras da análise OpenAlex (IA nas Humanidades, internacional).

Paralelo a figuras_capes_2021_2024.py e figuras_scielo_articlemeta.py —
mesmo padrão visual (utils.aplicar_estilo_padrao) e mesma nomenclatura de
subcampos.

Pré-requisito: rodar antes
    python analise_openalex.py --modo agregado --mailto SEU_EMAIL      (global + BR)
    python analise_openalex.py --modo agregado --pais BR --mailto ...  (por ano BR)
    python analise_openalex.py --modo corpus  --pais BR --mailto ...   (subcampos)

Figuras geradas em figuras/:
    openalex_01_ranking_paises.png     — top países por volume (Brasil em destaque)
    openalex_02_taxa_interna_paises.png — taxa interna por país (marginalidade BR)
    openalex_03_brasil_temporal.png    — evolução anual do Brasil + taxa interna
    openalex_04_subcampos_3bases.png   — subcampos comparados: CAPES × SciELO × OpenAlex

Uso:
    python figuras_openalex.py
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    COR_CAPES,
    COR_DESTAQUE,
    COR_NEUTRO,
    COR_OPENALEX,
    COR_SCIELO,
    CORES_INTERMEDIARIAS,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    dotplot,
    dumbbell,
    eixo_ptbr,
    estilo_editorial,
    garantir_diretorio,
    num_ptbr,
    pct_ptbr,
    salvar_figura,
)

aplicar_estilo_padrao()

# Caminhos. Módulo-level para permitir override em teste.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")

COR_BRASIL = COR_DESTAQUE   # magenta: Brasil em destaque (categoria em foco)
COR_DEST = COR_OPENALEX     # vermelho-alaranjado: cor-assinatura da base OpenAlex
COR_NEUTRA = COR_NEUTRO     # cinza: demais

# Subcampos canônicos das outras bases (decisoes_metodologicas.md I.5 e II.5),
# em % do respectivo corpus IA. OpenAlex é lido do resumo_BR.csv em tempo real.
SUB_ORDER = ["IA stricto", "ML", "DL", "LLM", "Correlatos"]
CAPES_SUB = {"IA stricto": 29.40, "ML": 40.66, "DL": 33.29, "LLM": 3.89, "Correlatos": 38.26}
SCIELO_SUB = {"IA stricto": 29.64, "ML": 21.87, "DL": 25.04, "LLM": 7.13, "Correlatos": 22.19}
SUB_MAP = {
    "SUBCAMPO_IA_STRICTO": "IA stricto",
    "SUBCAMPO_ML": "ML",
    "SUBCAMPO_DL": "DL",
    "SUBCAMPO_LLM": "LLM",
    "SUBCAMPO_CORRELATOS": "Correlatos",
}


def _salvar(fig, nome: str) -> None:
    # PNG + SVG; a figura é identificada pelo nome do arquivo (sem título embutido).
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), nome)
    fig.tight_layout()
    salvar_figura(out, fig)
    plt.close(fig)
    print(f"  -> {out}")


def _ler_csv(nome: str) -> pd.DataFrame | None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, nome)
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[pulando] não encontrei {caminho} — rode analise_openalex.py antes.\n")
        return None
    return pd.read_csv(caminho)


def _cores(rotulos, destaque="Brazil", topo_idx=0):
    """Cinza para todos; magenta de destaque no Brasil (categoria em foco)."""
    cores = []
    for i, r in enumerate(rotulos):
        if isinstance(r, str) and ("brazil" in r.lower() or "brasil" in r.lower()):
            cores.append(COR_BRASIL)
        else:
            cores.append(COR_NEUTRA)
    return cores


def fig_ranking_paises(top: int = 15) -> None:
    """openalex_01 — top países por volume de IA-Humanas (conceito), Brasil destacado."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    # menor embaixo (dot plot): ordena ascendente.
    df = df.sort_values("count_ia_hum", ascending=False).head(top).iloc[::-1]
    labels = df["pais"].astype(str).tolist()
    vals = df["count_ia_hum"].tolist()
    cores = _cores(labels)

    fig, ax = plt.subplots(figsize=(10, 6.5))
    dotplot(ax, labels, vals, cores)
    estilo_editorial(ax, nota=(
        "Publicações de IA nas Humanidades (2016–2024), definição por conceito do "
        "OpenAlex. Brasil em destaque (magenta)."))
    _salvar(fig, "openalex_01_ranking_paises.png")


def fig_taxa_interna_paises(top: int = 15) -> None:
    """openalex_02 — taxa interna por país; evidencia a marginalidade do Brasil."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    # Top por volume (mesmos países da fig 1), ordenados por taxa (menor embaixo).
    df = df.sort_values("count_ia_hum", ascending=False).head(top)
    df = df.sort_values("taxa_interna_%", ascending=True)
    labels = df["pais"].astype(str).tolist()
    vals = df["taxa_interna_%"].tolist()
    cores = _cores(labels)
    rot = [f"{pct_ptbr(v)}%" for v in vals]

    fig, ax = plt.subplots(figsize=(10, 6.5))
    dotplot(ax, labels, vals, cores, rotulos=rot)
    estilo_editorial(ax, nota=(
        "Taxa interna: % das Humanidades do país que tocam IA (2016–2024). "
        "Brasil em destaque (magenta)."))
    _salvar(fig, "openalex_02_taxa_interna_paises.png")


def fig_brasil_temporal() -> None:
    """openalex_03 — evolução anual do Brasil: volume (barras) + taxa interna (linha)."""
    df = _ler_csv("openalex_ia_humanas_por_ano_BR.csv")
    if df is None:
        return
    df = df.sort_values("ano")

    fig, ax1 = plt.subplots(figsize=(10, 6))
    ax1.bar(df["ano"].astype(int).astype(str), df["count_ia_hum"], color=COR_DEST, label="Volume")
    ax1.set_ylabel("Publicações de IA nas Humanidades", color=COR_DEST)
    ax1.tick_params(axis="y", labelcolor=COR_DEST)
    for x, v in enumerate(df["count_ia_hum"]):
        ax1.text(x, v, f"{num_ptbr(int(v))}".replace(",", "."), ha="center", va="bottom", fontsize=8)

    ax2 = ax1.twinx()
    ax2.plot(df["ano"].astype(int).astype(str), df["taxa_interna_%"],
             color=COR_SCIELO, marker="o", linewidth=2, label="Taxa interna")
    ax2.set_ylabel("Taxa interna (%)", color=COR_SCIELO)
    ax2.tick_params(axis="y", labelcolor=COR_SCIELO)
    ax2.grid(False)
    eixo_ptbr(ax1, "y")
    eixo_ptbr(ax2, "y")

    _salvar(fig, "openalex_03_brasil_temporal.png")


def fig_subcampos_3bases() -> None:
    """openalex_04 — subcampos comparados entre CAPES, SciELO e OpenAlex (% do corpus IA)."""
    df = _ler_csv("openalex_ia_humanas_resumo_BR.csv")
    if df is None:
        return
    foco = df[df["tipo"] == "FOCO_IA"]
    n_ia = int(foco[foco["categoria"] != "Outros Temas"]["obras_unicas"].sum())
    if n_ia == 0:
        sys.stderr.write("[pulando subcampos] nenhum trabalho que toca IA no resumo.\n")
        return
    sub = df[df["tipo"] == "SUBCAMPO"].set_index("categoria")["obras_unicas"]
    openalex_sub = {SUB_MAP[k]: 100 * v / n_ia for k, v in sub.items() if k in SUB_MAP}

    bases = {
        "CAPES (corpus IA total)": CAPES_SUB,
        "SciELO (corpus IA total)": SCIELO_SUB,
        "OpenAlex (Brasil, Humanas)": openalex_sub,
    }
    cores = {
        "CAPES (corpus IA total)": COR_CAPES,
        "SciELO (corpus IA total)": COR_SCIELO,
        "OpenAlex (Brasil, Humanas)": COR_OPENALEX,
    }
    # Dumbbell: por subcampo, um ponto por base, ligados. Ordena pela média.
    ordem = sorted(SUB_ORDER, key=lambda s: sum(b.get(s, 0) for b in bases.values()))
    series = {nm: [bases[nm].get(s, 0) for s in ordem] for nm in bases}

    fig, ax = plt.subplots(figsize=(11, 5.2))
    dumbbell(ax, ordem, series, cores)
    eixo_ptbr(ax, "x")
    ax.set_xlabel("% do corpus de IA da base (multi-label)")
    ax.legend(loc="lower right", frameon=False, fontsize=9)
    _salvar(fig, "openalex_04_subcampos_3bases.png")


def fig_bolha_universo_penetracao(top: int = 40) -> None:
    """openalex_05 — bolhas: universo de Humanidades x taxa interna (tamanho = volume)."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    df = df.sort_values("count_ia_hum", ascending=False).head(top)
    is_br = df["pais"].str.contains("brazil|brasil", case=False, na=False)
    tam = 40 + 3000 * df["count_ia_hum"] / df["count_ia_hum"].max()

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(df.loc[~is_br, "count_universo_hum"], df.loc[~is_br, "taxa_interna_%"],
               s=tam[~is_br], color=COR_NEUTRA, alpha=0.6, edgecolor="white", linewidth=0.5)
    ax.scatter(df.loc[is_br, "count_universo_hum"], df.loc[is_br, "taxa_interna_%"],
               s=tam[is_br], color=COR_BRASIL, alpha=0.9, edgecolor="black",
               linewidth=0.9, zorder=5)
    rotular = set(df.sort_values("count_ia_hum", ascending=False).head(6)["pais"]) \
        | set(df.loc[is_br, "pais"])
    for _, r in df.iterrows():
        if r["pais"] in rotular:
            ax.annotate(r["pais"], (r["count_universo_hum"], r["taxa_interna_%"]),
                        fontsize=8, xytext=(6, 5), textcoords="offset points")
    ax.set_xscale("log")
    ax.set_xlabel("Universo de publicações em Humanidades (escala log)")
    ax.set_ylabel("Taxa interna: % das Humanidades que tocam IA")
    _salvar(fig, "openalex_05_bolha_universo_penetracao.png")


def _radar(ax, valores, label, cor) -> None:
    n = len(valores)
    angulos = np.linspace(0, 2 * np.pi, n, endpoint=False).tolist()
    valores = list(valores) + [valores[0]]
    angulos = angulos + [angulos[0]]
    ax.plot(angulos, valores, color=cor, linewidth=2, label=label)
    ax.fill(angulos, valores, color=cor, alpha=0.1)


def fig_radar_subcampos() -> None:
    """openalex_06 — radar dos subcampos comparando as 3 bases."""
    df = _ler_csv("openalex_ia_humanas_resumo_BR.csv")
    if df is None:
        return
    foco = df[df["tipo"] == "FOCO_IA"]
    n_ia = int(foco[foco["categoria"] != "Outros Temas"]["obras_unicas"].sum())
    if n_ia == 0:
        return
    sub = df[df["tipo"] == "SUBCAMPO"].set_index("categoria")["obras_unicas"]
    openalex_sub = {SUB_MAP[k]: 100 * v / n_ia for k, v in sub.items() if k in SUB_MAP}

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
    _radar(ax, [CAPES_SUB[s] for s in SUB_ORDER], "CAPES (corpus IA total)", CORES_INTERMEDIARIAS[2])
    _radar(ax, [SCIELO_SUB[s] for s in SUB_ORDER], "SciELO (corpus IA total)", CORES_INTERMEDIARIAS[3])
    _radar(ax, [openalex_sub.get(s, 0) for s in SUB_ORDER], "OpenAlex (Brasil, Humanas)", COR_BRASIL)
    ax.set_xticks(np.linspace(0, 2 * np.pi, len(SUB_ORDER), endpoint=False))
    ax.set_xticklabels(SUB_ORDER)
    ax.legend(loc="upper right", bbox_to_anchor=(1.35, 1.12), fontsize=8)
    _salvar(fig, "openalex_06_radar_subcampos.png")


def fig_quadrante_paises(top: int = 40) -> None:
    """openalex_07 — quadrante volume × penetração (medianas), Brasil destacado."""
    df = _ler_csv("openalex_ia_humanas_por_pais_global.csv")
    if df is None:
        return
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    df = df.sort_values("count_ia_hum", ascending=False).head(top)
    is_br = df["pais"].str.contains("brazil|brasil", case=False, na=False)
    mx, my = df["count_ia_hum"].median(), df["taxa_interna_%"].median()

    fig, ax = plt.subplots(figsize=(11, 7))
    ax.scatter(df.loc[~is_br, "count_ia_hum"], df.loc[~is_br, "taxa_interna_%"],
               color=COR_NEUTRA, alpha=0.6)
    ax.scatter(df.loc[is_br, "count_ia_hum"], df.loc[is_br, "taxa_interna_%"],
               color=COR_BRASIL, s=130, edgecolor="black", linewidth=0.9, zorder=5)
    ax.axvline(mx, color="gray", linestyle="--", linewidth=0.8)
    ax.axhline(my, color="gray", linestyle="--", linewidth=0.8)
    ax.set_xscale("log")
    rotular = set(df.sort_values("count_ia_hum", ascending=False).head(8)["pais"]) \
        | set(df.loc[is_br, "pais"])
    for _, r in df.iterrows():
        if r["pais"] in rotular:
            ax.annotate(r["pais"], (r["count_ia_hum"], r["taxa_interna_%"]),
                        fontsize=8, xytext=(6, 3), textcoords="offset points")
    xmin, xmax = df["count_ia_hum"].min(), df["count_ia_hum"].max()
    ymin, ymax = df["taxa_interna_%"].min(), df["taxa_interna_%"].max()
    ax.text(xmax, ymax, "Líderes", fontsize=9, ha="right", va="top", color="gray", style="italic")
    ax.text(xmin, ymax, "Nicho", fontsize=9, ha="left", va="top", color="gray", style="italic")
    ax.text(xmax, ymin, "Gigantes latentes", fontsize=9, ha="right", va="bottom", color="gray", style="italic")
    ax.text(xmin, ymin, "Periféricos", fontsize=9, ha="left", va="bottom", color="gray", style="italic")
    ax.set_xlabel("Volume de publicações de IA nas Humanidades (escala log)")
    ax.set_ylabel("Taxa interna (%)")
    _salvar(fig, "openalex_07_quadrante_paises.png")


def fig_trajetoria_brasil() -> None:
    """openalex_08 — trajetória do Brasil em (volume, taxa interna) ano a ano."""
    df = _ler_csv("openalex_ia_humanas_por_ano_BR.csv")
    if df is None:
        return
    df = df.sort_values("ano")
    fig, ax = plt.subplots(figsize=(10, 7))
    ax.plot(df["count_ia_hum"], df["taxa_interna_%"], color=COR_NEUTRA, linewidth=1.2, zorder=1)
    ax.scatter(df["count_ia_hum"], df["taxa_interna_%"], color=COR_BRASIL, s=90,
               edgecolor="black", linewidth=0.7, zorder=3)
    for _, r in df.iterrows():
        ax.annotate(str(int(r["ano"])), (r["count_ia_hum"], r["taxa_interna_%"]),
                    fontsize=8, xytext=(7, 4), textcoords="offset points")
    ax.set_xlabel("Volume de publicações de IA nas Humanidades")
    ax.set_ylabel("Taxa interna (%)")
    _salvar(fig, "openalex_08_trajetoria_brasil.png")


def main() -> None:
    print("Gerando figuras OpenAlex em figuras/ ...")
    fig_ranking_paises()
    fig_taxa_interna_paises()
    fig_brasil_temporal()
    fig_subcampos_3bases()
    fig_bolha_universo_penetracao()
    fig_radar_subcampos()
    fig_quadrante_paises()
    fig_trajetoria_brasil()
    print("Concluído.")


if __name__ == "__main__":
    main()
