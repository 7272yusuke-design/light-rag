#!/bin/bash
# Usage: ./measure_search.sh <label> <query> <mode> <output_dir>
# 5回 search_knowledge を実行して、全レスポンスを保存する
# 中央値計算は別スクリプト (compute_median.py) で行う
set -euo pipefail

LABEL="${1:?Usage: $0 <label> <query> <mode> <output_dir>}"
QUERY="${2:?query required}"
MODE="${3:?mode required}"
OUTDIR="${4:?output_dir required}"

mkdir -p "$OUTDIR"

echo ">>> [$LABEL] query='$QUERY' mode='$MODE' x5回実行" >&2

for i in 1 2 3 4 5; do
  OUTFILE="${OUTDIR}/${LABEL}_run${i}.json"
  PAYLOAD=$(python3 -c "
import json
print(json.dumps({
    'jsonrpc': '2.0',
    'id': $i,
    'method': 'tools/call',
    'params': {
        'name': 'search_knowledge',
        'arguments': {'query': '''$QUERY''', 'mode': '$MODE'}
    }
}))
")
  curl -s -X POST http://localhost:9622/mcp \
    -H "Content-Type: application/json" \
    -H "Accept: application/json, text/event-stream" \
    -d "$PAYLOAD" \
    > "$OUTFILE"
  
  # サイズ確認(0バイトや異常を即検知)
  SIZE=$(stat -c %s "$OUTFILE")
  echo "  run${i}: ${SIZE} bytes -> ${OUTFILE}" >&2
  
  # サーバ負荷を考慮して間隔を空ける
  sleep 1
done

echo ">>> 完了" >&2
