# LightRAG検索運用ルール v1.0

> **作成日**: 2026-05-10
> **目的**: 検索結果10件上限の構造的制約への運用回避策
> **背景**: ナレッジ163件に対し1検索10件まで → 広いクエリでは取りこぼし

---

## 1. 制約の整理

| 項目 | 値 |
|------|---|
| 総ナレッジ件数 | 163件(2026-05-10時点) |
| 1検索の最大返却件数 | 10件 |
| 取りこぼしリスク | 全体の94%のエントリが1検索で見えない |

---

## 2. 運用ルール

### 2.1 クエリの粒度を絞る

❌ **悪い例**: 「自動化」「AI」「RAG」などの広すぎる単語1つ
✅ **良い例**: 「n8nワークフロー設計パターン」「LightRAG ingestion mode」など複合語

### 2.2 観点を変えた複数検索

1検索で全部出ないことを前提に、**3〜5回検索を繰り返す**:

- 1回目: 直接的な単語(例: "n8n")
- 2回目: 類似語(例: "workflow automation")
- 3回目: 関連技術(例: "webhook integration")
- 4回目: パターン名(例: "self-improving agent")
- 5回目: タグ単独(例: "cron-driven")

### 2.3 レイヤー別フィルタの活用

L3(部品)を探すかL2(パターン)を探すかで戦略が変わる:

- **実装で具体的なライブラリが欲しい** → L3を狙う(例: "n8n-l3")
- **設計の組み合わせ方が知りたい** → L2を狙う(例: "n8n-workflow-design-patterns")
- **検証中の候補を見たい** → L2cを狙う(例: "rag-retrieval-quality-l2c")

### 2.4 ファイル名直撃検索

特定エントリが既に存在しそうなときは、ファイル名そのもの(または推定形)で検索:

- `n8n-workflow-design-patterns-l2_lightrag.txt`
- リポジトリ名+`-l3_`(例: `obsidian-skills-l3_lightrag.txt`)

### 2.5 検索結果が10件埋まったら追加検索

10件返却 = 「これで全部」ではなく「11件目以降が打ち切られている可能性」のサイン。
広いクエリだと判明したら、より絞った別キーワードで再検索する。

---

## 3. 棚卸しスクリプトの活用

検索が困難な場合は、SQL直接クエリの方が確実:

```bash
# 全件一覧(レイヤー別)
bash /docker/lightrag/scripts/inventory.sh
cat /docker/lightrag/docs/KNOWLEDGE-INDEX.md

# 特定キーワードを含むファイル名検索
docker compose exec -T postgres psql -U lightrag -d lightrag -c \
  "SELECT file_path FROM lightrag_doc_status WHERE file_path LIKE '%KEYWORD%';"

# 本文検索(タグ等含む)
docker compose exec -T postgres psql -U lightrag -d lightrag -c \
  "SELECT file_path FROM lightrag_doc_full df JOIN lightrag_doc_status ds ON df.id = ds.id WHERE content LIKE '%KEYWORD%' LIMIT 30;"
```

---

## 4. 中長期的な改修案(参考)

現状の運用回避でも限界がある場合:

- **MCPサーバー側でtop_kパラメータを上限緩和**(現状10件→30件等)
- **検索結果のページング対応**
- **タグ専用インデックス検索エンドポイント追加**

これらはLightRAG MCP側の改修が必要なため、運用ルールで凌ぎつつ、頻度を見て検討。

---

**ルール終わり**
