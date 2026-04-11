# 再開手順書

## このドキュメントについて

LightRAGナレッジパイプラインの作業を、新しいチャットセッションで再開する際の手順。Claude.aiまたはClaude Codeに渡す。

---

## 即座に伝えること

LightRAGナレッジパイプラインの続きをやります。

VPS: 76.13.187.66
作業ディレクトリ: /docker/lightrag/
Git: https://github.com/7272yusuke-design/light-rag

プロジェクトの計画書を読んでください:
- docs/GSD-PLAN.md（全体計画とフェーズ）
- docs/ARCHITECTURE.md（システム設計）
- docs/DATA-SCHEMA.md（データ構造ルール）

現在のフェーズ: Phase 1-6完了、Phase 7（バージョンアップ）進行中
直近の作業状態: 51ドキュメント投入済み（うち4件レベル3）、summarize_repo.pyリトライ改修済み、KNOWLEDGE-INDEX自動生成対応

---

## 環境確認コマンド

  cd /docker/lightrag && docker compose ps
  systemctl status ollama --no-pager
  curl -s http://localhost:9621/health || echo "LightRAG is down"
  docker exec lightrag-postgres pg_isready -U lightrag
  repomix --version

## 環境復旧（止まっていた場合）

  sudo systemctl start ollama
  cd /docker/lightrag && docker compose up -d

---

## 現在のインフラ構成

VPS (76.13.187.66)
├── Ollama (systemd, port 11434)
│   └── nomic-embed-text (embedding, 768dim)
├── Docker
│   ├── lightrag-postgres (pgvector:pg16, port 5433)
│   └── lightrag-server (port 9621, network_mode: host)
│       ├── LLM: OpenRouter → anthropic/claude-sonnet-4.6
│       ├── Embedding: Ollama → nomic-embed-text
│       └── Storage: PostgreSQL + NetworkX
├── Repomix (npm global, Node.js 20)
├── Claude Code (npm global, VPS上で実行)
│   └── MCP: lightrag → mcp_lightrag.py（search_knowledge + list_knowledge + list_projects）
├── graphify (pip global, Claude Code SKILL)
└── OpenClaw (Docker, port 46819) ※別プロジェクト

## 採用ツール

| ツール | 用途 | 利用方法 |
|---|---|---|
| Repomix | リポジトリ → テキスト化 | VPS CLI (repomix --remote) |
| DeepWiki MCP | リポジトリ構造分析 | Claude Code MCP |
| OpenRouter | LLM要約・自動分類 | VPS API（既存） |
| LightRAG | 知識グラフDB | VPS Docker（既存） |
| mcp_lightrag.py | Claude Code → LightRAG検索 | Claude Code MCP（stdio） |
| graphify | コード構造解析 | Claude Code内で /graphify <dir> |

## 認証情報

重要: .envファイルはgitに含まれていない。VPS上の /docker/lightrag/.env を参照。

- WebUI: http://76.13.187.66:9621 → admin / LightRag@2026!
- LightRAG API: Bearer token（login APIで取得）
- OpenRouter: .env内の LLM_BINDING_API_KEY

## API利用の定型パターン

トークン取得:
  curl -s -X POST "http://localhost:9621/login" -d "username=admin&password=LightRag@2026!" | python3 -c "import sys,json; print(json.load(sys.stdin)['access_token'])"

ドキュメント投入:
  curl -s -X POST "http://localhost:9621/documents/upload" -H "Authorization: Bearer $TOKEN" -F "file=@target.txt"

ドキュメント削除:
  curl -s -X DELETE "http://localhost:9621/documents/delete_document" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"doc_ids": ["doc-xxx"]}'

検索:
  curl -s -X POST "http://localhost:9621/query" -H "Authorization: Bearer $TOKEN" -H "Content-Type: application/json" -d '{"query":"検索クエリ", "mode":"hybrid"}'

ドキュメント一覧:
  curl -s "http://localhost:9621/documents" -H "Authorization: Bearer $TOKEN"

---

## 進捗管理

### 完了済み
- [x] LightRAG基盤構築（Docker + PostgreSQL + Ollama + OpenRouter）
- [x] WebUI動作確認
- [x] ドキュメント投入・検索の動作確認
- [x] Gitリポジトリ初期push
- [x] GSD計画書・アーキテクチャ・データスキーマ策定
- [x] ツール選定（Repomix + DeepWiki MCP + OpenRouter）
- [x] Phase 1: GitHub Ingestion Pipeline（ingest_github.sh完成）
- [x] Phase 2: SKILL Ingestion（9スキル投入）
- [x] Phase 3: ナレッジ活用SKILL（search_knowledge.sh + プロジェクト手順設定）
- [x] Phase 4: データ管理（タグ正規化・重複検知・鮮度チェック）
- [x] Phase 5: Cross-Project & Agent共有（MCP連携・プロジェクトフィルタリング・API利用ガイド・Git自動push）
- [x] graphifyインストール・Claude Code SKILL登録
- [x] ナレッジ42件投入（不正ドキュメント10件削除済み）

### 残タスク
- [ ] OpenRouter APIキーローテーション（セキュリティ。即対応）
- [ ] ドメイン取得 → Cloudflare Named Tunnel → MCP固定URL化（現状動作中のためスキップ可）
- [ ] プロジェクト固有ナレッジ投入（OpenClaw CostGuard、バグ修正パターン、jizokuka-ai）
- [ ] 検索品質ベンチマーク（テストクエリ10件、合格基準8/10）
- [ ] 中期: langgraph/crewai/browser-use レベル3化
- [ ] 中期: ingest_github.sh改修（Option C: 実装チャンク自動抽出）
- [x] DATA-SCHEMA.mdにバグパターンテンプレート追加
- [x] KNOWLEDGE-INDEX.md自動生成スクリプト化（update_knowledge_index.py）
- [x] ccxt/freqtrade/n8n/openclaw レベル3化
- [x] ARCHITECTURE.md投入
- [x] 新規9リポジトリ投入（career-ops, stripe-cli, FFmpeg, cli, vercel, llmfit, autoresearch, OpenSpace, claude-peers-mcp）
- [x] summarize_repo.py リトライ+フォールバック+コード例自動生成（レベル1相当）

---

## 蓄積済みナレッジ（51件）
