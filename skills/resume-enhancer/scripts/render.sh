#!/usr/bin/env bash
# Render a resume .tex to PDF and enforce a page limit.
# Usage: render.sh <src.tex> <out.pdf> [pages]      pages: 1 (default) or 2
# Exit codes: 0 rendered within the limit; 1 bad arguments, LaTeX error, missing package or over
# the limit (no PDF written); 3 no LaTeX installed. Set PDFLATEX to use a specific binary.
set -euo pipefail

[ $# -ge 2 ] || { echo "usage: render.sh <src.tex> <out.pdf> [pages]"; exit 1; }
SRC="$1"
OUT="$2"
LIMIT="${3:-1}"
case "$LIMIT" in
  1|2) ;;
  *) echo "pages must be 1 or 2, got: $LIMIT"; exit 1 ;;
esac

if [ -z "${PDFLATEX:-}" ]; then
  export PATH="/Library/TeX/texbin:$PATH"   # where the macOS TeX distribution puts it
  PDFLATEX=pdflatex
fi
command -v "$PDFLATEX" >/dev/null 2>&1 || {
  echo "no LaTeX found (looked for $PDFLATEX). See latex.md in the skill folder."
  exit 3
}

BUILD="$(mktemp -d)"
trap 'rm -rf "$BUILD"' EXIT
cp "$SRC" "$BUILD/resume.tex"
if ! (cd "$BUILD" && "$PDFLATEX" -interaction=nonstopmode -halt-on-error resume.tex >/dev/null 2>&1); then
  MISSING=$(sed -n "s/.*File \`\([^']*\)' not found.*/\1/p" "$BUILD/resume.log" 2>/dev/null | head -1)
  if [ -n "$MISSING" ]; then
    echo "missing LaTeX package: $MISSING"
  else
    echo "LaTeX failed:"
    grep -A3 '^!' "$BUILD/resume.log" 2>/dev/null | head -30
  fi
  exit 1
fi

PAGES=$(grep -o 'Output written on resume.pdf ([0-9]* page' "$BUILD/resume.log" | grep -o '[0-9]*' | head -1)
if [ "$PAGES" -gt "$LIMIT" ]; then
  echo "FAIL: rendered $PAGES pages, limit is $LIMIT. Cut content, don't shrink the macros."
  exit 1
fi
OVERFULL=$(grep -c 'Overfull \\hbox' "$BUILD/resume.log" || true)
if [ "$OVERFULL" -gt 0 ]; then
  echo "WARN: $OVERFULL overfull hbox(es), something runs past the right margin:"
  grep 'Overfull \\hbox' "$BUILD/resume.log" | head -5
fi

cp "$BUILD/resume.pdf" "$OUT"
[ "$PAGES" = 1 ] && UNIT=page || UNIT=pages
echo "OK — $PAGES $UNIT -> $OUT"
