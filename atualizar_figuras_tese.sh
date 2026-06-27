#!/usr/bin/env bash
#
# atualizar_figuras_tese.sh
# -------------------------
# Regenera as figuras da analise bibliometrica e copia, com os mesmos nomes,
# para os caminhos que os \includegraphics da tese (ex_cap2.tex) referenciam.
#
# Numa sessao com os dois repositorios lado a lado, basta rodar:
#
#     ./atualizar_figuras_tese.sh
#
# Caminho da tese:
#   - default: ../tecno-etnografia-centro-ia (irmao deste repo)
#   - sobrescreva com:  TESE_DIR=/caminho/para/tese ./atualizar_figuras_tese.sh
#
# Opcoes:
#   --skip-install   nao roda pip install -r requirements.txt
#   --skip-generate  nao roda os scripts; so copia as PNGs ja existentes
#
# IMPORTANTE: a lista de figuras abaixo espelha exatamente os caminhos
# referenciados em ex_cap2.tex. Se a tese passar a usar outras figuras
# (ou renomear as pastas), atualize as listas/destinos aqui.

set -euo pipefail

# Diretorio deste repo (onde o script mora), independente de onde foi chamado.
REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$REPO_DIR"

TESE_DIR="${TESE_DIR:-$REPO_DIR/../tecno-etnografia-centro-ia}"
FIG_SRC="$REPO_DIR/figuras"

SKIP_INSTALL=0
SKIP_GENERATE=0
for arg in "$@"; do
  case "$arg" in
    --skip-install)  SKIP_INSTALL=1 ;;
    --skip-generate) SKIP_GENERATE=1 ;;
    *) echo "argumento desconhecido: $arg" >&2; exit 2 ;;
  esac
done

PY="${PYTHON:-python3}"

# --- Destinos na tese (espelham ex_cap2.tex) ------------------------------
# Pasta cap.2/capes-scielo/ : figuras capes_/scielo_/comparativo
# Pasta cap.2/ (raiz)        : figuras openalex_*
# (espelha exatamente os \includegraphics de ex_cap2.tex)
DST_AB="$TESE_DIR/figuras/cap.2/capes-scielo"
DST_OA="$TESE_DIR/figuras/cap.2"

FIG_AB=(
  capes_11_grande_area_share.png
  capes_13_heatmap_area_keyword.png
  capes_21_subcampos_distribuicao.png
  capes_22_heatmap_subcampo_grande_area.png
  capes_h01_areas_humanas.png
  capes_h02_temporal_humanas.png
  scielo_11_subject_area_share.png
  scielo_21_subcampos_distribuicao.png
  comparativo_scielo_capes_2026.png
)
FIG_OA=(
  openalex_01_ranking_paises.png
  openalex_02_taxa_interna_paises.png
  openalex_03_brasil_temporal.png
  openalex_04_subcampos_3bases.png
)

# --- Verificacoes ---------------------------------------------------------
if [ ! -d "$TESE_DIR" ]; then
  echo "ERRO: pasta da tese nao encontrada: $TESE_DIR" >&2
  echo "      defina TESE_DIR=/caminho/para/tecno-etnografia-centro-ia" >&2
  exit 1
fi

# --- 1) Dependencias ------------------------------------------------------
if [ "$SKIP_INSTALL" -eq 0 ]; then
  echo "==> Instalando dependencias (pip install -r requirements.txt)"
  "$PY" -m pip install -r requirements.txt
fi

# --- 2) Geracao das figuras ----------------------------------------------
# Os dumps brutos da CAPES estao em Git LFS; os scripts usam o intermediario
# dados_capes/capes_2021_2024_ia_auditoria.xlsx, que ja esta versionado.
if [ "$SKIP_GENERATE" -eq 0 ]; then
  echo "==> Gerando figuras"
  export MPLBACKEND=Agg
  "$PY" figuras_capes_2021_2024.py
  "$PY" analise_capes_humanas.py
  "$PY" figuras_scielo_articlemeta.py
  "$PY" analise_comparativa_2026.py
  "$PY" figuras_openalex.py
fi

# --- 3) Copia para os caminhos da tese (so PNGs) --------------------------
echo "==> Copiando PNGs para a tese"
mkdir -p "$DST_AB"

copiar() {  # $1 = arquivo, $2 = pasta destino
  local f="$1" dst="$2"
  if [ ! -f "$FIG_SRC/$f" ]; then
    echo "ERRO: figura ausente em $FIG_SRC: $f" >&2
    exit 1
  fi
  cp -f "$FIG_SRC/$f" "$dst/$f"
  echo "   -> ${dst#$TESE_DIR/}/$f"
}

for f in "${FIG_AB[@]}"; do copiar "$f" "$DST_AB"; done
for f in "${FIG_OA[@]}"; do copiar "$f" "$DST_OA"; done

# --- 4) Resumo ------------------------------------------------------------
echo
echo "==> git diff --stat da tese (figuras/cap.2)"
git -C "$TESE_DIR" add -A figuras/cap.2
git -C "$TESE_DIR" --no-pager diff --cached --stat -- figuras/cap.2

echo
echo "Pronto. Revise o diff acima e, se estiver ok, faca o commit/push na tese:"
echo "   git -C \"$TESE_DIR\" commit -m \"Atualiza figuras da analise bibliometrica\""
echo "   git -C \"$TESE_DIR\" push"
# -------------------------------------------------------------------
# Copia as figuras geradas em figuras/ deste repositório para a pasta
# de imagens da tese (repositório tecno-etnografia-centro-ia),
# mantendo exatamente os mesmos nomes de arquivo — assim os
# \includegraphics{...} e \caption{...} do .tex continuam válidos
# sem precisar editar o LaTeX.
#
# Por padrão atualiza SOMENTE as figuras que JÁ existem na tese
# (não despeja arquivos novos que a tese não usa) e copia apenas
# .png (o que o \includegraphics consome). Os .svg são ignorados
# porque mudam a cada execução só por metadados (data/IDs), sem
# diferença visual.
#
# USO:
#   ./atualizar_figuras_tese.sh <pasta_de_figuras_da_tese> [opções]
#
#   Se a pasta não for informada, o script tenta localizar
#   automaticamente uma pasta de figuras dentro de um repositório
#   irmão chamado "tecno-etnografia-centro-ia".
#
# OPÇÕES:
#   --regenerar   Roda os scripts de análise antes de copiar, para
#                 garantir que as figuras estão atualizadas.
#   --svg         Copia também os .svg (além dos .png).
#   --todas       Copia todas as figuras, inclusive as que ainda não
#                 existem na tese (default: só atualiza as existentes).
#   --dry-run     Mostra o que seria feito, sem copiar nada.
#   -h, --help    Mostra esta ajuda.
#
# EXEMPLOS:
#   ./atualizar_figuras_tese.sh ../tecno-etnografia-centro-ia/figuras
#   ./atualizar_figuras_tese.sh --regenerar ../tese/img
#   ./atualizar_figuras_tese.sh --dry-run
# -------------------------------------------------------------------
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIGURAS_SRC="$REPO_DIR/figuras"

DEST=""
REGENERAR=0
COPIAR_SVG=0
COPIAR_TODAS=0
DRY_RUN=0

for arg in "$@"; do
  case "$arg" in
    --regenerar) REGENERAR=1 ;;
    --svg)       COPIAR_SVG=1 ;;
    --todas)     COPIAR_TODAS=1 ;;
    --dry-run)   DRY_RUN=1 ;;
    -h|--help)   sed -n '2,/^set -euo/p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//; /^set -euo/d'; exit 0 ;;
    -*)          echo "Opção desconhecida: $arg" >&2; exit 1 ;;
    *)           DEST="$arg" ;;
  esac
done

# ---------------------------------------------------------------
# 1. Localiza a pasta de figuras da tese
# ---------------------------------------------------------------
if [[ -z "$DEST" ]]; then
  echo "Nenhuma pasta de destino informada — tentando localizar automaticamente..."
  for base in "$REPO_DIR/.." "$REPO_DIR/../.."; do
    cand="$(find "$base" -maxdepth 3 -type d -path '*tecno-etnografia-centro-ia*' \
              \( -iname figuras -o -iname figures -o -iname img -o -iname imagens \) \
              2>/dev/null | head -1 || true)"
    if [[ -n "$cand" ]]; then DEST="$cand"; break; fi
  done
  if [[ -z "$DEST" ]]; then
    echo "ERRO: não encontrei a pasta de figuras da tese automaticamente." >&2
    echo "Informe o caminho: ./atualizar_figuras_tese.sh <pasta_da_tese>" >&2
    exit 1
  fi
  echo "  → encontrada: $DEST"
fi

if [[ ! -d "$DEST" ]]; then
  echo "ERRO: pasta de destino não existe: $DEST" >&2
  exit 1
fi

# ---------------------------------------------------------------
# 2. (Opcional) Regenera as figuras
# ---------------------------------------------------------------
if [[ "$REGENERAR" -eq 1 ]]; then
  echo
  echo "=== Regenerando figuras ==="
  cd "$REPO_DIR"
  python3 -m pip install -q -r requirements.txt
  for script in \
      figuras_capes_2021_2024.py \
      analise_capes_humanas.py \
      figuras_scielo_articlemeta.py \
      analise_comparativa_2026.py \
      figuras_openalex.py; do
    echo "  - $script"
    python3 "$script" >/dev/null 2>&1 || echo "    (aviso: $script falhou — provavelmente faltam dados; seguindo)"
  done
fi

# ---------------------------------------------------------------
# 3. Copia as figuras
# ---------------------------------------------------------------
echo
echo "=== Copiando figuras ==="
echo "  Origem:  $FIGURAS_SRC"
echo "  Destino: $DEST"
[[ "$DRY_RUN" -eq 1 ]] && echo "  (DRY-RUN: nada será copiado)"

exts=("png")
[[ "$COPIAR_SVG" -eq 1 ]] && exts+=("svg")

atualizadas=0
puladas=0

for ext in "${exts[@]}"; do
  for src in "$FIGURAS_SRC"/*."$ext"; do
    [[ -e "$src" ]] || continue
    nome="$(basename "$src")"
    alvo="$DEST/$nome"
    if [[ -e "$alvo" || "$COPIAR_TODAS" -eq 1 ]]; then
      if cmp -s "$src" "$alvo" 2>/dev/null; then
        continue  # idêntico, nada a fazer
      fi
      if [[ "$DRY_RUN" -eq 1 ]]; then
        echo "  [atualizaria] $nome"
      else
        cp "$src" "$alvo"
        echo "  [ok] $nome"
      fi
      atualizadas=$((atualizadas+1))
    else
      puladas=$((puladas+1))
    fi
  done
done

echo
echo "=== Resumo ==="
echo "  Figuras atualizadas/diferentes: $atualizadas"
echo "  Figuras na origem sem par na tese (puladas): $puladas"
echo "    (use --todas para copiar essas também)"

# ---------------------------------------------------------------
# 4. Avisa sobre figuras da tese que não têm origem aqui
# ---------------------------------------------------------------
orfas=0
for alvo in "$DEST"/*.png; do
  [[ -e "$alvo" ]] || continue
  nome="$(basename "$alvo")"
  if [[ ! -e "$FIGURAS_SRC/$nome" ]]; then
    [[ "$orfas" -eq 0 ]] && echo && echo "  Atenção: figuras na tese sem correspondente em figuras/ (não tocadas):"
    echo "    - $nome"
    orfas=$((orfas+1))
  fi
done

echo
echo "Pronto. Revise com:  git -C \"$(dirname "$DEST")\" status --short  (e git diff --stat)"
echo "Depois commit/push no repositório da tese."
