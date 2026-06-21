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
# Pasta cap.2/analise_bibliometrica/ : figuras capes_/scielo_/comparativo
# Pasta cap.2/ (raiz)                : figuras openalex_*
DST_AB="$TESE_DIR/figuras/cap.2/analise_bibliometrica"
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
