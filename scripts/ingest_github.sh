#!/bin/bash
set -euo pipefail

REPO_URL="${1:?Usage: $0 <GitHub URL>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="/tmp/lightrag_ingest"
OBSIDIAN_DIR="${SCRIPT_DIR}/../obsidian-export"

mkdir -p "$WORK_DIR"

REPO_NAME=$(echo "$REPO_URL" | sed 's|.*/||;s|\.git$||' | tr '[:upper:]' '[:lower:]')
REPOMIX_OUT="$WORK_DIR/${REPO_NAME}_repomix.md"

echo "=== [1/4] Repomix: リポジトリをテキスト化 ==="
repomix --remote "$REPO_URL" --compress --style markdown -o "$REPOMIX_OUT"

echo ""
echo "=== [2/4] LLM: 構造化要約を生成 ==="
PATHS_JSON=$(python3 "$SCRIPT_DIR/summarize_repo.py" "$REPOMIX_OUT" --repo-url "$REPO_URL" --output-dir "$WORK_DIR")
LIGHTRAG_TEXT=$(echo "$PATHS_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['lightrag_text'])")
META_JSON=$(echo "$PATHS_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['meta_json'])")

echo ""
echo "=== [3/4] LightRAG: 知識DBに投入 ==="
python3 "$SCRIPT_DIR/submit_to_lightrag.py" "$LIGHTRAG_TEXT"

echo ""
echo "=== [4/4] Obsidian: 学習用MD出力 ==="
python3 "$SCRIPT_DIR/export_obsidian.py" "$META_JSON" -o "$OBSIDIAN_DIR"

echo ""
echo "=== 完了 ==="
echo "LightRAG投入テキスト: $LIGHTRAG_TEXT"
echo "Obsidian MD: $OBSIDIAN_DIR/$REPO_NAME/"
