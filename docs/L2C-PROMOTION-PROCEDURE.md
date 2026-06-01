# L2c → L2 昇格手順 v1.0

> **作成日**: 2026-05-10
> **目的**: L2c(候補パターン)を実検証してL2(検証済みパターン)に昇格させる手順を標準化

---

## 1. 昇格条件

L2cがL2に昇格できるのは、**以下のいずれかを満たした場合**:

- 自環境(Hostinger VPS / Vault / OpenClaw等)で実装・運用し、再現性を確認した
- 顧客案件で実装・納品し、効果を確認した
- 関連OSSが複数現れ、業界標準パターンとして固まった
- A/B測定など定量的な検証データが取れた

---

## 2. 昇格手順

### 2.1 検証完了の確認
- 各エントリ本文の「検証条件」「再検討条件」セクションを満たしたか確認

### 2.2 ファイル取得
```bash
# 既存L2cの本文を取得
docker compose exec -T postgres psql -U lightrag -d lightrag -tAc \
  "SELECT content FROM lightrag_doc_full df JOIN lightrag_doc_status ds ON df.id = ds.id WHERE file_path = '<旧ファイル名>-l2c_lightrag.txt';" > /tmp/l2c-content.txt
```

### 2.3 内容更新
- ステータスを `未検証(L2c候補)` → `検証済み(L2)`
- レイヤーを `L2c` → `L2`
- 検証結果(具体的な数値・実装URL等)を追記
- ファイル名を `*-l2c_lightrag.txt` → `*-l2_lightrag.txt`

### 2.4 投入前チェック
```bash
bash /docker/lightrag/scripts/pre-ingest-check.sh /tmp/l2c-content.txt
```

### 2.5 旧L2c削除 + 新L2投入
- handoff §4.4 の削除SQLテンプレートで旧L2cを削除
- 新ファイルをLightRAG MCP `upload_document` で投入

### 2.6 整合性確認
```bash
docker compose exec -T postgres psql -U lightrag -d lightrag -c \
  "SELECT (SELECT count(*) FROM lightrag_doc_full) AS docs, (SELECT count(*) FROM lightrag_full_entities) AS entities, (SELECT count(*) FROM lightrag_full_relations) AS relations;"
```

3つとも同じ件数ならOK。

### 2.7 KNOWLEDGE-DECISIONS.md記録
- 昇格判断・検証データ・日付を追記

### 2.8 棚卸し再実行
```bash
bash /docker/lightrag/scripts/inventory.sh
```

---

## 3. 現L2c一覧(2026-05-10時点 20件)

`bash /docker/lightrag/scripts/inventory.sh` 実行後、`/docker/lightrag/docs/KNOWLEDGE-INDEX.md` の L2c セクション参照。

---

**手順終わり**
