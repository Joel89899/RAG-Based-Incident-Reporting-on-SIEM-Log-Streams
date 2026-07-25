#!/usr/bin/env bash
# Driver for the SIEM RAG thesis repo.
# Builds the thesis PDF, runs the offline analyses behind its figures/tables,
# and renders a page to PNG for visual verification. Everything here runs
# headless in a clean container -- NO GPU, NO GGUF weights, NO llama-cpp.
# The full LLM pipeline (notebooks) is the GPU path; see SKILL.md.
#
# Usage: driver.sh {build|analyses|figure|verify|all}
# Run from the repo root. Paths below are relative to it.
set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
cd "$ROOT"
THESIS="$ROOT/My_thesis_document"
PY="$ROOT/.venv/bin/python"
OUT="${THESIS_VERIFY_DIR:-/tmp/thesis_verify}"
mkdir -p "$OUT"

hr(){ printf '\n=== %s ===\n' "$1"; }
fail(){ printf 'FAIL: %s\n' "$1" >&2; exit 1; }

build(){
  hr "build thesis PDF (latexmk + biber)"
  command -v latexmk >/dev/null || fail "latexmk not found (apt-get install texlive-full latexmk)"
  cd "$THESIS"
  latexmk -pdf -interaction=nonstopmode main.tex >"$OUT/build.log" 2>&1
  local rc=$?
  cd "$ROOT"
  [ $rc -eq 0 ] || { tail -20 "$OUT/build.log"; fail "latexmk exit $rc"; }
  local undef pages
  undef=$(grep -ic undefined "$THESIS/main.log")
  pages=$(pdfinfo "$THESIS/main.pdf" 2>/dev/null | awk '/Pages/{print $2}')
  echo "PDF: $THESIS/main.pdf | pages=$pages | undefined-refs=$undef"
  [ "$undef" = "0" ] || fail "$undef undefined references (see $THESIS/main.log)"
  [ "${pages:-0}" -ge 100 ] || fail "only $pages pages -- build likely truncated"
}

analyses(){
  hr "offline analyses (no GPU, reads saved results/)"
  [ -x "$PY" ] || fail "venv missing; see SKILL.md Prerequisites"
  "$PY" revision_scripts/cicids_unscoped_rerank_baseline.py 2>/dev/null | tail -3 \
    || fail "ablation script failed"
  "$PY" revision_scripts/cicids_multilabel_check.py 2>/dev/null | tail -3 \
    || fail "multilabel check failed"
}

figure(){
  hr "regenerate quadrant figure"
  "$PY" revision_scripts/make_quadrant_figure.py 2>/dev/null | tail -1 \
    || fail "figure script failed"
}

verify(){
  hr "render a PDF page to PNG (visual check)"
  [ -f "$THESIS/main.pdf" ] || fail "no main.pdf; run 'build' first"
  pdftoppm -f 79 -l 79 -r 80 -png "$THESIS/main.pdf" "$OUT/page" \
    || fail "pdftoppm failed (apt-get install poppler-utils)"
  echo "wrote $OUT/page-079.png  -- open it and confirm the quadrant figure renders"
}

case "${1:-all}" in
  build)    build ;;
  analyses) analyses ;;
  figure)   figure ;;
  verify)   verify ;;
  all)      build; analyses; figure; verify; hr "all steps passed" ;;
  *) echo "usage: driver.sh {build|analyses|figure|verify|all}"; exit 2 ;;
esac
