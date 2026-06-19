# -*- coding: utf-8 -*-
"""Mapa-múndi coroplético da penetração de IA nas Humanidades (OpenAlex).

Figura complementar a figuras_openalex.py, em script separado porque depende
de bibliotecas geográficas (geopandas, pycountry) que não são necessárias
para o restante do projeto.

Pré-requisito de dados:
    python analise_openalex.py --modo agregado --mailto SEU_EMAIL
    (gera dados_openalex/openalex_ia_humanas_por_pais_global.csv)

Pré-requisito de pacotes:
    pip install "geopandas<1.0" pycountry
    (a versão <1.0 traz o mapa-múndi naturalearth_lowres embutido, sem rede.)

Saída:
    figuras/openalex_09_mapa_taxa_interna.png

Uso:
    python figuras_openalex_mapa.py
"""

from __future__ import annotations

import os
import sys
import warnings

import pandas as pd
import matplotlib.pyplot as plt

try:
    import geopandas as gpd
    import pycountry
except ImportError as e:  # pragma: no cover
    sys.stderr.write(
        f"[erro] faltam pacotes: {e}. Instale com: "
        'pip install "geopandas<1.0" pycountry\n')
    raise SystemExit(1)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_OPENALEX_DIR = os.path.join(BASE_DIR, "dados_openalex")
FIGURAS_DIR = os.path.join(BASE_DIR, "figuras")

# Teto da escala de cor. A China (~16,9%) é outlier e achata o gradiente; o
# teto preserva contraste no grosso dos países (a barra indica "ou mais").
TETO_COR = 10.0

# naturalearth_lowres traz iso_a3 = "-99" para alguns países; corrigimos os
# relevantes por nome para não perdê-los no merge.
FIX_ISO_A3 = {
    "France": "FRA",
    "Norway": "NOR",
    "Kosovo": "XKX",
    "N. Cyprus": "CYP",
    "Somaliland": "SOM",
}

# Códigos alpha-2 que o pycountry não resolve direto.
ISO2_EXCECOES = {"XK": "XKX"}  # Kosovo


def iso2_para_iso3(code: str) -> str | None:
    code = str(code).strip().upper()
    if code in ISO2_EXCECOES:
        return ISO2_EXCECOES[code]
    pais = pycountry.countries.get(alpha_2=code)
    return pais.alpha_3 if pais else None


def main() -> None:
    caminho = os.path.join(DADOS_OPENALEX_DIR, "openalex_ia_humanas_por_pais_global.csv")
    if not os.path.isfile(caminho):
        sys.stderr.write(f"[erro] não encontrei {caminho}. Rode analise_openalex.py "
                         "--modo agregado antes.\n")
        raise SystemExit(1)

    df = pd.read_csv(caminho)
    df = df[df["pais_codigo"].astype(str).str.strip() != ""].copy()
    df["iso3"] = df["pais_codigo"].map(iso2_para_iso3)
    nao_resolvidos = df[df["iso3"].isna()]["pais_codigo"].tolist()
    if nao_resolvidos:
        sys.stderr.write(f"[aviso] códigos não convertidos (fora do mapa): {nao_resolvidos}\n")
    df = df.dropna(subset=["iso3"])

    with warnings.catch_warnings():
        warnings.simplefilter("ignore")  # silencia o FutureWarning de gpd.datasets
        world = gpd.read_file(gpd.datasets.get_path("naturalearth_lowres"))
    world = world[world["name"] != "Antarctica"].copy()
    mask = world["name"].isin(FIX_ISO_A3)
    world.loc[mask, "iso_a3"] = world.loc[mask, "name"].map(FIX_ISO_A3)

    merged = world.merge(
        df[["iso3", "pais", "taxa_interna_%", "count_ia_hum"]],
        left_on="iso_a3", right_on="iso3", how="left",
    )

    fig, ax = plt.subplots(figsize=(14, 7))
    merged.plot(
        ax=ax,
        column="taxa_interna_%",
        cmap="YlOrRd",
        vmin=0, vmax=TETO_COR,
        edgecolor="white", linewidth=0.3,
        legend=True,
        legend_kwds={
            "label": "Taxa interna (%) — % das Humanidades que tocam IA",
            "shrink": 0.5, "orientation": "horizontal", "pad": 0.02,
        },
        missing_kwds={"color": "#ECECEC", "label": "Sem dados"},
    )
    ax.set_axis_off()

    # Sem título embutido: a figura é identificada pelo nome do arquivo (PNG + SVG).
    os.makedirs(FIGURAS_DIR, exist_ok=True)
    base = os.path.join(FIGURAS_DIR, "openalex_09_mapa_taxa_interna")
    out = base + ".png"
    fig.savefig(out, dpi=300, bbox_inches="tight", facecolor="white")
    fig.savefig(base + ".svg", bbox_inches="tight", facecolor="white")
    plt.close(fig)
    n = merged["taxa_interna_%"].notna().sum()
    print(f"  -> {out}  ({n} países com dados no mapa)")


if __name__ == "__main__":
    main()
