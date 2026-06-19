# -*- coding: utf-8 -*-
"""
Análise completa - Catálogo de Teses CAPES sobre Inteligência Artificial.

Lê o catálogo de teses/dissertações da CAPES (xlsx ou csv em `dados_capes/`),
classifica os trabalhos por foco em IA, gera estatísticas descritivas e
salva gráficos em `figuras/` e planilha consolidada em `dados_capes/`.

Uso:
    python analise_capes.py

Requisitos: ver requirements.txt
"""

import os
import sys
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

from utils import (
    BASE_DIR,
    CORES_INTERMEDIARIAS,
    DADOS_CAPES_DIR,
    FIGURAS_DIR,
    STOPWORDS_PT,
    aplicar_estilo_padrao,
    classificar_foco_ia,
    garantir_diretorio,
    buscar_arquivo,
)

aplicar_estilo_padrao()
garantir_diretorio(FIGURAS_DIR)

# Cores específicas
COR_AZUL_PRINCIPAL = CORES_INTERMEDIARIAS[3]
COR_MESTRADO = CORES_INTERMEDIARIAS[3]
COR_DOUTORADO = CORES_INTERMEDIARIAS[1]
COR_MEDIANA = CORES_INTERMEDIARIAS[0]
COR_IA_CENTRAL = CORES_INTERMEDIARIAS[0]
COR_IA_RELACIONADA = CORES_INTERMEDIARIAS[1]
COR_IA_OUTROS = CORES_INTERMEDIARIAS[3]
CORES_TOP3 = [CORES_INTERMEDIARIAS[0], CORES_INTERMEDIARIAS[1], CORES_INTERMEDIARIAS[2]]

def gerar_paleta_expandida(n):
    """Gera uma paleta de cores intermediárias harmoniosas para n itens"""
    if n <= len(CORES_INTERMEDIARIAS):
        return CORES_INTERMEDIARIAS[:n]
    
    paleta = CORES_INTERMEDIARIAS.copy()
    cores_extras = sns.color_palette("tab10", n - len(paleta))
    
    def mute_color(rgb_tuple):
        r, g, b = [int(c * 255) for c in rgb_tuple]
        r_muted = (r + 224) // 2 
        g_muted = (g + 224) // 2
        b_muted = (b + 224) // 2
        return '#{:02x}{:02x}{:02x}'.format(r_muted, g_muted, b_muted)

    for cor in cores_extras:
        paleta.append(mute_color(cor))
    
    return paleta[:n]

print("="*80)
print("ANÁLISE DO CATÁLOGO DE TESES CAPES - INTELIGÊNCIA ARTIFICIAL")
print("="*80)

# =============================================================================
# 1. CARREGAR DADOS
# =============================================================================
print("\n[1/10] Carregando dados...")

arquivos_possiveis = [
    'catalogo_teses_analise.xlsx',
    'catalogo_teses_analise__2_.xlsx',
    'catalogo_teses_limpo__2_.csv',
    'catalogodeteses__4_.csv',
]

# Busca em dados_capes/ (preferencial) e no diretório do script (compatibilidade).
arquivo_dados = buscar_arquivo(arquivos_possiveis, DADOS_CAPES_DIR, BASE_DIR)

if arquivo_dados is None:
    print("\n[ERRO] Nenhum arquivo de dados encontrado.")
    print(f"   Diretórios consultados: {DADOS_CAPES_DIR}, {BASE_DIR}")
    print(f"   Arquivos esperados: {arquivos_possiveis}")
    sys.exit(1)

try:
    if arquivo_dados.endswith('.xlsx'):
        df = pd.read_excel(arquivo_dados, sheet_name='Dados Completos')
    else:
        df = pd.read_csv(arquivo_dados)
    print(f"✓ Arquivo carregado: {arquivo_dados}")
except Exception as e:
    print(f"[ERRO] Ao carregar arquivo: {e}")
    sys.exit(1)

# Verificar colunas necessárias
colunas_necessarias = ['titulo', 'autor', 'ano_defesa', 'nivel', 'area', 'instituicao']
colunas_faltantes = [col for col in colunas_necessarias if col not in df.columns]

if colunas_faltantes:
    print(f"\n[ERRO] Colunas faltantes no dataset: {colunas_faltantes}")
    print(f"   Colunas disponíveis: {list(df.columns)}")
    sys.exit(1)

# Limpeza inicial
if 'id' in df.columns:
    df = df[df['id'] != 'col-md-1'].copy()

df = df[df['titulo'].notna()].copy()
df = df[df['autor'].notna()].copy()

# Normalização
df['area_normalizada'] = df['area'].fillna('NÃO ESPECIFICADA').str.upper().str.strip()
df['ano_defesa'] = pd.to_numeric(df['ano_defesa'], errors='coerce')
df = df[df['ano_defesa'].notna()].copy()  # Remover registros sem ano
df['ano_defesa'] = df['ano_defesa'].astype(int)
df['decada'] = (df['ano_defesa'] // 10 * 10)

# Tratar cidade se existir
if 'cidade' in df.columns:
    df['cidade'] = df['cidade'].fillna('NÃO ESPECIFICADA')
else:
    df['cidade'] = 'NÃO ESPECIFICADA'

# Tratar páginas se existir
if 'num_paginas' in df.columns:
    df['num_paginas'] = pd.to_numeric(df['num_paginas'], errors='coerce')
else:
    df['num_paginas'] = np.nan

print(f"✓ {len(df)} publicações carregadas")
print(f"✓ Período: {df['ano_defesa'].min()}-{df['ano_defesa'].max()}")

# =============================================================================
# 2. CLASSIFICAÇÃO POR FOCO EM IA
# =============================================================================
print("\n[2/10] Classificando por foco em IA...")

# Classificação via utils.classificar_foco_ia (regex com word boundaries).
# Inclui resumo quando a coluna existe, para reduzir o erro de classificar
# apenas pelo título.
def _texto_para_classificacao(row):
    partes = [str(row.get('titulo', '') or '')]
    if 'resumo' in row.index and pd.notna(row.get('resumo')):
        partes.append(str(row['resumo']))
    if 'palavras_chave' in row.index and pd.notna(row.get('palavras_chave')):
        partes.append(str(row['palavras_chave']))
    return ' '.join(partes)

df['foco_ia'] = df.apply(lambda r: classificar_foco_ia(_texto_para_classificacao(r)), axis=1)
foco_counts = df['foco_ia'].value_counts()

print("✓ Classificação concluída:")
for foco, count in foco_counts.items():
    print(f"  - {foco}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 3. ANÁLISE TEMPORAL
# =============================================================================
print("\n[3/10] Analisando tendências temporais...")

pub_por_ano = df.groupby('ano_defesa').size().reset_index(name='quantidade')
pub_por_ano = pub_por_ano.sort_values('ano_defesa').reset_index(drop=True)

anos_recentes = pub_por_ano[pub_por_ano['ano_defesa'] >= 2020]['quantidade'].sum()

# Crescimento bruto (sensível a denominador pequeno — reportado junto com CAGR).
if len(pub_por_ano) > 1:
    base = pub_por_ano.iloc[0]['quantidade']
    fim = pub_por_ano.iloc[-1]['quantidade']
    n_anos = pub_por_ano.iloc[-1]['ano_defesa'] - pub_por_ano.iloc[0]['ano_defesa']
    crescimento = (fim - base) / base * 100 if base else float('nan')
    # CAGR: taxa anual composta. Menos enganosa quando a base é pequena.
    cagr = ((fim / base) ** (1 / n_anos) - 1) * 100 if base and n_anos > 0 else float('nan')
    print(f"✓ Crescimento bruto: {crescimento:.0f}% "
          f"({pub_por_ano.iloc[0]['ano_defesa']}→{pub_por_ano.iloc[-1]['ano_defesa']})")
    print(f"✓ CAGR (crescimento anual composto): {cagr:.1f}% a.a.")
else:
    crescimento = 0
    cagr = float('nan')
    print("✓ Dados insuficientes para calcular crescimento")

# Média móvel de 3 anos suaviza picos pontuais em uma série pequena.
pub_por_ano['media_movel_3a'] = pub_por_ano['quantidade'].rolling(3, min_periods=1).mean()

print(f"✓ Últimos 3 anos: {anos_recentes} publicações ({anos_recentes/len(df)*100:.1f}%)")

# =============================================================================
# 4. ANÁLISE POR NÍVEL
# =============================================================================
print("\n[4/10] Analisando nível acadêmico...")

nivel_counts = df['nivel'].value_counts()
nivel_ano = df.groupby(['ano_defesa', 'nivel']).size().unstack(fill_value=0)

print(f"✓ Mestrados: {nivel_counts.get('Mestrado', 0)} ({nivel_counts.get('Mestrado', 0)/len(df)*100:.1f}%)")
print(f"✓ Doutorados: {nivel_counts.get('Doutorado', 0)} ({nivel_counts.get('Doutorado', 0)/len(df)*100:.1f}%)")

# =============================================================================
# 5. ANÁLISE DE ÁREAS (TODAS)
# =============================================================================
print("\n[5/10] Analisando todas as áreas temáticas...")

area_counts = df['area_normalizada'].value_counts()
areas_freq_maior_1 = area_counts[area_counts > 1].sort_values(ascending=False) 
areas_freq_1 = area_counts[area_counts == 1]

print(f"✓ Total de áreas: {len(area_counts)}")
print(f"✓ Áreas com 2+ publicações: {len(areas_freq_maior_1)}")
print(f"✓ Áreas com 1 publicação: {len(areas_freq_1)}")
if len(area_counts) >= 3:
    print(f"✓ Top 3 áreas:")
    for i, (area, count) in enumerate(area_counts.head(3).items(), 1):
        print(f"  {i}. {area}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 6. ANÁLISE DE INSTITUIÇÕES (TODAS)
# =============================================================================
print("\n[6/10] Analisando todas as instituições...")

inst_counts = df['instituicao'].value_counts()
inst_freq_maior_1 = inst_counts[inst_counts > 1].sort_values(ascending=False)
inst_freq_1 = inst_counts[inst_counts == 1]

print(f"✓ Total de instituições: {len(inst_counts)}")
print(f"✓ Instituições com 2+ publicações: {len(inst_freq_maior_1)}")
print(f"✓ Instituições com 1 publicação: {len(inst_freq_1)}")
if len(inst_counts) >= 3:
    print(f"✓ Top 3 instituições:")
    for i, (inst, count) in enumerate(inst_counts.head(3).items(), 1):
        print(f"  {i}. {inst}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 7. ANÁLISE DE CIDADES
# =============================================================================
print("\n[7/10] Analisando distribuição por cidades...")

cidade_counts = df['cidade'].value_counts()
print("✓ Top 5 cidades:")
for i, (cidade, count) in enumerate(cidade_counts.head(5).items(), 1):
    print(f"  {i}. {cidade}: {count} ({count/len(df)*100:.1f}%)")

# =============================================================================
# 8. ANÁLISE DE TERMOS FREQUENTES
# =============================================================================
print("\n[8/10] Extraindo termos mais frequentes...")

import re as _re
import unicodedata as _ud

def _normalizar(texto):
    """Lowercase + remove pontuação; mantém acentos para casar stopwords."""
    if pd.isna(texto):
        return []
    t = str(texto).lower()
    # Remove pontuação básica
    t = _re.sub(r'[^\w\sáàâãéêíóôõúüçñ-]', ' ', t, flags=_re.UNICODE)
    return [p for p in t.split() if len(p) > 3 and p not in STOPWORDS_PT]

def extrair_termos(texto):
    """Tokens unigrama relevantes."""
    return _normalizar(texto)

def extrair_bigrams(texto):
    """Bigrams (pares de palavras consecutivas) — captura 'redes neurais',
    'aprendizado de máquina' etc., que se perdem em análises unigrama."""
    tokens = _normalizar(texto)
    return [f"{a} {b}" for a, b in zip(tokens, tokens[1:])]

todos_termos = []
todos_bigrams = []
for titulo in df['titulo'].dropna():
    todos_termos.extend(extrair_termos(titulo))
    todos_bigrams.extend(extrair_bigrams(titulo))

termo_freq = Counter(todos_termos)
bigram_freq = Counter(todos_bigrams)
top_termos = termo_freq.most_common(20)
top_bigrams = bigram_freq.most_common(20)

if top_termos:
    print(f"✓ Top 5 termos: {', '.join([t[0] for t in top_termos[:5]])}")
if top_bigrams:
    print(f"✓ Top 5 bigrams: {', '.join([b[0] for b in top_bigrams[:5]])}")

# =============================================================================
# 9. ANÁLISE DE PÁGINAS
# =============================================================================
print("\n[9/10] Analisando número de páginas...")

if df['num_paginas'].notna().sum() > 0:
    paginas_stats = df['num_paginas'].describe()
    print(f"✓ Média: {paginas_stats['mean']:.0f} páginas")
    print(f"✓ Mediana: {paginas_stats['50%']:.0f} páginas")
else:
    print("✓ Dados de páginas não disponíveis")

# =============================================================================
# 10. CRIAR PASTA PARA GRÁFICOS
# =============================================================================
print("\n[10/10] Preparando geração de gráficos...")
print(f"✓ Diretório de saída: {FIGURAS_DIR}")

# =============================================================================
# 11. GERAR GRÁFICOS
# =============================================================================
print("\n" + "="*80)
print("GERANDO GRÁFICOS COM CORES INTERMEDIÁRIAS E GRADIENTES")
print("="*80)

# GRÁFICO 1: Evolução Temporal - 4 VERSÕES PADRONIZADAS
print("\n📊 Gráfico 1/9: Evolução Temporal das Publicações (4 versões)")

# Cores principais (paleta tab10-muted do projeto, em utils.CORES_INTERMEDIARIAS)
COR_PRINCIPAL = CORES_INTERMEDIARIAS[3]  # azul: barras/linhas principais
COR_REALCE = CORES_INTERMEDIARIAS[0]     # vermelho: realce do valor máximo

try:
    # ===== VERSÃO 1: BARRAS - SIMPLES =====
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    bars = ax.bar(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'],
                  color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
    
    for bar, row in zip(bars, pub_por_ano.itertuples()):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{int(row.quantidade)}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    
    ax.set_xlabel('Ano de Defesa', fontsize=12)
    ax.set_ylabel('Quantidade de Publicações', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '01a_temporal_barras_simples.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Versão 1 (Barras Simples) gerada com sucesso")
    
    # ===== VERSÃO 2: BARRAS - COM DESTAQUE =====
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    bars = ax.bar(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'],
                  color=COR_PRINCIPAL, edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Destacar ano com mais publicações
    max_idx = pub_por_ano['quantidade'].idxmax()
    bars[max_idx].set_color(COR_REALCE)
    bars[max_idx].set_linewidth(2.5)
    bars[max_idx].set_alpha(1.0)
    
    for bar, row in zip(bars, pub_por_ano.itertuples()):
        ax.text(bar.get_x() + bar.get_width()/2., bar.get_height(),
                f'{int(row.quantidade)}', ha='center', va='bottom', 
                fontweight='bold', fontsize=9)
    
    ax.set_xlabel('Ano de Defesa', fontsize=12)
    ax.set_ylabel('Quantidade de Publicações', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')
    ax.set_axisbelow(True)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '01b_temporal_barras_destaque.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Versão 2 (Barras Destaque) gerada com sucesso")
    
    # ===== VERSÃO 3: LINHA - SIMPLES =====
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    ax.plot(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'], 
            marker='o', linewidth=3, markersize=8, 
            color=COR_PRINCIPAL, markerfacecolor=COR_REALCE,
            markeredgecolor='black', markeredgewidth=1.5)

    for i, row in pub_por_ano.iterrows():
        ax.text(row['ano_defesa'], row['quantidade'] + pub_por_ano['quantidade'].max()*0.02, 
                str(int(row['quantidade'])), ha='center', va='bottom', 
                fontweight='bold', fontsize=9)

    ax.set_xlabel('Ano de Defesa', fontsize=12)
    ax.set_ylabel('Quantidade de Publicações', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, linestyle='--')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '01c_temporal_linha_simples.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Versão 3 (Linha Simples) gerada com sucesso")
    
    # ===== VERSÃO 4: LINHA - COM ÁREA PREENCHIDA =====
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')
    
    ax.plot(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'], 
            marker='o', linewidth=3, markersize=8, 
            color=COR_REALCE, markerfacecolor=COR_PRINCIPAL,
            markeredgecolor='black', markeredgewidth=1.5, label='Publicações')
    
    ax.fill_between(pub_por_ano['ano_defesa'], pub_por_ano['quantidade'], 
                    alpha=0.3, color=COR_PRINCIPAL)

    for i, row in pub_por_ano.iterrows():
        ax.text(row['ano_defesa'], row['quantidade'] + pub_por_ano['quantidade'].max()*0.02, 
                str(int(row['quantidade'])), ha='center', va='bottom', 
                fontweight='bold', fontsize=9)

    ax.set_xlabel('Ano de Defesa', fontsize=12)
    ax.set_ylabel('Quantidade de Publicações', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.legend(fontsize=11, loc='upper left')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '01d_temporal_linha_area.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Versão 4 (Linha com Área) gerada com sucesso")
    
    print("✓ 4 versões de Evolução Temporal geradas com sucesso")
    
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 1: {e}")

# GRÁFICO 2: Distribuição por Nível
print("\n📊 Gráfico 2/9: Distribuição por Nível Acadêmico")
try:
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    nivel_counts_sorted = nivel_counts.sort_values(ascending=False)
    colors = [COR_MESTRADO, COR_DOUTORADO]
    bars = ax.bar(range(len(nivel_counts_sorted)), nivel_counts_sorted.values,
                  color=colors[:len(nivel_counts_sorted)], edgecolor='black', linewidth=1.5)

    ax.set_xticks(range(len(nivel_counts_sorted)))
    ax.set_xticklabels(nivel_counts_sorted.index, fontsize=11)
    ax.set_ylabel('Quantidade', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    for bar, v in zip(bars, nivel_counts_sorted.values):
        pct = (v/len(df))*100
        ax.text(bar.get_x() + bar.get_width()/2, v + 1, 
                f'{v}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '02_nivel_academico.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Gráfico 2 gerado com sucesso")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 2: {e}")

# GRÁFICO 3: TODAS AS ÁREAS TEMÁTICAS
print("\n📊 Gráfico 3/9: Todas as Áreas Temáticas (Frequência > 1)")
try:
    if len(areas_freq_maior_1) > 0:
        fig, ax = plt.subplots(figsize=(14, max(10, len(areas_freq_maior_1) * 0.4)), facecolor='white')

        areas_display = areas_freq_maior_1.copy()
        N = len(areas_display)

        bars = ax.barh(range(N), areas_display.values,
                       color=COR_PRINCIPAL, edgecolor='black', linewidth=1.2)

        ax.set_yticks(range(N))
        ax.set_yticklabels(areas_display.index, fontsize=9)
        ax.invert_yaxis()

        ax.set_xlabel('Quantidade de Publicações', fontsize=11)
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')

        for bar, v in zip(bars, areas_display.values):
            pct = (v/len(df))*100
            ax.text(v + 0.2, bar.get_y() + bar.get_height()/2,
                    f'{int(v)} ({pct:.1f}%)', va='center', fontsize=8, fontweight='bold')

        if len(areas_freq_1) > 0:
            areas_outras_lista = ', '.join(areas_freq_1.index[:10])
            if len(areas_freq_1) > 10:
                areas_outras_lista += f', ... (mais {len(areas_freq_1) - 10})'
            
            fig.text(0.12, 0.02, f'* Áreas com 1 publicação (total {len(areas_freq_1)}) incluem: {areas_outras_lista}',
                     fontsize=8, style='italic', wrap=True,
                     bbox=dict(boxstyle='round', facecolor=CORES_INTERMEDIARIAS[5], alpha=0.6))

        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08)
        plt.savefig(os.path.join(FIGURAS_DIR, '03_todas_areas.png'), dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Gráfico 3 gerado com sucesso")
    else:
        print("⚠ Sem dados suficientes para gráfico de áreas")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 3: {e}")

# GRÁFICO 4: TODAS AS INSTITUIÇÕES
print("\n📊 Gráfico 4/9: Todas as Instituições (Frequência > 1)")
try:
    if len(inst_freq_maior_1) > 0:
        fig, ax = plt.subplots(figsize=(14, max(10, len(inst_freq_maior_1) * 0.4)), facecolor='white')

        inst_display = inst_freq_maior_1.copy()
        N = len(inst_display)

        bars = ax.barh(range(N), inst_display.values,
                       color=COR_PRINCIPAL, edgecolor='black', linewidth=1.2)

        ax.set_yticks(range(N))
        ax.set_yticklabels(inst_display.index, fontsize=9)
        ax.invert_yaxis()

        ax.set_xlabel('Quantidade de Publicações', fontsize=11)
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')

        for bar, v in zip(bars, inst_display.values):
            pct = (v/len(df))*100
            ax.text(v + 0.15, bar.get_y() + bar.get_height()/2,
                    f'{int(v)} ({pct:.1f}%)', va='center', fontsize=8, fontweight='bold')

        if len(inst_freq_1) > 0:
            inst_outras_lista = ', '.join(inst_freq_1.index[:8])
            if len(inst_freq_1) > 8:
                inst_outras_lista += f', ... (mais {len(inst_freq_1) - 8})'
            
            fig.text(0.12, 0.02, f'* Instituições com 1 publicação (total {len(inst_freq_1)}) incluem: {inst_outras_lista}',
                     fontsize=8, style='italic', wrap=True,
                     bbox=dict(boxstyle='round', facecolor=CORES_INTERMEDIARIAS[5], alpha=0.6))

        plt.tight_layout()
        plt.subplots_adjust(bottom=0.08)
        plt.savefig(os.path.join(FIGURAS_DIR, '04_todas_instituicoes.png'), dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Gráfico 4 gerado com sucesso")
    else:
        print("⚠ Sem dados suficientes para gráfico de instituições")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 4: {e}")

# GRÁFICO 5: Classificação por Foco em IA
print("\n📊 Gráfico 5/9: Classificação por Foco em IA")
try:
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    foco_order = ['IA - Foco Central', 'IA - Foco Relacionado', 'Outros Temas']
    foco_counts_ordered = foco_counts.reindex(foco_order, fill_value=0)

    colors_foco = [COR_IA_CENTRAL, COR_IA_RELACIONADA, COR_IA_OUTROS]
    bars = ax.bar(range(len(foco_counts_ordered)), foco_counts_ordered.values,
                  color=colors_foco, edgecolor='black', linewidth=1.5)

    ax.set_xticks(range(len(foco_counts_ordered)))
    ax.set_xticklabels(foco_counts_ordered.index, fontsize=11, rotation=15, ha='right')
    ax.set_ylabel('Quantidade', fontsize=12)
    ax.set_facecolor('white')
    ax.grid(True, alpha=0.3, axis='y', linestyle='--')

    for bar, v in zip(bars, foco_counts_ordered.values):
        pct = (v/len(df))*100
        ax.text(bar.get_x() + bar.get_width()/2, v + 1,
                f'{v}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=10)

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '05_foco_ia.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Gráfico 5 gerado com sucesso")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 5: {e}")

# GRÁFICO 6: Evolução por Nível
print("\n📊 Gráfico 6/9: Evolução Temporal por Nível")
try:
    fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

    colors_nivel = [COR_MESTRADO, COR_DOUTORADO]
    for i, nivel in enumerate(['Mestrado', 'Doutorado']):
        if nivel in nivel_ano.columns:
            ax.plot(nivel_ano.index, nivel_ano[nivel], marker='o',
                    label=nivel, linewidth=3, color=colors_nivel[i], markersize=10)

    ax.set_xlabel('Ano', fontsize=12)
    ax.set_ylabel('Publicações', fontsize=12)
    ax.legend(fontsize=11, loc='upper left')
    ax.grid(True, alpha=0.3, linestyle='--')
    ax.set_facecolor('white')

    plt.tight_layout()
    plt.savefig(os.path.join(FIGURAS_DIR, '06_evolucao_nivel.png'), dpi=300, bbox_inches='tight', facecolor='white')
    print("✓ Gráfico 6 gerado com sucesso")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 6: {e}")

# GRÁFICO 7: Distribuição de Páginas
print("\n📊 Gráfico 7/9: Distribuição do Número de Páginas")
try:
    paginas_limpo = df['num_paginas'].dropna()
    
    if len(paginas_limpo) > 0:
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

        ax.hist(paginas_limpo, bins=25, color=COR_AZUL_PRINCIPAL,
                edgecolor='black', alpha=0.8, linewidth=1.5)

        media = paginas_limpo.mean()
        mediana = paginas_limpo.median()

        ax.set_xlabel('Número de Páginas', fontsize=12)
        ax.set_ylabel('Frequência', fontsize=12)
        ax.axvline(mediana, color=COR_MEDIANA, linestyle='--',
                   linewidth=3, label=f'Mediana: {mediana:.0f} páginas')
        ax.legend(fontsize=11, loc='upper right')
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='y', linestyle='--')

        plt.tight_layout()
        plt.savefig(os.path.join(FIGURAS_DIR, '07_distribuicao_paginas.png'), dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Gráfico 7 gerado com sucesso")
    else:
        print("⚠ Sem dados de páginas disponíveis")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 7: {e}")

# GRÁFICO 8: Top 10 Cidades
print("\n📊 Gráfico 8/9: Top 10 Cidades com Mais Publicações")
try:
    top10_cidades = cidade_counts.head(10)
    
    if len(top10_cidades) > 0:
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

        N = len(top10_cidades)

        bars = ax.barh(range(N), top10_cidades.values,
                       color=COR_PRINCIPAL,
                       edgecolor='black', linewidth=1.5)

        ax.set_yticks(range(N))
        ax.set_yticklabels(top10_cidades.index, fontsize=10)
        ax.invert_yaxis()

        ax.set_xlabel('Quantidade de Publicações', fontsize=11)
        ax.set_facecolor('white')
        ax.grid(True, alpha=0.3, axis='x', linestyle='--')

        for bar, v in zip(bars, top10_cidades.values):
            pct = (v/len(df))*100
            ax.text(v + 0.2, bar.get_y() + bar.get_height()/2,
                    f'{int(v)} ({pct:.1f}%)', va='center', fontsize=9, fontweight='bold')

        plt.tight_layout()
        plt.savefig(os.path.join(FIGURAS_DIR, '08_top10_cidades.png'), dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Gráfico 8 gerado com sucesso")
    else:
        print("⚠ Sem dados de cidades disponíveis")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 8: {e}")

# GRÁFICO 9: Evolução das Top 3 Áreas
print("\n📊 Gráfico 9/9: Evolução temporal - Top 3 áreas")
try:
    if len(area_counts) >= 3:
        fig, ax = plt.subplots(figsize=(12, 7), facecolor='white')

        top3_areas = area_counts.head(3).index
        colors_top3 = CORES_TOP3
        for i, area in enumerate(top3_areas):
            evolucao = df[df['area_normalizada'] == area].groupby('ano_defesa').size()
            if len(evolucao) > 0:
                ax.plot(evolucao.index, evolucao.values, marker='o', label=area,
                        linewidth=3, color=colors_top3[i], markersize=10)

        ax.set_xlabel('Ano', fontsize=12)
        ax.set_ylabel('Publicações', fontsize=12)
        ax.legend(fontsize=11, loc='upper left')
        ax.grid(True, alpha=0.3, linestyle='--')
        ax.set_facecolor('white')

        plt.tight_layout()
        plt.savefig(os.path.join(FIGURAS_DIR, '09_evolucao_top3_areas.png'), dpi=300, bbox_inches='tight', facecolor='white')
        print("✓ Gráfico 9 gerado com sucesso")
    else:
        print("⚠ Sem dados suficientes para top 3 áreas")
except Exception as e:
    print(f"❌ Erro ao gerar gráfico 9: {e}")

print("\n✅ Geração de gráficos concluída")

# =============================================================================
# 12. EXPORTAR RESULTADOS
# =============================================================================
print("\n" + "="*80)
print("Exportando resultados detalhados...")
print("="*80)

try:
    output_excel = os.path.join(DADOS_CAPES_DIR, 'resultados_detalhados_capes.xlsx')

    with pd.ExcelWriter(output_excel, engine='openpyxl') as writer:
        # Resumo Geral
        resumo = pd.DataFrame({
            'Métrica': [
                'Total de Publicações',
                'Período Analisado',
                'Mestrados',
                'Doutorados',
                'IA - Foco Central',
                'IA - Foco Relacionado',
                'Outros Temas',
                'Número de Áreas',
                'Áreas com 2+ publicações',
                'Áreas com 1 publicação',
                'Número de Instituições',
                'Instituições com 2+ publicações',
                'Instituições com 1 publicação',
                'Crescimento bruto (%)',
                'CAGR (% a.a.)',
                'Concentração Últimos 3 anos (%)'
            ],
            'Valor': [
                len(df),
                f"{df['ano_defesa'].min()} - {df['ano_defesa'].max()}",
                nivel_counts.get('Mestrado', 0),
                nivel_counts.get('Doutorado', 0),
                foco_counts.get('IA - Foco Central', 0),
                foco_counts.get('IA - Foco Relacionado', 0),
                foco_counts.get('Outros Temas', 0),
                len(area_counts),
                len(areas_freq_maior_1),
                len(areas_freq_1),
                len(inst_counts),
                len(inst_freq_maior_1),
                len(inst_freq_1),
                f"{crescimento:.0f}%",
                f"{cagr:.1f}%",
                f"{anos_recentes/len(df)*100:.1f}%"
            ]
        })
        resumo.to_excel(writer, sheet_name='Resumo Geral', index=False)

        # Auditoria da classificação por foco em IA: permite à pesquisadora
        # revisar amostra a amostra como cada título/resumo foi rotulado.
        cols_auditoria = ['ano_defesa', 'nivel', 'area_normalizada', 'instituicao',
                          'titulo', 'foco_ia']
        cols_auditoria = [c for c in cols_auditoria if c in df.columns]
        df[cols_auditoria].sort_values('foco_ia').to_excel(
            writer, sheet_name='Auditoria Foco IA', index=False)

        # Outras planilhas
        pub_por_ano.to_excel(writer, sheet_name='Publicações por Ano', index=False)
        area_counts.to_frame('Quantidade').to_excel(writer, sheet_name='Todas as Áreas')
        inst_counts.to_frame('Quantidade').to_excel(writer, sheet_name='Todas as Instituições')
        foco_counts.to_frame('Quantidade').to_excel(writer, sheet_name='Foco em IA')

        if len(areas_freq_1) > 0:
            areas_freq_1.to_frame('Quantidade').to_excel(writer, sheet_name='Áreas com 1 pub')

        if len(inst_freq_1) > 0:
            inst_freq_1.to_frame('Quantidade').to_excel(writer, sheet_name='Instituições com 1 pub')

        if top_termos:
            termos_df = pd.DataFrame(top_termos, columns=['Termo', 'Frequência'])
            termos_df.to_excel(writer, sheet_name='Top Termos', index=False)

        if top_bigrams:
            bigrams_df = pd.DataFrame(top_bigrams, columns=['Bigram', 'Frequência'])
            bigrams_df.to_excel(writer, sheet_name='Top Bigrams', index=False)

        df.to_excel(writer, sheet_name='Dataset Completo', index=False)

    print(f"✓ Resultados salvos: {output_excel}")
except Exception as e:
    print(f"[ERRO] Ao exportar resultados: {e}")

# =============================================================================
# 13. RELATÓRIO FINAL
# =============================================================================
print("\n" + "="*80)
print("RELATÓRIO FINAL - INSIGHTS PRINCIPAIS")
print("="*80)

top3_areas_str = "\n     ".join([f"{i+1}. {area}" for i, area in enumerate(area_counts.head(3).index)])
top3_inst_str = "\n     ".join([f"{i+1}. {inst}" for i, inst in enumerate(inst_counts.head(3).index)])

print(f"""
📊 RESUMO EXECUTIVO:

1. VOLUME E CRESCIMENTO:
   • Total de {len(df)} teses/dissertações analisadas
   • Período: {df['ano_defesa'].min()} a {df['ano_defesa'].max()}
   • Mestrados: {nivel_counts.get('Mestrado', 0)} ({nivel_counts.get('Mestrado', 0)/len(df)*100:.1f}%)
   • Doutorados: {nivel_counts.get('Doutorado', 0)} ({nivel_counts.get('Doutorado', 0)/len(df)*100:.1f}%)

2. FOCO EM INTELIGÊNCIA ARTIFICIAL:
   • IA como foco central: {foco_counts.get('IA - Foco Central', 0)} ({foco_counts.get('IA - Foco Central', 0)/len(df)*100:.1f}%)
   • IA como tema relacionado: {foco_counts.get('IA - Foco Relacionado', 0)} ({foco_counts.get('IA - Foco Relacionado', 0)/len(df)*100:.1f}%)

3. PRINCIPAIS ÁREAS:
   • Top 3 áreas:
     {top3_areas_str}

4. PRINCIPAIS INSTITUIÇÕES:
   • Top 3 instituições:
     {top3_inst_str}
""")

print("="*80)
print("ANÁLISE CONCLUÍDA")
print("="*80)
print(f"\nArquivos gerados:")
print(f"  • Gráficos: {FIGURAS_DIR}")
print(f"  • Planilha: {output_excel}")
print("\n" + "="*80)
