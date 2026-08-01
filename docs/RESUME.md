# 再開手順書

> **最終更新: 2026-08-01**
> このファイルは「**現在地**」のみを保持する。肥大させないこと。
> - 過去のセッション記録 → `SESSION-LOG.md`
> - 環境情報・インフラ構成・認証 → `ARCHITECTURE.md` および Claude.ai側 `project-instructions-v2.md`
> - ナレッジ運用ルール（レイヤー定義・投入フロー・verified定義） → `DATA-SCHEMA.md`
> - 投入判断ログ → `KNOWLEDGE-DECISIONS.md`（追記は MCP `record_decision` 経由が標準）
> - ナレッジ一覧 → `KNOWLEDGE-INDEX.md`（AUTO区画は `inventory.sh` が自動更新）

## セッション開始時の手順

1. 本ファイルを読む
2. `./scripts/inventory.sh` を実行して件数と整合性を確認する
3. 直近の作業経緯を追う必要がある場合のみ `SESSION-LOG.md` の末尾を読む

## 現在地

### ナレッジベース（2026-08-01時点）

**Total 247 / 整合性 full=247 status=247 processed=247 graph=247/247（完全一致）**

| レイヤー | 件数 | 割合 |
|---------|------|------|
| L3（実装・部品在庫） | 192 | 77.7% |
| L2c（候補パターン） | 31 | 12.6% |
| L2（検証済みパターン） | 20 | 8.1% |
| L1（横断運用メタ知識） | 3 | 1.2% |
| L0（設計原理） | 1 | 0.4% |

**L2比率 8.1%（目標20-25%）。** L3のみが増加し続ける構造が継続中。
L2を増やす唯一の正規ルートは「L2cを実装して自環境で検証する」pull型昇格。
収集ではなく**実装のフェーズ**にある。

### フェーズ

**更新キュー解消完了（2026-08-01）。** psql削除→再投入の手順が `lightrag-knowledge-maintenance` スキルとして確立し、長期停滞していた ECC v2.0.0 / AstrBot v4.26.7 の2件を処理済み。
次のフェーズは **L2c実装による検証**。

## 環境確認コマンド

    cd /docker/lightrag && docker compose ps
    systemctl status ollama --no-pager
    curl -s http://localhost:9621/health || echo "LightRAG is down"
    docker exec lightrag-postgres pg_isready -U lightrag
    systemctl status mcp-lightrag --no-pager
    systemctl status cloudflared-mcp --no-pager

## 環境復旧（停止していた場合）

    sudo systemctl start ollama
    cd /docker/lightrag && docker compose up -d
    sudo systemctl start mcp-lightrag
    sudo systemctl start cloudflared-mcp

## 残タスク

### 最優先（セキュリティ・長期持ち越し）

1. [ ] **OpenRouter APIキーのローテーション**（チャットで公開済み。複数セッションにわたり持ち越し中）
2. [ ] **露出PAT（ghp_ItVf...）のRevoke最終確認**（credential helper経由のpush成功により運用影響なしは実証済み、未確認なら実施）

### ナレッジ運用

3. [ ] **L2c実装による検証**（L2比率改善の唯一の道）
   - 候補A: three-role-agent-development-loop の n8n版
   - 候補B: video-to-knowledge パイプライン
4. [ ] **同テーマ複数エントリの重複調査**（superpowers / ComfyUI / RAG / n8n 等）
5. [ ] **L0 Phase 1投入（6件）** — L0-006/007/002/008/009/010。SKILL改訂（Step 4）完了が前提。
   ファイル名は必ず `*-l0_lightrag.txt`（inventory.sh のレイヤー判定はファイル名依存）
6. [ ] **未評価3件の評価** — skyway/ai-noise-canceller、llm-jp/awesome-japanese-llm、AI Data Scientist Handbook

### システム・技術負債

7. [ ] **entity_chunks / relation_chunks のゴースト要素クリーンアップ**
   （`lightrag_full_entities.id = doc_id` の発見により一部解明済み。残るのは共有エンティティの孤児）
8. [ ] **2段階クエリ戦略のスキル化**（理論は DATA-SCHEMA.md 記載済み、スキル化のみ未着手）
9. [ ] **圧縮ミドルウェア フェーズ1A セッション4**（Deduplication実装）
10. [ ] **untracked管理ドキュメントのcommit**（MEMORY-NOTATION-RULES / SEARCH-OPERATION-RULES / scripts/inventory.sh 等）

## 進行中のブランチ・stash

- **feature/compression-middleware**: セッション3（パススルー実装）まで完了。セッション4未着手。
  main と双方向マージ済みで、両ブランチ同一コミット。
- **stash@{0}**: `20260510-cleanup-pending`（config/project_profiles.json、docs/KNOWLEDGE-DECISIONS.md、docs/KNOWLEDGE-INDEX.md）

## 重要な前提（失うと再調査になる）

- **DELETE API は禁止**（全消しバグ）。ただし **psql直接操作は可能**。
  「psqlも実行不可」は誤認だった（2026-08-01に実証）。手順は `lightrag-knowledge-maintenance` スキル。
- **`upload_document` の `overwrite: True` は HTTP 404 で失敗する。** 更新は削除→再投入の2段。
- **`inventory.sh` のレイヤー判定はファイル名のパターンマッチ依存。** 本文中のタグは分類に使われない。
- **`lightrag_full_entities.id` = doc_id そのもの**（1行1ドキュメント）。削除漏れは `graph=` のずれとして現れる。
- **`file_path` は `lightrag_doc_status` 側**。`lightrag_doc_full` には無いため JOIN が必要。
- 保留・更新キューを記録する際は、**psqlで既存本文を確認してから実差分のみを書く**。
  推測で差分を登録すると二重計上になる（2026-07-23のAstrBot記録で発生）。

## Claude.aiプロジェクト スキル

- `combination-architect`: ナレッジ組み合わせ → 企画提案・設計
- `knowledge-navigator`: ナレッジ検索 → 実装提案・技術選定
- `skill-verifier`: Claudeception方式で品質検証
- `lightrag-knowledge-maintenance`: 更新・削除・リネームのpsql手順
- `loop-architect` / `project-control-tower` / `n8n-workflow-builder` / `n8n-workflow-sync` 他
