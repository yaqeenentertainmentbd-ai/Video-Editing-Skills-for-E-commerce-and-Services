#!/usr/bin/env bash
# Per-user font install for macOS and Linux. No sudo needed. Never downloads anything.
# Usage: bash Scripts/install_fonts.sh [--legacy]
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
case "$(uname -s)" in
  Darwin) DEST="$HOME/Library/Fonts" ;;
  Linux)  DEST="${XDG_DATA_HOME:-$HOME/.local/share}/fonts/video-editing" ;;
  *) echo "Unsupported OS $(uname -s)"; exit 1 ;;
esac
mkdir -p "$DEST"
find "$ROOT/Fonts" -name '*.ttf' | while read -r f; do
  case "$f" in *Legacy_v1_*) [ "${1:-}" = "--legacy" ] || continue ;; esac
  b="$(basename "$f")"
  if [ -e "$DEST/$b" ]; then
    cmp -s "$f" "$DEST/$b" && echo "skip (identical) $b" || echo "WARNING: $b exists with different content, not overwriting"
  else
    cp "$f" "$DEST/$b" && echo "installed $b"
  fi
done
if [ "$(uname -s)" = "Linux" ]; then fc-cache -f "$DEST"; fi
echo "Done. Restart editing apps, then run: python3 Scripts/verify_fonts.py"
