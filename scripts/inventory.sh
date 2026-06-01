#!/bin/bash
# LightRAG ナレッジベース棚卸し
# 出力: /docker/lightrag/docs/KNOWLEDGE-INDEX.md
# 使い方: bash /docker/lightrag/scripts/inventory.sh

set -e
cd /docker/lightrag

OUT=/docker/lightrag/docs/KNOWLEDGE-INDEX.md
TMP=$(mktemp)
DATE=$(date +%Y-%m-%d)

# 整合性チェック
INTEGRITY=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "SELECT (SELECT count(*) FROM lightrag_doc_full) || '/' || (SELECT count(*) FROM lightrag_full_entities) || '/' || (SELECT count(*) FROM lightrag_full_relations);")

# レイヤー別件数
docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "
SELECT
  CASE
    WHEN file_path LIKE '%-l3_%' THEN 'L3'
    WHEN file_path LIKE '%-l2c_%' THEN 'L2c'
    WHEN file_path LIKE '%-l2_%' THEN 'L2'
    WHEN file_path LIKE '%-l1-%' THEN 'L1'
    ELSE 'UNKNOWN'
  END AS layer,
  count(*)
FROM lightrag_doc_status
GROUP BY 1
ORDER BY layer;
" > $TMP

TOTAL=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "SELECT count(*) FROM lightrag_doc_full;")

# 全エントリ取得（レイヤー別）
ENTRIES=$(docker compose exec -T postgres psql -U lightrag -d lightrag -tAc "
SELECT
  CASE
    WHEN file_path LIKE '%-l3_%' THEN 'L3'
    WHEN file_path LIKE '%-l2c_%' THEN 'L2c'
    WHEN file_path LIKE '%-l2_%' THEN 'L2'
    WHEN file_path LIKE '%-l1-%' THEN 'L1'
    ELSE 'UNKNOWN'
  END AS layer,
  file_path
FROM lightrag_doc_status
ORDER BY 1, file_path;
")

{
  echo "# KNOWLEDGE-INDEX (LightRAG 蓄積済み 全${TOTAL}件)"
  echo ""
  echo "> 自動生成ファイル。\`bash /docker/lightrag/scripts/inventory.sh\` で更新。"
  echo "> 最終更新: ${DATE}"
  echo "> 整合性 (docs/entities/relations): ${INTEGRITY}"
  echo ""
  echo "## レイヤー別件数"
  echo ""
  echo "| レイヤー | 件数 |"
  echo "|---------|------|"
  while IFS='|' read -r layer cnt; do
    [ -z "$layer" ] && continue
    echo "| ${layer} | ${cnt} |"
  done < $TMP
  echo ""
  echo "---"
  echo ""

  CURRENT_LAYER=""
  echo "$ENTRIES" | while IFS='|' read -r layer file_path; do
    [ -z "$layer" ] && continue
    if [ "$layer" != "$CURRENT_LAYER" ]; then
      echo ""
      echo "## ${layer}"
      echo ""
      CURRENT_LAYER="$layer"
    fi
    echo "- \`${file_path}\`"
  done
} > $OUT

rm -f $TMP
echo "Updated: $OUT"
echo "Total: ${TOTAL} docs / Integrity: ${INTEGRITY}"
