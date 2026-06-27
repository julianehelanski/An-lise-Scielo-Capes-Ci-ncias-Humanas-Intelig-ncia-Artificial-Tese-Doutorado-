# -*- coding: utf-8 -*-
"""Gera o conjunto de figuras da análise SciELO 2021-2024 via ArticleMeta.

Paralelo ao figuras_capes_2021_2024.py — mesmo padrão visual e mesma
nomenclatura de subcampos, ajustada para a fonte SciELO.

Pré-requisito: rodar `python analise_scielo_articlemeta.py` antes.

Mapeamento CAPES → SciELO:
  capes_11 grande área → scielo_11 subject_area
  capes_12 temporal por grande área → scielo_12 temporal por subject_area
  capes_13 heatmap área × keyword → scielo_13 heatmap subject_area × keyword
  capes_14 evolução total Central vs Correlato → scielo_14
  capes_15 nível acadêmico → scielo_15 idioma do artigo
  capes_16 top áreas de conhecimento → scielo_16 top periódicos
  capes_17 top IES → (sem equivalente — SciELO não captura instituição do autor)
  capes_18 região/UF → (sem equivalente — não capturado)
  capes_19 páginas → (sem equivalente — não capturado)
  capes_20 top termos → scielo_20
  capes_21 subcampos distribuição → scielo_21
  capes_22 heatmap subcampo × grande área → scielo_22 heatmap subcampo × subject_area
  capes_23 temporal por subcampo → scielo_23

Saídas em figuras/: scielo_11_*.png a scielo_23_*.png (10 figuras).

Uso:
    python figuras_scielo_articlemeta.py
"""

from __future__ import annotations

import os
import re
import sys
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

from utils import (
    CMAP_SEQUENCIAL,
    COR_DESTAQUE,
    COR_SCIELO,
    CORES_INTERMEDIARIAS,
    DADOS_SCIELO_DIR,
    FIGURAS_DIR,
    STOPWORDS_PT,
    aplicar_estilo_padrao,
    dotplot,
    eixo_ptbr,
    estilo_editorial,
    garantir_diretorio,
    num_ptbr,
    pct_ptbr,
    salvar_figura,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

CSV_IA = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_ia_subcampos_auditoria.xlsx")
CSV_UNIVERSO = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_universo.csv")
CSV_UNIVERSO_AGREGADO = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_universo_agregado.csv")
# Fallbacks: recorte antigo
CSV_IA_FALLBACK = os.path.join(DADOS_SCIELO_DIR, "scielo_ia_subcampos.csv")
CSV_UNIVERSO_FALLBACK = os.path.join(DADOS_SCIELO_DIR, "scielo_humanas_universo.csv")

COR_HUMANAS = CORES_INTERMEDIARIAS[0]      # vermelho-muted (Humanas em destaque)
COR_DEST = CORES_INTERMEDIARIAS[3]         # azul
COR_NEUTRA = CORES_INTERMEDIARIAS[9]       # cinza-azulado

ANO_MIN, ANO_MAX = 2021, 2024

# As 8 subject_areas canônicas do SciELO. Periódicos multi-area viram
# "Multidisciplinar".
SUBJECT_AREAS_SCIELO = [
    "Agricultural Sciences",
    "Applied Social Sciences",
    "Biological Sciences",
    "Engineering",
    "Exact and Earth Sciences",
    "Health Sciences",
    "Human Sciences",
    "Linguistics, Letters and Arts",
]
SUBJECT_AREA_MULTI = "Multidisciplinar"

KEYWORDS_HEATMAP = [
    ("inteligência artificial", r"\b(intelig[êe]ncia\s+artificial|artificial\s+intelligence)\b"),
    ("machine/deep learning", r"\b(machine\s+learning|deep\s+learning|aprendizado\s+de\s+m[áa]quina|aprendizado\s+profundo)\b"),
    ("redes neurais", r"\b(redes?\s+neurais|neural\s+networks?)\b"),
    ("LLM / modelo de linguagem", r"\b(llms?|large\s+language\s+models?|modelos?\s+de\s+linguagem)\b"),
    ("ChatGPT / GPT-N", r"\b(chatgpt|gpt-\d)\b"),
    ("IA generativa", r"\b(ia\s+generativa|generative\s+ai)\b"),
    ("robótica / automação", r"\b(rob[óo]tica|rob[ôo]s|automa[çc][ãa]o|automation)\b"),
    ("NLP", r"\b(processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp)\b"),
    ("big data / mineração", r"\b(big\s+data|minera[çc][ãa]o\s+de\s+dados|data\s+mining)\b"),
    ("visão computacional", r"\b(vis[ãa]o\s+computacional|computer\s+vision)\b"),
]

SUBCAMPO_COLS = [
    ("SUBCAMPO_IA_STRICTO", "IA em sentido estrito"),
    ("SUBCAMPO_ML", "Aprendizado de máquina (ML)"),
    ("SUBCAMPO_DL", "Aprendizado profundo & redes neurais"),
    ("SUBCAMPO_LLM", "Modelos de linguagem & IA generativa"),
    ("SUBCAMPO_CORRELATOS", "Tecnologias correlatas"),
]
SUBCAMPO_CORES = [
    CORES_INTERMEDIARIAS[3], CORES_INTERMEDIARIAS[2], CORES_INTERMEDIARIAS[4],
    CORES_INTERMEDIARIAS[6], CORES_INTERMEDIARIAS[9],
]


def _bool(s):
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1"])


def _subject_area_primary(sa_str):
    """Reduz a string 'A; B; C' para UMA área primária.

    Periódicos com 1 área: devolve essa área.
    Periódicos com 2+ áreas: devolve 'Multidisciplinar'.
    Sem info: devolve '(s/info)'.
    """
    if pd.isna(sa_str) or not sa_str:
        return "(s/info)"
    sas = [s.strip() for s in str(sa_str).split(";") if s.strip()]
    if not sas:
        return "(s/info)"
    if len(sas) == 1:
        return sas[0]
    return SUBJECT_AREA_MULTI


def carregar_ia() -> pd.DataFrame:
    """Carrega o subset IA. Prefere a versão Brasil completo (98k universo)
    sobre o recorte antigo (33k universo)."""
    if os.path.isfile(CSV_IA):
        print(f"  usando {os.path.basename(CSV_IA)} (universo Brasil completo)")
        df = pd.read_excel(CSV_IA, engine="openpyxl")
    elif os.path.isfile(CSV_IA_FALLBACK):
        print(f"  fallback: usando {os.path.basename(CSV_IA_FALLBACK)} (recorte Humanas)")
        df = pd.read_csv(CSV_IA_FALLBACK, low_memory=False)
    else:
        sys.exit(f"ERRO: rode antes analise_scielo_articlemeta.py — falta {CSV_IA}")
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    n_pre = len(df)
    df = df[(df["ano"] >= ANO_MIN) & (df["ano"] <= ANO_MAX)].copy()
    print(f"  {n_pre} → {len(df)} artigos após restrição a {ANO_MIN}-{ANO_MAX}")
    df["subject_area_primary"] = df["subject_areas_periodico"].map(_subject_area_primary)
    return df


def carregar_universo() -> pd.DataFrame | None:
    """Carrega o universo, com vários fallbacks por ordem de preferência:
    1) CSV agregado pequeno (scielo_brasil_universo_agregado.csv) — leve,
       comitável.
    2) CSV completo Brasil (não comitado).
    3) CSV antigo do recorte Humanas.
    """
    if os.path.isfile(CSV_UNIVERSO_AGREGADO):
        print(f"  usando {os.path.basename(CSV_UNIVERSO_AGREGADO)} (agregado leve)")
        agg = pd.read_csv(CSV_UNIVERSO_AGREGADO)
        # Devolve um pseudo-dataframe expandido (uma linha por unidade) só pra
        # ter a interface igual ao caso original
        return agg
    if os.path.isfile(CSV_UNIVERSO):
        print(f"  usando {os.path.basename(CSV_UNIVERSO)} (universo Brasil completo)")
        df = pd.read_csv(CSV_UNIVERSO, low_memory=False)
        df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
        df = df[(df["ano"] >= ANO_MIN) & (df["ano"] <= ANO_MAX)].copy()
        df["subject_area_primary"] = df["subject_areas_periodico"].map(_subject_area_primary)
        return df
    if os.path.isfile(CSV_UNIVERSO_FALLBACK):
        print(f"  fallback: usando {os.path.basename(CSV_UNIVERSO_FALLBACK)} (recorte Humanas)")
        df = pd.read_csv(CSV_UNIVERSO_FALLBACK, low_memory=False)
        df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
        df = df[(df["ano"] >= ANO_MIN) & (df["ano"] <= ANO_MAX)].copy()
        df["subject_area_primary"] = df["subject_areas_periodico"].map(_subject_area_primary)
        return df
    return None


def _counts_universo(universo: pd.DataFrame | None) -> pd.Series | None:
    """Devolve contagem do universo por subject_area_primary."""
    if universo is None or not len(universo):
        return None
    # Se for o formato agregado (colunas grande_area/total), reconstroi
    if "subject_area" in universo.columns and "total" in universo.columns:
        return pd.Series(universo["total"].values, index=universo["subject_area"].values)
    return universo["subject_area_primary"].value_counts()


def texto_classificacao(df):
    s = df["titulo"].fillna("").astype(str)
    for c in ["resumo", "keywords"]:
        if c in df.columns:
            s = s + " | " + df[c].fillna("").astype(str)
    return s


def _cor_sa(label):
    # Base SciELO em azul; Human Sciences (foco) em magenta de destaque.
    return COR_DESTAQUE if "Human Sciences" == label else COR_SCIELO


# ---------------------------------------------------------------------------
# Figura 11: distribuição por subject_area + taxa interna
# ---------------------------------------------------------------------------
def fig11_subject_area(df, universo):
    counts = df["subject_area_primary"].value_counts().sort_values()
    labels = list(counts.index)
    vals = list(counts.values)
    total = counts.sum()
    cores = [_cor_sa(l) for l in labels]
    pcts = [v / total * 100 for v in vals]
    univ_counts = _counts_universo(universo)
    nota = (f"SciELO Brasil · 2021–2024 · N = {num_ptbr(total)}. "
            "Human Sciences em destaque (magenta).")

    if univ_counts is not None:
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6), gridspec_kw={"wspace": 0.6})
    else:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = None

    dotplot(ax1, labels, vals, cores, pcts=pcts)
    estilo_editorial(ax1, titulo="Volume no corpus de IA", nota=nota)

    if ax2 is not None:
        taxa = []
        for sa in labels:
            t = counts.get(sa, 0) / univ_counts.get(sa, float("nan")) * 100
            taxa.append(0.0 if pd.isna(t) else t)
        rot = [f"{pct_ptbr(t, 2)}%" for t in taxa]
        dotplot(ax2, labels, taxa, cores, rotulos=rot)
        ax2.set_yticklabels([])
        estilo_editorial(ax2, titulo="Taxa interna (% da área que toca o campo)")

    out = os.path.join(FIGURAS_DIR, "scielo_11_subject_area_share.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 12: evolução temporal por subject_area
# ---------------------------------------------------------------------------
def fig12_temporal_subject_area(df):
    pivot = (df.groupby(["ano", "subject_area_primary"]).size()
             .unstack(fill_value=0).sort_index())
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(10, 5.5))
    for i, sa in enumerate(pivot.columns):
        is_human = sa == "Human Sciences"
        cor = COR_HUMANAS if is_human else CORES_INTERMEDIARIAS[(i + 2) % 12]
        lw = 3.0 if is_human else 1.6
        ax.plot(pivot.index, pivot[sa], marker="o", linewidth=lw, color=cor,
                label=sa, alpha=1.0 if is_human else 0.8)
        x_end = pivot.index[-1]
        y_end = pivot[sa].iloc[-1]
        ax.text(x_end + 0.05, y_end, f"  {sa} ({y_end})",
                fontsize=8, va="center", color=cor)
    ax.set_xlabel("Ano de publicação")
    ax.set_ylabel("Artigos sobre Tecnologias IA/ML/DL")
    ax.set_xticks(sorted(pivot.index))
    ax.set_xlim(min(pivot.index) - 0.2, max(pivot.index) + 2.5)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_12_temporal_subject_area.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 13: heatmap subject_area × keyword (normalizado por coluna)
# ---------------------------------------------------------------------------
def fig13_heatmap_sa_keyword(df):
    texto = texto_classificacao(df)
    presenca = pd.DataFrame({
        label: texto.str.contains(pat, flags=re.IGNORECASE, regex=True, na=False)
        for label, pat in KEYWORDS_HEATMAP
    })
    presenca["SA"] = df["subject_area_primary"].values
    bruto = presenca.groupby("SA").sum(numeric_only=True)
    totais = df["subject_area_primary"].value_counts()
    keep = totais[totais >= 5].index
    bruto = bruto.loc[bruto.index.intersection(keep)]
    bruto = bruto.loc[totais.loc[bruto.index].sort_values(ascending=False).index]
    norm = bruto.div(bruto.sum(axis=0).replace(0, np.nan), axis=1).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(11, 4.5))
    im = ax.imshow(norm.values, aspect="auto", cmap=CMAP_SEQUENCIAL, vmin=0, vmax=norm.values.max())
    ax.set_xticks(range(len(norm.columns)))
    ax.set_xticklabels(norm.columns, rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(len(norm.index)))
    ax.set_yticklabels(norm.index, fontsize=9)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            v = norm.values[i, j]
            raw = int(bruto.values[i, j])
            if raw > 0:
                ax.text(j, i, f"{pct_ptbr(v, 0)}%\n({raw})",
                        ha="center", va="center",
                        color="#333" if v > norm.values.max() * 0.6 else "white",
                        fontsize=7)
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("% do termo concentrado na subject area", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_13_heatmap_sa_keyword.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 14: evolução total (Central vs Correlato)
# ---------------------------------------------------------------------------
def fig14_temporal_total(df):
    pivot = (df.groupby(["ano", "FOCO_IA"]).size()
             .unstack(fill_value=0).sort_index())
    fig, ax = plt.subplots(figsize=(10, 5.5))
    anos = pivot.index.astype(int).tolist()
    bottom = np.zeros(len(anos))
    cores = {"Tecnologias IA/ML/DL - Foco Central": COR_DEST,
             "Tecnologias IA/ML/DL - Correlato": CORES_INTERMEDIARIAS[1]}
    for foco in ["Tecnologias IA/ML/DL - Foco Central", "Tecnologias IA/ML/DL - Correlato"]:
        if foco not in pivot.columns:
            continue
        vals = pivot[foco].values
        ax.bar(anos, vals, bottom=bottom, color=cores[foco], label=foco.split(" - ")[1],
               edgecolor="white")
        for x, v, b in zip(anos, vals, bottom):
            if v > 5:
                ax.text(x, b + v/2, f"{int(v)}", ha="center", va="center",
                        color="white", fontsize=9)
        bottom = bottom + vals
    for x, total in zip(anos, bottom):
        ax.text(x, total + bottom.max() * 0.02, f"{int(total)}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xlabel("Ano de publicação")
    ax.set_ylabel("Artigos sobre Tecnologias IA/ML/DL")
    ax.set_xticks(anos)
    ax.legend(loc="upper left", frameon=False)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_14_temporal_total.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 15: idioma do artigo (paralelo ao 'nivel academico' da CAPES)
# ---------------------------------------------------------------------------
def fig15_idioma(df):
    serie = df["idioma"].fillna("(s/info)").value_counts()
    # Normaliza siglas comuns
    mapa = {"pt": "Português", "en": "Inglês", "es": "Espanhol",
            "fr": "Francês", "it": "Italiano", "de": "Alemão"}
    serie.index = [mapa.get(str(i).lower(), str(i)) for i in serie.index]
    serie = serie.groupby(level=0).sum().sort_values(ascending=False)
    total = serie.sum()
    fig, ax = plt.subplots(figsize=(9, 5))
    cores = [COR_DEST, CORES_INTERMEDIARIAS[1], CORES_INTERMEDIARIAS[2], COR_NEUTRA][:len(serie)]
    cores = (cores * 3)[:len(serie)]
    bars = ax.bar(serie.index, serie.values, color=cores, edgecolor="white")
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_x() + bar.get_width()/2,
                bar.get_height() + total * 0.005,
                f"{val}\n({pct_ptbr(val/total*100, 1)}%)",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Artigos sobre Tecnologias IA/ML/DL")
    ax.set_ylim(0, serie.max() * 1.20)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_15_idioma.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 16: top 20 periódicos (paralelo ao 'top áreas' da CAPES)
# ---------------------------------------------------------------------------
def fig16_top_periodicos(df):
    serie = df["periodico"].fillna("(s/info)").value_counts().head(20).sort_values()
    cores = []
    mapa_sa = (df.dropna(subset=["periodico"])
               .groupby("periodico")["subject_area_primary"]
               .agg(lambda s: s.mode().iat[0] if not s.mode().empty else "(s/info)"))
    for p in serie.index:
        sa = mapa_sa.get(p, "")
        cores.append(_cor_sa(sa))

    fig, ax = plt.subplots(figsize=(11, 8))
    bars = ax.barh(serie.index, serie.values, color=cores, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_width() + serie.max() * 0.01,
                bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", fontsize=8)
    ax.set_xlabel("Artigos sobre Tecnologias IA/ML/DL (top 20 periódicos)")
    ax.set_xlim(0, serie.max() * 1.12)
    from matplotlib.patches import Patch
    ax.legend(handles=[
        Patch(color=COR_DESTAQUE, label="Periódico em Human Sciences"),
        Patch(color=COR_SCIELO, label="Outras subject areas"),
    ], loc="lower right", frameon=False, fontsize=8)
    # Trunca labels longas
    ax.set_yticklabels([t[:42] + "…" if len(t) > 42 else t for t in serie.index], fontsize=8)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_16_top_periodicos.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 20: top termos
# ---------------------------------------------------------------------------
def fig20_top_termos(df):
    texto = df["titulo"].fillna("").astype(str).str.lower()
    texto = texto.str.replace(r"[^\wáéíóúâêôãõçà\s-]", " ", regex=True)
    termos_ia = {
        "inteligência", "artificial", "machine", "deep", "learning", "aprendizado",
        "máquina", "maquina", "profundo", "redes", "rede", "neurais", "neural",
        "ia", "llm", "llms", "chatgpt", "gpt", "transformer", "transformers",
        "generativa", "modelos", "modelo", "linguagem",
    }
    stop = STOPWORDS_PT | termos_ia | {"the", "of", "and", "in", "for", "to", "a", "an", "on", "with",
                                        "intelligence", "learning", "based", "study", "analysis"}
    counter = Counter()
    for t in texto:
        for tok in t.split():
            tok = tok.strip("-")
            if len(tok) >= 4 and tok not in stop:
                counter[tok] += 1
    top = counter.most_common(25)
    if not top:
        print("  (sem termos para fig20)")
        return
    labels, vals = zip(*reversed(top))
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(labels, vals, color=COR_DEST, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals) * 0.02,
                bar.get_y() + bar.get_height()/2,
                f"{val}", va="center", fontsize=8)
    ax.set_xlabel("Ocorrências em títulos (top 25, exclui termos canônicos)")
    ax.set_xlim(0, max(vals) * 1.18)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_20_top_termos.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 21: distribuição por subcampo
# ---------------------------------------------------------------------------
def fig21_subcampos_dist(df):
    pares = []
    total = len(df)
    for (col, label), cor in zip(SUBCAMPO_COLS, SUBCAMPO_CORES):
        n = int(_bool(df[col]).sum()) if col in df.columns else 0
        pares.append((label, n, cor))
    pares.sort(key=lambda x: x[1])
    labels = [p[0] for p in pares]
    vals = [p[1] for p in pares]
    pcts = [v / total * 100 for v in vals]
    fig, ax = plt.subplots(figsize=(10, 5.2))
    dotplot(ax, labels, vals, COR_SCIELO, pcts=pcts)
    estilo_editorial(ax, nota=(
        f"Artigos que mencionam o subcampo · N = {num_ptbr(total)}. "
        "Um artigo pode estar em múltiplos subcampos; percentuais somam mais que 100%."))
    out = os.path.join(FIGURAS_DIR, "scielo_21_subcampos_distribuicao.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 22: heatmap subcampo × subject_area
# ---------------------------------------------------------------------------
def fig22_heatmap_subcampo_sa(df):
    df = df.copy()
    rows = []
    for col, label in SUBCAMPO_COLS:
        sub = df[_bool(df[col])]
        counts = sub["subject_area_primary"].value_counts()
        rows.append(counts.rename(label))
    bruto = pd.DataFrame(rows).fillna(0).astype(int)
    ordem_cols = df["subject_area_primary"].value_counts().index
    bruto = bruto.reindex(columns=ordem_cols)
    norm = bruto.div(bruto.sum(axis=1).replace(0, np.nan), axis=0).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(11, 4.5))
    im = ax.imshow(norm.values, aspect="auto", cmap=CMAP_SEQUENCIAL, vmin=0, vmax=norm.values.max())
    ax.set_xticks(range(len(norm.columns)))
    ax.set_xticklabels(norm.columns, rotation=20, ha="right", fontsize=8)
    ax.set_yticks(range(len(norm.index)))
    ax.set_yticklabels(norm.index, fontsize=9)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            v = norm.values[i, j]
            raw = int(bruto.values[i, j])
            if raw > 0:
                ax.text(j, i, f"{pct_ptbr(v, 0)}%\n({raw})",
                        ha="center", va="center",
                        color="#333" if v > norm.values.max() * 0.6 else "white",
                        fontsize=7)
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("% da subject area dentro do subcampo (por linha)", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_22_heatmap_subcampo_sa.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 23: evolução temporal por subcampo
# ---------------------------------------------------------------------------
def fig23_temporal_subcampos(df):
    anos = sorted(df["ano"].dropna().unique().tolist())
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for (col, label), cor in zip(SUBCAMPO_COLS, SUBCAMPO_CORES):
        serie = df[_bool(df[col])].groupby("ano").size().reindex(anos, fill_value=0)
        ax.plot(serie.index, serie.values, marker="o", linewidth=2.3, color=cor, label=label)
        x_end = serie.index[-1]
        y_end = serie.iloc[-1]
        ax.text(x_end + 0.06, y_end, f" {y_end}", fontsize=8, va="center", color=cor)
    ax.set_xlabel("Ano de publicação")
    ax.set_ylabel("Artigos que mencionam o subcampo")
    ax.set_xticks(anos)
    ax.set_xlim(min(anos) - 0.2, max(anos) + 1.0)
    ax.legend(loc="upper left", frameon=False, fontsize=8)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "scielo_23_temporal_subcampos.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


if __name__ == "__main__":
    print("Carregando subset IA SciELO ...")
    df = carregar_ia()
    print(f"\nCarregando universo (para taxa interna) ...")
    universo = carregar_universo()
    if universo is None:
        print("  universo indisponível — figura 11 sem taxa interna")
    else:
        if "subject_area" in universo.columns and "total" in universo.columns:
            print(f"  agregado leve: {int(universo['total'].sum()):,} artigos no universo")
        else:
            print(f"  {len(universo):,} artigos no universo {ANO_MIN}-{ANO_MAX}")

    print("\nGerando figuras:")
    fig11_subject_area(df, universo)
    fig12_temporal_subject_area(df)
    fig13_heatmap_sa_keyword(df)
    fig14_temporal_total(df)
    fig15_idioma(df)
    fig16_top_periodicos(df)
    fig20_top_termos(df)
    fig21_subcampos_dist(df)
    fig22_heatmap_subcampo_sa(df)
    fig23_temporal_subcampos(df)
    print("\nPronto.")
