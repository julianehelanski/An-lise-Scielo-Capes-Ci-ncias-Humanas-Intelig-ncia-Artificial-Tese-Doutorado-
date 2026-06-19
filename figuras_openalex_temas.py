# -*- coding: utf-8 -*-
"""Figuras temáticas do universo de Humanidades (OpenAlex) — de que ele é feito.

Complementa figuras_openalex.py. Ilustra a COMPOSIÇÃO da produção de Ciências
Humanas (do que o país publica) e onde a IA penetra. Usa a paleta padrão do
projeto (tab10, via utils.aplicar_estilo_padrao) — sem colormaps chamativos.
A penetração da IA aparece como texto "IA x%" ao lado de cada barra.

Pré-requisito de dados:
    python analise_openalex.py --modo temas --pais BR --mailto SEU_EMAIL
    python analise_openalex.py --modo temas --pais BR --subfield \
        "Anthropology,Sociology and Political Science,Political Science and International Relations" \
        --mailto SEU_EMAIL

Pré-requisito de pacotes:
    pip install squarify

Saídas em figuras/:
    openalex_10_treemap_temas.png    composição por subfield (treemap)
    openalex_11_topics_temas.png     temas específicos mais frequentes
    openalex_12_painel_ciencias_sociais.png   painel das 3 ciências sociais
    openalex_13/14/15_<area>.png     barras desmembradas, uma por área

Uso:
    python figuras_openalex_temas.py [--pais BR]
"""

from __future__ import annotations

import argparse
import os
import sys
import textwrap

import matplotlib.pyplot as plt
import pandas as pd

from utils import FIGURAS_DIR, aplicar_estilo_padrao, garantir_diretorio, salvar_figura

try:
    import squarify
except ImportError:  # pragma: no cover
    squarify = None

aplicar_estilo_padrao()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")

# Cores padrão do matplotlib (tab10), iguais às do resto do projeto.
PALETA = list(plt.cm.tab10.colors)
COR_BARRA = PALETA[0]   # azul padrão, cor única das barras

# Áreas das ciências sociais (slug do arquivo, título exibido).
AREAS_SOCIAIS = [
    ("anthropology", "Antropologia"),
    ("sociology_and_political_science", "Sociologia e Ciência Política"),
    ("political_science_and_international_relations", "Ciência Política e Rel. Internacionais"),
]


def _ler(nome: str) -> pd.DataFrame | None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, nome)
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[pulando] não encontrei {caminho} — rode "
                         "analise_openalex.py --modo temas antes.\n")
        return None
    return pd.read_csv(caminho)


def _salvar(fig, nome: str) -> None:
    # PNG + SVG; a figura é identificada pelo nome do arquivo (sem título embutido).
    out = os.path.join(garantir_diretorio(FIGURAS_DIR), nome)
    salvar_figura(out, fig)
    plt.close(fig)
    print(f"  -> {out}")


def fig_treemap(sufixo: str, top: int = 16) -> None:
    """openalex_10 — treemap de composição (cores padrão tab10)."""
    df = _ler(f"openalex_temas_humanas{sufixo}.csv")
    if df is None:
        return
    df = df.sort_values("count_universo", ascending=False).reset_index(drop=True)
    total = df["count_universo"].sum()

    topo = df.head(top).copy()
    resto = df.iloc[top:]
    if len(resto):
        topo = pd.concat([topo, pd.DataFrame([{
            "subfield": f"Outros ({len(resto)} áreas)",
            "count_universo": int(resto["count_universo"].sum()),
            "pct_do_universo": round(100 * resto["count_universo"].sum() / total, 2),
        }])], ignore_index=True)

    if squarify is None:
        sys.stderr.write("[aviso] squarify ausente; gerando barra no lugar do treemap.\n")
        fig, ax = plt.subplots(figsize=(12, 9))
        d = topo.iloc[::-1]
        ax.barh(d["subfield"], d["count_universo"], color=COR_BARRA, edgecolor="white")
        _salvar(fig, "openalex_10_treemap_temas.png")
        return

    cores = [PALETA[i % len(PALETA)] for i in range(len(topo))]
    labels = []
    for _, r in topo.iterrows():
        share = r["count_universo"] / total
        nome = "\n".join(textwrap.wrap(str(r["subfield"]), 18))
        if share >= 0.03:
            labels.append(f"{nome}\n{r['pct_do_universo']:.1f}%")
        elif share >= 0.013:
            labels.append(nome)
        else:
            labels.append("")

    fig, ax = plt.subplots(figsize=(16, 9))
    squarify.plot(sizes=topo["count_universo"], label=labels, color=cores,
                  ax=ax, pad=True, ec="white",
                  text_kwargs={"fontsize": 9, "color": "white", "fontweight": "bold"})
    ax.axis("off")
    _salvar(fig, "openalex_10_treemap_temas.png")


def fig_topics(sufixo: str, top: int = 20) -> None:
    """openalex_11 — barras dos temas específicos (topics) mais frequentes."""
    df = _ler(f"openalex_topics_humanas{sufixo}.csv")
    if df is None:
        return
    d = df.sort_values("count_universo", ascending=False).head(top).iloc[::-1]
    fig, ax = plt.subplots(figsize=(11, 9))
    ax.barh(d["topic"].astype(str), d["count_universo"], color=COR_BARRA, edgecolor="white")
    for y, (v, t) in enumerate(zip(d["count_universo"], d["taxa_ia_%"])):
        ax.text(v, y, f"  {int(v):,}".replace(",", ".") + f"  ·  IA {t:.1f}%",
                va="center", fontsize=8)
    ax.set_xlabel("publicações no universo de Humanidades (2016–2024)")
    ax.margins(x=0.20)
    _salvar(fig, "openalex_11_topics_temas.png")


def fig_painel_areas(sufixo: str, top: int = 10, areas=AREAS_SOCIAIS) -> None:
    """openalex_12 — painel: top temas de cada ciência social (cor única)."""
    dfs = []
    for slug, titulo in areas:
        df = _ler(f"openalex_topics_{slug}{sufixo}.csv")
        if df is not None and not df.empty:
            dfs.append((titulo, df))
    if not dfs:
        sys.stderr.write("[pulando painel] rode antes analise_openalex.py --modo temas "
                         "--subfield \"...\"\n")
        return

    n = len(dfs)
    fig, axes = plt.subplots(n, 1, figsize=(12, 4.7 * n), constrained_layout=True)
    if n == 1:
        axes = [axes]
    for ax, (titulo, df) in zip(axes, dfs):
        d = df.sort_values("count_universo", ascending=False).head(top).iloc[::-1]
        ax.barh(d["topic"].astype(str), d["count_universo"], color=COR_BARRA, edgecolor="white")
        for y, (v, t) in enumerate(zip(d["count_universo"], d["taxa_ia_%"])):
            ax.text(v, y, f"  {int(v):,}".replace(",", ".") + f"  ·  IA {t:.1f}%",
                    va="center", fontsize=7.5)
        ax.set_title(titulo, fontsize=12, loc="left", fontweight="bold")
        ax.set_xlabel("publicações no universo de Humanidades (2016–2024)")
        ax.margins(x=0.22)
    _salvar(fig, "openalex_12_painel_ciencias_sociais.png")


def fig_areas_individuais(sufixo: str, top: int = 12, areas=AREAS_SOCIAIS) -> None:
    """openalex_13..15 — uma figura por ciência social (cor única, IA% no rótulo)."""
    for i, (slug, titulo) in enumerate(areas):
        df = _ler(f"openalex_topics_{slug}{sufixo}.csv")
        if df is None or df.empty:
            continue
        d = df.sort_values("count_universo", ascending=False).head(top).iloc[::-1]
        fig, ax = plt.subplots(figsize=(11, 7))
        ax.barh(d["topic"].astype(str), d["count_universo"], color=COR_BARRA, edgecolor="white")
        for y, (v, t) in enumerate(zip(d["count_universo"], d["taxa_ia_%"])):
            ax.text(v, y, f"  {int(v):,}".replace(",", ".") + f"  ·  IA {t:.1f}%",
                    va="center", fontsize=8)
        ax.set_xlabel("publicações no universo de Humanidades (2016–2024)")
        ax.margins(x=0.22)
        _salvar(fig, f"openalex_{13 + i}_{slug}.png")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pais", default="BR", help="Sufixo do país (default BR; vazio p/ global)")
    args = parser.parse_args()
    sufixo = f"_{args.pais.upper()}" if args.pais else "_global"
    print("Gerando figuras temáticas OpenAlex em figuras/ ...")
    fig_treemap(sufixo)
    fig_topics(sufixo)
    fig_painel_areas(sufixo)
    fig_areas_individuais(sufixo)
    print("Concluído.")


if __name__ == "__main__":
    main()
