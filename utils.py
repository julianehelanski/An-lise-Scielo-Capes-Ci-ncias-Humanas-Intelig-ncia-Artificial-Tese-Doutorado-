# -*- coding: utf-8 -*-
"""
Utilitários compartilhados entre os scripts de análise bibliométrica.

Centraliza:
- Estilo e paleta dos gráficos
- Regex de identificação de IA (com word boundaries)
- Lista de stopwords em português
- Detecção de diretórios de dados/saída em caminhos relativos
"""

import os
import re

import matplotlib.pyplot as plt
import seaborn as sns


# Caminhos relativos ao repositório
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DADOS_SCIELO_DIR = os.path.join(BASE_DIR, 'dados_scielo')
DADOS_CAPES_DIR = os.path.join(BASE_DIR, 'dados_capes')
FIGURAS_DIR = os.path.join(BASE_DIR, 'figuras')


def aplicar_estilo_padrao():
    """Estilo único compartilhado entre todos os gráficos.

    Segue o "padrão Python" enxuto: defaults do matplotlib + grade discreta,
    sem bordas grossas, sem títulos em negrito enfático, sem cores saturadas
    fora da paleta tab10. Pensado para reprodução em texto acadêmico.
    """
    plt.style.use('default')
    sns.set_style("whitegrid")
    # Paleta default do matplotlib (tab10) — sóbria e reconhecível.
    plt.rcParams['axes.prop_cycle'] = plt.cycler(color=plt.cm.tab10.colors)
    plt.rcParams['figure.figsize'] = (10, 6)
    plt.rcParams['figure.facecolor'] = 'white'
    plt.rcParams['axes.facecolor'] = 'white'
    plt.rcParams['savefig.facecolor'] = 'white'
    plt.rcParams['savefig.edgecolor'] = 'none'
    plt.rcParams['figure.dpi'] = 100
    plt.rcParams['savefig.dpi'] = 300
    # Tipografia: fonte sans-serif única, tamanhos consistentes, sem bold.
    plt.rcParams['font.family'] = 'DejaVu Sans'
    plt.rcParams['font.size'] = 10
    plt.rcParams['axes.titlesize'] = 11
    plt.rcParams['axes.labelsize'] = 10
    plt.rcParams['axes.titleweight'] = 'normal'
    plt.rcParams['axes.labelweight'] = 'normal'
    plt.rcParams['legend.fontsize'] = 9
    plt.rcParams['xtick.labelsize'] = 9
    plt.rcParams['ytick.labelsize'] = 9
    # Spines: só esquerda e baixo, padrão de publicação.
    plt.rcParams['axes.spines.top'] = False
    plt.rcParams['axes.spines.right'] = False
    plt.rcParams['axes.grid'] = True
    plt.rcParams['grid.alpha'] = 0.3
    plt.rcParams['grid.linestyle'] = '--'
    plt.rcParams['grid.linewidth'] = 0.5


# Paleta usada por ambos os scripts
CORES_INTERMEDIARIAS = [
    '#E57373',  # 0: Muted Red
    '#FFB74D',  # 1: Muted Orange
    '#81C784',  # 2: Muted Green
    '#64B5F6',  # 3: Muted Blue
    '#BA68C8',  # 4: Muted Purple
    '#FFF176',  # 5: Muted Yellow
    '#F06292',  # 6: Muted Pink
    '#4DB6AC',  # 7: Muted Teal
    '#A1887F',  # 8: Muted Brown
    '#90A4AE',  # 9: Muted Blue-Gray
    '#B0BEC5',  # 10: Light Muted Gray
    '#E0E0E0',  # 11: Very Light Gray
]

# =============================================================================
# Paleta padrão das figuras (decisão de 27/06/2026).
#
# Categórico: Okabe-Ito, à prova de daltonismo. Cada base de dados tem uma
# cor-assinatura; a categoria em foco da tese (Humanas, Antropologia, Brasil)
# usa o magenta de destaque; as demais barras usam cinza neutro.
# Sequencial (heatmaps): "viridis".
# =============================================================================
OKABE_ITO = {
    "preto": "#000000", "laranja": "#E69F00", "azul_claro": "#56B4E9",
    "verde": "#009E73", "amarelo": "#F0E442", "azul": "#0072B2",
    "vermelho": "#D55E00", "roxo": "#CC79A7", "cinza": "#999999",
}
COR_CAPES = "#009E73"       # verde-azulado
COR_SCIELO = "#0072B2"      # azul
COR_OPENALEX = "#D55E00"    # vermelho-alaranjado
COR_DESTAQUE = "#CC79A7"    # magenta: categoria em foco (Humanas/Antropologia/Brasil)
COR_NEUTRO = "#999999"      # cinza: demais
CMAP_SEQUENCIAL = "viridis"  # heatmaps e escalas sequenciais


# =============================================================================
# Subcampos: reconhece que IA, ML, deep learning, LLMs e tecnologias correlatas
# têm genealogias e comunidades epistêmicas distintas. Cada subcampo é definido
# por seu próprio regex; um trabalho pode pertencer a mais de um subcampo
# simultaneamente. A coleção destes subcampos forma o que chamamos de
# "Tecnologias de IA, ML e aprendizado profundo" — rótulo descritivo, não
# afirmação de identidade entre os campos.
# =============================================================================

RE_SUBCAMPO_IA_STRICT = re.compile(
    r'\b('
    r'intelig[êe]ncia\s+artificial|artificial\s+intelligence'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_ML = re.compile(
    r'\b('
    r'machine\s+learning|'
    r'aprendizado\s+de\s+m[áa]quina'
    r')\b',
    flags=re.IGNORECASE,
)

RE_SUBCAMPO_DL = re.compile(
    r'\b('
    r'deep\s+learning|aprendizado\s+profundo|'
    r'redes?\s+neurais|neural\s+networks?'
    r')\b',
    flags=re.IGNORECASE,
)

# Termos inequívocos de LLM/IA generativa.
RE_SUBCAMPO_LLM_STRICT = re.compile(
    r'\b('
    r'llms?|large\s+language\s+models?|'
    r'modelos?\s+de\s+linguagem|'
    r'chatgpt|gpt-\d|'
    r'ia\s+generativa|generative\s+ai'
    r')\b',
    flags=re.IGNORECASE,
)

# 'transformer' tem dois sentidos em inglês: a arquitetura de rede neural
# (LLMs) E o substantivo literal "transformador/transformante" — comum em
# Engenharia Elétrica (equipamento físico) e em textos não-técnicos
# (educação, antropologia, turismo: "social transformer", "potential
# transformer of the context"). Por isso, isolado, dá falso positivo de
# grande magnitude. Só conta como LLM se coocorrer com contexto técnico
# (NLP, attention, BERT, neural, etc.) no mesmo texto.
RE_TRANSFORMER_AMBIGUO = re.compile(r'\btransformer[s]?\b', flags=re.IGNORECASE)
RE_CONTEXTO_NEURAL = re.compile(
    r'\b('
    r'neural|atten[çc][ãa]o|attention|bert|encoder|decoder|'
    r'self-?attention|pre-?train|fine-?tun|embedding|'
    r'deep\s+learning|aprendizado\s+profundo|'
    r'natural\s+language|processamento\s+de\s+linguagem|nlp|'
    r'language\s+model|modelo\s+de\s+linguagem|huggingface'
    r')\b',
    flags=re.IGNORECASE,
)


# Compatibilidade: a constante antiga ainda é usada por alguns lugares.
RE_SUBCAMPO_LLM = RE_SUBCAMPO_LLM_STRICT

RE_SUBCAMPO_CORRELATOS = re.compile(
    r'\b('
    r'transhumanismo|p[óo]s-humanismo|'
    r'rob[óo]tica|rob[ôo]s|'
    r'automa[çc][ãa]o|automation|'
    r'minera[çc][ãa]o\s+de\s+dados|data\s+mining|'
    r'big\s+data|'
    r'vis[ãa]o\s+computacional|computer\s+vision|'
    r'processamento\s+de\s+linguagem\s+natural|natural\s+language\s+processing|nlp'
    r')\b',
    flags=re.IGNORECASE,
)

# Ordem é didática: do mais "alto nível" (IA conceito) até o mais "técnico"
# (correlatos). Os primeiros 4 são canonicamente IA/ML/DL/LLMs; o 5º agrupa
# tecnologias adjacentes que circulam no entorno mas não são equivalentes.
SUBCAMPOS = [
    ("IA em sentido estrito", RE_SUBCAMPO_IA_STRICT),
    ("Aprendizado de máquina (ML)", RE_SUBCAMPO_ML),
    ("Aprendizado profundo & redes neurais", RE_SUBCAMPO_DL),
    ("Modelos de linguagem & IA generativa", RE_SUBCAMPO_LLM),
    ("Tecnologias correlatas (robótica, NLP, big data…)", RE_SUBCAMPO_CORRELATOS),
]

# Subcampos "centrais" (1-4) vs "correlato" (5). Útil para preservar a
# distinção Central / Correlato sem aglutinar IA com ML/DL/LLMs.
SUBCAMPOS_CENTRAIS = [s for s, _ in SUBCAMPOS[:4]]
SUBCAMPO_CORRELATOS = SUBCAMPOS[4][0]


def classificar_subcampos(texto):
    """Retorna o conjunto de subcampos que aparecem no texto.

    Um trabalho pode estar em zero, um ou vários subcampos. A presença
    do conjunto vazio indica que o trabalho não toca o campo coberto
    pelo regex e fica em 'Outros Temas'.

    Regras de co-ocorrência para reduzir falsos positivos:
      - 'transformer' isolado (sem termos técnicos de NN/NLP no mesmo texto)
        NÃO conta para o subcampo LLM. Esta regra evita capturar
        transformadores elétricos (Engenharia) e usos metafóricos do
        substantivo em inglês ("social transformer", "transformer of the
        context").
    """
    if not texto or isinstance(texto, float):
        return set()
    s = str(texto)
    encontrados = {label for label, padrao in SUBCAMPOS if padrao.search(s)}

    # Adendo: se "transformer" aparece e há contexto técnico de NN/NLP,
    # conta como LLM (recupera os ~193 trabalhos com contexto técnico
    # que ficariam de fora pelo regex estrito de LLM).
    if RE_TRANSFORMER_AMBIGUO.search(s) and RE_CONTEXTO_NEURAL.search(s):
        encontrados.add("Modelos de linguagem & IA generativa")

    return encontrados


# 'IA' como sigla. Só conta como central se coocorrer com termo do núcleo
# ou correlatos no mesmo texto (regra de co-ocorrência).
RE_IA_SIGLA = re.compile(r'\b(ia|i\.a\.)\b', flags=re.IGNORECASE)

# Alias retrocompatível: scripts antigos usam RE_IA_FORTE / RE_IA_RELACIONADA.
# RE_IA_NUCLEO agora é derivado: união dos 4 regexes centrais (sem 'transformer'
# isolado, que está na regra de co-ocorrência dentro de classificar_subcampos).
RE_IA_NUCLEO = re.compile(
    r'(' + RE_SUBCAMPO_IA_STRICT.pattern + r')|('
    + RE_SUBCAMPO_ML.pattern + r')|('
    + RE_SUBCAMPO_DL.pattern + r')|('
    + RE_SUBCAMPO_LLM_STRICT.pattern + r')',
    flags=re.IGNORECASE,
)
RE_IA_FORTE = RE_IA_NUCLEO
RE_IA_RELACIONADA = RE_SUBCAMPO_CORRELATOS


def classificar_foco_ia(texto):
    """Classifica um texto em três categorias quanto ao foco no campo.

    Implementação atual delega a classificar_subcampos para garantir
    consistência: se algum subcampo central (1-4) está presente, é
    'Foco Central'; se só correlatos está presente, é 'Correlato'
    (ou Central, se a sigla 'IA' coocorrer com correlatos); se nenhum
    subcampo está presente, é 'Outros Temas'.

    Importante: o rótulo guarda-chuva NÃO afirma que IA, ML, DL, LLMs e
    correlatos são a mesma coisa. Ele apenas agrupa, para fins de
    contagem total, trabalhos que mencionam qualquer uma dessas
    tecnologias.
    """
    if not texto or isinstance(texto, float):
        return 'Outros Temas'
    subc = classificar_subcampos(texto)
    if not subc:
        return 'Outros Temas'
    centrais_presentes = subc & set(SUBCAMPOS_CENTRAIS)
    if centrais_presentes:
        return 'Tecnologias IA/ML/DL - Foco Central'
    # só correlatos: pode virar Central se houver sigla 'IA' coocorrendo
    if RE_IA_SIGLA.search(str(texto)):
        return 'Tecnologias IA/ML/DL - Foco Central'
    return 'Tecnologias IA/ML/DL - Correlato'


# Rótulo guarda-chuva descritivo, sem afirmar identidade entre os campos.
LABEL_GUARDA_CHUVA = "Tecnologias de IA, ML e aprendizado profundo"
LABEL_GUARDA_CHUVA_CURTO = "Tecnologias IA/ML/DL"


# Stopwords em português, expandida. Cobre artigos, preposições, conjunções,
# pronomes, verbos auxiliares mais comuns e termos vazios típicos de títulos
# acadêmicos ("estudo", "análise", "uma", "sobre" etc.).
STOPWORDS_PT = {
    # Artigos e contrações
    'a', 'o', 'as', 'os', 'um', 'uma', 'uns', 'umas',
    'à', 'às', 'ao', 'aos', 'da', 'do', 'das', 'dos',
    'na', 'no', 'nas', 'nos', 'pela', 'pelo', 'pelas', 'pelos',
    'numa', 'num', 'numas', 'nuns', 'duma', 'dum', 'desta', 'deste',
    'desse', 'dessa', 'daquele', 'daquela', 'isto', 'isso', 'aquilo',
    # Preposições e conjunções
    'de', 'em', 'para', 'por', 'com', 'sem', 'sob', 'sobre',
    'entre', 'até', 'após', 'ante', 'desde', 'durante',
    'e', 'ou', 'mas', 'que', 'se', 'como', 'quando', 'onde',
    'porque', 'pois', 'então', 'assim', 'também', 'ainda',
    # Pronomes e demonstrativos
    'eu', 'tu', 'ele', 'ela', 'nós', 'vós', 'eles', 'elas',
    'este', 'esta', 'esse', 'essa', 'aquele', 'aquela',
    'seu', 'sua', 'seus', 'suas', 'meu', 'minha', 'nosso', 'nossa',
    # Verbos auxiliares e cópulas comuns
    'é', 'são', 'foi', 'foram', 'ser', 'sendo', 'sido',
    'estar', 'está', 'estão', 'estava', 'estavam',
    'ter', 'tem', 'têm', 'tinha', 'tinham', 'há', 'havia',
    # Vazios típicos de títulos acadêmicos
    'estudo', 'estudos', 'análise', 'analise',
    'pesquisa', 'pesquisas', 'trabalho', 'trabalhos',
    'sobre', 'através', 'partir', 'contexto', 'caso', 'casos',
    'uso', 'usos', 'utilização', 'utilizacao',
    'investigação', 'investigacao', 'abordagem', 'abordagens',
    'perspectiva', 'perspectivas', 'reflexão', 'reflexoes', 'reflexão',
}


def garantir_diretorio(caminho):
    """Cria o diretório se não existir. Retorna o caminho."""
    os.makedirs(caminho, exist_ok=True)
    return caminho


def num_ptbr(valor) -> str:
    """Inteiro no padrão brasileiro: ponto como separador de milhar.

    Ex.: 5284 -> "5.284", 631 -> "631". Usado nos rótulos das figuras para
    alinhar a notação numérica das imagens ao texto da tese (pt-BR).
    """
    return f"{int(round(valor)):,}".replace(",", ".")


def pct_ptbr(valor, casas: int = 1) -> str:
    """Percentual no padrão brasileiro: vírgula decimal, sem o símbolo '%'.

    Ex.: 40.66 -> "40,7". O caller acrescenta o '%'. Mantém o ponto de milhar
    pt-BR quando houver (ex.: 1234.5 -> "1.234,5").
    """
    return f"{valor:,.{casas}f}".replace(",", "\x00").replace(".", ",").replace("\x00", ".")


def _tick_ptbr(x, pos=None) -> str:
    """Formata um valor de tick de eixo em pt-BR (milhar com ponto, decimal
    com vírgula). Inteiros saem sem casas decimais."""
    if float(x).is_integer():
        return num_ptbr(int(round(x)))
    return f"{x:g}".replace(".", ",")


def eixo_ptbr(ax, eixo: str = "x") -> None:
    """Aplica notação numérica pt-BR aos ticks de um eixo NUMÉRICO.

    Use apenas em eixos contínuos (não categóricos). ``eixo`` aceita
    'x', 'y' ou 'ambos'.
    """
    from matplotlib.ticker import FuncFormatter
    fmt = FuncFormatter(_tick_ptbr)
    if eixo in ("x", "ambos"):
        ax.xaxis.set_major_formatter(fmt)
    if eixo in ("y", "ambos"):
        ax.yaxis.set_major_formatter(fmt)


# ---------------------------------------------------------------------------
# Identidade visual (decisão de 27/06/2026): marcador "bolinha + halo",
# dot plot de Cleveland, dumbbell e estilo editorial (sem eixos/grade/molduras).
# A bolinha é a forma comum a gráficos, bolhas e nós da rede.
# ---------------------------------------------------------------------------
GUIA_COR = "#e9eef2"     # linha-guia sutil
# Tipografia padrão das figuras (decisão de 27/06/2026): sem título embutido
# (a legenda do LaTeX titula), sem negrito, sem preto puro. Texto em cinza
# escuro suave; notas e descritores em cinza médio. Fonte sans-serif única.
_TXT = "#404040"         # rótulos e números (cinza escuro, não preto)
_TXT_FRACO = "#8a8a8a"   # notas, percentuais, descritores de painel
FONTE = "DejaVu Sans"
PONTO_S = 200            # tamanho do marcador
HALO_S = 520             # tamanho do halo
HALO_ALPHA = 0.18


def estilo_editorial(ax, titulo=None, subtitulo=None, nota=None) -> None:
    """Remove molduras/grade/ticks. Sem título embutido: ``titulo`` e
    ``subtitulo``, quando passados, viram descritores discretos (cinza, sem
    negrito) para distinguir painéis; ``nota`` é a legenda curta em itálico.
    O título de fato fica na legenda (caption) do LaTeX."""
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.grid(False)
    if titulo is not None:
        ax.text(0, 1.06, titulo, transform=ax.transAxes, fontsize=10.5,
                color="#5a5a5a")
    if subtitulo is not None:
        ax.text(0, 1.015, subtitulo, transform=ax.transAxes, fontsize=9,
                color=_TXT_FRACO)
    if nota is not None:
        ax.text(0, -0.14, nota, transform=ax.transAxes, fontsize=8.5,
                style="italic", color=_TXT_FRACO)


def _rotulo_num_pct(ax, x, i, num_str, pct_str, mx) -> None:
    # Folga em pontos (não em unidades de dado): o número fica sempre à
    # direita da bolinha, sem encostar, mesmo quando o eixo é curto e o
    # marcador ocupa uma fração grande do intervalo (ex.: painéis do
    # comparativo, com mx pequeno). Sem negrito, em cinza.
    t_num = ax.annotate(num_str, xy=(x, i), xytext=(12, 0),
                        textcoords="offset points", va="center", ha="left",
                        fontsize=10, color=_TXT)
    if pct_str is not None:
        # Ancora o percentual à borda direita real do número (medida no
        # desenho), com folga fixa em pontos: nunca encosta, independe da
        # quantidade de dígitos e da escala do eixo.
        ax.annotate(pct_str, xycoords=t_num, xy=(1, 0.5), xytext=(5, 0),
                    textcoords="offset points", va="center", ha="left",
                    fontsize=9.5, color=_TXT_FRACO)


def dotplot(ax, labels, vals, cores, pcts=None, rotulos=None, halo=False,
            rotulo=True) -> None:
    """Dot plot de Cleveland com halo + linha-guia (marcador-identidade).

    labels: categorias (eixo Y, do menor para o maior). vals: valores.
    cores: cor por ponto (lista) ou cor única (str). pcts: percentuais para o
    rótulo entre parênteses, ou None. rotulos: rótulo principal já formatado
    (ex.: "14,3%") por ponto; se None, usa ``num_ptbr(val)``. Não desenha
    título — combine com ``estilo_editorial``.
    """
    n = len(labels)
    y = list(range(n))
    mx = max(vals) if vals else 1
    if isinstance(cores, str):
        cores = [cores] * n
    for i, v in enumerate(vals):
        ax.plot([0, v], [i, i], color=GUIA_COR, linewidth=1.2, zorder=1)
    if halo:
        ax.scatter(vals, y, s=HALO_S, color=cores, alpha=HALO_ALPHA, zorder=2,
                   edgecolors="none")
    ax.scatter(vals, y, s=PONTO_S, color=cores, zorder=3, edgecolors="white",
               linewidths=1.6)
    if rotulo:
        for i, v in enumerate(vals):
            num = rotulos[i] if rotulos is not None else num_ptbr(v)
            pct = None if pcts is None else f"({pct_ptbr(pcts[i])}%)"
            _rotulo_num_pct(ax, v, i, num, pct, mx)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11, color=_TXT)
    ax.set_xticks([])
    # Folga à esquerda do 0: bolinhas com valor pequeno/zero não são cortadas
    # pela borda do eixo.
    ax.set_xlim(-mx * 0.03, mx * 1.45)
    ax.set_ylim(-0.6, n - 0.4)


def dumbbell(ax, labels, series, cores, sufixo="") -> None:
    """Dumbbell: por categoria, um ponto por série ligado por uma linha.

    labels: categorias (eixo Y). series: dict {nome: [valores por categoria]}.
    cores: dict {nome: cor}. Mantém um eixo X discreto (valores legíveis) com
    grade vertical sutil; usa o mesmo marcador-identidade (sem halo, para não
    poluir a comparação). ``sufixo`` é anexado ao rótulo de cada ponto.
    """
    n = len(labels)
    y = list(range(n))
    nomes = list(series.keys())
    todos = [v for s in series.values() for v in s]
    mx = max(todos) if todos else 1
    for i in range(n):
        pontos = [series[nm][i] for nm in nomes]
        ax.plot([min(pontos), max(pontos)], [i, i], color=GUIA_COR,
                linewidth=2.4, zorder=1, solid_capstyle="round")
    for nm in nomes:
        ax.scatter(series[nm], y, s=150, color=cores[nm], zorder=3,
                   edgecolors="white", linewidths=1.4, label=nm)
    ax.set_yticks(y)
    ax.set_yticklabels(labels, fontsize=11, color=_TXT)
    # Folga à esquerda do 0: bolinhas em valor pequeno/zero não são cortadas.
    ax.set_xlim(-mx * 0.03, mx * 1.12)
    ax.set_ylim(-0.6, n - 0.4)
    for s in ax.spines.values():
        s.set_visible(False)
    ax.tick_params(left=False, bottom=False)
    ax.grid(axis="x", linestyle=":", linewidth=0.6, color="#dddddd", zorder=0)


def bolha_matriz(ax, matriz, cmap=CMAP_SEQUENCIAL, rotulos=False,
                 s_min=40, s_max=900):
    """Matriz como grade de bolinhas (balloon plot) no lugar de heatmap.

    Em cada cruzamento linha×coluna entra uma bolinha cuja ÁREA codifica o
    valor e cuja cor segue ``cmap`` (viridis), reforçando a magnitude.
    Células com valor zero ficam vazias. Mantém a identidade da bolinha sem
    abrir mão do sequencial perceptual. ``matriz`` é um DataFrame (linhas =
    índice, colunas = colunas). Devolve o PathCollection (para colorbar)."""
    rows = list(matriz.index)
    cols = list(matriz.columns)
    vmax = 1.0
    for r in range(len(rows)):
        for c in range(len(cols)):
            vmax = max(vmax, float(matriz.iat[r, c]))
    xs, ys, sizes, vals = [], [], [], []
    for i in range(len(rows)):
        for j in range(len(cols)):
            v = float(matriz.iat[i, j])
            if v <= 0:
                continue
            xs.append(j)
            ys.append(i)
            sizes.append(s_min + (s_max - s_min) * (v / vmax))  # área ∝ valor
            vals.append(v)
    sc = ax.scatter(xs, ys, s=sizes, c=vals, cmap=cmap, zorder=3,
                    edgecolors="white", linewidths=0.8)
    if rotulos:
        for x, y, v in zip(xs, ys, vals):
            ax.annotate(num_ptbr(v), xy=(x, y), xytext=(0, 0),
                        textcoords="offset points", ha="center", va="center",
                        fontsize=6.5, color="white"
                        if v > vmax * 0.55 else _TXT)
    ax.set_xticks(range(len(cols)))
    ax.set_xticklabels(cols, fontsize=9, color=_TXT)
    ax.set_yticks(range(len(rows)))
    ax.set_yticklabels(rows, fontsize=9, color=_TXT)
    ax.set_xlim(-0.6, len(cols) - 0.4)
    ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.invert_yaxis()
    ax.set_axisbelow(True)
    ax.grid(True, color="#eef0f2", linewidth=0.8, zorder=0)
    ax.tick_params(left=False, bottom=False)
    for s in ax.spines.values():
        s.set_visible(False)
    return sc


def salvar_figura(caminho, fig=None, **kwargs):
    """Salva a figura em PNG e SVG usando o caminho como nome-base.

    A figura é identificada pelo nome do arquivo (ex.: ``capes_15_nivel.png``
    e ``capes_15_nivel.svg``), sem título embutido na imagem — a legenda fica
    no texto/LaTeX. Aceita um caminho com ou sem extensão; a extensão é
    substituída por ``.png`` e ``.svg``.

    Args:
        caminho: caminho de saída (a extensão, se houver, é ignorada).
        fig: Figure a salvar; se None, usa a figura atual (``plt``).
        **kwargs: repassados a ``savefig`` (sobrescrevem os padrões).

    Retorna o caminho-base (sem extensão) das figuras salvas.
    """
    base = os.path.splitext(caminho)[0]
    opcoes = dict(dpi=300, bbox_inches='tight', facecolor='white')
    opcoes.update(kwargs)
    alvo = fig if fig is not None else plt
    for ext in ('png', 'svg'):
        alvo.savefig(f'{base}.{ext}', **opcoes)
    return base


def buscar_arquivo(nomes, *diretorios):
    """Procura o primeiro arquivo existente nos diretórios dados.

    Args:
        nomes: lista de nomes possíveis (ex.: ['catalogo.xlsx', 'catalogo.csv']).
        diretorios: diretórios onde buscar, em ordem de prioridade.

    Retorna o caminho absoluto do primeiro arquivo encontrado, ou None.
    """
    for diretorio in diretorios:
        for nome in nomes:
            caminho = os.path.join(diretorio, nome)
            if os.path.isfile(caminho):
                return caminho
    return None
