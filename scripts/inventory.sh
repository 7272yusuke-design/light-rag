#!/bin/bash
# LightRAG ナレッジベース棚卸し（ハイブリッド版 v2 2026-07-07）
# AUTO区画のみ自動更新、手動エリアは保護される
# 使い方: bash /docker/lightrag/scripts/inventory.sh
set -e
cd /docker/lightrag
OUT=/docker/lightrag/docs/KNOWLEDGE-INDEX.md
AUTO=$(mktemp)
DATE=$(date +%Y-%m-%d)

PSQL="docker compose exec -T postgres psql -U lightrag -d lightrag -tAc"

# 実運用整合性: doc_full / doc_status / processed
DOCFULL=$($PSQL "SELECT count(*) FROM lightrag_doc_full;")
DOCSTATUS=$($PSQL "SELECT count(*) FROM lightrag_doc_status;")
PROCESSED=$($PSQL "SELECT count(*) FROM lightrag_doc_status WHERE status='processed';")
UNPROCESSED=$($PSQL "SELECT count(*) FROM lightrag_doc_status WHERE status<>'processed';")
# 旧指標（グラフ側）も併記
GRAPH=$($PSQL "SELECT (SELECT count(*) FROM lightrag_full_entities) || '/' || (SELECT count(*) FROM lightrag_full_relations);")

# 未処理エントリの明細
UNPROC_LIST=$($PSQL "SELECT '- \`' || file_path || '\` (status: ' || status || ', updated: ' || to_char(updated_at,'YYYY-MM-DD') || ')' FROM lightrag_doc_status WHERE status<>'processed' ORDER BY updated_at;")

# レイヤー別件数 + 全エントリ
LAYER_CASE="CASE
    WHEN file_path LIKE '%-l3_%' THEN 'L3'
    WHEN file_path LIKE '%-l2c_%' THEN 'L2c'
    WHEN file_path LIKE '%-l2_%' THEN 'L2'
    WHEN file_path LIKE '%-l1-%' THEN 'L1'
    WHEN file_path LIKE '%-l0_%' THEN 'L0'
    ELSE 'UNKNOWN'
  END"
COUNTS=$($PSQL "SELECT ${LAYER_CASE} AS layer, count(*) FROM lightrag_doc_status GROUP BY 1 ORDER BY 1;")
ENTRIES=$($PSQL "SELECT ${LAYER_CASE} AS layer, file_path FROM lightrag_doc_status ORDER BY 1, 2;")

# ---- AUTO区画の中身を生成 ----
{
  echo "<!-- AUTO:START (このマーカー間は inventory.sh が上書きする。手動編集禁止) -->"
  echo "# KNOWLEDGE-INDEX (LightRAG 蓄積済み 全${DOCFULL}件)"
  echo ""
  echo "> 自動生成エリア。\`bash /docker/lightrag/scripts/inventory.sh\` で更新。"
  echo "> 最終更新: ${DATE}"
  echo "> 整合性: doc_full=${DOCFULL} / doc_status=${DOCSTATUS} / processed=${PROCESSED} (未処理=${UNPROCESSED})"
  echo "> グラフ側 (entities/relations): ${GRAPH}"
  echo ""
  if [ "$UNPROCESSED" != "0" ]; then
    echo "## ⚠️ 未処理エントリ（processed以外）"
    echo ""
    echo "$UNPROC_LIST"
    echo ""
  fi
  echo "## レイヤー別件数"
  echo ""
  echo "| レイヤー | 件数 |"
  echo "|---------|------|"
  echo "$COUNTS" | while IFS='|' read -r layer cnt; do
    [ -z "$layer" ] && continue
    echo "| ${layer} | ${cnt} |"
  done
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
  echo ""
  echo "<!-- AUTO:END -->"
} > $AUTO

# ---- 出力: 既存ファイルにAUTO区画があれば差し替え、なければ手動エリア雛形付きで新規生成 ----
if [ -f "$OUT" ] && grep -q "<!-- AUTO:START" "$OUT"; then
  # AUTO区画だけ差し替え（手動エリア保護）
  TMP_OUT=$(mktemp)
  awk -v autofile="$AUTO" '
    /<!-- AUTO:START/ { while ((getline line < autofile) > 0) print line; skip=1; next }
    /<!-- AUTO:END -->/ { skip=0; next }
    skip != 1 { print }
  ' "$OUT" > "$TMP_OUT"
  mv "$TMP_OUT" "$OUT"
else
  # 初回: AUTO区画 + 手動エリア雛形
  {
    cat $AUTO
    echo ""
    echo "---"
    echo ""
    echo "<!-- MANUAL: 以下は手動エリア。inventory.sh は触らない -->"
    echo ""
    echo "# 手動管理エリア"
    echo ""
    echo "## 既知の未処理・異常（原因が判明しているもの）"
    echo ""
    echo "- \`last30days-skill-l3_lightrag.txt\` = failed（2026-06-21、OpenRouterクレジット枯渇でグラフ抽出未完走。本文は投入済み。クレジット復活後に再処理で221/221に揃う）"
    echo ""
    echo "## 重複要調査リスト"
    echo ""
    echo "- [ ] superpowers 系の複数エントリ"
    echo "- [ ] ComfyUI 系の複数エントリ"
    echo "- [ ] RAG 系の複数エントリ"
    echo "- [ ] n8n 系の複数エントリ"
    echo ""
    echo "## L2c→L2 昇格ウォッチ（pull型: 実案件で使ったら昇格検討）"
    echo ""
    echo "- 現状昇格0件（2026-06-13レビューで全26件が verified:self 未達）"
    echo ""
    echo "## 棚卸しメモ・DECISIONS.mdアンカー"
    echo ""
    echo "- 全評価履歴: \`docs/KNOWLEDGE-DECISIONS.md\`"
    echo "- 投入ルール: \`docs/DATA-SCHEMA.md\`（verified定義D、L2c昇格手順は \`L2C-PROMOTION-PROCEDURE.md\`）"
  } > "$OUT"
fi

rm -f $AUTO
echo "Updated: $OUT"
echo "Total: ${DOCFULL} docs / Integrity: full=${DOCFULL} status=${DOCSTATUS} processed=${PROCESSED} / graph=${GRAPH}"
