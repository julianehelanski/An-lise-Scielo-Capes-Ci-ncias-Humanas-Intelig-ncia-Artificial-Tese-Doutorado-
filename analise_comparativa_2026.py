# -*- coding: utf-8 -*-
"""Análise comparativa SciELO × CAPES — versão 2026.

Substitui o analise_comparativa.py antigo. Lê os outputs novos de
ambas as bases (SciELO via ArticleMeta + CAPES via dump oficial),
restringe a 2021-2024 estrito, e produz figura comparativa + tabelas.

Pré-requisitos:
- dados_scielo/scielo_ia_subcampos.csv (gerado por
  analise_scielo_articlemeta.py)
- dados_capes/capes_2021_2024_ia_auditoria.xlsx (gerado por
  analise_capes_2021_2024.py)

Saídas:
- figuras/comparativo_scielo_capes_2026.png
- tabelas_comparativas_2026.md
"""

from __future__ import annotations

import os
import sys

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    DADOS_SCIELO_DIR,
    FIGURAS_DIR,
    aplicar_estilo_padrao,
    dotplot,
    dumbbell,
    garantir_diretorio,
    num_ptbr,
    pct_ptbr,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

COR_SCIELO = "#0072B2"   # azul (cor-assinatura SciELO, Okabe-Ito)
COR_CAPES = "#009E73"    # verde (cor-assinatura CAPES, Okabe-Ito)

ANO_MIN = 2021
ANO_MAX = 2024

SUBCAMPOS = [
    ("SUBCAMPO_IA_STRICTO", "IA em sentido estrito"),
    ("SUBCAMPO_ML", "Aprendizado de máquina (ML)"),
    ("SUBCAMPO_DL", "Aprendizado profundo & redes neurais"),
    ("SUBCAMPO_LLM", "Modelos de linguagem & IA generativa"),
    ("SUBCAMPO_CORRELATOS", "Tecnologias correlatas"),
]


def _bool(s):
    if s.dtype == bool:
        return s
    return s.astype(str).str.lower().isin(["true", "1"])


def carregar_scielo() -> pd.DataFrame:
    """Carrega SciELO Brasil completo (universo todas as áreas).

    Filtra para Human Sciences puro para paridade real com CAPES Humanas
    (ambos os subsets passam pelo mesmo classificar_subcampos).
    """
    # Prefere o universo Brasil completo (XLSX), com fallback para o
    # recorte de áreas-alvo (CSV) caso o XLSX não esteja disponível.
    xlsx = os.path.join(DADOS_SCIELO_DIR, "scielo_brasil_ia_subcampos_auditoria.xlsx")
    csv = os.path.join(DADOS_SCIELO_DIR, "scielo_ia_subcampos.csv")
    if os.path.isfile(xlsx):
        df = pd.read_excel(xlsx, engine="openpyxl")
        fonte = "SciELO Brasil completo (XLSX, 8 subject_areas)"
    elif os.path.isfile(csv):
        df = pd.read_csv(csv, low_memory=False)
        fonte = "SciELO recorte 3 áreas-alvo (CSV, fallback)"
    else:
        sys.exit("ERRO: rode antes analise_scielo_articlemeta.py")
    df["ano"] = pd.to_numeric(df["ano"], errors="coerce").astype("Int64")
    n_pre = len(df)
    df = df[(df["ano"] >= ANO_MIN) & (df["ano"] <= ANO_MAX)].copy()
    print(f"{fonte}: {n_pre} → {len(df)} após restrição a {ANO_MIN}-{ANO_MAX}")
    return df


def carregar_scielo_human_sciences(sci_total: pd.DataFrame) -> pd.DataFrame:
    """Subset apenas de Human Sciences puro (para paridade com CAPES Humanas).

    Inclui apenas periódicos cuja subject_area é exatamente 'Human Sciences'
    (excluindo multidisciplinares e outras categorias).
    """
    hs = sci_total[sci_total["subject_areas_periodico"]
                   .fillna("").astype(str).str.strip() == "Human Sciences"].copy()
    print(f"SciELO Human Sciences (estrito): {len(hs)}")
    return hs


def carregar_capes() -> pd.DataFrame:
    """Carrega CAPES IA-Humanas (restrito à grande área Ciências Humanas)."""
    df = pd.read_excel(os.path.join(DADOS_CAPES_DIR, "capes_2021_2024_ia_auditoria.xlsx"),
                       engine="openpyxl")
    df["AN_BASE"] = pd.to_numeric(df["AN_BASE"], errors="coerce").astype("Int64")
    df = df[df["NM_GRANDE_AREA_CONHECIMENTO"].str.contains("HUMANAS", case=False, na=False)]
    df = df[(df["AN_BASE"] >= ANO_MIN) & (df["AN_BASE"] <= ANO_MAX)].copy()
    print(f"CAPES Humanas: {len(df)} ({ANO_MIN}-{ANO_MAX})")
    return df


def fig_comparativa(sci: pd.DataFrame, cap: pd.DataFrame) -> None:
    fig, axes = plt.subplots(2, 2, figsize=(13, 10), constrained_layout=True)

    # ----- (A) Evolução temporal sobreposta -----
    ax = axes[0, 0]
    s_ano = sci.groupby("ano").size().reindex(range(ANO_MIN, ANO_MAX + 1), fill_value=0)
    c_ano = cap.groupby("AN_BASE").size().reindex(range(ANO_MIN, ANO_MAX + 1), fill_value=0)
    ax.plot(s_ano.index, s_ano.values, marker="o", color=COR_SCIELO, linewidth=2.5,
            label=f"SciELO Human Sciences (n={s_ano.sum()})")
    ax.plot(c_ano.index, c_ano.values, marker="s", color=COR_CAPES, linewidth=2.5,
            label=f"CAPES Humanas (n={c_ano.sum()})")
    for x, y in zip(s_ano.index, s_ano.values):
        ax.text(x, y + 3, f"{y}", ha="center", color=COR_SCIELO, fontsize=8)
    for x, y in zip(c_ano.index, c_ano.values):
        ax.text(x, y + 3, f"{y}", ha="center", color=COR_CAPES, fontsize=8)
    ax.set_title("Evolução 2021–2024", fontsize=10, loc="left", color="#5a5a5a")
    ax.set_xlabel("Ano")
    ax.set_ylabel("Publicações sobre IA/ML/DL")
    ax.set_xticks(range(ANO_MIN, ANO_MAX + 1))
    ax.legend(loc="upper left", frameon=False)

    for sp in ("top", "right"):
        ax.spines[sp].set_visible(False)

    def _painel_dot(ax, labels, vals, cor, titulo):
        dotplot(ax, list(labels), list(vals), cor)
        for s in ax.spines.values():
            s.set_visible(False)
        ax.tick_params(left=False)
        ax.set_title(titulo, fontsize=10, loc="left", color="#5a5a5a")

    # ----- (B) Distribuição por subcampo (dumbbell SciELO × CAPES) -----
    ax = axes[0, 1]
    labels = [l for _, l in SUBCAMPOS]
    sci_vals, cap_vals = [], []
    for col, _ in SUBCAMPOS:
        sci_vals.append(int(_bool(sci[col]).sum()) if col in sci.columns else 0)
        cap_vals.append(int(_bool(cap[col]).sum()) if col in cap.columns else 0)
    sci_pct = (np.array(sci_vals) / max(len(sci), 1) * 100).tolist()
    cap_pct = (np.array(cap_vals) / max(len(cap), 1) * 100).tolist()
    ordem = sorted(range(len(labels)), key=lambda i: (sci_pct[i] + cap_pct[i]) / 2)
    labs_b = [labels[i].replace(" & ", "\n& ").replace(" (", "\n(") for i in ordem]
    series = {"SciELO Human Sciences": [sci_pct[i] for i in ordem],
              "CAPES Humanas": [cap_pct[i] for i in ordem]}
    cores_b = {"SciELO Human Sciences": COR_SCIELO, "CAPES Humanas": COR_CAPES}
    dumbbell(ax, labs_b, series, cores_b)
    ax.tick_params(axis="y", labelsize=8)
    ax.set_title("Distribuição por subcampo (% do corpus de cada base)", fontsize=10,
                 loc="left", color="#5a5a5a")
    ax.legend(loc="lower right", frameon=False, fontsize=8)

    # ----- (C) Top periódicos SciELO -----
    top_per = sci["periodico"].fillna("(s/info)").value_counts().head(10).sort_values()
    labs_c = [t[:38] + "…" if len(t) > 38 else t for t in top_per.index]
    _painel_dot(axes[1, 0], labs_c, top_per.values, COR_SCIELO,
                "SciELO Human Sciences: top 10 periódicos")

    # ----- (D) Top áreas CAPES Humanas -----
    top_area = cap["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().head(10).sort_values()
    _painel_dot(axes[1, 1], list(top_area.index), top_area.values, COR_CAPES,
                "CAPES Humanas: top 10 áreas de conhecimento")

    out = os.path.join(FIGURAS_DIR, "comparativo_scielo_capes_2026.png")
    plt.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    plt.savefig(out.replace(".png", ".svg"), bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print(f"  → {out}")


def tabela_markdown(sci: pd.DataFrame, cap: pd.DataFrame,
                    sci_total: pd.DataFrame | None = None) -> None:
    """Gera tabelas comparativas em Markdown.

    - sci: SciELO Human Sciences puro (paridade com CAPES Humanas).
    - cap: CAPES grande área Ciências Humanas.
    - sci_total: SciELO Brasil completo (panorama; opcional, gera seção extra).
    """
    linhas = []
    linhas.append("# Tabelas comparativas SciELO × CAPES (2026)\n")
    linhas.append("Coleta atualizada em 22/05/2026. SciELO via API ArticleMeta com")
    linhas.append("universo Brasil completo (todas as 8 subject_areas); CAPES via dump oficial 2021-2024.")
    linhas.append("Classificação por regex de subcampos `utils.classificar_subcampos`,")
    linhas.append("com regras de co-ocorrência para `transformer` e para a sigla 'IA'.\n")
    linhas.append("**Recorte deste documento:** comparativo de paridade — SciELO restrito")
    linhas.append("a subject_area = 'Human Sciences' (puro, sem multidisciplinares ou")
    linhas.append("Applied Social Sciences) contra CAPES grande área Ciências Humanas.")
    linhas.append("Tabelas do panorama Brasil completo (referência) ao final.\n")

    # Sumário SciELO Human Sciences × CAPES Humanas
    linhas.append("## Sumário (2021–2024)\n")
    linhas.append("| Indicador | SciELO Human Sciences | CAPES Humanas |")
    linhas.append("|---|---:|---:|")
    linhas.append(f"| Total no campo | {len(sci):,} | {len(cap):,} |")
    sci_central = int((sci["FOCO_IA"] == "Tecnologias IA/ML/DL - Foco Central").sum())
    cap_central = int((cap["FOCO_IA"] == "Tecnologias IA/ML/DL - Foco Central").sum())
    linhas.append(f"| Foco Central | {sci_central} | {cap_central} |")
    linhas.append(f"| Correlatos | {len(sci)-sci_central} | {len(cap)-cap_central} |")

    # Subcampos
    linhas.append("\n## Distribuição por subcampo\n")
    linhas.append("| Subcampo | SciELO Human Sci. | % SciELO | CAPES | % CAPES |")
    linhas.append("|---|---:|---:|---:|---:|")
    for col, label in SUBCAMPOS:
        s = int(_bool(sci[col]).sum()) if col in sci.columns else 0
        c = int(_bool(cap[col]).sum()) if col in cap.columns else 0
        linhas.append(f"| {label} | {s} | {s/max(len(sci),1)*100:.1f}% | {c} | {c/max(len(cap),1)*100:.1f}% |")

    # Temporal
    linhas.append("\n## Evolução temporal\n")
    linhas.append("| Ano | SciELO Human Sci. | CAPES Humanas |")
    linhas.append("|---:|---:|---:|")
    for ano in range(ANO_MIN, ANO_MAX + 1):
        s = int((sci["ano"] == ano).sum())
        c = int((cap["AN_BASE"] == ano).sum())
        linhas.append(f"| {ano} | {s} | {c} |")

    # Top periódicos / top áreas
    linhas.append("\n## SciELO Human Sciences — top 10 periódicos\n")
    linhas.append("| Periódico | Artigos |")
    linhas.append("|---|---:|")
    for per, n in sci["periodico"].fillna("(s/info)").value_counts().head(10).items():
        linhas.append(f"| {per} | {n} |")

    linhas.append("\n## CAPES Humanas — top 10 áreas\n")
    linhas.append("| Área | Defesas |")
    linhas.append("|---|---:|")
    for area, n in cap["NM_AREA_CONHECIMENTO"].fillna("(s/info)").value_counts().head(10).items():
        linhas.append(f"| {area} | {n} |")

    # Seção opcional: panorama Brasil completo
    if sci_total is not None and len(sci_total):
        linhas.append("\n---\n")
        linhas.append("## Panorama de referência: SciELO Brasil completo (todas as áreas)\n")
        linhas.append(f"Para situar os {len(sci):,} artigos de Human Sciences puro no universo")
        linhas.append(f"mais amplo, segue o agregado do corpus IA/ML/DL no SciELO Brasil completo")
        linhas.append(f"(recorte estrito 2021–2024).\n")
        linhas.append(f"**Total SciELO Brasil 2021–2024:** {len(sci_total):,} artigos no campo,")
        sci_total_central = int((sci_total["FOCO_IA"] == "Tecnologias IA/ML/DL - Foco Central").sum())
        linhas.append(f"sendo {sci_total_central} Foco Central e {len(sci_total)-sci_total_central} Correlatos.\n")
        linhas.append("**Distribuição por subject_area primária:**\n")
        linhas.append("| Subject area | Artigos |")
        linhas.append("|---|---:|")
        def _sa(s):
            if pd.isna(s) or not s: return "(s/info)"
            parts = [p.strip() for p in str(s).split(";") if p.strip()]
            return parts[0] if len(parts) == 1 else "Multidisciplinar"
        sa_counts = sci_total["subject_areas_periodico"].map(_sa).value_counts()
        for sa, n in sa_counts.items():
            linhas.append(f"| {sa} | {n} |")

    out = "tabelas_comparativas_2026.md"
    with open(out, "w", encoding="utf-8") as f:
        f.write("\n".join(linhas) + "\n")
    print(f"  → {out}")


if __name__ == "__main__":
    print("Carregando SciELO ...")
    sci_total = carregar_scielo()
    sci_hs = carregar_scielo_human_sciences(sci_total)
    print("Carregando CAPES Humanas ...")
    cap = carregar_capes()
    # O comparativo "humanas × humanas" usa o subset estrito Human Sciences
    # do SciELO contra CAPES Humanas (paridade real).
    print("\nGerando comparativo (SciELO Human Sciences × CAPES Humanas):")
    fig_comparativa(sci_hs, cap)
    tabela_markdown(sci_hs, cap, sci_total=sci_total)
    print("\nPronto.")
