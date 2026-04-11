#!/bin/bash
set -euo pipefail
REPO_URL="${1:?Usage: $0 <GitHub URL>}"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
WORK_DIR="/tmp/lightrag_ingest"
OBSIDIAN_DIR="${SCRIPT_DIR}/../obsidian-export"
mkdir -p "$WORK_DIR"
REPO_NAME=$(echo "$REPO_URL" | sed 's|.*/||;s|\.git$||' | tr '[:upper:]' '[:lower:]')
REPOMIX_OUT="$WORK_DIR/${REPO_NAME}_repomix.md"

echo "=== [1/5] Repomix: リポジトリをテキスト化 ==="
repomix --remote "$REPO_URL" --compress --style markdown \
  --ignore "**/*.test.*,**/*.spec.*,**/tests/**,**/test/**,**/__tests__/**,**/cassettes/**,**/fixtures/**,**/node_modules/**,**/*.yaml,**/*.yml,**/dist/**,**/build/**,.git/**" \
  -o "$REPOMIX_OUT"

echo ""
echo "=== [2/5] LLM: 構造化要約を生成 ==="
PATHS_JSON=$(python3 "$SCRIPT_DIR/summarize_repo.py" "$REPOMIX_OUT" --repo-url "$REPO_URL" --output-dir "$WORK_DIR")
LIGHTRAG_TEXT=$(echo "$PATHS_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['lightrag_text'])")
META_JSON=$(echo "$PATHS_JSON" | python3 -c "import sys,json; print(json.load(sys.stdin)['meta_json'])")

echo ""
echo "=== [3/5] LightRAG: 知識DBに投入 ==="
python3 "$SCRIPT_DIR/submit_to_lightrag.py" "$LIGHTRAG_TEXT"

echo ""
echo "=== [4/5] Obsidian: 学習用MD出力 ==="
python3 "$SCRIPT_DIR/export_obsidian.py" "$META_JSON" -o "$OBSIDIAN_DIR"

echo ""
echo "=== [5/5] SKILL.md: エージェント用スキル定義を生成 ==="
SKILL_DIR="${SCRIPT_DIR}/../skills-export"
mkdir -p "$SKILL_DIR"
bash "$SCRIPT_DIR/generate_skill.sh" "$META_JSON" -o "$SKILL_DIR" || echo "WARN: SKILL.md生成をスキップ"

echo ""
echo "=== Git: 変更をpush ==="
cd /docker/lightrag
git add obsidian-export/ skills-export/
git commit -m "knowledge: add ${REPO_NAME}" || echo "No changes to commit"
git push || echo "WARN: git push failed"

echo ""
echo "=== 完了 ==="

# ナレッジインデックス自動更新
python3 /docker/lightrag/scripts/update_knowledge_index.py
