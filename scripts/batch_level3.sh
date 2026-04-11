#!/bin/bash
set -euo pipefail
cd /docker/lightrag

TOKEN=$(curl -s -X POST "http://localhost:9621/login" \
  -d "username=admin&password=LightRag@2026!" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

REPOS=(
  "crewaiinc/crewai"
  "langchain-ai/langgraph"
  "mastra-ai/mastra"
  "supabase/supabase"
  "vercel/ai"
  "shadcn-ui/ui"
  "browser-use/browser-use"
  "microsoft/playwright-cli"
  "HKUDS/OpenSpace"
  "karpathy/autoresearch"
  "HKUDS/LightRAG"
  "anthropics/anthropic-cookbook"
)

INCLUDES=(
  "docs/**,README.md,examples/**"
  "docs/**,README.md,examples/**,libs/langgraph/langgraph/**"
  "docs/**,README.md,examples/**,packages/core/src/**"
  "apps/docs/**,README.md,examples/**"
  "docs/**,README.md,examples/**,packages/ai/src/**"
  "apps/www/**,README.md,packages/shadcn/src/**"
  "docs/**,README.md,examples/**,browser_use/**"
  "README.md,src/**,skills/**"
  "README.md,docs/**,openspace/**"
  "README.md,train.py,run.py,*.md"
  "docs/**,README.md,lightrag/**,examples/**"
  "README.md,*.ipynb,misc/**"
)

LOGFILE="/tmp/batch_level3_$(date +%Y%m%d_%H%M%S).log"
echo "=== Batch Level 3 Start: $(date) ===" | tee "$LOGFILE"

for i in "${!REPOS[@]}"; do
  REPO="${REPOS[$i]}"
  INCLUDE="${INCLUDES[$i]}"
  NAME=$(echo "$REPO" | cut -d/ -f2 | tr '[:upper:]' '[:lower:]')
  URL="https://github.com/$REPO"

  echo "" | tee -a "$LOGFILE"
  echo "=== [$((i+1))/${#REPOS[@]}] $REPO ===" | tee -a "$LOGFILE"

  # Step 1: repomix
  echo "  [1] Repomix..." | tee -a "$LOGFILE"
  if ! repomix --remote "$URL" --compress --include "$INCLUDE" -o "/tmp/${NAME}_repomix.txt" >> "$LOGFILE" 2>&1; then
    echo "  WARN: include filter failed, trying full repo" | tee -a "$LOGFILE"
    repomix --remote "$URL" --compress -o "/tmp/${NAME}_repomix.txt" >> "$LOGFILE" 2>&1 || { echo "  FAIL: repomix" | tee -a "$LOGFILE"; continue; }
  fi

  # Step 2: LLM summarize (level 3)
  echo "  [2] LLM summarize..." | tee -a "$LOGFILE"
  if ! python3 scripts/summarize_repo.py "/tmp/${NAME}_repomix.txt" --repo-url "$URL" --output-dir /tmp >> "$LOGFILE" 2>&1; then
    echo "  FAIL: summarize" | tee -a "$LOGFILE"
    continue
  fi

  # Step 3: 旧ドキュメント削除
  echo "  [3] Delete old doc..." | tee -a "$LOGFILE"
  OLD_ID=$(curl -s "http://localhost:9621/documents" -H "Authorization: Bearer $TOKEN" | \
    python3 -c "
import sys,json
for d in json.loads(sys.stdin.read())['statuses']['processed']:
    fp = d.get('file_path','').lower()
    if '${NAME}' in fp and 'level3' not in fp:
        print(d['id']); break
" 2>/dev/null || true)

  if [ -n "$OLD_ID" ]; then
    curl -s -X DELETE "http://localhost:9621/documents/delete_document" \
      -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" \
      -d "{\"doc_ids\": [\"$OLD_ID\"]}" >> "$LOGFILE" 2>&1
    sleep 5
  fi

  # Step 4: 新ドキュメント投入
  echo "  [4] Upload new doc..." | tee -a "$LOGFILE"
  curl -s -X POST "http://localhost:9621/documents/upload" \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@/tmp/${NAME}_lightrag.txt" >> "$LOGFILE" 2>&1
  echo "" >> "$LOGFILE"

  echo "  OK: $REPO" | tee -a "$LOGFILE"
  sleep 10  # レートリミット対策
done

echo "" | tee -a "$LOGFILE"
echo "=== Waiting 120s for processing ===" | tee -a "$LOGFILE"
sleep 120

# インデックス更新
python3 scripts/update_knowledge_index.py | tee -a "$LOGFILE"

# git push
git add -A && git commit -m "Batch level 3 upgrade: 12 repos" && git push

echo "=== Batch Level 3 Complete: $(date) ===" | tee -a "$LOGFILE"
echo "Log: $LOGFILE"
