#!/usr/bin/env bash
#
# atualizar_figuras_tese.sh
# -------------------------------------------------------------------
# Copia as figuras de uma pasta de ORIGEM para a pasta de imagens da
# tese (repositório tecno-etnografia-centro-ia), mantendo exatamente
# os mesmos nomes de arquivo — assim os \includegraphics{...} e
# \caption{...} do .tex continuam válidos sem editar o LaTeX.
#
# Serve para qualquer análise cujas figuras sejam consumidas pela tese:
#   - bibliometria (este repo, origem default = ./figuras)
#   - lexicometria (repo analise-figuracoes-latour, via --origem)
#
# Por padrão atualiza SOMENTE as figuras que JÁ existem na tese
# (não despeja arquivos novos que a tese não usa) e copia apenas
# .png (o que o \includegraphics consome). Os .svg são ignorados
# porque mudam a cada execução só por metadados (data/IDs), sem
# diferença visual.
#
# USO:
#   ./atualizar_figuras_tese.sh [pasta_de_figuras_da_tese] [opções]
#
#   Se a pasta da tese não for informada, o script tenta localizar
#   automaticamente uma pasta de figuras dentro de um repositório
#   irmão chamado "tecno-etnografia-centro-ia".
#
# OPÇÕES:
#   --origem DIR  Pasta de figuras de origem (default: ./figuras deste
#                 repo). Use para copiar de outra análise, p. ex. a
#                 lexicométrica em analise-figuracoes-latour.
#   --regenerar   Roda os scripts de análise deste repo antes de copiar.
#                 Só vale para a origem default (bibliometria); para
#                 outra origem, regenere as figuras no repo de origem
#                 antes de rodar este script.
#   --svg         Copia também os .svg (além dos .png).
#   --todas       Copia todas as figuras, inclusive as que ainda não
#                 existem na tese (default: só atualiza as existentes).
#   --dry-run     Mostra o que seria feito, sem copiar nada.
#   -h, --help    Mostra esta ajuda.
#
# EXEMPLOS:
#   # bibliometria -> tese
#   ./atualizar_figuras_tese.sh --regenerar ../tecno-etnografia-centro-ia/figuras
#   # lexicometria -> tese
#   ./atualizar_figuras_tese.sh \
#       --origem ../analise-figuracoes-latour/figuras \
#       ../tecno-etnografia-centro-ia/figuras
# -------------------------------------------------------------------
set -euo pipefail

REPO_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
FIGURAS_SRC_DEFAULT="$REPO_DIR/figuras"
FIGURAS_SRC="$FIGURAS_SRC_DEFAULT"

DEST=""
REGENERAR=0
COPIAR_SVG=0
COPIAR_TODAS=0
DRY_RUN=0

while [[ $# -gt 0 ]]; do
  case "$1" in
    --origem)    FIGURAS_SRC="$(cd "$2" 2>/dev/null && pwd || echo "$2")"; shift 2 ;;
    --regenerar) REGENERAR=1; shift ;;
    --svg)       COPIAR_SVG=1; shift ;;
    --todas)     COPIAR_TODAS=1; shift ;;
    --dry-run)   DRY_RUN=1; shift ;;
    -h|--help)   sed -n '2,/^set -euo/p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//; /^set -euo/d'; exit 0 ;;
    -*)          echo "Opção desconhecida: $1" >&2; exit 1 ;;
    *)           DEST="$1"; shift ;;
  esac
done

if [[ ! -d "$FIGURAS_SRC" ]]; then
  echo "ERRO: pasta de origem não existe: $FIGURAS_SRC" >&2
  exit 1
fi

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
if [[ "$REGENERAR" -eq 1 && "$FIGURAS_SRC" != "$FIGURAS_SRC_DEFAULT" ]]; then
  echo
  echo "AVISO: --regenerar só vale para a origem default (bibliometria)."
  echo "       Para a origem '$FIGURAS_SRC', regenere as figuras no repo de"
  echo "       origem antes de rodar este script. Pulando regeneração."
  REGENERAR=0
fi

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
