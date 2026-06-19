# -*- coding: utf-8 -*-
"""
Geração dos gráficos da análise bibliométrica a partir dos dados reais
contidos em dados_capes/resultados_detalhados_capes.xlsx e
dados_scielo/resultados_detalhados_scielo.xlsx.

Salva todas as figuras em PNG na pasta `figuras/`.
"""

import os
import pandas as pd
import matplotlib.pyplot as plt

from utils import (
    FIGURAS_DIR,
    CORES_INTERMEDIARIAS,
    aplicar_estilo_padrao,
    garantir_diretorio,
)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FIG_DIR = garantir_diretorio(FIGURAS_DIR)
CAPES_XLSX = os.path.join(BASE_DIR, 'dados_capes', 'resultados_detalhados_capes.xlsx')
SCIELO_XLSX = os.path.join(BASE_DIR, 'dados_scielo', 'resultados_detalhados_scielo.xlsx')

# Estilo único do projeto (defaults do matplotlib + paleta tab10-muted).
aplicar_estilo_padrao()

# Cores de papel — todas dentro da paleta padrão (utils.CORES_INTERMEDIARIAS),
# sem esquemas roxo/verde próprios nem gradientes arco-íris.
COR_PRINCIPAL = CORES_INTERMEDIARIAS[3]   # azul: barras/linhas principais
COR_REALCE = CORES_INTERMEDIARIAS[0]      # vermelho: realce (máximo, mediana)
COR_NEUTRA = CORES_INTERMEDIARIAS[10]     # cinza claro
COR_AZUL = CORES_INTERMEDIARIAS[3]
COR_MESTRADO = CORES_INTERMEDIARIAS[3]
COR_DOUTORADO = CORES_INTERMEDIARIAS[1]
COR_IA_CENTRAL = CORES_INTERMEDIARIAS[0]
COR_IA_REL = CORES_INTERMEDIARIAS[1]
COR_IA_OUTROS = CORES_INTERMEDIARIAS[9]
COR_MEDIANA = CORES_INTERMEDIARIAS[0]


def salvar(nome):
    if nome.startswith('capes'):
        titulo = 'CAPES'
    elif nome.startswith('scielo'):
        titulo = 'SciELO'
    else:
        titulo = None
    if titulo:
        plt.gca().set_title(titulo, fontsize=14, fontweight='bold', pad=15)
    plt.tight_layout()
    plt.savefig(os.path.join(FIG_DIR, nome), dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  ✓ {nome}")


# =============================================================================
# CARREGAR DADOS
# =============================================================================
print("=" * 70)
print("Carregando dados reais dos arquivos xlsx")
print("=" * 70)

capes_pub = pd.read_excel(CAPES_XLSX, sheet_name='Publicações por Ano')
capes_areas = pd.read_excel(CAPES_XLSX, sheet_name='Todas as Áreas')
capes_inst = pd.read_excel(CAPES_XLSX, sheet_name='Todas as Instituições')
capes_foco = pd.read_excel(CAPES_XLSX, sheet_name='Foco em IA')
capes_termos = pd.read_excel(CAPES_XLSX, sheet_name='Top Termos')
capes_dataset = pd.read_excel(CAPES_XLSX, sheet_name='Dataset Completo')

scielo_pub = pd.read_excel(SCIELO_XLSX, sheet_name='Publicações por Ano')
scielo_per = pd.read_excel(SCIELO_XLSX, sheet_name='Periódicos')
scielo_tipo = pd.read_excel(SCIELO_XLSX, sheet_name='Tipo de Literatura')
scielo_cit = pd.read_excel(SCIELO_XLSX, sheet_name='Citável vs Não Citável')

total_capes = len(capes_dataset)
total_scielo = scielo_pub['quantidade'].sum()

print(f"CAPES: {total_capes} teses/dissertações")
print(f"SciELO: {total_scielo} artigos")

# =============================================================================
# CAPES
# =============================================================================
print("\n[CAPES]")

anos = capes_pub['ano_defesa'].astype(int).tolist()
qtd = capes_pub['quantidade'].astype(int).tolist()

# 01a — Temporal barras simples
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(anos, qtd, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
for b, v in zip(bars, qtd):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.set_xticks(anos)
ax.grid(True, alpha=0.3, axis='y', linestyle='--'); ax.set_axisbelow(True)
salvar('capes_01a_temporal_barras_simples.png')

# 01b — Barras com destaque
fig, ax = plt.subplots(figsize=(12, 7))
bars = ax.bar(anos, qtd, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
idx_max = qtd.index(max(qtd))
bars[idx_max].set_color(COR_REALCE); bars[idx_max].set_alpha(1.0)
for b, v in zip(bars, qtd):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.set_xticks(anos)
ax.grid(True, alpha=0.3, axis='y', linestyle='--'); ax.set_axisbelow(True)
salvar('capes_01b_temporal_barras_destaque.png')

# 01c — Linha simples
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(anos, qtd, marker='o', linewidth=3, markersize=9, color=COR_PRINCIPAL,
        markerfacecolor=COR_REALCE, markeredgecolor='black', markeredgewidth=1.5)
for x, y in zip(anos, qtd):
    ax.text(x, y + max(qtd) * 0.02, str(y), ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.set_xticks(anos)
ax.grid(True, alpha=0.3, linestyle='--')
salvar('capes_01c_temporal_linha_simples.png')

# 01d — Linha com área
fig, ax = plt.subplots(figsize=(12, 7))
ax.plot(anos, qtd, marker='o', linewidth=3, markersize=9, color=COR_PRINCIPAL,
        markerfacecolor=COR_REALCE, markeredgecolor='black', markeredgewidth=1.5, label='Publicações')
ax.fill_between(anos, qtd, alpha=0.3, color=COR_PRINCIPAL)
for x, y in zip(anos, qtd):
    ax.text(x, y + max(qtd) * 0.02, str(y), ha='center', va='bottom', fontweight='bold', fontsize=10)
ax.set_xlabel('Ano de Defesa'); ax.set_ylabel('Quantidade de Publicações')
ax.set_xticks(anos)
ax.grid(True, alpha=0.3, linestyle='--'); ax.legend(loc='upper left')
salvar('capes_01d_temporal_linha_area.png')

# 02 — Nível acadêmico
nivel_counts = capes_dataset['nivel'].value_counts()
fig, ax = plt.subplots(figsize=(10, 7))
labels = nivel_counts.index.tolist(); vals = nivel_counts.values.tolist()
cores_n = [COR_MESTRADO, COR_DOUTORADO][:len(labels)]
bars = ax.bar(labels, vals, color=cores_n, edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    pct = v / total_capes * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=11)
ax.set_ylabel('Quantidade'); ax.grid(True, alpha=0.3, axis='y', linestyle='--')
salvar('capes_02_nivel_academico.png')

# 03 — Áreas com 2+ publicações
areas_2 = capes_areas[capes_areas['Quantidade'] > 1].sort_values('Quantidade', ascending=False)
areas_1 = capes_areas[capes_areas['Quantidade'] == 1]
N = len(areas_2)
fig, ax = plt.subplots(figsize=(14, max(8, N * 0.5)))
bars = ax.barh(range(N), areas_2['Quantidade'].values, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.2)
ax.set_yticks(range(N))
ax.set_yticklabels(areas_2['area_normalizada'].values, fontsize=9)
ax.invert_yaxis()
for b, v in zip(bars, areas_2['Quantidade'].values):
    pct = v / total_capes * 100
    ax.text(v + 0.15, b.get_y() + b.get_height() / 2, f'{int(v)} ({pct:.1f}%)',
            va='center', fontweight='bold', fontsize=9)
ax.set_xlabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
nota = f'* Áreas com 1 publicação: {len(areas_1)} categorias adicionais'
fig.text(0.12, 0.02, nota, fontsize=8, style='italic',
         bbox=dict(boxstyle='round', facecolor=CORES_INTERMEDIARIAS[5], alpha=0.6))
plt.subplots_adjust(bottom=0.08)
salvar('capes_03_todas_areas.png')

# 04 — Foco em IA
foco_order = ['IA - Foco Central', 'IA - Foco Relacionado', 'Outros Temas']
foco_dict = dict(zip(capes_foco['foco_ia'], capes_foco['Quantidade']))
foco_vals = [foco_dict.get(k, 0) for k in foco_order]
fig, ax = plt.subplots(figsize=(11, 7))
cores_foco = [COR_IA_CENTRAL, COR_IA_REL, COR_IA_OUTROS]
bars = ax.bar(foco_order, foco_vals, color=cores_foco, edgecolor='black', linewidth=1.5)
for b, v in zip(bars, foco_vals):
    pct = v / total_capes * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=11)
ax.set_ylabel('Quantidade'); ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.xticks(rotation=15, ha='right')
salvar('capes_04_foco_ia.png')

# 05 — Top 15 instituições
top_inst = capes_inst.head(15)
N = len(top_inst)
fig, ax = plt.subplots(figsize=(14, max(8, N * 0.45)))
bars = ax.barh(range(N), top_inst['Quantidade'].values, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.2)
ax.set_yticks(range(N))
ax.set_yticklabels(top_inst['instituicao'].values, fontsize=9)
ax.invert_yaxis()
for b, v in zip(bars, top_inst['Quantidade'].values):
    pct = v / total_capes * 100
    ax.text(v + 0.1, b.get_y() + b.get_height() / 2, f'{int(v)} ({pct:.1f}%)',
            va='center', fontweight='bold', fontsize=9)
ax.set_xlabel('Quantidade de Publicações')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
salvar('capes_05_top_instituicoes.png')

# 06 — Evolução por nível
nivel_ano = capes_dataset.groupby(['ano_defesa', 'nivel']).size().unstack(fill_value=0)
fig, ax = plt.subplots(figsize=(12, 7))
cores_n = {'Mestrado': COR_MESTRADO, 'Doutorado': COR_DOUTORADO}
for nivel in ['Mestrado', 'Doutorado']:
    if nivel in nivel_ano.columns:
        ax.plot(nivel_ano.index, nivel_ano[nivel], marker='o', label=nivel,
                linewidth=3, color=cores_n[nivel], markersize=10,
                markeredgecolor='black', markeredgewidth=1)
ax.set_xlabel('Ano'); ax.set_ylabel('Publicações')
ax.set_xticks(nivel_ano.index)
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
salvar('capes_06_evolucao_nivel.png')

# 07 — Distribuição de páginas
paginas = pd.to_numeric(capes_dataset['num_paginas'], errors='coerce').dropna()
if len(paginas) > 0:
    fig, ax = plt.subplots(figsize=(12, 7))
    ax.hist(paginas, bins=25, color=COR_AZUL, edgecolor='black', alpha=0.85, linewidth=1.5)
    mediana = paginas.median()
    ax.axvline(mediana, color=COR_MEDIANA, linestyle='--', linewidth=3,
               label=f'Mediana: {mediana:.0f} páginas')
    ax.set_xlabel('Número de Páginas'); ax.set_ylabel('Frequência')
    ax.legend(loc='upper right')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    salvar('capes_07_distribuicao_paginas.png')

# 08 — Top 10 cidades
if 'cidade' in capes_dataset.columns:
    cidades = capes_dataset['cidade'].fillna('NÃO ESPECIFICADA').value_counts().head(10)
    N = len(cidades)
    fig, ax = plt.subplots(figsize=(12, 7))
    bars = ax.barh(range(N), cidades.values, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5)
    ax.set_yticks(range(N))
    ax.set_yticklabels(cidades.index, fontsize=10)
    ax.invert_yaxis()
    for b, v in zip(bars, cidades.values):
        pct = v / total_capes * 100
        ax.text(v + 0.1, b.get_y() + b.get_height() / 2, f'{int(v)} ({pct:.1f}%)',
                va='center', fontweight='bold', fontsize=10)
    ax.set_xlabel('Quantidade de Publicações')
    ax.grid(True, alpha=0.3, axis='x', linestyle='--')
    salvar('capes_08_top10_cidades.png')

# 09 — Top termos
fig, ax = plt.subplots(figsize=(12, 8))
top_termos = capes_termos.head(15)
N = len(top_termos)
bars = ax.barh(range(N), top_termos['Frequência'].values, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.2)
ax.set_yticks(range(N))
ax.set_yticklabels(top_termos['Termo'].values, fontsize=10)
ax.invert_yaxis()
for b, v in zip(bars, top_termos['Frequência'].values):
    ax.text(v + 0.3, b.get_y() + b.get_height() / 2, str(int(v)),
            va='center', fontweight='bold', fontsize=10)
ax.set_xlabel('Frequência')
ax.grid(True, alpha=0.3, axis='x', linestyle='--')
salvar('capes_09_top_termos.png')

# 10 — Evolução das top 3 áreas
top3_areas_nomes = capes_areas.head(3)['area_normalizada'].tolist()
fig, ax = plt.subplots(figsize=(12, 7))
cores_top3 = [CORES_INTERMEDIARIAS[0], CORES_INTERMEDIARIAS[1], CORES_INTERMEDIARIAS[2]]
for i, area in enumerate(top3_areas_nomes):
    evol = capes_dataset[capes_dataset['area_normalizada'] == area].groupby('ano_defesa').size()
    if len(evol) > 0:
        ax.plot(evol.index, evol.values, marker='o', label=area,
                linewidth=3, color=cores_top3[i], markersize=10,
                markeredgecolor='black', markeredgewidth=1)
ax.set_xlabel('Ano'); ax.set_ylabel('Publicações')
ax.legend(loc='upper left')
ax.grid(True, alpha=0.3, linestyle='--')
salvar('capes_10_evolucao_top3_areas.png')

# =============================================================================
# SCIELO
# =============================================================================
print("\n[SciELO]")

anos_s = scielo_pub['ano_publicacao'].astype(int).tolist()
qtd_s = scielo_pub['quantidade'].astype(int).tolist()

# 01a — Barras simples
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(anos_s, qtd_s, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
for b, v in zip(bars, qtd_s):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(anos_s, rotation=45, ha='right')
salvar('scielo_01a_temporal_barras_simples.png')

# 01b — Barras com destaque
fig, ax = plt.subplots(figsize=(16, 8))
bars = ax.bar(anos_s, qtd_s, color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
idx_max = qtd_s.index(max(qtd_s))
bars[idx_max].set_color(COR_REALCE); bars[idx_max].set_alpha(1.0)
for b, v in zip(bars, qtd_s):
    ax.text(b.get_x() + b.get_width() / 2, b.get_height(), str(v),
            ha='center', va='bottom', fontweight='bold', fontsize=9)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(axis='y', alpha=0.3, linestyle='--'); ax.set_axisbelow(True)
ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(anos_s, rotation=45, ha='right')
salvar('scielo_01b_temporal_barras_destaque.png')

# 01c — Linha simples
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(anos_s, qtd_s, marker='o', linewidth=3, markersize=9,
        color=COR_PRINCIPAL, markerfacecolor=COR_REALCE, markeredgecolor='black', markeredgewidth=1.5)
for x, y in zip(anos_s, qtd_s):
    ax.text(x, y + max(qtd_s) * 0.02, str(y), ha='center', va='bottom',
            fontweight='bold', fontsize=9)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--'); ax.set_ylim(0, max(qtd_s) * 1.15)
plt.xticks(anos_s, rotation=45, ha='right')
salvar('scielo_01c_temporal_linha_simples.png')

# 01d — Linha com área
fig, ax = plt.subplots(figsize=(16, 8))
ax.plot(anos_s, qtd_s, marker='o', linewidth=3, markersize=9,
        color=COR_PRINCIPAL, markerfacecolor=COR_REALCE, markeredgecolor='black',
        markeredgewidth=1.5, label='Publicações')
ax.fill_between(anos_s, qtd_s, alpha=0.3, color=COR_PRINCIPAL)
for x, y in zip(anos_s, qtd_s):
    ax.text(x, y + max(qtd_s) * 0.02, str(y), ha='center', va='bottom',
            fontweight='bold', fontsize=9)
ax.set_xlabel('Ano', fontweight='bold'); ax.set_ylabel('Número de Artigos', fontweight='bold')
ax.grid(True, alpha=0.3, linestyle='--'); ax.set_ylim(0, max(qtd_s) * 1.15)
ax.legend(loc='upper left')
plt.xticks(anos_s, rotation=45, ha='right')
salvar('scielo_01d_temporal_linha_area.png')

# 02 — Top 15 periódicos
top_per = scielo_per.head(15)
N = len(top_per)
fig, ax = plt.subplots(figsize=(14, max(9, N * 0.5)))
bars = ax.barh(range(N), top_per['quantidade'].values, color=COR_PRINCIPAL,
               edgecolor='black', linewidth=1.5, alpha=0.9)
bars[0].set_color(COR_REALCE); bars[0].set_linewidth(2.5)
nomes = [n.replace('&amp;', '&') for n in top_per['periodico'].values]
nomes = [n if len(n) <= 60 else n[:57] + '...' for n in nomes]
for i, (b, v) in enumerate(zip(bars, top_per['quantidade'].values)):
    pct = v / total_scielo * 100
    ax.text(v + 0.2, i, f'{int(v)} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=11)
ax.set_yticks(range(N))
ax.set_yticklabels(nomes, fontsize=10)
ax.invert_yaxis()
ax.set_xlabel('Número de Artigos', fontweight='bold')
ax.grid(axis='x', alpha=0.3, linestyle='--')
ax.set_xlim(0, max(top_per['quantidade'].values) * 1.18)
salvar('scielo_02_top_periodicos.png')

# 03 — Periódicos menos frequentes (com 2 artigos)
outros_per = scielo_per.iloc[15:]
outros_2 = outros_per[outros_per['quantidade'] >= 2]
if len(outros_2) > 0:
    N = len(outros_2)
    fig, ax = plt.subplots(figsize=(14, max(8, N * 0.4)))
    bars = ax.barh(range(N), outros_2['quantidade'].values, color=COR_PRINCIPAL,
                   edgecolor='black', linewidth=1.5, alpha=0.9)
    nomes_o = [n.replace('&amp;', '&') for n in outros_2['periodico'].values]
    nomes_o = [n if len(n) <= 60 else n[:57] + '...' for n in nomes_o]
    for i, (b, v) in enumerate(zip(bars, outros_2['quantidade'].values)):
        pct = v / total_scielo * 100
        ax.text(v + 0.05, i, f'{int(v)} ({pct:.1f}%)', va='center', fontweight='bold', fontsize=10)
    ax.set_yticks(range(N))
    ax.set_yticklabels(nomes_o, fontsize=10)
    ax.invert_yaxis()
    ax.set_xlabel('Número de Artigos', fontweight='bold')
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_xlim(0, max(outros_2['quantidade'].values) * 1.25)
    salvar('scielo_03_outros_periodicos.png')

# 04 — Citável vs Não citável
fig, ax = plt.subplots(figsize=(10, 8))
labels = scielo_cit['categoria'].tolist(); sizes = scielo_cit['quantidade'].tolist()
cores_pie = [CORES_INTERMEDIARIAS[3], CORES_INTERMEDIARIAS[0]]
wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=cores_pie,
                                   startangle=90, explode=(0.05, 0.05),
                                   textprops={'fontsize': 13, 'fontweight': 'bold'})
for at in autotexts:
    at.set_color('white'); at.set_fontsize(14)
for t, s in zip(texts, sizes):
    t.set_text(f'{t.get_text()}\n({s} docs)')
salvar('scielo_04_citavel.png')

# 05 — Tipo de literatura
fig, ax = plt.subplots(figsize=(11, 7))
labels = scielo_tipo['tipo_literatura'].tolist()
vals = scielo_tipo['quantidade'].tolist()
cores_lit = CORES_INTERMEDIARIAS[:len(labels)]
bars = ax.bar(labels, vals, color=cores_lit, edgecolor='black', linewidth=1.5)
for b, v in zip(bars, vals):
    pct = v / sum(vals) * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 0.5, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=11)
ax.set_ylabel('Quantidade')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
plt.xticks(rotation=20, ha='right')
salvar('scielo_05_tipo_literatura.png')

# 06 — Resumo combinado (boxplot ou comparativo)
fig, ax = plt.subplots(figsize=(12, 7))
recentes = scielo_pub[scielo_pub['ano_publicacao'] >= 2020]['quantidade'].sum()
antigos = scielo_pub[scielo_pub['ano_publicacao'] < 2020]['quantidade'].sum()
labels = ['Antes de 2020', '2020 em diante']
vals = [antigos, recentes]
cores_c = [COR_NEUTRA, COR_PRINCIPAL]
bars = ax.bar(labels, vals, color=cores_c, edgecolor='black', linewidth=2)
for b, v in zip(bars, vals):
    pct = v / total_scielo * 100
    ax.text(b.get_x() + b.get_width() / 2, v + 1, f'{v}\n({pct:.1f}%)',
            ha='center', fontweight='bold', fontsize=14)
ax.set_ylabel('Número de Artigos')
ax.grid(True, alpha=0.3, axis='y', linestyle='--')
salvar('scielo_06_concentracao_temporal.png')

print("\n" + "=" * 70)
print(f"✅ Gráficos gerados em: {FIG_DIR}")
print("=" * 70)
