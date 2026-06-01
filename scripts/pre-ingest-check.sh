#!/bin/bash
# LightRAG 投入前チェック
# 使い方: bash /docker/lightrag/scripts/pre-ingest-check.sh <投入予定ファイルパス>

set -e

FILE="$1"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "ERROR: ファイル指定なし or 存在しない: $FILE"
  echo "使い方: bash $0 <投入予定ファイル.txt>"
  exit 1
fi

cd /docker/lightrag

FNAME=$(basename "$FILE")
ERRORS=0
WARNS=0

echo "=== 投入前チェック: $FNAME ==="
echo ""

# 1. ファイル名規則チェック
echo "[1] ファイル名規則"
if [[ "$FNAME" =~ -l[0-9]+(c)?(-[a-z]+)?_lightrag\.txt$ ]]; then
  echo "  OK: レイヤー接尾辞あり"
else
  echo "  ERROR: レイヤー接尾辞 (-l3_, -l2_, -l2c_, -l1-infra_, -l1-ops_) が無い"
  ERRORS=$((ERRORS+1))
fi
echo ""

# 2. ファイル名衝突
echo "[2] ファイル名衝突"
EXIST=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "SELECT count(*) FROM lightrag_doc_status WHERE file_path = '$FNAME';")
if [ "$EXIST" = "0" ]; then
  echo "  OK: 同名なし"
else
  echo "  ERROR: 同じファイル名が既にDB内に存在 ($EXIST件)"
  ERRORS=$((ERRORS+1))
fi
echo ""

# 3. タイトル(表示名)取得・衝突確認
echo "[3] 表示名衝突"
TITLE=$(grep -m1 '^# ' "$FILE" | sed 's/^# //')
if [ -z "$TITLE" ]; then
  echo "  ERROR: 1行目が '# タイトル' 形式でない"
  ERRORS=$((ERRORS+1))
else
  echo "  タイトル: $TITLE"
  CONFLICT=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "SELECT count(*) FROM lightrag_doc_full WHERE content LIKE '# ${TITLE}%';")
  if [ "$CONFLICT" = "0" ]; then
    echo "  OK: 表示名衝突なし"
  else
    echo "  WARN: 同じ表示名のエントリが存在 ($CONFLICT件)"
    WARNS=$((WARNS+1))
  fi
fi
echo ""

# 4. URL重複チェック
echo "[4] URL重複"
URL=$(grep -oE 'https?://[^ )]+' "$FILE" | head -1)
if [ -z "$URL" ]; then
  echo "  WARN: URLが見つからない (URL不要なエントリなら無視可)"
  WARNS=$((WARNS+1))
else
  echo "  URL: $URL"
  URL_ESC=$(echo "$URL" | sed "s/'/''/g")
  DUPE=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "SELECT count(*) FROM lightrag_doc_full WHERE content LIKE '%${URL_ESC}%';")
  if [ "$DUPE" = "0" ]; then
    echo "  OK: 同URLなし"
  else
    echo "  WARN: 同じURLを含むエントリが既存 ($DUPE件) → 観点が違うか確認 (MEMORY-NOTATION-RULES.md §6)"
    WARNS=$((WARNS+1))
  fi
fi
echo ""

# 5. タグ行存在チェック
echo "[5] タグ行"
if grep -qE '^- タグ: ' "$FILE"; then
  TAGS=$(grep -m1 '^- タグ: ' "$FILE" | sed 's/^- タグ: //')
  echo "  OK: タグあり ($TAGS)"
else
  echo "  ERROR: '- タグ: ' 行がない"
  ERRORS=$((ERRORS+1))
fi
echo ""

echo "=== 結果 ==="
echo "ERROR: $ERRORS / WARN: $WARNS"
if [ $ERRORS -gt 0 ]; then
  echo "投入NG: ERRORを解決してください"
  exit 1
else
  echo "投入OK"
  exit 0
fi
