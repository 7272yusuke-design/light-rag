#!/bin/bash
# Usage: ./search_knowledge.sh "検索クエリ" [mode] [project]
# mode: hybrid(default), naive, local, global, mix
# project: openclaw, virtual-protocol, website, webapp, workflow
set -euo pipefail
QUERY="${1:?Usage: $0 <query> [mode] [project]}"
MODE="${2:-hybrid}"
PROJECT="${3:-}"
API="http://localhost:9621"
USER="admin"
PASS="LightRag@2026!"
PROFILE_DIR="/docker/lightrag/config/project_profiles.json"

# プロジェクト指定時はコンテキストをクエリに付加
if [ -n "$PROJECT" ] && [ -f "$PROFILE_DIR" ]; then
  CONTEXT=$(python3 -c "
import json
with open('$PROFILE_DIR') as f:
    profiles = json.load(f)
p = profiles.get('$PROJECT', {})
if p:
    print(p.get('context', ''))
")
  if [ -n "$CONTEXT" ]; then
    QUERY="[プロジェクト文脈: $CONTEXT] $QUERY"
    echo ">>> プロジェクト '$PROJECT' のコンテキストを付加" >&2
  fi
fi

TOKEN=$(curl -s -X POST "$API/login" \
  -d "username=$USER&password=$PASS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -s -X POST "$API/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "$(python3 -c "import json; print(json.dumps({'query': '''$QUERY''', 'mode': '$MODE'}))")" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('response', json.dumps(data, ensure_ascii=False, indent=2)))
"
