# LightRAG ナレッジシステム 仕様書
**作成日:** 2026-04-12  
**バージョン:** 1.0

---

## 目次
1. システム概要
2. インフラ構成
3. データ管理
4. API・操作仕様
5. インシデント記録
6. 運用手順
7. 今後の高度化ロードマップ

---

## 1. システム概要

LightRAGを「外部脳」として運用。GitHub OSS・Claude Code SKILL・技術ドキュメントから知識を構造化・蓄積し、複数プロジェクト（OpenClaw・Webアプリ・AIエージェント等）の開発に横断的に活用するナレッジパイプライン。

- **利用者:** 1名（開発者本人）
- **主要活用先:** OpenClaw（仮想通貨自動取引）/ Virtual Protocol関連 / Website・Webアプリ・n8nワークフロー開発

---

## 2. インフラ構成

### VPS
- Hostinger KVM2 / 2 vCPU / 8GB RAM / Ubuntu
- IP: 76.13.187.66
- 作業ディレクトリ: `/docker/lightrag/`
- Git: https://github.com/7272yusuke-design/light-rag

### コンポーネント一覧

| コンポーネント | 技術 | ポート | 備考 |
|--------------|------|--------|------|
| LightRAG本体 | Docker | 9621 | network_mode: host |
| データベース | PostgreSQL + pgvector:pg16 | 5433 | ベクトル・グラフ・チャンク全保存 |
| 埋め込みモデル | Ollama + nomic-embed-text | 11434 | 768次元 / systemd管理 |
| LLM | OpenRouter → claude-sonnet-4.6 | 外部API | ナレッジ投入・合成に使用 |
| MCP公開 | Cloudflare Named Tunnel | 9622 | mcp.7272yusuke.cloud/mcp |
| テキスト化 | Repomix (npm global) | — | GitHubリポジトリのテキスト化 |
| 別プロジェクト | OpenClaw | 46819 | 干渉注意 |

### MCP接続情報
- URL: `https://mcp.7272yusuke.cloud/mcp`
- Tunnel ID: `d30cf53a-204c-46b5-9061-f2edc4226b59`
- ドメイン: `7272yusuke.cloud`（Cloudflare DNS管理）
- Services: `mcp-lightrag.service` + `cloudflared-mcp.service`

### WebUI認証
- URL: `http://76.13.187.66:9621`
- User: `admin` / Pass: `LightRag@2026!`
- .env: git管理外 / VPS上 `/docker/lightrag/.env`

---

## 3. データ管理

### DBテーブル構成

| テーブル | 内容 |
|---------|------|
| `lightrag_doc_status` | ドキュメント管理（ID・ファイル名・ステータス・チャンク数） |
| `lightrag_doc_chunks` | 分割チャンク本文 |
| `lightrag_doc_full` | フルテキスト |
| `lightrag_full_entities` | 抽出エンティティ（グラフノード） |
| `lightrag_full_relations` | エンティティ間関係（グラフエッジ） |
| `lightrag_vdb_*_nomic_embed_text_768d` | ベクトルインデックス（chunks/entity/relation） |
| `lightrag_llm_cache` | LLM推論キャッシュ |

### ナレッジ構成（2026-04-12時点: 52件）
- **GitHub OSS 43件:** CrewAI, LangGraph, n8n, ccxt, freqtrade, browser-use, mastra, vercel-ai, shadcn-ui, framer-motion, LightRAG, FFmpeg, firecrawl 等
- **SKILL L3 9件:** docx, pdf, pdf-reading, pptx, xlsx, frontend-design, file-reading, product-self-knowledge, skill-creator

### ナレッジ実装レベル定義
| レベル | 内容 |
|--------|------|
| L0 | 概要・設計思想のみ |
| L1 | コードサンプルあり（最低3件） |
| L2 | 引数・戻り値・例外が明記 |
| L3 | エラーハンドリング・テスト例・ベストプラクティスあり |

---

## 4. API・操作仕様

### ⚠️ 重要: DELETE APIの危険な挙動

`DELETE /documents` に `{"ids": ["doc-xxx"]}` を渡しても、特定IDのみ削除されず**全件削除**される。  
**ドキュメント削除は必ずPostgreSQL直接操作で実施すること。**

### API操作一覧

| 操作 | 方法 | 安全度 |
|------|------|--------|
| 認証トークン取得 | `POST /login` (username/password form) | ✅ 安全 |
| ドキュメント一覧 | `GET /documents` → `.statuses.processed[]` | ✅ 安全 |
| テキスト投入 | `POST /documents/text` (content, file_name) | ✅ 安全 |
| MCP経由投入 | `upload_document` ツール (MCP) | ✅ 安全 |
| 検索 | `POST /query` (query, mode) | ✅ 安全 |
| ドキュメント削除 | `DELETE /documents` | ❌ 禁止（全件削除バグあり） |
| ドキュメント削除（正） | PostgreSQL直接 DELETE文 | ✅ 安全 |

### 安全なドキュメント削除手順

```bash
# Step 1: 対象確認
docker exec lightrag-postgres psql -U lightrag lightrag -c "
SELECT id, file_path FROM public.lightrag_doc_status WHERE id IN ('doc-xxx');
"

# Step 2: 確認後に削除
docker exec lightrag-postgres psql -U lightrag lightrag -c "
DELETE FROM public.lightrag_doc_status WHERE id IN ('doc-xxx');
SELECT COUNT(*) FROM public.lightrag_doc_status;
"
```

### 検索モード

| モード | 特徴 | 用途 |
|--------|------|------|
| `hybrid` | グラフ+ベクトル複合 | デフォルト推奨 |
| `local` | 近傍エンティティ中心 | 特定技術の詳細 |
| `global` | グラフ全体俯瞰 | 横断的な関係把握 |
| `naive` | ベクトル検索のみ | シンプルな類似検索 |

### 高速検索エンドポイント
`POST /query/data` → 生データ返却（LLM合成スキップ）  
効果: 58秒 → 3.5秒。MCP経由での推奨方法。

---

## 5. インシデント記録

### INC-001: DELETE API全件削除事故（2026-04-12）
- **症状:** 特定IDを指定して削除したところ62件→0件に全件消失
- **原因:** `DELETE /documents` APIがidsパラメータを無視して全件クリアするバグ
- **影響:** ナレッジ全62件消失（約10分間）
- **復旧:** 同日取得のPostgreSQLバックアップ（104MB）から完全復旧
- **再発防止:** DELETE APIの使用を全面禁止。削除はPostgreSQL直接操作に統一

### INC-002: OpenRouter APIキー公開（2026-04-11以前）
- **症状:** Claude.aiチャット内でAPIキー（sk-or-v1-fd1687c...）が露出
- **原因:** デバッグ目的でチャットに貼り付け
- **影響:** キーが会話ログに残存。不正利用リスク
- **対応状況:** ⚠️ 未完了 - 要ローテーション
- **手順:** OpenRouterダッシュボード → 新キー発行 → `.env`更新 → `docker compose up -d` → 旧キー無効化

### INC-003: Quick TunnelでMCPセッション断（2026-04-11）
- **症状:** cloudflared Quick Tunnel経由のMCP接続がセッション維持できない
- **原因:** Quick TunnelはURL毎回変化 + セッション維持に不向き
- **影響:** Claude.aiからMCP安定接続不可
- **復旧:** Cloudflare Named Tunnel（固定URL）に移行し解決。`mcp.7272yusuke.cloud`で安定稼働中

### INC-004: ナレッジ消失（2026-04-12）
- **症状:** セッション中に31件のナレッジが消失
- **原因:** DELETE API誤操作の可能性
- **復旧:** 再投入で62件に回復
- **教訓:** バックアップを操作前に必ず取得する運用ルール策定のきっかけ

---

## 6. 運用手順

### バックアップ（操作前に必ず実行）
```bash
docker exec lightrag-postgres pg_dump -U lightrag lightrag > /tmp/lightrag_backup_$(date +%Y%m%d_%H%M).sql
ls -lh /tmp/lightrag_backup_*.sql
# 正常: 100MB以上のファイルが生成される
```

### バックアップからの復旧
```bash
docker exec -i lightrag-postgres psql -U lightrag lightrag < /tmp/lightrag_backup_YYYYMMDD_HHMM.sql
# ERRORが多数出るが COPY N行 が表示されれば成功
docker exec lightrag-postgres psql -U lightrag lightrag -c "SELECT COUNT(*) FROM public.lightrag_doc_status;"
```

### ナレッジ投入
```bash
# GitHubリポジトリ
cd /docker/lightrag && ./scripts/ingest_github.sh <GitHub URL>

# MCP経由（Claude.aiから直接）
# upload_document ツールを使用
```

### ナレッジ検索
```bash
cd /docker/lightrag && ./scripts/search_knowledge.sh "検索クエリ"
./scripts/search_knowledge.sh "クエリ" local
./scripts/search_knowledge.sh "クエリ" hybrid openclaw
```

### サービス確認・再起動
```bash
systemctl status mcp-lightrag cloudflared-mcp --no-pager
cd /docker/lightrag && docker compose ps
docker compose restart
```

### 件数確認
```bash
docker exec lightrag-postgres psql -U lightrag lightrag -c "SELECT COUNT(*) FROM public.lightrag_doc_status;"
```

### 操作前チェックリスト
1. バックアップ取得・サイズ確認（100MB以上）
2. 件数確認（lightrag_doc_statusのCOUNT）
3. 削除対象のSELECT確認（IDと件数が一致するか）
4. 削除実行（PostgreSQL直接のみ。DELETE APIは使わない）
5. 操作後の件数確認

---

## 7. 今後の高度化ロードマップ

| 優先度 | タスク | ステータス |
|--------|--------|-----------|
| 最優先 | OpenRouter APIキーローテーション | 未完了 |
| 高 | KNOWLEDGE-INDEX.md更新（SKILL L0→L3反映） | 未完了 |
| 高 | GSD-PLAN / RESUME更新（Phase完了反映） | 未完了 |
| 中 | ccxt / freqtrade / langgraph / crewai をL3品質化 | 未着手 |
| 中 | n8nワークフロー実装例追加（3件以上） | 未着手 |
| 中 | OpenClaw固有ドキュメント投入（CostGuard等） | 未着手 |
| 中 | バグ修正パターンをテンプレートで構造化投入 | 未着手 |
| 低 | 検索品質ベンチマーク（10クエリ×8件合格基準） | 未着手 |
| 低 | ingest_github.sh改修（実装チャンク自動抽出） | 未着手 |

### 技術的負債
DELETE APIバグはLightRAG本体のバグの可能性が高い。バージョンアップ時に挙動変化の可能性があるため、バージョン更新時は削除APIの動作を必ず確認すること。
