#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")" && pwd)"
OUT="$ROOT/rendered"

if ! command -v mmdc >/dev/null 2>&1; then
  echo "mmdc not found. Install @mermaid-js/mermaid-cli first." >&2
  exit 1
fi

mkdir -p "$OUT"

for src in "$ROOT"/F*.mmd; do
  base="$(basename "$src" .mmd)"
  echo "render: $base"
  mmdc     --input "$src"     --output "$OUT/$base.svg"     --backgroundColor transparent
done

echo "rendered SVG files: $OUT"
