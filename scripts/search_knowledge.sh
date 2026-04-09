#!/bin/bash
# Usage: ./search_knowledge.sh "検索クエリ" [mode]
# mode: hybrid(default), naive, local, global, mix
set -euo pipefail

QUERY="${1:?Usage: $0 <query> [mode]}"
MODE="${2:-hybrid}"
API="http://localhost:9621"
USER="admin"
PASS="LightRag@2026!"

TOKEN=$(curl -s -X POST "$API/login" \
  -d "username=$USER&password=$PASS" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])")

curl -s -X POST "$API/query" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d "{\"query\":\"$QUERY\", \"mode\":\"$MODE\"}" | python3 -c "
import sys, json
data = json.load(sys.stdin)
print(data.get('response', json.dumps(data, ensure_ascii=False, indent=2)))
"
