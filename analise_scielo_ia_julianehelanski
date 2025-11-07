# -*- coding: utf-8 -*-
"""
Created on Thu Nov  6 21:09:40 2025

@author: julia
"""
# -*- coding: utf-8 -*-
"""
ANÁLISE: ARTIGOS SCIELO COM FOCO EM INTELIGÊNCIA ARTIFICIAL
Versão Windows - com integração de dados CSV e arquivo RIS
Autor: Análise Automatizada
Data: Novembro 2025
"""

import re
import os
import csv
from collections import defaultdict, Counter
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
from matplotlib.gridspec import GridSpec

# Configurar estilo dos gráficos
sns.set_style("whitegrid")
plt.rcParams['font.size'] = 10
plt.rcParams['figure.max_open_warning'] = 50

# ============================================================================
# CONFIGURAÇÃO DOS ARQUIVOS - WINDOWS
# ============================================================================

# Diretório base - AJUSTADO PARA WINDOWS
BASE_DIR = r'C:\Users\julia\Downloads'
OUTPUT_DIR = r'C:\Users\julia\Downloads\resultados_analise'

# Arquivos de entrada
ARQUIVO_RIS = os.path.join(BASE_DIR, 'export_scielo.ris')
CSV_AREAS = os.path.join(BASE_DIR, 'scielo_areas_tematicas.csv')
CSV_CITAVEL = os.path.join(BASE_DIR, 'scielo_citavel_naocitavel.csv')
CSV_CITACOES = os.path.join(BASE_DIR, 'scielo_indice_citacoes.csv')
CSV_PERIODICOS = os.path.join(BASE_DIR, 'scielo_periódicos.csv')
CSV_ANO = os.path.join(BASE_DIR, 'scielo_publi_ano.csv')
CSV_LITERATURA = os.path.join(BASE_DIR, 'scielo_tipo__literatura.csv')

# Criar diretório de saída se não existir
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ============================================================================
# FUNÇÕES DE LEITURA DE CSV
# ============================================================================

def ler_csv_generico(caminho_csv):
    """Lê um arquivo CSV e retorna um dicionário com os dados"""
    dados = {}
    try:
        with open(caminho_csv, 'r', encoding='utf-8-sig') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # A primeira coluna é a chave, a segunda é o valor
                chave = list(row.values())[0]
                valor = int(list(row.values())[1])
                dados[chave] = valor
        print(f"✓ CSV carregado: {os.path.basename(caminho_csv)} ({len(dados)} registros)")
    except Exception as e:
        print(f"Erro ao ler {os.path.basename(caminho_csv)}: {e}")
    return dados

def carregar_dados_csv():
    """Carrega todos os arquivos CSV"""
    print("\n" + "="*80)
    print("CARREGAMENTO DOS DADOS CSV")
    print("="*80)
    
    dados_csv = {
        'areas_tematicas': ler_csv_generico(CSV_AREAS),
        'citavel': ler_csv_generico(CSV_CITAVEL),
        'citacoes': ler_csv_generico(CSV_CITACOES),
        'periodicos': ler_csv_generico(CSV_PERIODICOS),
        'ano': ler_csv_generico(CSV_ANO),
        'literatura': ler_csv_generico(CSV_LITERATURA)
    }
    
    return dados_csv

# ============================================================================
# FUNÇÕES DE LEITURA E PROCESSAMENTO DO RIS
# ============================================================================

def ler_arquivo_ris(caminho_ris):
    """Lê arquivo RIS e divide em registros individuais"""
    print("\n" + "="*80)
    print("PASSO 1: LEITURA DO ARQUIVO RIS")
    print("="*80)
    print(f"Lendo arquivo: {caminho_ris}")
    
    try:
        with open(caminho_ris, 'r', encoding='utf-8', errors='ignore') as f:
            conteudo = f.read()
        
        # Dividir em registros
        records = re.split(r'ER\s+-\s*\n', conteudo)
        records = [r for r in records if r.strip()]
        
        print(f"✓ {len(records)} registros encontrados")
        return records
        
    except FileNotFoundError:
        print(f"ERRO: Arquivo não encontrado!")
        print(f"    Caminho: {caminho_ris}")
        return []
    except Exception as e:
        print(f"ERRO na leitura: {e}")
        return []

def extrair_dados_artigo(record):
    """Extrai informações de um registro RIS"""
    if not record.strip():
        return None
    
    # Padrões mais robustos
    title_match = re.search(r'TI\s+-\s*(.+?)(?=\n[A-Z]{2}\s+-\s+|$)', record, re.DOTALL)
    abstract_matches = re.findall(r'AB\s+-\s*(.+?)(?=\n[A-Z]{2}\s+-\s+|$)', record, re.DOTALL)
    keywords_matches = re.findall(r'KW\s+-\s*(.+)', record)
    year_match = re.search(r'PY\s+-\s*(\d{4})', record)
    journal_match = re.search(r'JO\s+-\s*(.+)', record)
    language_match = re.search(r'LA\s+-\s*(.+)', record)
    type_match = re.search(r'TY\s+-\s*(.+)', record)
    
    if not title_match:
        return None
    
    title = title_match.group(1).strip().replace('\n', ' ')
    abstract = ' '.join([a.strip().replace('\n', ' ') for a in abstract_matches]) if abstract_matches else ""
    keywords = [k.strip() for k in keywords_matches]
    year = year_match.group(1) if year_match else "N/A"
    journal = journal_match.group(1).strip() if journal_match else "N/A"
    language = language_match.group(1).strip() if language_match else "N/A"
    doc_type = type_match.group(1).strip() if type_match else "N/A"
    
    return {
        'title': title,
        'year': year,
        'journal': journal,
        'language': language,
        'abstract': abstract,
        'keywords': keywords,
        'type': doc_type
    }

def verificar_foco_ia(artigo):
    """Determina se o artigo tem IA como foco principal"""
    
    ia_keywords_principais = [
        'inteligência artificial', 'artificial intelligence', 'inteligencia artificial',
        'machine learning', 'aprendizado de máquina', 'deep learning',
        'chatgpt', 'gpt', 'inteligencia artificial'
    ]
    
    ia_keywords_secundarias = [
        'neural network', 'rede neural', 'algoritmo', 'algorithm', 
        'automação', 'automation', 'ia ', ' ai ', 'dados', 'data'
    ]
    
    title_lower = artigo['title'].lower()
    abstract_lower = artigo['abstract'].lower()
    keywords_lower = ' '.join(artigo['keywords']).lower()
    
    # Verifica menções
    all_ia_keywords = ia_keywords_principais + ia_keywords_secundarias
    mentions_ai = any(kw in title_lower or kw in abstract_lower or kw in keywords_lower 
                     for kw in all_ia_keywords)
    
    # Verifica foco principal
    about_ai = False
    if mentions_ai:
        # Foco principal se IA está no título
        if any(kw in title_lower for kw in ia_keywords_principais):
            about_ai = True
        # Ou se IA está nas primeiras 3 palavras-chave
        elif any(kw.lower() in keywords_lower.split()[:10] 
                for kw in ia_keywords_principais):
            about_ai = True
    
    artigo['mentions_ai'] = mentions_ai
    artigo['about_ai'] = about_ai
    
    return artigo

def categorizar_artigo(artigo):
    """Categoriza artigo por tema principal"""
    title_lower = artigo['title'].lower()
    keywords_str = ' '.join(artigo['keywords']).lower()
    abstract_lower = artigo['abstract'].lower()
    
    categorias = {
        'Educação': [
            'educação', 'education', 'ensino', 'teaching', 'aprendizagem', 
            'learning', 'escola', 'professor', 'teacher', 'estudante', 
            'student', 'pedagog', 'didát', 'currículo', 'curriculum'
        ],
        'Ética': [
            'ética', 'ethics', 'ético', 'moral', 'bioética', 'bioethics',
            'responsabilidade', 'transparency', 'transparência'
        ],
        'Saúde': [
            'saúde', 'health', 'medicina', 'medical', 'diagnóstico', 
            'clínica', 'hospital', 'paciente', 'patient'
        ],
        'Economia/Trabalho': [
            'economia', 'economy', 'trabalho', 'labor', 'emprego', 
            'indústria', 'industry', 'organizações', 'organizations',
            'empresa', 'mercado', 'market'
        ],
        'Política/Democracia': [
            'democracia', 'democracy', 'política', 'policy', 'político',
            'governo', 'government', 'estado', 'state', 'eleição'
        ],
        'Direito': [
            'direito', 'law', 'legal', 'jurídico', 'justice', 'judicial',
            'tribunal', 'legislação', 'regulation'
        ],
        'IA Generativa (ChatGPT)': [
            'chatgpt', 'gpt', 'generative', 'generativa', 'llm'
        ],
        'Filosofia': [
            'filosofia', 'philosophy', 'epistemolog', 'ontolog',
            'cognição', 'cognition', 'consciência', 'consciousness'
        ],
        'História': [
            'história', 'history', 'histórico', 'historical'
        ],
        'Comunicação': [
            'comunicação', 'communication', 'mídia', 'media'
        ]
    }
    
    # Prioriza título, depois keywords, depois abstract
    for categoria, palavras in categorias.items():
        if any(palavra in title_lower for palavra in palavras):
            return categoria
        elif any(palavra in keywords_str for palavra in palavras):
            return categoria
    
    # Se não encontrou nas categorias específicas
    for categoria, palavras in categorias.items():
        if any(palavra in abstract_lower for palavra in palavras):
            return categoria
    
    return 'Outros'

def processar_artigos(records):
    """Processa todos os registros RIS"""
    print("\n" + "="*80)
    print("PASSO 2: PROCESSAMENTO DOS ARTIGOS")
    print("="*80)
    
    artigos = []
    for i, record in enumerate(records, 1):
        artigo = extrair_dados_artigo(record)
        if artigo:
            artigo = verificar_foco_ia(artigo)
            artigos.append(artigo)
        
        if i % 50 == 0 or i == len(records):
            print(f"    Processados: {i}/{len(records)} artigos...")
    
    print(f"✓ {len(artigos)} artigos processados")
    return artigos

def gerar_estatisticas(artigos):
    """Gera estatísticas sobre os artigos"""
    print("\n" + "="*80)
    print("PASSO 3: GERAÇÃO DE ESTATÍSTICAS")
    print("="*80)
    
    total = len(artigos)
    mentions_ai = sum(1 for a in artigos if a['mentions_ai'])
    about_ai = sum(1 for a in artigos if a['about_ai'])
    tangenciam = mentions_ai - about_ai
    sem_ia = total - mentions_ai
    
    print(f"\nRESUMO GERAL:")
    print(f"   Total de artigos: {total}")
    print(f"   Artigos que MENCIONAM IA: {mentions_ai} ({mentions_ai/total*100:.1f}%)")
    print(f"   Artigos SOBRE IA (foco principal): {about_ai} ({about_ai/total*100:.1f}%)")
    print(f"   Artigos que TANGENCIAM IA: {tangenciam} ({tangenciam/total*100:.1f}%)")
    print(f"   Artigos SEM relação com IA: {sem_ia} ({sem_ia/total*100:.1f}%)")
    
    return {
        'total': total,
        'mentions_ai': mentions_ai,
        'about_ai': about_ai,
        'tangenciam': tangenciam,
        'sem_ia': sem_ia
    }

def categorizar_artigos_ia(artigos):
    """Categoriza artigos que focam em IA"""
    print("\n" + "="*80)
    print("PASSO 4: CATEGORIZAÇÃO TEMÁTICA")
    print("="*80)
    
    ia_focused = [a for a in artigos if a['about_ai']]
    
    categorias = defaultdict(list)
    for artigo in ia_focused:
        categoria = categorizar_artigo(artigo)
        categorias[categoria].append(artigo)
    
    print(f"\nDISTRIBUIÇÃO POR CATEGORIA (Artigos com foco em IA):")
    for categoria, arts in sorted(categorias.items(), 
                                   key=lambda x: len(x[1]), 
                                   reverse=True):
        porcentagem = len(arts) / len(ia_focused) * 100 if len(ia_focused) > 0 else 0
        print(f"   {categoria}: {len(arts)} artigos ({porcentagem:.1f}%)")
    
    return categorias

# ============================================================================
# VISUALIZAÇÕES
# ============================================================================

def criar_grafico_foco_ia(stats, output_path):
    """Cria gráfico de barras único para classificação por foco em IA"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 1: CLASSIFICAÇÃO POR FOCO EM IA")
    print("="*80)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Dados para o gráfico - APENAS FOCO E TANGENCIAL
    categorias = ['Foco Principal\nem IA', 'Mencionam IA\n(Tangencial)']
    valores = [stats['about_ai'], stats['tangenciam']]
    cores = ['#A8D5BA', '#C8E6C9']
    
    # Criar barras
    bars = ax.bar(categorias, valores, color=cores, 
                   edgecolor='black', linewidth=2.5, alpha=0.9)
    
    # Adicionar valores e percentuais nas barras
    for i, (bar, valor) in enumerate(zip(bars, valores)):
        height = bar.get_height()
        pct = valor/stats['mentions_ai']*100
        
        # Texto dentro da barra
        ax.text(bar.get_x() + bar.get_width()/2., height/2,
                f'{valor}\nartigos',
                ha='center', va='center', 
                fontweight='bold', fontsize=14, color='black')
        
        # Percentual acima da barra
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{pct:.1f}%',
                ha='center', va='bottom', 
                fontweight='bold', fontsize=13, color='black')
    
    # Configurações do gráfico
    ax.set_ylabel('Número de Artigos', fontsize=14, fontweight='bold')
    ax.set_title(f'CLASSIFICAÇÃO POR FOCO EM INTELIGÊNCIA ARTIFICIAL\n'
                 f'Artigos que mencionam IA: {stats["mentions_ai"]} de {stats["total"]} totais', 
                 fontsize=16, fontweight='bold', pad=20)
    
    ax.grid(axis='y', alpha=0.3, linestyle='--', linewidth=1)
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(valores) * 1.15)
    ax.tick_params(axis='x', labelsize=12)
    ax.tick_params(axis='y', labelsize=11)
    
    # Adicionar caixa de estatísticas
    textstr = f'''RESUMO:
━━━━━━━━━━━━━━━━━━━━━━
Total Analisado: {stats["total"]}
Mencionam IA: {stats["mentions_ai"]} ({stats["mentions_ai"]/stats["total"]*100:.1f}%)
  • Foco em IA: {stats["about_ai"]} ({stats["about_ai"]/stats["total"]*100:.1f}%)
  • Tangencial: {stats["tangenciam"]} ({stats["tangenciam"]/stats["total"]*100:.1f}%)
Sem menção a IA: {stats["sem_ia"]} ({stats["sem_ia"]/stats["total"]*100:.1f}%)
'''
    
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.8, edgecolor='black', linewidth=2)
    ax.text(0.98, 0.97, textstr, transform=ax.transAxes, fontsize=11,
            verticalalignment='top', horizontalalignment='right',
            bbox=props, fontfamily='monospace', fontweight='bold')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_publicacoes_ano(artigos, dados_csv, output_path):
    """Gráfico: Distribuição de Publicações por Ano"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 2: DISTRIBUIÇÃO POR ANO")
    print("="*80)
    
    # Dados do RIS
    years_ris = [int(a['year']) for a in artigos if a['year'] != 'N/A' and a['year'].isdigit()]
    year_counts_ris = Counter(years_ris)
    
    total_artigos = len(years_ris)
    n_anos = len(year_counts_ris)
    ano_min = min(years_ris) if years_ris else 0
    ano_max = max(years_ris) if years_ris else 0
    
    # Criar figura
    fig, ax = plt.subplots(figsize=(16, 8))
    
    years_sorted = sorted(year_counts_ris.keys())
    counts = [year_counts_ris[y] for y in years_sorted]
    
    bars = ax.bar(years_sorted, counts, color='#5B9BD5', 
                   edgecolor='black', linewidth=1.5, alpha=0.8)
    
    # Destacar ano com mais publicações
    max_count = max(counts)
    max_year = years_sorted[counts.index(max_count)]
    bars[counts.index(max_count)].set_color('#FF6B6B')
    bars[counts.index(max_count)].set_edgecolor('black')
    bars[counts.index(max_count)].set_linewidth(2.5)
    
    # Adicionar valores nas barras
    for bar, count, year in zip(bars, counts, years_sorted):
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{int(count)}',
                ha='center', va='bottom', fontweight='bold', fontsize=9)
    
    ax.set_xlabel('Ano', fontsize=13, fontweight='bold')
    ax.set_ylabel('Número de Artigos', fontsize=13, fontweight='bold')
    ax.set_title(f'Distribuição de Publicações por Ano ({ano_min}-{ano_max})\n{total_artigos} artigos • {n_anos} anos • Pico em {max_year} ({max_count} artigos)', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(counts) * 1.15)
    
    # Rotacionar labels se necessário
    if len(years_sorted) > 15:
        plt.xticks(rotation=45, ha='right')
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_top_journals(artigos, dados_csv, output_path):
    """Gráfico: Top 10 Periódicos (apenas RIS)"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 3A: TOP 10 PERIÓDICOS")
    print("="*80)
    
    # Dados do RIS apenas
    journals_ris = [a['journal'] for a in artigos if a['journal'] != 'N/A']
    journal_counts = Counter(journals_ris)
    
    total_artigos = len(journals_ris)
    total_periodicos = len(journal_counts)
    
    # Top 10
    top_10 = journal_counts.most_common(10)
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    journal_names = [j[0][:60] + '...' if len(j[0]) > 60 else j[0] for j in top_10]
    valores = [j[1] for j in top_10]
    
    colors = plt.cm.Blues(np.linspace(0.4, 0.9, len(journal_names)))
    bars = ax.barh(range(len(journal_names)), valores, color=colors, 
                    edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Destacar o primeiro lugar
    bars[0].set_color('#FFD700')
    bars[0].set_edgecolor('black')
    bars[0].set_linewidth(2.5)
    
    # Adicionar valores e percentuais
    for i, (bar, valor) in enumerate(zip(bars, valores)):
        pct = valor/total_artigos*100
        ax.text(valor + 0.3, i, f'{valor} ({pct:.1f}%)', 
                va='center', fontweight='bold', fontsize=11)
    
    ax.set_yticks(range(len(journal_names)))
    ax.set_yticklabels(journal_names)
    ax.invert_yaxis()
    ax.set_xlabel('Número de Artigos', fontsize=13, fontweight='bold')
    ax.set_title(f'Top 10 Periódicos por Número de Publicações\n{total_artigos} artigos analisados • {total_periodicos} periódicos únicos', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(valores) * 1.15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()

def criar_grafico_outros_journals(artigos, dados_csv, output_path):
    """Gráfico: Periódicos Fora do Top 10 (exceto os com apenas 1 publicação)"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 3B: PERIÓDICOS FORA DO TOP 10")
    print("="*80)
    
    # Dados do RIS apenas
    journals_ris = [a['journal'] for a in artigos if a['journal'] != 'N/A']
    journal_counts = Counter(journals_ris)
    
    total_artigos = len(journals_ris)
    
    # Pegar todos exceto top 10
    all_journals = journal_counts.most_common()
    outros_journals = all_journals[10:]  # Tudo após o top 10
    
    if not outros_journals:
        print("Não há periódicos fora do top 10")
        return
    
    # Separar: periódicos com >1 publicação vs periódicos com apenas 1 publicação
    journals_multiplos = [(j, c) for j, c in outros_journals if c > 1]
    journals_unicos = [(j, c) for j, c in outros_journals if c == 1]
    
    n_multiplos = len(journals_multiplos)
    n_unicos = len(journals_unicos)
    total_artigos_multiplos = sum([j[1] for j in journals_multiplos])
    total_artigos_unicos = sum([j[1] for j in journals_unicos])
    
    # Criar figura com espaço extra para a legenda
    fig, ax = plt.subplots(figsize=(16, max(12, n_multiplos * 0.35 + 4)))
    
    if journals_multiplos:
        journal_names = [j[0][:70] + '...' if len(j[0]) > 70 else j[0] for j in journals_multiplos]
        valores = [j[1] for j in journals_multiplos]
        
        colors = plt.cm.Greens(np.linspace(0.3, 0.8, len(journal_names)))
        bars = ax.barh(range(len(journal_names)), valores, color=colors,
                        edgecolor='black', linewidth=1, alpha=0.85)
        
        # Adicionar valores
        for i, (bar, valor) in enumerate(zip(bars, valores)):
            pct = valor/total_artigos*100
            ax.text(valor + 0.15, i, f'{valor} ({pct:.1f}%)', 
                    va='center', fontweight='bold', fontsize=9)
        
        ax.set_yticks(range(len(journal_names)))
        ax.set_yticklabels(journal_names, fontsize=9)
        ax.invert_yaxis()
    else:
        ax.text(0.5, 0.5, 'Não há periódicos com múltiplas publicações fora do Top 10',
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
    
    ax.set_xlabel('Número de Artigos', fontsize=13, fontweight='bold')
    
    # Título com informação sobre periódicos excluídos
    titulo = f'Periódicos Fora do Top 10 (Posições 11-{10+len(outros_journals)})\n'
    titulo += f'{total_artigos_multiplos} artigos em {n_multiplos} periódicos (com 2+ publicações)\n'
    titulo += f'{n_unicos} periódicos com 1 publicação listados abaixo'
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    if valores:
        ax.set_xlim(0, max(valores) * 1.2)
    
    # Criar legenda com periódicos de 1 publicação
    if journals_unicos:
        # Organizar em colunas
        journal_names_unicos = [j[0] for j in journals_unicos]
        
        # Criar texto da legenda
        legenda_texto = "Periódicos com 1 Publicação:\n" + "─" * 80 + "\n"
        
        # Dividir em 3 colunas
        n_por_coluna = (len(journal_names_unicos) + 2) // 3
        colunas = [journal_names_unicos[i:i + n_por_coluna] 
                   for i in range(0, len(journal_names_unicos), n_por_coluna)]
        
        # Preencher colunas para terem o mesmo tamanho
        max_len = max(len(col) for col in colunas)
        for col in colunas:
            while len(col) < max_len:
                col.append('')
        
        # Criar linhas combinando as 3 colunas
        max_width = 35  # largura máxima por coluna
        for i in range(max_len):
            linha_partes = []
            for col in colunas:
                if i < len(col) and col[i]:
                    # Truncar nome se muito longo
                    nome = col[i][:max_width-3] + '...' if len(col[i]) > max_width else col[i]
                    linha_partes.append(f"• {nome:<{max_width}}")
                else:
                    linha_partes.append(' ' * (max_width + 2))
            legenda_texto += '  '.join(linha_partes) + '\n'
        
        # Adicionar legenda na parte inferior
        plt.figtext(0.1, 0.02, legenda_texto, 
                   fontsize=14, fontfamily='monospace',
                   verticalalignment='bottom',
                   bbox=dict(boxstyle='round', facecolor='lightyellow', 
                            alpha=0.8, edgecolor='black', linewidth=1))
    
    plt.tight_layout(rect=[0, 0.25, 1, 1])  # Mais espaço para a legenda maior
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    print(f"  • {n_multiplos} periódicos no gráfico (2+ publicações)")
    print(f"  • {n_unicos} periódicos na legenda (1 publicação)")
    plt.show()

def criar_grafico_idiomas(artigos, output_path):
    """Gráfico: Distribuição por Idioma"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 4: DISTRIBUIÇÃO POR IDIOMA")
    print("="*80)
    
    languages = [a['language'] for a in artigos if a['language'] != 'N/A']
    
    language_map = {
        'Portuguese': 'Português', 'por': 'Português', 'pt': 'Português',
        'English': 'Inglês', 'eng': 'Inglês', 'en': 'Inglês',
        'Spanish': 'Espanhol', 'spa': 'Espanhol', 'es': 'Espanhol'
    }
    
    languages_mapped = [language_map.get(lang, lang) for lang in languages]
    language_counts = Counter(languages_mapped)
    
    total_artigos = len(languages_mapped)
    n_idiomas = len(language_counts)
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = list(language_counts.keys())
    sizes = list(language_counts.values())
    colors = ['#90CAF9', '#FFE082', '#CE93D8'][:len(labels)]
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90,
                                         textprops={'fontsize': 12, 'fontweight': 'bold'},
                                         explode=[0.05]*len(labels))
    
    for autotext in autotexts:
        autotext.set_color('black')
        autotext.set_fontsize(13)
        autotext.set_fontweight('bold')
    
    # Adicionar contagens aos labels
    for i, (text, size) in enumerate(zip(texts, sizes)):
        text.set_text(f'{text.get_text()}\n({size} artigos)')
        text.set_fontweight('bold')
    
    ax.set_title(f'Distribuição por Idioma de Publicação\n{total_artigos} artigos • {n_idiomas} idiomas', 
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_tipo_literatura(artigos, dados_csv, output_path):
    """Gráfico: Distribuição por Tipo de Literatura (CSV)"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 5: TIPO DE LITERATURA")
    print("="*80)
    
    tipo_counts = dados_csv['literatura']
    
    if not tipo_counts:
        print("Nenhum dado de tipo de literatura encontrado")
        return
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    # Ordenar por valor
    tipos_sorted = sorted(tipo_counts.items(), key=lambda x: x[1], reverse=True)
    tipos = [t[0] for t in tipos_sorted]
    valores = [t[1] for t in tipos_sorted]
    
    total_docs = sum(valores)
    n_tipos = len(tipos)
    
    colors = plt.cm.Set3(np.linspace(0, 1, len(tipos)))
    
    bars = ax.bar(range(len(tipos)), valores, color=colors, edgecolor='black', linewidth=2, alpha=0.85)
    
    # Adicionar valores e percentuais nas barras
    for i, (bar, valor) in enumerate(zip(bars, valores)):
        height = bar.get_height()
        pct = valor/total_docs*100
        ax.text(bar.get_x() + bar.get_width()/2., height,
                f'{valor}\n({pct:.1f}%)',
                ha='center', va='bottom', fontweight='bold', fontsize=10)
    
    ax.set_xticks(range(len(tipos)))
    ax.set_xticklabels(tipos, rotation=45, ha='right')
    ax.set_ylabel('Número de Publicações', fontsize=13, fontweight='bold')
    ax.set_title(f'Distribuição por Tipo de Literatura\n{total_docs} documentos analisados • {n_tipos} tipos', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='y', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_ylim(0, max(valores) * 1.15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_citavel(dados_csv, output_path):
    """Gráfico: Distribuição Citável vs Não Citável"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 6: CITÁVEL VS NÃO CITÁVEL")
    print("="*80)
    
    citavel_counts = dados_csv['citavel']
    total_docs = sum(citavel_counts.values())
    
    fig, ax = plt.subplots(figsize=(10, 8))
    
    labels = list(citavel_counts.keys())
    sizes = list(citavel_counts.values())
    colors = ['#66C2A5', '#FC8D62']
    explode = (0.05, 0.05)
    
    wedges, texts, autotexts = ax.pie(sizes, labels=labels, autopct='%1.1f%%',
                                         colors=colors, startangle=90, explode=explode,
                                         textprops={'fontsize': 13, 'fontweight': 'bold'})
    
    for autotext in autotexts:
        autotext.set_color('white')
        autotext.set_fontsize(14)
        autotext.set_fontweight('bold')
    
    # Adicionar contagens aos labels
    for i, (text, size) in enumerate(zip(texts, sizes)):
        text.set_text(f'{text.get_text()}\n({size} docs)')
        text.set_fontweight('bold')
    
    ax.set_title(f'Distribuição: Documentos Citáveis vs Não Citáveis\n{total_docs} documentos analisados', 
                 fontsize=15, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_indice_citacoes(dados_csv, output_path):
    """Gráfico: Distribuição por Índice de Citações"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 7: ÍNDICE DE CITAÇÕES")
    print("="*80)
    
    citacoes_counts = dados_csv['citacoes']
    total_docs = sum(citacoes_counts.values())
    n_indices = len(citacoes_counts)
    
    fig, ax = plt.subplots(figsize=(12, 8))
    
    indices = list(citacoes_counts.keys())
    valores = list(citacoes_counts.values())
    colors = ['#8DD3C7', '#FFFFB3', '#BEBADA'][:len(indices)]
    
    bars = ax.barh(range(len(indices)), valores, color=colors, 
                    edgecolor='black', linewidth=2, alpha=0.85)
    
    # Adicionar valores e percentuais
    for i, (bar, valor) in enumerate(zip(bars, valores)):
        pct = valor/total_docs*100
        ax.text(valor + 0.5, i, f'{valor} ({pct:.1f}%)', 
                va='center', fontweight='bold', fontsize=12)
    
    ax.set_yticks(range(len(indices)))
    ax.set_yticklabels(indices)
    ax.invert_yaxis()
    ax.set_xlabel('Número de Publicações', fontsize=13, fontweight='bold')
    ax.set_title(f'Distribuição por Índice de Citações WoS\n{total_docs} artigos indexados • {n_indices} índices', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(valores) * 1.2)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

def criar_grafico_areas_tematicas(dados_csv, output_path):
    """Gráfico: Top 10 Áreas Temáticas"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 8A: TOP 10 ÁREAS TEMÁTICAS")
    print("="*80)
    
    areas_counts = dados_csv['areas_tematicas']
    total_areas = len(areas_counts)
    total_mencoes = sum(areas_counts.values())
    
    top_10 = sorted(areas_counts.items(), key=lambda x: x[1], reverse=True)[:10]
    
    fig, ax = plt.subplots(figsize=(14, 10))
    
    areas = [a[0] for a in top_10]
    valores = [a[1] for a in top_10]
    colors = plt.cm.Reds(np.linspace(0.4, 0.9, len(areas)))
    
    bars = ax.barh(range(len(areas)), valores, color=colors, 
                    edgecolor='black', linewidth=1.5, alpha=0.85)
    
    # Destacar o primeiro lugar
    bars[0].set_color('#FFD700')
    bars[0].set_edgecolor('black')
    bars[0].set_linewidth(2.5)
    
    # Adicionar valores e percentuais
    for i, (bar, valor) in enumerate(zip(bars, valores)):
        pct = valor/total_mencoes*100
        ax.text(valor + 0.5, i, f'{valor} ({pct:.1f}%)', 
                va='center', fontweight='bold', fontsize=11)
    
    ax.set_yticks(range(len(areas)))
    ax.set_yticklabels(areas)
    ax.invert_yaxis()
    ax.set_xlabel('Número de Menções', fontsize=13, fontweight='bold')
    ax.set_title(f'Top 10 Áreas Temáticas WoS\n{total_mencoes} menções • {total_areas} áreas únicas', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    ax.set_xlim(0, max(valores) * 1.15)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()

def criar_grafico_outras_areas(dados_csv, output_path):
    """Gráfico: Áreas Temáticas Fora do Top 10 (exceto as com apenas 1 ou 2 menções)"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 8B: ÁREAS TEMÁTICAS FORA DO TOP 10")
    print("="*80)
    
    areas_counts = dados_csv['areas_tematicas']
    total_mencoes = sum(areas_counts.values())
    
    all_areas = sorted(areas_counts.items(), key=lambda x: x[1], reverse=True)
    outras_areas = all_areas[10:]  # Tudo após o top 10
    
    if not outras_areas:
        print("Não há áreas fora do top 10")
        return
    
    # Separar: áreas com 3+ menções vs áreas com 1-2 menções
    areas_multiplas = [(a, c) for a, c in outras_areas if c >= 3]
    areas_poucas = [(a, c) for a, c in outras_areas if c <= 2]
    
    n_multiplas = len(areas_multiplas)
    n_poucas = len(areas_poucas)
    total_mencoes_multiplas = sum([a[1] for a in areas_multiplas])
    total_mencoes_poucas = sum([a[1] for a in areas_poucas])
    
    # Separar as poucas em 1 e 2 menções para detalhar
    areas_uma = [(a, c) for a, c in areas_poucas if c == 1]
    areas_duas = [(a, c) for a, c in areas_poucas if c == 2]
    
    # Criar figura com espaço extra para a legenda
    fig, ax = plt.subplots(figsize=(14, max(10, n_multiplas * 0.4 + 5)))
    
    if areas_multiplas:
        areas = [a[0] for a in areas_multiplas]
        valores = [a[1] for a in areas_multiplas]
        colors = plt.cm.Purples(np.linspace(0.4, 0.9, len(areas)))
        
        bars = ax.barh(range(len(areas)), valores, color=colors,
                        edgecolor='black', linewidth=1.5, alpha=0.85)
        
        # Adicionar valores
        for i, (bar, valor) in enumerate(zip(bars, valores)):
            pct = valor/total_mencoes*100
            ax.text(valor + 0.3, i, f'{valor} ({pct:.1f}%)', 
                    va='center', fontweight='bold', fontsize=10)
        
        ax.set_yticks(range(len(areas)))
        ax.set_yticklabels(areas, fontsize=10)
        ax.invert_yaxis()
    else:
        ax.text(0.5, 0.5, 'Não há áreas com 3+ menções fora do Top 10',
                ha='center', va='center', transform=ax.transAxes, fontsize=12)
    
    ax.set_xlabel('Número de Menções', fontsize=13, fontweight='bold')
    
    # Título com informação sobre áreas excluídas
    titulo = f'Áreas Temáticas WoS Fora do Top 10 (Posições 11-{10+len(outras_areas)})\n'
    titulo += f'{total_mencoes_multiplas} menções em {n_multiplas} áreas (3+ menções)\n'
    titulo += f'{n_poucas} áreas com 1-2 menções listadas abaixo'
    
    ax.set_title(titulo, fontsize=14, fontweight='bold', pad=20)
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_axisbelow(True)
    
    if valores:
        ax.set_xlim(0, max(valores) * 1.2)
    
    # Criar legenda com áreas de 1-2 menções
    if areas_poucas:
        # Criar texto da legenda separando 1 e 2 menções
        legenda_texto = "Áreas Temáticas com 1-2 Menções:\n" + "─" * 95 + "\n"
        
        # Adicionar áreas com 2 menções primeiro (se houver)
        if areas_duas:
            legenda_texto += f"Com 2 Menções ({len(areas_duas)} áreas):\n"
            area_names_duas = [a[0] for a in areas_duas]
            
            # Dividir em 3 colunas
            n_por_coluna = (len(area_names_duas) + 2) // 3
            colunas = [area_names_duas[i:i + n_por_coluna] 
                       for i in range(0, len(area_names_duas), n_por_coluna)]
            
            # Preencher colunas
            max_len = max(len(col) for col in colunas) if colunas else 0
            for col in colunas:
                while len(col) < max_len:
                    col.append('')
            
            # Criar linhas
            max_width = 30
            for i in range(max_len):
                linha_partes = []
                for col in colunas:
                    if i < len(col) and col[i]:
                        nome = col[i][:max_width-3] + '...' if len(col[i]) > max_width else col[i]
                        linha_partes.append(f"• {nome:<{max_width}}")
                    else:
                        linha_partes.append(' ' * (max_width + 2))
                legenda_texto += '  '.join(linha_partes) + '\n'
            
            legenda_texto += '\n'
        
        # Adicionar áreas com 1 menção
        if areas_uma:
            legenda_texto += f"Com 1 Menção ({len(areas_uma)} áreas):\n"
            area_names_uma = [a[0] for a in areas_uma]
            
            # Dividir em 3 colunas
            n_por_coluna = (len(area_names_uma) + 2) // 3
            colunas = [area_names_uma[i:i + n_por_coluna] 
                       for i in range(0, len(area_names_uma), n_por_coluna)]
            
            # Preencher colunas
            max_len = max(len(col) for col in colunas) if colunas else 0
            for col in colunas:
                while len(col) < max_len:
                    col.append('')
            
            # Criar linhas
            max_width = 30
            for i in range(max_len):
                linha_partes = []
                for col in colunas:
                    if i < len(col) and col[i]:
                        nome = col[i][:max_width-3] + '...' if len(col[i]) > max_width else col[i]
                        linha_partes.append(f"• {nome:<{max_width}}")
                    else:
                        linha_partes.append(' ' * (max_width + 2))
                legenda_texto += '  '.join(linha_partes) + '\n'
        
        # Adicionar legenda na parte inferior
        plt.figtext(0.08, 0.02, legenda_texto, 
                   fontsize=14, fontfamily='monospace',
                   verticalalignment='bottom',
                   bbox=dict(boxstyle='round', facecolor='lavender', 
                            alpha=0.8, edgecolor='black', linewidth=1.5))
    
    plt.tight_layout(rect=[0, 0.30, 1, 1])  # Mais espaço para a legenda expandida e maior
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    print(f"  • {n_multiplas} áreas no gráfico (3+ menções)")
    print(f"  • {len(areas_duas)} áreas na legenda (2 menções)")
    print(f"  • {len(areas_uma)} áreas na legenda (1 menção)")
    print(f"  • Total na legenda: {n_poucas} áreas")
    plt.show()

def criar_visualizacao_categorias(categorias, total_ia, output_path):
    """Cria visualização das categorias temáticas dos artigos com foco em IA"""
    print("\n" + "="*80)
    print("VISUALIZAÇÃO 9: CATEGORIAS TEMÁTICAS (ARTIGOS COM FOCO EM IA)")
    print("="*80)
    
    if total_ia == 0:
        print("Nenhum artigo com foco principal em IA para categorizar")
        return
    
    fig, ax = plt.subplots(figsize=(14, 8))
    
    cats_sorted = sorted(categorias.items(), key=lambda x: len(x[1]), reverse=True)
    labels = [c[0] for c in cats_sorted]
    values = [len(c[1]) for c in cats_sorted]
    colors = plt.cm.Spectral(np.linspace(0.2, 0.8, len(labels)))
    
    bars = ax.barh(labels, values, color=colors, 
                    edgecolor='black', linewidth=2, alpha=0.85)
    
    for i, (bar, value) in enumerate(zip(bars, values)):
        pct = value/total_ia*100
        ax.text(value + 0.3, i, f'{value} ({pct:.1f}%)', 
                va='center', fontweight='bold', fontsize=11)
    
    ax.set_xlabel('Número de Artigos', fontsize=13, fontweight='bold')
    ax.set_title(f'DISTRIBUIÇÃO TEMÁTICA DOS ARTIGOS COM FOCO EM IA\n'
                 f'Total: {total_ia} artigos', 
                 fontsize=15, fontweight='bold', pad=20)
    ax.invert_yaxis()
    ax.grid(axis='x', alpha=0.3, linestyle='--')
    ax.set_xlim(0, max(values) * 1.15 if values else 1)
    
    plt.tight_layout()
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"✓ Gráfico salvo: {output_path}")
    plt.show()  # Mostrar gráfico na tela

# ============================================================================
# RELATÓRIO DETALHADO
# ============================================================================

def gerar_relatorio_detalhado(categorias, artigos, stats, dados_csv, output_path):
    """Gera relatório textual detalhado"""
    print("\n" + "="*80)
    print("GERAÇÃO DO RELATÓRIO DETALHADO")
    print("="*80)
    
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write("="*80 + "\n")
        f.write("RELATÓRIO INTEGRADO: ARTIGOS COM FOCO EM INTELIGÊNCIA ARTIFICIAL\n")
        f.write("Análise combinada de dados RIS e CSV do SciELO\n")
        f.write("="*80 + "\n\n")
        
        # Estatísticas gerais
        f.write("ESTATÍSTICAS GERAIS\n")
        f.write("-"*80 + "\n")
        f.write(f"Total de artigos analisados (RIS): {stats['total']}\n")
        f.write(f"Artigos que MENCIONAM IA: {stats['mentions_ai']} ({stats['mentions_ai']/stats['total']*100:.1f}%)\n")
        f.write(f"Artigos com FOCO EM IA: {stats['about_ai']} ({stats['about_ai']/stats['total']*100:.1f}%)\n")
        f.write(f"Artigos que TANGENCIAM IA: {stats['tangenciam']} ({stats['tangenciam']/stats['total']*100:.1f}%)\n")
        f.write(f"Artigos SEM relação com IA: {stats['sem_ia']} ({stats['sem_ia']/stats['total']*100:.1f}%)\n\n")
        
        # Dados dos CSVs
        f.write("DADOS ADICIONAIS (CSVs)\n")
        f.write("-"*80 + "\n\n")
        
        f.write("Distribuição por Tipo de Literatura:\n")
        for tipo, count in sorted(dados_csv['literatura'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"  • {tipo}: {count}\n")
        f.write("\n")
        
        f.write("Documentos Citáveis vs Não Citáveis:\n")
        for cat, count in dados_csv['citavel'].items():
            f.write(f"  • {cat}: {count}\n")
        f.write("\n")
        
        f.write("Índices de Citação WoS:\n")
        for indice, count in sorted(dados_csv['citacoes'].items(), key=lambda x: x[1], reverse=True):
            f.write(f"  • {indice}: {count}\n")
        f.write("\n\n")
        
        # Categorias temáticas dos artigos com foco em IA
        if stats['about_ai'] > 0:
            f.write("ARTIGOS COM FOCO EM IA - POR CATEGORIA\n")
            f.write("-"*80 + "\n\n")
            
            for categoria, arts in sorted(categorias.items(), 
                                          key=lambda x: len(x[1]), 
                                          reverse=True):
                porcentagem = len(arts) / stats['about_ai'] * 100
                f.write(f"### {categoria.upper()} ({len(arts)} artigos - {porcentagem:.1f}%)\n")
                f.write("-"*80 + "\n\n")
                
                for i, art in enumerate(arts, 1):
                    f.write(f"{i}. [{art['year']}] {art['title']}\n")
                    f.write(f"   Journal: {art['journal']}\n")
                    if art['keywords']:
                        f.write(f"   Palavras-chave: {', '.join(art['keywords'][:8])}\n")
                    f.write("\n")
                
                f.write("\n")
        
        # Top periódicos
        f.write("TOP 10 PERIÓDICOS (DADOS CSV)\n")
        f.write("-"*80 + "\n")
        top_periodicos = sorted(dados_csv['periodicos'].items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (periodico, count) in enumerate(top_periodicos, 1):
            f.write(f"{i}. {periodico}: {count} artigos\n")
        f.write("\n\n")
        
        # Top áreas temáticas
        f.write("TOP 10 ÁREAS TEMÁTICAS WoS (DADOS CSV)\n")
        f.write("-"*80 + "\n")
        top_areas = sorted(dados_csv['areas_tematicas'].items(), key=lambda x: x[1], reverse=True)[:10]
        for i, (area, count) in enumerate(top_areas, 1):
            f.write(f"{i}. {area}: {count}\n")
        f.write("\n\n")
        
        f.write("="*80 + "\n")
        f.write("FIM DO RELATÓRIO\n")
        f.write("="*80 + "\n")
    
    print(f"✓ Relatório salvo: {output_path}")

# ============================================================================
# FUNÇÃO PRINCIPAL
# ============================================================================

def main():
    """Função principal"""
    print("\n")
    print("╔" + "="*78 + "╗")
    print("║  ANÁLISE INTEGRADA: ARTIGOS SCIELO COM FOCO EM IA".center(80) + "║")
    print("║  Versão Windows - C:\\Users\\julia\\Downloads".center(80) + "║")
    print("╚" + "="*78 + "╝")
    print("\n")
    
    print(f"Arquivo RIS: {ARQUIVO_RIS}")
    print(f"Diretório de saída: {OUTPUT_DIR}")
    print("\nIniciando análise...")
    
    try:
        # Carregar dados CSV
        dados_csv = carregar_dados_csv()
        
        # Ler e processar arquivo RIS
        records = ler_arquivo_ris(ARQUIVO_RIS)
        if not records:
            print("\nNão foi possível continuar sem o arquivo RIS.")
            print("   Verifique se o arquivo existe em:", ARQUIVO_RIS)
            input("\nPressione ENTER para sair...")
            return
        
        artigos = processar_artigos(records)
        stats = gerar_estatisticas(artigos)
        categorias = categorizar_artigos_ia(artigos)
        
        # Gerar todas as visualizações
        print("\n" + "="*80)
        print("GERANDO VISUALIZAÇÕES")
        print("="*80)
        
        criar_grafico_foco_ia(stats, os.path.join(OUTPUT_DIR, '01_foco_ia_classificacao.png'))
        criar_grafico_publicacoes_ano(artigos, dados_csv, os.path.join(OUTPUT_DIR, '02_publicacoes_por_ano.png'))
        criar_grafico_top_journals(artigos, dados_csv, os.path.join(OUTPUT_DIR, '03a_top10_journals.png'))
        criar_grafico_outros_journals(artigos, dados_csv, os.path.join(OUTPUT_DIR, '03b_outros_journals.png'))
        criar_grafico_idiomas(artigos, os.path.join(OUTPUT_DIR, '04_distribuicao_idiomas.png'))
        criar_grafico_tipo_literatura(artigos, dados_csv, os.path.join(OUTPUT_DIR, '05_tipo_literatura.png'))
        criar_grafico_citavel(dados_csv, os.path.join(OUTPUT_DIR, '06_citavel_naocitavel.png'))
        criar_grafico_indice_citacoes(dados_csv, os.path.join(OUTPUT_DIR, '07_indice_citacoes.png'))
        criar_grafico_areas_tematicas(dados_csv, os.path.join(OUTPUT_DIR, '08a_top10_areas.png'))
        criar_grafico_outras_areas(dados_csv, os.path.join(OUTPUT_DIR, '08b_outras_areas.png'))
        criar_visualizacao_categorias(categorias, stats['about_ai'], 
                                       os.path.join(OUTPUT_DIR, '09_categorias_tematicas_ia.png'))
        
        # Gerar relatório
        gerar_relatorio_detalhado(categorias, artigos, stats, dados_csv, 
                                   os.path.join(OUTPUT_DIR, 'relatorio_completo.txt'))
        
        print("\n" + "="*80)
        print("✓✓✓ ANÁLISE CONCLUÍDA COM SUCESSO! ✓✓✓")
        print("="*80)
        print(f"\nArquivos gerados em: {OUTPUT_DIR}")
        print("\nGRÁFICOS GERADOS (11 no total):")
        print("  01_foco_ia_classificacao.png - Classificação por foco em IA")
        print("  02_publicacoes_por_ano.png - Distribuição temporal")
        print("  03a_top10_journals.png - Top 10 Periódicos")
        print("  03b_outros_journals.png - Periódicos fora do Top 10")
        print("  04_distribuicao_idiomas.png - Distribuição por idioma")
        print("  05_tipo_literatura.png - Tipos de documentos")
        print("  06_citavel_naocitavel.png - Distribuição citável/não citável")
        print("  07_indice_citacoes.png - Índices de citação WoS")
        print("  08a_top10_areas.png - Top 10 Áreas Temáticas")
        print("  08b_outras_areas.png - Áreas Temáticas fora do Top 10")
        print("  09_categorias_tematicas_ia.png - Categorias temáticas (foco IA)")
        print("\nRELATÓRIO:")
        print("  relatorio_completo.txt - Relatório textual detalhado")
        print("\nDICA: Feche as janelas dos gráficos para continuar.")
        print("="*80 + "\n")
        
        # Pausa para ver resultados (Windows)
        input("Pressione ENTER para abrir a pasta de resultados...")
        
        # Abrir pasta de resultados no Explorer
        import subprocess
        subprocess.Popen(f'explorer "{OUTPUT_DIR}"')
        
    except Exception as e:
        print(f"\nERRO: {e}")
        import traceback
        traceback.print_exc()
        input("\nPressione ENTER para sair...")

if __name__ == "__main__":
    main()
