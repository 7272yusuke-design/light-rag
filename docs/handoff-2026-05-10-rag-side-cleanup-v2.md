# LightRAG RAG側整理セッション v2 引き継ぎドキュメント

> **作成日**: 2026-05-10
> **前回引き継ぎ**: handoff-2026-05-10-lightrag-cleanup.md (本セッションの起点)
> **目的**: 前回handoffの「次セッションで取り組む課題」全完了 + 残タスクの引き継ぎ

---

## 1. 本セッションで完了した作業

### 1.1 セキュリティ
- **OpenRouter APIキーローテーション**完了
  - 旧キー(`sk-or-v1-fd1687c...`)はOpenRouterダッシュボード側で無効化済み
  - 新キーは`/docker/lightrag/.env`に反映、コンテナ再起動済み
  - `.env.bak`(旧キー含む)は削除済み

### 1.2 再発防止スクリプト3点(新規)
- `/docker/lightrag/scripts/inventory.sh` — DB→KNOWLEDGE-INDEX.md自動生成
- `/docker/lightrag/scripts/pre-ingest-check.sh` — 投入前チェック(ファイル名規則/URL重複/表示名衝突/タグ存在/ファイル名衝突)
- `/docker/lightrag/docs/MEMORY-NOTATION-RULES.md` — メモリ表記ルール(「未分類」≠「未投入」、同一URL複数エントリ判定基準等)

### 1.3 同テーマ複数エントリ調査
4系統13エントリすべて「観点が異なる」ため統合不要:
- superpowers系2件(workflow=概要 + full=詳細、相補関係を本文に明記済み)
- ComfyUI系2件(api-server + graph-execution、別観点)
- RAG系4件(L3 framework + L2 patterns 3種、別観点)
- n8n系5件(L3 2件は別リポジトリ + L2/L2c 3件は別パターン)

副産物: 「同一URL複数エントリ許容ルール」を `MEMORY-NOTATION-RULES.md §6` に明文化、`pre-ingest-check.sh` のURL重複検知をERROR→WARN化。

### 1.4 KNOWLEDGE-INDEX.md再棚卸し
- `inventory.sh` 実行で `/docker/lightrag/docs/KNOWLEDGE-INDEX.md` 自動生成
- 現状: 163件 (L1=3 / L2=19 / L2c=20 / L3=121)、整合性 163/163/163

### 1.5 KNOWLEDGE-DECISIONS.md URL補完
4件すべて補完完了:
- rtk: https://github.com/rtk-ai/rtk
- MiniCode: https://github.com/LiuMengxuan04/MiniCode
- JeecgBoot: https://github.com/jeecgboot/JeecgBoot
- Agent Lightning: https://github.com/microsoft/agent-lightning

### 1.6 検索運用ルール策定
- `/docker/lightrag/docs/SEARCH-OPERATION-RULES.md` 新規作成
- 10件上限への運用回避策(クエリ粒度/観点を変えた複数検索/レイヤー別フィルタ/SQL直接クエリ等)

### 1.7 プロジェクトフィルタ古ラベル削除
- `/docker/lightrag/config/project_profiles.json`からv2時代の3ラベル(l1-external/l2-combination/l3-package)削除
- 業務5プロジェクト(openclaw/virtual-protocol/website/webapp/workflow)のみ残存
- バックアップ: `/docker/lightrag/config/project_profiles.json.bak-20260510-030202`

### 1.8 list_knowledge表示バグ修正
- 原因: `content_summary`(API由来の冒頭切り抜き)からタグ抽出していたため、タグ行がサマリ範囲外で空表示になっていた
- 修正: `mcp_remote.py` の `do_list_knowledge` をDB直接クエリ + SQL側でname/category/tags抽出する方式に変更
- バックアップ: `/docker/lightrag/scripts/mcp_remote.py.bak-20260510-*`
- 動作確認: 全163件でtags欄が正しく表示されるようになった

### 1.9 L2c→L2昇格手順文書化
- `/docker/lightrag/docs/L2C-PROMOTION-PROCEDURE.md` 新規作成
- 昇格条件 + 8ステップの手順 + 関連ツール

---

## 2. 次セッションで取り組む課題

### 2.1 継続的タスク(優先度判断はYusukeさん)

**2.1.1 L2c→L2 昇格判定(20件)**
- 現L2c 20件のうち、自環境/案件で実検証済みのものをL2へ昇格
- 手順: `/docker/lightrag/docs/L2C-PROMOTION-PROCEDURE.md` 参照
- 判定はYusukeさんの実作業に基づくため、検証完了時に1件ずつ実施

**2.1.2 新規ナレッジ投入時のフロー定着**
- `pre-ingest-check.sh` を必ず投入前に実行
- `inventory.sh` を投入後に実行してKNOWLEDGE-INDEX.md更新

### 2.2 Phase 1関連(別セッション、SKILL改訂完了後)

役割境界に基づき、本セッションでは扱わない:
- L0 Phase 1投入(L0-002/006/007/008/009/010 の6件)
- Vault側担当(SKILL改訂、PMM、knowledge-bridge)
- プロダクト側担当(商品化憲章、Tier別SKU、価格、SLA、UX)

### 2.3 探索的(余裕があれば)

- list_knowledge表示バグの完全解消確認(本セッションで修正したが、複雑なエッジケースが残っている可能性は低い)
- 検索結果10件上限のMCPサーバー側改修(運用ルールで凌げているなら不要)

---

## 3. 主要ドキュメント・スクリプト早見表

### 3.1 運用スクリプト
| ファイル | 用途 |
|---|---|
| `/docker/lightrag/scripts/inventory.sh` | 棚卸し → KNOWLEDGE-INDEX.md自動生成 |
| `/docker/lightrag/scripts/pre-ingest-check.sh <file>` | 投入前チェック |

### 3.2 ルール・手順ドキュメント
| ファイル | 用途 |
|---|---|
| `/docker/lightrag/docs/MEMORY-NOTATION-RULES.md` | メモリ表記ルール + 同一URL複数エントリ判定 |
| `/docker/lightrag/docs/SEARCH-OPERATION-RULES.md` | 検索10件上限への運用ルール |
| `/docker/lightrag/docs/L2C-PROMOTION-PROCEDURE.md` | L2c→L2昇格手順 |
| `/docker/lightrag/docs/KNOWLEDGE-DECISIONS.md` | 投入判断記録(常設) |
| `/docker/lightrag/docs/KNOWLEDGE-INDEX.md` | 全エントリ一覧(自動生成) |

### 3.3 環境情報
- VPS: Hostinger KVM2、IP 76.13.187.66
- 作業ディレクトリ: `/docker/lightrag/`
- ターミナル: Hostinger Web Terminal(SSHなし、コマンド直接)
- PostgreSQL: `lightrag` user / `lightrag` DB / port 5433
- LightRAG MCP: `https://mcp.7272yusuke.cloud/mcp`(Cloudflare Named Tunnel)

### 3.4 整合性確認SQL
```bash
cd /docker/lightrag && docker compose exec -T postgres psql -U lightrag -d lightrag -c "SELECT (SELECT count(*) FROM lightrag_doc_full) AS docs, (SELECT count(*) FROM lightrag_full_entities) AS entities, (SELECT count(*) FROM lightrag_full_relations) AS relations;"
```
3つとも同じ数なら整合OK。

---

## 4. 役割境界(継続事項)

本セッションもRAG側担当領域のみで完結。次セッションも同様の範囲を推奨:
- ✅ LightRAGレイヤー(L0/L1/L2/L3)の判断
- ✅ ファイル仕様、命名規則、タグ運用
- ✅ 既存ナレッジとの整合・重複チェック
- ✅ KNOWLEDGE-DECISIONS.mdへの記録
- ✅ 運用スクリプト・MCPサーバーの保守

以下は本セッションでは扱わなかった:
- Vault側担当: universal-agent-vault設計、SKILL改訂、PMM、knowledge-bridge
- プロダクト側担当: 商品化憲章、Tier別SKU、価格、SLA、UX
- L0 Phase 1投入: SKILL改訂完了後(別セッション)

---

**引き継ぎドキュメント以上**
