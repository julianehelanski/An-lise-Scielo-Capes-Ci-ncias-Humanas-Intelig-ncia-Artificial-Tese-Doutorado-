# -*- coding: utf-8 -*-
"""Gera o conjunto de figuras da análise CAPES 2021-2024.

Pré-requisito: rodar `python analise_capes_2021_2024.py` antes.

Saídas em figuras/:
  capes_11_grande_area_share.png        IA por grande área (absoluto + taxa interna)
  capes_12_temporal_grande_area.png     evolução 2021-2024 por grande área
  capes_13_heatmap_area_keyword.png     heatmap grande área × keyword
  capes_14_temporal_total.png           total IA por ano (Central + Relacionado)
  capes_15_nivel_academico.png          mestrado / doutorado / profissional
  capes_16_top_areas_conhecimento.png   top 20 áreas de conhecimento
  capes_17_top_instituicoes.png         top 20 instituições
  capes_18_regiao_uf.png                IA por região e UF
  capes_19_paginas.png                  distribuição de páginas
  capes_20_top_termos.png               top termos no corpus IA

Uso:
    python figuras_capes_2021_2024.py
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
    COR_CAPES,
    COR_DESTAQUE,
    COR_NEUTRO,
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    FIGURAS_DIR,
    LABEL_GUARDA_CHUVA,
    LABEL_GUARDA_CHUVA_CURTO,
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

CSV_IA = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia.csv")
CSV_AUDIT = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia_auditoria.xlsx")

COR_HUMANAS = CORES_INTERMEDIARIAS[0]      # destaque vermelho-muted
COR_NEUTRA = CORES_INTERMEDIARIAS[9]       # cinza-azulado
COR_DEST = CORES_INTERMEDIARIAS[3]         # azul
COR_OUTROS = CORES_INTERMEDIARIAS[11]      # cinza muito claro

KEYWORDS_HEATMAP = [
    ("inteligência artificial", r"\b(intelig[êe]ncia\s+artificial|artificial\s+intelligence)\b"),
    ("machine/deep learning", r"\b(machine\s+learning|deep\s+learning|aprendizado\s+de\s+m[áa]quina|aprendizado\s+profundo)\b"),
    ("redes neurais", r"\b(redes?\s+neurais|neural\s+networks?)\b"),
    ("LLM / modelo de linguagem", r"\b(llms?|large\s+language\s+models?|modelos?\s+de\s+linguagem|transformer[s]?)\b"),
    ("ChatGPT / GPT-N", r"\b(chatgpt|gpt-\d)\b"),
    ("IA generativa", r"\b(ia\s+generativa|generative\s+ai)\b"),
    ("robótica / automação", r"\b(rob[óo]tica|rob[ôo]s|automa[çc][ãa]o|automation)\b"),
    ("NLP", r"\b(processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp)\b"),
    ("big data / mineração", r"\b(big\s+data|minera[çc][ãa]o\s+de\s+dados|data\s+mining)\b"),
    ("visão computacional", r"\b(vis[ãa]o\s+computacional|computer\s+vision)\b"),
]


def carregar_ia() -> pd.DataFrame:
    if os.path.isfile(CSV_IA):
        return pd.read_csv(CSV_IA, low_memory=False)
    if os.path.isfile(CSV_AUDIT):
        sys.stderr.write(
            f"[aviso] usando {CSV_AUDIT} (sem resumo). Termos no heatmap ficarão mais escassos.\n"
        )
        return pd.read_excel(CSV_AUDIT, engine="openpyxl")
    sys.exit(f"ERRO: rode antes analise_capes_2021_2024.py — falta {CSV_IA}")


CACHE_TOTAIS = os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_universo_por_grande_area.csv")


def carregar_totais_grande_area() -> pd.Series | None:
    """Lê os totais por grande área no universo completo, com cache.

    Primeira vez: lê os 4 XLSX (~10 min) e salva CSV em `CACHE_TOTAIS`.
    Próximas: lê o CSV direto (instantâneo).
    """
    # Cache hit
    if os.path.isfile(CACHE_TOTAIS):
        df = pd.read_csv(CACHE_TOTAIS)
        return pd.Series(df["total"].values, index=df["grande_area"].values)
    # Cache miss: precisa dos XLSX
    capes_dir = os.environ.get("CAPES_DATA_DIR", DADOS_CAPES_DIR)
    import glob
    xlsx = sorted(glob.glob(os.path.join(capes_dir, "br-capes-btd-*.xlsx")))
    if not xlsx or any(os.path.getsize(x) < 1024 for x in xlsx):
        return None
    print(f"  [cache miss] lendo {len(xlsx)} XLSX para calcular universo por grande área (uma vez só)...")
    partes = [pd.read_excel(p, usecols=["NM_GRANDE_AREA_CONHECIMENTO"], engine="openpyxl") for p in xlsx]
    full = pd.concat(partes, ignore_index=True)
    serie = full["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(não informado)").value_counts()
    # Salva cache
    serie.reset_index().rename(columns={"index": "grande_area", "NM_GRANDE_AREA_CONHECIMENTO": "grande_area", "count": "total"}).to_csv(CACHE_TOTAIS, index=False)
    print(f"  [cache write] {CACHE_TOTAIS}")
    return serie


def texto_classificacao(df: pd.DataFrame) -> pd.Series:
    s = df["NM_PRODUCAO"].fillna("").astype(str)
    for c in ["DS_RESUMO", "DS_PALAVRA_CHAVE", "DS_ABSTRACT", "DS_KEYWORD"]:
        if c in df.columns:
            s = s + " | " + df[c].fillna("").astype(str)
    return s


def _cor_por_humanas(label: str) -> str:
    # Base CAPES em verde; Ciências Humanas (foco) em magenta de destaque.
    # Caixa-insensível: os rótulos vêm em maiúsculas ("CIÊNCIAS HUMANAS").
    return COR_DESTAQUE if "humanas" in str(label).lower() else COR_CAPES


# ---------------------------------------------------------------------------
# Figura 11: IA por grande área — absoluto + taxa interna (dois painéis)
# ---------------------------------------------------------------------------
def fig11_grande_area(df: pd.DataFrame, totais_universo: pd.Series | None) -> None:
    counts = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().sort_values()
    labels = list(counts.index)
    vals = list(counts.values)
    total = counts.sum()
    cores = [_cor_por_humanas(a) for a in labels]
    pcts = [v / total * 100 for v in vals]
    nota = (f"CAPES · 2021–2024 · N = {num_ptbr(total)}. "
            "Ciências Humanas em destaque (magenta).")

    if totais_universo is not None:
        # Dois painéis (mesma ordem): volume no corpus + taxa interna.
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 6.2), gridspec_kw={"wspace": 0.5})
    else:
        fig, ax1 = plt.subplots(figsize=(10, 6))
        ax2 = None

    dotplot(ax1, labels, vals, cores, pcts=pcts)
    estilo_editorial(ax1, titulo="Volume no corpus de IA", nota=nota)

    if ax2 is not None:
        taxa = []
        for a in labels:
            t = counts.get(a, 0) / totais_universo.get(a, float("nan")) * 100
            taxa.append(0.0 if pd.isna(t) else t)
        rot = [f"{pct_ptbr(t)}%" for t in taxa]
        dotplot(ax2, labels, taxa, cores, rotulos=rot)
        ax2.set_yticklabels([])  # eixo Y alinhado ao painel da esquerda
        estilo_editorial(ax2, titulo="Taxa interna (% da área que toca IA)")

    out = os.path.join(FIGURAS_DIR, "capes_11_grande_area_share.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 12: evolução temporal por grande área
# ---------------------------------------------------------------------------
def fig12_temporal_grande_area(df: pd.DataFrame) -> None:
    df = df.copy()
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce")
    df = df.dropna(subset=["AN_BASE"])
    df["AN_BASE"] = df["AN_BASE"].astype(int)
    df["NM_GRANDE_AREA_CONHECIMENTO"] = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(s/info)")

    pivot = (df.groupby(["AN_BASE", "NM_GRANDE_AREA_CONHECIMENTO"]).size()
             .unstack(fill_value=0).sort_index())
    pivot = pivot[pivot.sum().sort_values(ascending=False).index]

    fig, ax = plt.subplots(figsize=(11, 6.5))
    for i, area in enumerate(pivot.columns):
        is_humanas = "Humanas" in str(area)
        cor = COR_HUMANAS if is_humanas else CORES_INTERMEDIARIAS[(i + 2) % 12]
        lw = 3.0 if is_humanas else 1.4
        ax.plot(pivot.index, pivot[area], marker="o", linewidth=lw,
                color=cor, label=str(area),
                alpha=1.0 if is_humanas else 0.7)
        # Rótulo no fim de cada linha
        x_end = pivot.index[-1]
        y_end = pivot[area].iloc[-1]
        ax.text(x_end + 0.05, y_end, f"  {area} ({num_ptbr(y_end)})",
                fontsize=8, va="center", color=cor)

    ax.set_xlabel("Ano base de defesa")
    ax.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL")
    ax.set_xticks(sorted(pivot.index))
    ax.set_xlim(min(pivot.index) - 0.2, max(pivot.index) + 2.2)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_12_temporal_grande_area.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 13: heatmap grande área × keyword
# ---------------------------------------------------------------------------
def fig13_heatmap_area_keyword(df: pd.DataFrame) -> None:
    texto = texto_classificacao(df)
    presenca = pd.DataFrame({
        label: texto.str.contains(pat, flags=re.IGNORECASE, regex=True, na=False)
        for label, pat in KEYWORDS_HEATMAP
    })
    presenca["GRANDE_AREA"] = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(s/info)").values

    bruto = presenca.groupby("GRANDE_AREA").sum(numeric_only=True)
    totais = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts()
    keep = totais[totais >= 20].index
    bruto = bruto.loc[bruto.index.intersection(keep)]
    bruto = bruto.loc[totais.loc[bruto.index].sort_values(ascending=False).index]

    # Normaliza por COLUNA (termo): mostra concentração geográfica do termo nas áreas
    norm_col = bruto.div(bruto.sum(axis=0).replace(0, np.nan), axis=1).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(11, 6.5))
    im = ax.imshow(norm_col.values, aspect="auto", cmap=CMAP_SEQUENCIAL, vmin=0, vmax=norm_col.values.max())
    ax.set_xticks(range(len(norm_col.columns)))
    ax.set_xticklabels(norm_col.columns, rotation=40, ha="right", fontsize=8)
    ax.set_yticks(range(len(norm_col.index)))
    ax.set_yticklabels(norm_col.index, fontsize=9)
    for i in range(norm_col.shape[0]):
        for j in range(norm_col.shape[1]):
            v = norm_col.values[i, j]
            raw = int(bruto.values[i, j])
            if raw > 0:
                txt = f"{pct_ptbr(v, 0)}%\n({num_ptbr(raw)})"
                ax.text(j, i, txt, ha="center", va="center",
                        color="#333" if v > norm_col.values.max() * 0.6 else "white",
                        fontsize=6.5)
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("% do termo concentrado na grande área", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_13_heatmap_area_keyword.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 14: evolução temporal total (Central vs Relacionado)
# ---------------------------------------------------------------------------
def fig14_temporal_total(df: pd.DataFrame) -> None:
    df = df.copy()
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce").astype("Int64")
    pivot = (df.groupby(["AN_BASE", "FOCO_IA"]).size()
             .unstack(fill_value=0).sort_index())

    fig, ax = plt.subplots(figsize=(10, 5.5))
    anos = pivot.index.astype(int).tolist()
    bottom = np.zeros(len(anos))
    cores = {"Tecnologias IA/ML/DL - Foco Central": COR_DEST, "Tecnologias IA/ML/DL - Correlato": CORES_INTERMEDIARIAS[1]}
    for foco in ["Tecnologias IA/ML/DL - Foco Central", "Tecnologias IA/ML/DL - Correlato"]:
        if foco not in pivot.columns:
            continue
        vals = pivot[foco].values
        ax.bar(anos, vals, bottom=bottom, color=cores[foco], label=foco, edgecolor="white")
        for x, v, b in zip(anos, vals, bottom):
            if v > 50:
                ax.text(x, b + v / 2, f"{num_ptbr(int(v))}", ha="center", va="center",
                        color="white", fontsize=9)
        bottom = bottom + vals
    # Total no topo
    for x, total in zip(anos, bottom):
        ax.text(x, total + max(bottom) * 0.02, f"{num_ptbr(int(total))}",
                ha="center", va="bottom", fontsize=10, fontweight="bold")
    ax.set_xlabel("Ano base de defesa")
    ax.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL")
    ax.set_xticks(anos)
    ax.legend(loc="upper left", frameon=False)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_14_temporal_total.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 15: nível acadêmico (Mestrado / Doutorado / Profissional)
# ---------------------------------------------------------------------------
def fig15_nivel_academico(df: pd.DataFrame) -> None:
    serie = df["NM_GRAU_ACADEMICO"].fillna("(s/info)").value_counts()
    total = serie.sum()

    fig, ax = plt.subplots(figsize=(9, 5))
    cores = [COR_DEST, CORES_INTERMEDIARIAS[1], CORES_INTERMEDIARIAS[2], COR_NEUTRA][: len(serie)]
    bars = ax.bar(serie.index, serie.values, color=cores, edgecolor="white")
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + total * 0.005,
                f"{num_ptbr(val)}\n({pct_ptbr(val/total*100, 1)}%)",
                ha="center", va="bottom", fontsize=9)
    ax.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL")
    ax.set_ylim(0, serie.max() * 1.18)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_15_nivel_academico.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 16: top 20 áreas de conhecimento
# ---------------------------------------------------------------------------
def fig16_top_areas_conhecimento(df: pd.DataFrame) -> None:
    serie = (df["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().head(20)
             .sort_values())
    cores = []
    # Para esta figura precisamos saber a grande área de cada área
    mapa_ga = (df.dropna(subset=["NM_AREA_CONHECIMENTO"])
               .groupby("NM_AREA_CONHECIMENTO")["NM_GRANDE_AREA_CONHECIMENTO"]
               .agg(lambda s: s.mode().iat[0] if not s.mode().empty else "(s/info)"))
    for area in serie.index:
        ga = mapa_ga.get(area, "")
        cores.append(_cor_por_humanas(ga))

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(serie.index, serie.values, color=cores, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_width() + serie.max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{num_ptbr(val)}", va="center", fontsize=8)
    ax.set_xlabel("Trabalhos no campo Tecnologias IA/ML/DL (top 20 áreas de conhecimento)")
    ax.set_xlim(0, serie.max() * 1.12)
    # Legenda explicando cor
    from matplotlib.patches import Patch
    legend_handles = [
        Patch(color=COR_HUMANAS, label="Ciências Humanas"),
        Patch(color=COR_NEUTRA, label="Outras grandes áreas"),
    ]
    ax.legend(handles=legend_handles, loc="lower right", frameon=False, fontsize=8)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_16_top_areas_conhecimento.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 17: top 20 instituições
# ---------------------------------------------------------------------------
def fig17_top_instituicoes(df: pd.DataFrame) -> None:
    serie = (df["SG_ENTIDADE_ENSINO"].fillna("(s/info)").value_counts().head(20)
             .sort_values())
    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(serie.index, serie.values, color=COR_DEST, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, serie.values):
        ax.text(bar.get_width() + serie.max() * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{num_ptbr(val)}", va="center", fontsize=8)
    ax.set_xlabel("Trabalhos no campo Tecnologias IA/ML/DL (top 20 IES)")
    ax.set_xlim(0, serie.max() * 1.12)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_17_top_instituicoes.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 18: IA por região e UF
# ---------------------------------------------------------------------------
def fig18_regiao_uf(df: pd.DataFrame) -> None:
    regiao = df["NM_REGIAO"].fillna("(s/info)").value_counts()
    uf = df["SG_UF_IES"].fillna("?").value_counts().head(15)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 5.5), gridspec_kw={"width_ratios": [1, 1.4]})
    cores_r = [CORES_INTERMEDIARIAS[i] for i in [3, 1, 2, 4, 7]][: len(regiao)]
    bars = ax1.bar(regiao.index, regiao.values, color=cores_r, edgecolor="white")
    for bar, val in zip(bars, regiao.values):
        ax1.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + regiao.max() * 0.01,
                 f"{num_ptbr(val)}", ha="center", va="bottom", fontsize=9)
    ax1.set_title("Por região", fontsize=10)
    ax1.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL")
    ax1.set_ylim(0, regiao.max() * 1.15)

    bars = ax2.bar(uf.index, uf.values, color=COR_DEST, edgecolor="white")
    for bar, val in zip(bars, uf.values):
        ax2.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + uf.max() * 0.01,
                 f"{num_ptbr(val)}", ha="center", va="bottom", fontsize=8)
    ax2.set_title("Top 15 UFs", fontsize=10)
    ax2.set_ylim(0, uf.max() * 1.15)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_18_regiao_uf.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 19: distribuição de páginas
# ---------------------------------------------------------------------------
def fig19_paginas(df: pd.DataFrame) -> None:
    p = pd.to_numeric(df["NR_PAGINAS"], errors="coerce")
    p = p[(p > 20) & (p < 800)]  # remove outliers de digitação
    fig, ax = plt.subplots(figsize=(10, 5.5))
    ax.hist(p, bins=40, color=COR_DEST, edgecolor="white", alpha=0.9)
    mediana = p.median()
    ax.axvline(mediana, color=CORES_INTERMEDIARIAS[0], linestyle="--", linewidth=2,
               label=f"mediana = {mediana:.0f} páginas")
    ax.set_xlabel("Número de páginas")
    ax.set_ylabel("Trabalhos no campo Tecnologias IA/ML/DL")
    ax.legend(frameon=False)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_19_paginas.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figura 20: top termos no corpus IA (n-gramas relevantes)
# ---------------------------------------------------------------------------
def fig20_top_termos(df: pd.DataFrame) -> None:
    """Conta termos dos títulos, removendo stopwords e termos do regex IA
    (que dominariam o ranking sem agregar informação)."""
    texto = df["NM_PRODUCAO"].fillna("").astype(str).str.lower()
    # Limpa pontuação básica
    texto = texto.str.replace(r"[^\wáéíóúâêôãõçà\s-]", " ", regex=True)
    # Remove termos do próprio regex IA (não traz informação nova)
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
        print("  (sem termos para fig20)")
        return
    labels, vals = zip(*reversed(top))

    fig, ax = plt.subplots(figsize=(10, 8))
    bars = ax.barh(labels, vals, color=COR_DEST, edgecolor="white", linewidth=0.5)
    for bar, val in zip(bars, vals):
        ax.text(bar.get_width() + max(vals) * 0.01,
                bar.get_y() + bar.get_height() / 2,
                f"{num_ptbr(val)}", va="center", fontsize=8)
    ax.set_xlabel("Ocorrências em títulos (top 25, exclui termos canônicos de IA)")
    ax.set_xlim(0, max(vals) * 1.12)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_20_top_termos.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# ---------------------------------------------------------------------------
# Figuras 21-23: subcampos (IA stricto, ML, DL, LLMs, correlatos)
# ---------------------------------------------------------------------------
SUBCAMPO_COLS = [
    ("SUBCAMPO_IA_STRICTO", "IA em sentido estrito"),
    ("SUBCAMPO_ML", "Aprendizado de máquina (ML)"),
    ("SUBCAMPO_DL", "Aprendizado profundo & redes neurais"),
    ("SUBCAMPO_LLM", "Modelos de linguagem & IA generativa"),
    ("SUBCAMPO_CORRELATOS", "Tecnologias correlatas"),
]
SUBCAMPO_CORES = [
    CORES_INTERMEDIARIAS[3],   # azul: IA stricto
    CORES_INTERMEDIARIAS[2],   # verde: ML
    CORES_INTERMEDIARIAS[4],   # roxo: DL/redes
    CORES_INTERMEDIARIAS[6],   # rosa: LLMs
    CORES_INTERMEDIARIAS[9],   # cinza-azulado: correlatos
]


def _bool_col(df: pd.DataFrame, col: str) -> pd.Series:
    """Converte coluna booleana (que pode vir como str do CSV) para bool."""
    if col not in df.columns:
        return pd.Series(False, index=df.index)
    s = df[col]
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1", "1.0", "yes"])


# Figura 21: distribuição dos 13.336 trabalhos por subcampo
def fig21_subcampos_distribuicao(df: pd.DataFrame) -> None:
    counts = []
    for col, label in SUBCAMPO_COLS:
        counts.append(_bool_col(df, col).sum())
    total = len(df)
    # Ordena do menor para o maior (dot plot: maior no topo). Base CAPES (verde).
    pares = sorted(zip([l for _, l in SUBCAMPO_COLS], counts), key=lambda x: x[1])
    labels = [p[0] for p in pares]
    vals = [p[1] for p in pares]
    pcts = [v / total * 100 for v in vals]

    fig, ax = plt.subplots(figsize=(10, 5.2))
    dotplot(ax, labels, vals, COR_CAPES, pcts=pcts)
    estilo_editorial(ax, nota=(
        f"Trabalhos que mencionam o subcampo · N = {num_ptbr(total)}. "
        "Um trabalho pode estar em múltiplos subcampos; percentuais somam mais que 100%."))
    out = os.path.join(FIGURAS_DIR, "capes_21_subcampos_distribuicao.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# Figura 22: heatmap subcampo × grande área (normalizado por coluna = subcampo)
def fig22_heatmap_subcampo_grande_area(df: pd.DataFrame) -> None:
    df = df.copy()
    df["NM_GRANDE_AREA_CONHECIMENTO"] = df["NM_GRANDE_AREA_CONHECIMENTO"].fillna("(s/info)")
    rows = []
    for col, label in SUBCAMPO_COLS:
        sub = df[_bool_col(df, col)]
        counts = sub["NM_GRANDE_AREA_CONHECIMENTO"].value_counts()
        rows.append(counts.rename(label))
    bruto = pd.DataFrame(rows).fillna(0).astype(int)
    # Ordena colunas (grandes áreas) por volume total no corpus IA
    ordem_cols = df["NM_GRANDE_AREA_CONHECIMENTO"].value_counts().index
    bruto = bruto.reindex(columns=ordem_cols)
    # Normaliza por linha (subcampo): mostra concentração geográfica do subcampo
    norm = bruto.div(bruto.sum(axis=1).replace(0, np.nan), axis=0).fillna(0) * 100

    fig, ax = plt.subplots(figsize=(13, 5.5))
    im = ax.imshow(norm.values, aspect="auto", cmap=CMAP_SEQUENCIAL, vmin=0, vmax=norm.values.max())
    ax.set_xticks(range(len(norm.columns)))
    ax.set_xticklabels(norm.columns, rotation=30, ha="right", fontsize=8)
    ax.set_yticks(range(len(norm.index)))
    ax.set_yticklabels(norm.index, fontsize=9)
    for i in range(norm.shape[0]):
        for j in range(norm.shape[1]):
            v = norm.values[i, j]
            raw = int(bruto.values[i, j])
            if raw > 0:
                ax.text(j, i, f"{pct_ptbr(v, 0)}%\n({num_ptbr(raw)})",
                        ha="center", va="center",
                        color="#333" if v > norm.values.max() * 0.6 else "white",
                        fontsize=7)
    cbar = plt.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.set_label("% do subcampo concentrado na grande área", fontsize=8)
    cbar.ax.tick_params(labelsize=7)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_22_heatmap_subcampo_grande_area.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


# Figura 23: evolução temporal por subcampo (5 linhas 2021-2024)
def fig23_temporal_subcampos(df: pd.DataFrame) -> None:
    df = df.copy()
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce").astype("Int64")
    anos = sorted(df["AN_BASE"].dropna().unique().tolist())

    fig, ax = plt.subplots(figsize=(10, 6))
    for (col, label), cor in zip(SUBCAMPO_COLS, SUBCAMPO_CORES):
        serie = df[_bool_col(df, col)].groupby("AN_BASE").size().reindex(anos, fill_value=0)
        ax.plot(serie.index, serie.values, marker="o", linewidth=2.3, color=cor, label=label)
        # Anota valor final
        x_end = serie.index[-1]
        y_end = serie.iloc[-1]
        ax.text(x_end + 0.06, y_end, f" {num_ptbr(y_end)}", fontsize=8, va="center", color=cor)

    ax.set_xlabel("Ano base de defesa")
    ax.set_ylabel("Trabalhos que mencionam o subcampo")
    ax.set_xticks(anos)
    ax.set_xlim(min(anos) - 0.2, max(anos) + 1.0)
    ax.legend(loc="upper left", frameon=False, fontsize=9)
    plt.tight_layout()
    out = os.path.join(FIGURAS_DIR, "capes_23_temporal_subcampos.png")
    salvar_figura(out)
    plt.close(fig)
    print(f"  → {out}")


if __name__ == "__main__":
    print("Carregando subset IA ...")
    df = carregar_ia()
    print(f"  {len(df):,} trabalhos no campo Tecnologias IA/ML/DL carregados")

    print("Carregando totais por grande área (universo completo) ...")
    totais_universo = carregar_totais_grande_area()
    if totais_universo is not None:
        print(f"  totais lidos para {len(totais_universo)} grandes áreas")
    else:
        print("  (universo total indisponível — figura 11 sem taxa interna)")

    print("\nGerando figuras:")
    fig11_grande_area(df, totais_universo)
    fig12_temporal_grande_area(df)
    fig13_heatmap_area_keyword(df)
    fig14_temporal_total(df)
    fig15_nivel_academico(df)
    fig16_top_areas_conhecimento(df)
    fig17_top_instituicoes(df)
    fig18_regiao_uf(df)
    fig19_paginas(df)
    fig20_top_termos(df)
    fig21_subcampos_distribuicao(df)
    fig22_heatmap_subcampo_grande_area(df)
    fig23_temporal_subcampos(df)
    print("\nPronto.")
