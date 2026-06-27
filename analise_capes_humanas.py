# -*- coding: utf-8 -*-
"""Zoom analítico em Ciências Humanas dentro do corpus IA CAPES 2021-2024.

Recorta os 441 trabalhos identificados como sobre IA cuja grande área é
"CIÊNCIAS HUMANAS" e gera figuras específicas que sustentam o argumento
da tese: a Antropologia ocupa posição marginal dentro de um campo
emergente nas humanidades.

Pré-requisito: rodar `python analise_capes_2021_2024.py` antes.

Saídas em figuras/:
  capes_h01_areas_humanas.png      áreas de conhecimento dentro de Humanas
  capes_h02_temporal_humanas.png   evolução 2021-2024 (Mestrado vs Doutorado)
  capes_h03_top_ies_humanas.png    top IES IA-Humanas
  capes_h04_regiao_humanas.png     IA-Humanas por região
  capes_h05_top_termos_humanas.png termos top no corpus IA-Humanas

Uso:
    python analise_capes_humanas.py
"""

from __future__ import annotations

import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    FIGURAS_DIR,
    STOPWORDS_PT,
    aplicar_estilo_padrao,
    garantir_diretorio,
    num_ptbr,
    pct_ptbr,
    salvar_figura,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

CSV_IA = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia.csv")
CSV_AUDIT = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia_auditoria.xlsx")

COR_PRINCIPAL = CORES_INTERMEDIARIAS[0]
COR_MESTRADO = CORES_INTERMEDIARIAS[3]
COR_DOUTORADO = CORES_INTERMEDIARIAS[1]
COR_PROFISSIONAL = CORES_INTERMEDIARIAS[2]
COR_ANTROPOLOGIA = CORES_INTERMEDIARIAS[6]
COR_OUTRAS = CORES_INTERMEDIARIAS[9]


def carregar_humanas() -> pd.DataFrame:
    if os.path.isfile(CSV_IA):
        df = pd.read_csv(CSV_IA, low_memory=False)
    elif os.path.isfile(CSV_AUDIT):
        df = pd.read_excel(CSV_AUDIT, engine="openpyxl")
    else:
        sys.exit(f"ERRO: rode antes analise_capes_2021_2024.py — falta {CSV_IA}")
    hum = df[df["NM_GRANDE_AREA_CONHECIMENTO"].str.contains("HUMANAS", case=False, na=False)].copy()
    return hum


def _cor_area(area: str) -> str:
    s = str(area).lower()
    if "antropologia" in s:
        return COR_ANTROPOLOGIA
    return COR_OUTRAS


def figh01_areas_humanas(df: pd.DataFrame) -> None:
    serie = df["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().sort_values()
    cores = [_cor_area(a) for a in serie.index]
    total = serie.sum()

    fig, ax = plt.subplots(figsize=(10, max(5, len(serie) * 0.35)))
    bars = ax.barh(serie.index, serie.values, color=cores, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_width() + serie.max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{val} ({pct_ptbr(val/total*100, 1)}%)", va="center", fontsize=8)
    ax.set_xlabel(f"Trabalhos no campo Tecnologias IA/ML/DL em Ciências Humanas (N = {total})")
    ax.set_xlim(0, serie.max() * 1.22)
    # Legenda
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(color=COR_ANTROPOLOGIA, label="Antropologia"),
        Patch(color=COR_OUTRAS, label="Outras áreas de Humanas"),
    ], loc="lower right", frameon=False, fontsize=8)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_h01_areas_humanas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


def figh02_temporal_humanas(df: pd.DataFrame) -> None:
    df = df.copy()
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce").astype("Int64")
    df["NM_GRAU_ACADEMICO"] = df["NM_GRAU_ACADEMICO"].fillna("(s/info)")
    pivot = (df.groupby(["AN_BASE", "NM_GRAU_ACADEMICO"]).size()
             .unstack(fill_value=0).sort_index())

    fig, ax = plt.subplots(figsize=(10, 5.5))
    anos = pivot.index.astype(int).tolist()
    bottom = np.zeros(len(anos))
    cor_map = {
        "MESTRADO": COR_MESTRADO,
        "DOUTORADO": COR_DOUTORADO,
        "MESTRADO PROFISSIONAL": COR_PROFISSIONAL,
    }
    ordem = ["DOUTORADO", "MESTRADO", "MESTRADO PROFISSIONAL"]
    presentes = [g for g in ordem if g in pivot.columns] + [g for g in pivot.columns if g not in ordem]
    for grau in presentes:
        cor = cor_map.get(grau, COR_OUTRAS)
        vals = pivot[grau].values
        ax.bar(anos, vals, bottom=bottom, color=cor, label=grau.title(), edgecolor="white")
        for x, v, b in zip(anos, vals, bottom):
            if v > 3:
                ax.text(x, b + v / 2, f"{int(v)}", ha="center", va="center",
                        color="white" if v > 8 else "#333", fontsize=8)
        bottom = bottom + vals
    for x, total in zip(anos, bottom):
        ax.text(x, total + bottom.max() * 0.02, f"{int(total)}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xlabel("Ano base de defesa")
    ax.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL em Ciências Humanas")
    ax.set_xticks(anos)
    ax.legend(loc="upper left", frameon=False)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_h02_temporal_humanas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


def figh03_top_ies_humanas(df: pd.DataFrame) -> None:
    serie = df["SG_ENTIDADE_ENSINO"].fillna("(s/info)").value_counts().head(15).sort_values()
    fig, ax = plt.subplots(figsize=(10, 6.5))
    bars = ax.barh(serie.index, serie.values, color=COR_PRINCIPAL, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_width() + serie.max() * 0.02,
                bar.get_y() + bar.get_height() / 2,
                f"{val}", va="center", fontsize=8)
    ax.set_xlabel("Trabalhos IA em Ciências Humanas (top 15 IES)")
    ax.set_xlim(0, serie.max() * 1.15)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_h03_top_ies_humanas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


def figh04_regiao_humanas(df: pd.DataFrame) -> None:
    serie = df["NM_REGIAO"].fillna("(s/info)").value_counts()
    total = serie.sum()
    fig, ax = plt.subplots(figsize=(8, 5))
    cores = [CORES_INTERMEDIARIAS[i] for i in [3, 1, 2, 4, 7, 9]][: len(serie)]
    bars = ax.bar(serie.index, serie.values, color=cores, edgecolor="white")
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + total * 0.01,
                f"{val}\n({pct_ptbr(val/total*100, 1)}%)",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Trabalhos IA em Humanas")
    ax.set_ylim(0, serie.max() * 1.18)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_h04_regiao_humanas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


def figh05_top_termos_humanas(df: pd.DataFrame) -> None:
    texto = df["NM_PRODUCAO"].fillna("").astype(str).str.lower()
    texto = texto.str.replace(r"[^\wáéíóúâêôãõçà\s-]", " ", regex=True)
    termos_ia = {
        "inteligência", "artificial", "machine", "deep", "learning", "aprendizado",
        "máquina", "maquina", "profundo", "redes", "rede", "neurais", "neural",
        "ia", "llm", "llms", "chatgpt", "gpt", "transformer", "transformers",
        "generativa", "modelos", "modelo", "linguagem",
    }
    stop = STOPWORDS_PT | termos_ia | {"the", "of", "and", "in", "for", "to", "a", "an", "on", "with"}
    counter: Counter[str] = Counter()
    for t in texto:
        for tok in t.split():
            tok = tok.strip("-")
            if len(tok) >= 4 and tok not in stop:
                counter[tok] += 1
    top = counter.most_common(25)
    if not top:
        print("  (sem termos)")
        return
    labels, vals = zip(*reversed(top))
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(labels, vals, color=COR_PRINCIPAL, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{val}", va="center", fontsize=8)
    ax.set_xlabel("Top 25 termos em títulos de IA-Humanas (exclui canônicos)")
    ax.set_xlim(0, max(vals) * 1.12)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_h05_top_termos_humanas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


def relatorio_resumo(df: pd.DataFrame) -> None:
    print("\n" + "=" * 60)
    print("ZOOM: IA EM CIÊNCIAS HUMANAS")
    print("=" * 60)
    print(f"Total IA-Humanas: {len(df):,}")
    print()
    print("Por área de conhecimento:")
    print(df["NM_AREA_CONHECIMENTO"].value_counts().to_string())
    print()
    print("Por nível acadêmico:")
    print(df["NM_GRAU_ACADEMICO"].value_counts().to_string())
    print()
    print("Por ano base:")
    print(df["AN_BASE"].value_counts().sort_index().to_string())
    print()
    print("Top 10 IES:")
    print(df["SG_ENTIDADE_ENSINO"].value_counts().head(10).to_string())
    print()
    print("Por região:")
    print(df["NM_REGIAO"].value_counts().to_string())

    # Antropologia em destaque
    antro = df[df["NM_AREA_CONHECIMENTO"].str.contains("ANTROPOLOGIA", case=False, na=False)]
    print()
    print(f"Antropologia: {len(antro)} trabalhos no campo Tecnologias IA/ML/DL")
    if len(antro):
        print("  Por sub-área:")
        print(antro["NM_SUBAREA_CONHECIMENTO"].fillna("(s/info)").value_counts().to_string())


if __name__ == "__main__":
    print("Carregando IA-Humanas ...")
    df = carregar_humanas()
    print(f"  {len(df)} trabalhos IA em Ciências Humanas")

    relatorio_resumo(df)

    print("\nGerando figuras:")
    figh01_areas_humanas(df)
    figh02_temporal_humanas(df)
    figh03_top_ies_humanas(df)
    figh04_regiao_humanas(df)
    figh05_top_termos_humanas(df)
    print("\nPronto.")
